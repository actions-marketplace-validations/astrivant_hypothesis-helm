"""
Select the same conservative incremental testing policy across CI providers.
"""

import argparse
import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path

from hypothesis_helm.charts.repositories.changes import chart_changed, comparison

__all__ = ("main", "select_rerun")


def select_rerun(
    chart: Path,
    *,
    incremental: bool,
    rerun: str = "auto",
    base_ref: str | None = None,
    report: Path | None = None,
    environment: Mapping[str, str] | None = None,
) -> str:
    """
    Reuse unchanged-chart successes while requiring fresh tests for release tags.

    Args:
        chart (Path): Original chart directory in the CI checkout.
        incremental (bool): Use Git comparison when the requested policy is automatic.
        rerun (str): Automatic selection, explicit failed-path retry, or a full run.
        base_ref (str | None): Optional comparison reference overriding provider metadata.
        report (Path | None): Optional destination for comparison evidence.
        environment (Mapping[str, str] | None): Provider variables, or the current environment.

    Returns:
        str: Policy accepted by the single-chart suite executor.

    Raises:
        ValueError: The requested rerun policy is unknown.
    """
    if rerun not in {"auto", "failed", "all"}:
        raise ValueError("rerun must be auto, failed, or all")
    env = os.environ if environment is None else environment
    tagged = bool(
        env.get("CI_COMMIT_TAG")
        or env.get("CIRCLE_TAG")
        or env.get("GITHUB_REF_TYPE") == "tag"
        or env.get("GITHUB_REF", "").startswith("refs/tags/")
    )
    selected = "all" if tagged else rerun
    if incremental:
        changes = comparison(chart.resolve(), base_ref, environment=env)
        if selected == "auto":
            selected = "all" if chart_changed(chart, changes) else "failed"
        changes["rerun"] = selected
        changes["release_tag"] = tagged
        if report is not None:
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps(changes, indent=2) + "\n")
        print(
            f"[INFO] Incremental chart comparison: {changes.get('base_ref')}; status={changes['status']}; rerun={selected}",
            file=sys.stderr,
        )
    return selected


def main(argv: list[str] | None = None) -> int:
    """
    Print a shell-consumable rerun policy without mixing diagnostics into stdout.

    Args:
        argv (list[str] | None): Explicit arguments, or the process command line.

    Returns:
        int: Zero after emitting one policy token.
    """
    parser = argparse.ArgumentParser(description="Select incremental CI retries using Git history; release tags always run fresh tests.")
    parser.add_argument("chart", type=Path, help="local chart directory")
    parser.add_argument("--incremental", choices=("true", "false"), default="true", help="enable Git-based selection (default: true)")
    parser.add_argument("--rerun", choices=("auto", "failed", "all"), default="auto", help="requested property retry policy")
    parser.add_argument("--base-ref", help="override the comparison reference")
    parser.add_argument("--report", type=Path, help="write Git comparison evidence to JSON")
    args = parser.parse_args(argv)
    print(select_rerun(args.chart, incremental=args.incremental == "true", rerun=args.rerun, base_ref=args.base_ref, report=args.report))
    return 0
