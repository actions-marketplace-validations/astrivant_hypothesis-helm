"""Command-line and Helm plugin entry point."""

import argparse
import json
from pathlib import Path

from .runner import Chart, audit, check_chart


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit and property-test Helm chart values.")
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("audit", help="discover value references and schema gaps")
    inspect.add_argument("chart", type=Path)
    inspect.add_argument(
        "--strict", action="store_true", help="fail on any finding or unresolved access"
    )
    test = commands.add_parser("test", help="render schema-generated values with Hypothesis")
    test.add_argument("chart", type=Path)
    test.add_argument("--max-examples", type=int, default=100)
    test.add_argument("--exhaustive", action="store_true")
    test.add_argument("--max-cases", type=int, default=1000)
    test.add_argument("--seed", type=int, default=0)
    test.add_argument("--timeout", type=float, default=30)
    test.add_argument("--helm", default="helm")
    test.add_argument("--release", default="hypothesis")
    test.add_argument("--namespace", default="default")
    test.add_argument("--kube-version")
    test.add_argument("--allow-empty", action="store_true")
    test.add_argument("--artifact-dir", type=Path, default=Path("reports/hypothesis-helm"))
    args = parser.parse_args(argv)
    try:
        chart = Chart.load(args.chart)
        if args.command == "audit":
            report = audit(chart)
            status = 1 if args.strict and (report["findings"] or report["unresolved"]) else 0
        else:
            report = check_chart(
                chart,
                max_examples=args.max_examples,
                random_seed=args.seed,
                timeout=args.timeout,
                helm=args.helm,
                release=args.release,
                namespace=args.namespace,
                kube_version=args.kube_version,
                allow_empty=args.allow_empty,
                artifact_dir=args.artifact_dir,
                exhaustive=args.exhaustive,
                max_cases=args.max_cases,
            )
            status = 0 if report["status"] == "passed" else 1
        print(json.dumps(report, indent=2))
        return status
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc), "type": type(exc).__name__}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
