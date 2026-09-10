"""
Command-line and Helm plugin entry point.
"""

import argparse
import json
import logging
import os
import sys
from contextlib import ExitStack, redirect_stdout
from pathlib import Path
from typing import Literal

from hypothesis_helm.charts.generate import generate_tests
from hypothesis_helm.charts.generated import RenderOptions
from hypothesis_helm.charts.runner import Chart, audit, check_chart
from hypothesis_helm.execution.suite import run_suite
from hypothesis_helm.integrations.sharding import parse_shard_option, resolve_shard
from hypothesis_helm.reporting.output import MANIFEST_FD
from hypothesis_helm.schemas.conformity import ENVIRONMENT, prepare


def parse_jobs(value: str) -> int | Literal["auto"]:
    """
    Parse automatic throughput tuning or a positive fixed worker count.

    Args:
        value (str): Value supplied to the jobs option.

    Returns:
        int | Literal["auto"]: Validated concurrency setting.
    """
    if value == "auto":
        return "auto"
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("jobs must be auto or a positive integer") from exc
    if count < 1:
        raise argparse.ArgumentTypeError("jobs must be auto or a positive integer")
    return count


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
    run.add_argument("--artifact-dir", type=Path, help="report directory for a saved suite")
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
    for command in (test, run):
        command.add_argument(
            "--kubeconform", action="store_true", help="validate Kubernetes API schemas"
        )
        command.add_argument(
            "--schema-version", default="latest", help="Kubernetes schema version: latest or X.Y.Z"
        )
        command.add_argument(
            "--schema-cache-dir", type=Path, default=Path(".cache/hypothesis-helm/schemas")
        )
        command.add_argument(
            "--schema-offline",
            action="store_true",
            help="reuse cached schemas without network access",
        )
        command.add_argument("--kubeconform-binary", default="kubeconform")
        command.add_argument(
            "--cache-dir", type=Path, help="persistent path-result cache directory"
        )
        command.add_argument("--no-cache", action="store_true", help="disable path-result caching")
        command.add_argument(
            "--rerun",
            choices=("auto", "all", "failed"),
            default="auto",
            help="auto: rerun failures locally; run all paths in CI",
        )
        command.add_argument(
            "--shard",
            type=parse_shard_option,
            default="auto",
            help="auto (default): detect CI node; INDEX/TOTAL: explicit shard; none: disable",
        )
        command.add_argument(
            "--jobs",
            "-j",
            type=parse_jobs,
            default="auto",
            help="auto (default): PID throughput tuning; N: fixed worker count; 1: serial",
        )
        command.add_argument(
            "--output",
            "-o",
            choices=("json",),
            help="stream one rendered manifest per JSON line on stdout; reports go to stderr",
        )
    args = parser.parse_args(argv)
    logger = logging.getLogger("hypothesis_helm")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    previous_level = logger.level
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    stack = ExitStack()
    descriptor = None
    token = None
    if getattr(args, "output", None) == "json":
        descriptor = os.dup(sys.stdout.fileno())
        token = MANIFEST_FD.set(descriptor)
        stack.enter_context(redirect_stdout(sys.stderr))
    previous_conformity = os.environ.pop(ENVIRONMENT, None)
    try:
        if args.command in ("test", "run"):
            if args.kubeconform and not args.collect_only:
                os.environ[ENVIRONMENT] = prepare(
                    args.schema_cache_dir,
                    args.schema_version,
                    args.kubeconform_binary,
                    args.schema_offline,
                )
            args.shard, shard_source = resolve_shard(args.shard, os.environ)
            if args.shard is not None:
                logger.info(
                    "Shard %s/%s selected from %s",
                    args.shard.index,
                    args.shard.total,
                    shard_source,
                )
        if args.command == "run":
            return run_suite(
                args.suite,
                seed=args.seed,
                match=args.match,
                collect_only=args.collect_only,
                jobs=args.jobs,
                shard=args.shard,
                cache_dir=args.cache_dir,
                cache=not args.no_cache,
                rerun=args.rerun,
                artifact_dir=args.artifact_dir,
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
            generated = args.artifact_dir
            if args.shard is not None:
                generated = generated / "shards" / args.shard.name
            report = generate_tests(
                chart,
                generated,
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
            print(f"Generated {report['tests']} value-path tests in {generated}", flush=True)
            diagnostics = report["diagnostics"]
            if diagnostics:
                print("Review paths.json for unresolved or inferred template values.", flush=True)
            return run_suite(
                generated,
                seed=args.seed,
                match=args.match,
                collect_only=args.collect_only,
                jobs=args.jobs,
                shard=args.shard,
                cache_dir=args.cache_dir,
                cache=not args.no_cache,
                rerun=args.rerun,
                artifact_dir=args.artifact_dir,
            )
        else:
            if args.shard is not None:
                raise ValueError("--shard applies to per-path suites only")
            if args.jobs not in ("auto", 1):
                raise ValueError("--jobs applies to per-path suites; whole-chart modes are serial")
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
    except KeyboardInterrupt:
        logger.info("Testing interrupted")
        return 130
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc), "type": type(exc).__name__}))
        return 2
    finally:
        os.environ.pop(ENVIRONMENT, None)
        if previous_conformity is not None:
            os.environ[ENVIRONMENT] = previous_conformity
        stack.close()
        if token is not None:
            MANIFEST_FD.reset(token)
        if descriptor is not None:
            os.close(descriptor)
        logger.removeHandler(handler)
        logger.setLevel(previous_level)


if __name__ == "__main__":
    raise SystemExit(main())
