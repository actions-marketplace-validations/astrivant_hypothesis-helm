"""
Measure the downstream effects of explicit values mutations without changing a chart.
"""

import argparse
import json
import time
from pathlib import Path

from hypothesis_helm.analysis.report import write_report
from hypothesis_helm.analysis.sensitivity import Mutation, analyze
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.reporting.budget import parse_time_limit
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("load_mutations", "main")


def load_mutations(path: Path) -> list[Mutation]:
    """
    Read explicit names, typed paths and replacement values from JSON.

    Args:
        path (Path): JSON array of mutation descriptors.

    Returns:
        list[Mutation]: Validated operation descriptors in input order.
    """
    mutations = []
    for entry in sequence(json.loads(path.read_text())):
        record = mapping(entry)
        name, parts = record["name"], sequence(record["path"])
        if not isinstance(name, str) or not name or not parts:
            raise ValueError("each mutation requires a nonempty string name and path")
        path_parts: list[str | int] = []
        for part in parts:
            if isinstance(part, str) or type(part) is int:
                path_parts.append(part)
            else:
                raise ValueError("path components must be string keys or integer indices")
        mutations.append(Mutation(name, tuple(path_parts), record["value"]))
    return mutations


def main(argv: list[str] | None = None) -> int:
    """
    Run a bounded local-chart sensitivity analysis and save its evidence.

    Args:
        argv (list[str] | None): Explicit arguments or process command line.

    Returns:
        int: Zero for a complete analysis, one for a budget-limited result.
    """
    refresh_env()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chart", type=Path, help="local chart containing values.yaml and values.schema.json")
    parser.add_argument("--mutations", required=True, type=Path, help="JSON array of name/path/value replacements")
    parser.add_argument("--output", type=Path, default=Path(f".cache/benchmarks/sensitivity/{time.time_ns()}"))
    parser.add_argument("--max-pairs", type=int, default=100)
    parser.add_argument("--max-mutations", type=int, default=100)
    parser.add_argument("--time-limit", type=parse_time_limit, default=180)
    parser.add_argument("--helm", default="helm")
    parser.add_argument("--release", default="hypothesis")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--kube-version")
    parser.add_argument("--plot", action="store_true", help="requires the benchmarking extra (matplotlib)")
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error("choose a fresh output directory")
    if args.max_pairs < 0 or args.max_mutations < 1:
        parser.error("max-pairs must be nonnegative and max-mutations must be positive")
    chart = Chart.load(args.chart)
    mutations = load_mutations(args.mutations)
    deadline = time.monotonic() + args.time_limit

    def invoke(values: dict[str, object]) -> object:
        """
        Render with a fixed invocation context and the remaining execution budget.

        Args:
            values (dict[str, object]): Schema-valid values configuration.

        Returns:
            object: Parsed, validated manifest bundle.
        """
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("analysis render deadline reached")
        return render(
            chart,
            values,
            helm=args.helm,
            release=args.release,
            namespace=args.namespace,
            kube_version=args.kube_version,
            timeout=min(30, remaining),
            stream=False,
        )

    document = analyze(
        chart.defaults,
        chart.schema,
        mutations,
        invoke,
        max_pairs=args.max_pairs,
        max_mutations=args.max_mutations,
        time_limit=args.time_limit,
    )
    document["context"] = {
        "chart": str(chart.path),
        "helm": args.helm,
        "release": args.release,
        "namespace": args.namespace,
        "kube_version": args.kube_version,
    }
    write_report(args.output, document, plots=args.plot)
    print(f"Sensitivity analysis: {document['status']}; {document['renders']} renders; report: {args.output / 'README.md'}")
    return 0 if document["status"] == "complete" else 1
