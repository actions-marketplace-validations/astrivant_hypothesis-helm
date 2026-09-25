"""
Build the native synthetic-input renderer or replay a recorded chart failure.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from hypothesis_helm.charts.testing.rendering import render_output
from hypothesis_helm.compiler.passes.inputs import load_input_chart
from hypothesis_helm.compiler.randomness.model import RandomInputs
from hypothesis_helm.compiler.randomness.toolchain import build
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("main",)


def main(argv: list[str] | None = None) -> int:
    """
    Prepare the optional pinned renderer or reproduce its exact synthetic inputs.

    Args:
        argv (list[str] | None): Explicit arguments, or the process command line.

    Returns:
        int: Zero on success, one for a reproduced chart failure, two for setup/replay errors, or 130 on interruption.
    """
    refresh_env()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chart", nargs="?", type=Path, help="prepared chart to replay")
    parser.add_argument("--build", action="store_true", help="build the pinned renderer without testing a chart")
    parser.add_argument("--go", default="go", help="Go executable used for the optional renderer build")
    parser.add_argument("--values", type=Path, help="saved values.json overrides")
    parser.add_argument("--random-inputs", type=Path, help="saved random-inputs.json tape")
    parser.add_argument("--helm", default="helm", help="Helm executable whose version must match the controlled SDK")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--release", default="hypothesis")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--kube-version")
    args = parser.parse_args(argv)
    if not args.build and (args.chart is None or args.values is None or args.random_inputs is None):
        parser.error("replay requires CHART, --values and --random-inputs")
    try:
        binary = build(go=args.go)
        if args.build:
            print(binary)
            return 0
        chart = load_input_chart(args.chart)
        case = RandomInputs.from_document(json.loads(args.random_inputs.read_text()))
        with case:
            print(
                render_output(
                    chart,
                    mapping(json.loads(args.values.read_text())),
                    timeout=args.timeout,
                    helm=args.helm,
                    release=args.release,
                    namespace=args.namespace,
                    kube_version=args.kube_version,
                ),
                end="",
            )
    except KeyboardInterrupt:
        print("Random-input rendering interrupted; child processes joined.", file=sys.stderr)
        return 130
    except RenderFailure as exc:
        print(exc, file=sys.stderr)
        return 1
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        diagnostic = exc.stderr if isinstance(exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
        print(diagnostic, file=sys.stderr)
        return 2
    return 0
