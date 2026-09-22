"""
Add requested sensitivity measurements to a live scan without changing its test outcomes.
"""

import argparse
import logging
import os
import time
from pathlib import Path

from hypothesis_helm.analysis.repository import prepare_figures
from hypothesis_helm.charts.suites.runtime import RenderOptions
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("enrich_scan",)

LOGGER = logging.getLogger(__name__)


def enrich_scan(report: dict[str, object], args: argparse.Namespace, *, root: Path, artifacts: Path, stem: Path) -> str:
    """
    Measure report figures while the scan's source checkout still exists.

    Args:
        report (dict[str, object]): Completed scan outcomes, updated only with figure metadata.
        args (argparse.Namespace): CLI measurement and renderer options.
        root (Path): Live local source or owned remote checkout.
        artifacts (Path): Raw run evidence directory.
        stem (Path): Final report destination, possibly including a Markdown or PDF extension.

    Returns:
        str: Complete, interrupted, or failed figure generation, independent of chart test statuses.
    """
    started = time.monotonic()
    metadata: dict[str, object] = {
        "status": "running",
        "maximum_mutations": args.max_mutations,
        "time_limit_seconds_per_chart": args.sensitivity_timeout,
    }
    report["figure_generation"] = metadata
    # Pending, invalid, and skipped charts do not become tested by requesting a figure.
    untested = {"pending", "skipped-library", "missing-values", "invalid-metadata", "invalid-values", "dependency-build-failed"}
    charts = [mapping(chart) for chart in sequence(report["charts"]) if mapping(chart).get("status") not in untested]
    requested = {**report, "charts": charts}
    output = stem.with_suffix("") if stem.suffix.lower() in {".md", ".pdf"} else stem
    LOGGER.info(
        "Measuring report sensitivity: up to %d fields per chart, %.0fs per chart in addition to testing",
        args.max_mutations,
        args.sensitivity_timeout,
    )
    try:
        prepare_figures(
            requested,
            output=output.parent / f"{output.name}-figures",
            cache=artifacts / "figures",
            source_root=root,
            jobs=(os.process_cpu_count() or 1) if args.jobs == "auto" else args.jobs,
            limit=args.max_mutations,
            seed=args.seed,
            seconds=args.sensitivity_timeout,
            helm=args.helm,
            verify_source=False,
            values_filename=args.values,
            build_dependencies=args.build_dependencies,
            render_options=RenderOptions(
                helm=args.helm,
                timeout=args.timeout,
                release=getattr(args, "release", "hypothesis"),
                namespace=getattr(args, "namespace", "default"),
                kube_version=getattr(args, "kube_version", None),
            ),
            progress=LOGGER.info,
        )
        metadata["status"] = "complete"
    except KeyboardInterrupt:
        metadata["status"] = "interrupted"
        LOGGER.warning("Report sensitivity interrupted; retaining scan results and completed figures")
    except Exception as error:
        metadata.update(status="failed", error=str(error))
        LOGGER.warning("Report sensitivity failed: %s; retaining scan results", error)
    finally:
        metadata["elapsed_seconds"] = time.monotonic() - started
    return str(metadata["status"])
