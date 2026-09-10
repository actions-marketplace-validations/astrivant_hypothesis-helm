"""
Command-line and Helm plugin entry point.
"""

import argparse
import json
import logging
from pathlib import Path

from .generate import generate_tests
from .generated import RenderOptions
from .runner import Chart, audit, check_chart
from .suite import run_suite


def main(argv: list[str] | None = None) -> int:
    """
    Dispatch chart auditing, generation, and property checks.

    Args:
        argv (list[str] | None): Command-line arguments, or the process arguments when omitted.

    Returns:
        int: Process exit status, zero on success.
    """
    parser = argparse.ArgumentParser(description="Audit and property-test Helm chart values.")
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser(
        "generate", help="generate one typed Python property test per values path"
    )
    generate.add_argument("chart", type=Path)
    generate.add_argument("--output", type=Path, default=Path("generated-tests"))
    generate.add_argument("--max-examples", type=int, default=100)
    inspect = commands.add_parser("audit", help="discover value references and schema gaps")
    inspect.add_argument("chart", type=Path)
    inspect.add_argument(
        "--strict", action="store_true", help="fail on any finding or unresolved access"
    )
    run = commands.add_parser("run", help="run a saved generated Python suite")
    run.add_argument("suite", type=Path)
    run.add_argument("--seed", type=int, default=0)
    run.add_argument("--match", help="select tests by value-path keyword")
    run.add_argument("--collect-only", action="store_true")
    test = commands.add_parser("test", help="generate and run a Hypothesis test per values path")
    test.add_argument(
        "chart",
        type=Path,
        nargs="?",
        default=Path("."),
        help="chart directory (defaults to the current directory)",
    )
    test.add_argument("--max-examples", type=int, default=100)
    modes = test.add_mutually_exclusive_group()
    modes.add_argument(
        "--exhaustive", action="store_true", help="enumerate finite whole-chart inputs"
    )
    modes.add_argument("--whole-chart", action="store_true", help="sample whole-chart inputs")
    test.add_argument("--match", help="select generated tests by value-path keyword")
    test.add_argument("--collect-only", action="store_true", help="generate and list tests")
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
    logger = logging.getLogger("hypothesis_helm")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    previous_level = logger.level
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    try:
        if args.command == "run":
            return run_suite(
                args.suite, seed=args.seed, match=args.match, collect_only=args.collect_only
            )
        chart = Chart.load(args.chart)
        if args.command == "generate":
            report = generate_tests(chart, args.output, max_examples=args.max_examples)
            status = 0
        elif args.command == "audit":
            report = audit(chart)
            status = 1 if args.strict and (report["findings"] or report["unresolved"]) else 0
        elif not args.whole_chart and not args.exhaustive:
            if args.timeout <= 0:
                raise ValueError("timeout must be positive")
            report = generate_tests(
                chart,
                args.artifact_dir,
                max_examples=args.max_examples,
                options=RenderOptions(
                    timeout=args.timeout,
                    helm=args.helm,
                    release=args.release,
                    namespace=args.namespace,
                    kube_version=args.kube_version,
                    allow_empty=args.allow_empty,
                ),
            )
            print(
                f"Generated {report['tests']} value-path tests in {args.artifact_dir}", flush=True
            )
            diagnostics = report["diagnostics"]
            if diagnostics:
                print("Review paths.json for unresolved or inferred template values.", flush=True)
            return run_suite(
                args.artifact_dir, seed=args.seed, match=args.match, collect_only=args.collect_only
            )
        else:
            if args.match is not None or args.collect_only:
                raise ValueError("--match and --collect-only apply to per-path tests only")
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
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)


if __name__ == "__main__":
    raise SystemExit(main())
