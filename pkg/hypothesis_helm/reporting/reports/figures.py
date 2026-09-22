"""
Locate published chart studies without substituting another chart's measurements.
"""

import json
from pathlib import Path, PurePosixPath

from attrs import frozen
from PIL import Image

from hypothesis_helm.reporting.reports.topology import GraphMetrics, published_metrics
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("ReportFigures", "SENSITIVITY_FIELDS_KEY", "study_figures")

SENSITIVITY_FIELDS_KEY = "hypothesis_helm_sensitivity_fields"


@frozen
class ReportFigures:
    """
    Bind report image labels to local assets, independently of published hyperlinks.

    Attributes:
        metrics (tuple[GraphMetrics, ...]): Published graph counts for this report's chart inventory only.
        charts (dict[str, tuple[Path | None, Path | None]]): Topology and sensitivity assets by exact chart identity.
        sensitivity_fields (dict[str, tuple[str, ...]]): Numbered paths embedded in each chart's sensitivity image.
    """

    metrics: tuple[GraphMetrics, ...]
    charts: dict[str, tuple[Path | None, Path | None]]
    sensitivity_fields: dict[str, tuple[str, ...]]


def study_figures(report: dict[str, object], destination: Path) -> ReportFigures:
    """
    Find study assets beside this report's project, retaining absent measurements as absent.

    Args:
        report (dict[str, object]): Scan with chart names and optional explicit figure paths.
        destination (Path): Report file or stem inside the project.

    Returns:
        ReportFigures: Available assets; unrelated working-directory studies are never imported.
    """
    root = next(
        (parent / "studies/chart-topologies" for parent in destination.resolve().parents if (parent / "studies/chart-topologies").is_dir()),
        None,
    )
    inventory = published_metrics(root) if root is not None else {}
    metrics = []
    charts = {}
    sensitivity_fields = {}
    for entry in sequence(report["charts"]):
        chart = mapping(entry)
        name = str(chart["chart"])
        parts = PurePosixPath(name)
        directory = root / name if root is not None and not parts.is_absolute() and ".." not in parts.parts else None
        explicit = mapping(chart.get("report_figures", {}))
        paths = []
        for kind in ("topology", "sensitivity"):
            path = Path(str(explicit[kind])) if kind in explicit else directory / f"{kind}.png" if directory else None
            paths.append(path if path is not None and path.is_file() else None)
        if any(paths):
            charts[name] = (paths[0], paths[1])
        if paths[1] is not None:
            # Read the key from the same image used by the report. Older plots
            # without a key remain usable, without inventing path assignments.
            with Image.open(paths[1]) as image:
                fields = json.loads(image.info.get(SENSITIVITY_FIELDS_KEY, "[]"))
            if isinstance(fields, list) and all(isinstance(field, str) for field in fields):
                sensitivity_fields[name] = tuple(fields)
        if paths[0] is not None:
            row = inventory.get(paths[0].resolve().parent)
            if row is not None and row.chart == name:
                metrics.append(row)
    return ReportFigures(tuple(metrics), charts, sensitivity_fields)
