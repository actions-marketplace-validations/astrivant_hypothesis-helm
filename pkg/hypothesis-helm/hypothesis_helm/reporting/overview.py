"""
Show chart findings and scan durations as aligned, navigable report matrices.
"""

import math
from collections.abc import Mapping
from pathlib import Path
from typing import Literal

from attrs import frozen

from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.schemas.contracts import mapping, sequence

type Level = Literal["violation", "warning", "diagnostic", "clean", "incomplete", "untested"]

LEVELS: dict[Level, tuple[str, str]] = {
    "violation": ("Violation", "#b54242"),
    "warning": ("Warning", "#efd080"),
    "diagnostic": ("Diagnostic", "#9ac6df"),
    "clean": ("No findings", "#b4d6bb"),
    "incomplete": ("Incomplete", "#d5dbe2"),
    "untested": ("Not tested", "#f1f3f5"),
}
FINISHED = frozenset({"passed", "cached-pass", "failed"})
UNTESTED = frozenset({"pending", "not-started", "skipped-library", "skipped", "missing-values"})


@frozen
class ChartCell:
    """
    Keep a chart's finding classification separate from its testing progress.

    Attributes:
        name (str): Full chart path, in report order.
        level (Level): Highest observed finding kind or a neutral testing status.
        unfinished (bool): Selected work remains, or meaningful test results are unavailable.
        seconds (float | None): Time within the overview's common measurement scope.
    """

    name: str
    level: Level
    unfinished: bool
    seconds: float | None


@frozen
class CellLink:
    """
    Locate a chart cell inside the saved figure for PDF navigation.

    Attributes:
        chart (int): Zero-based chart position in the report.
        bounds (tuple[float, float, float, float]): Left, bottom, right and top in figure-relative coordinates.
    """

    chart: int
    bounds: tuple[float, float, float, float]


@frozen
class Overview:
    """
    Retain every chart in both matrices, with explicit findings and timing scopes.

    Attributes:
        charts (tuple[ChartCell, ...]): Chart observations in report order, never grouped into Other.
        timing_label (str): Testing time or historical elapsed time, never a mixture.
        caption (str): Measurement limits displayed beside the figure.
    """

    charts: tuple[ChartCell, ...]
    timing_label: str
    caption: str


def measured_seconds(value: object) -> float | None:
    """
    Distinguish valid durations from missing, negative, or nonfinite measurements.

    Args:
        value (object): Duration recorded in a scan or historical report.

    Returns:
        float | None: Nonnegative finite seconds, or an unknown measurement.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        return None
    try:
        seconds = float(value)
    except (ValueError, OverflowError):
        return None
    return seconds if math.isfinite(seconds) and seconds >= 0 else None


def finding_kind(record: Mapping[str, object]) -> str | None:
    """
    Read a finding's evidence category without assigning an invented impact rating.

    Args:
        record (Mapping[str, object]): An audit finding or deduplicated runtime diagnostic.

    Returns:
        str | None: Violation, warning or diagnostic; suppressed observations have no category.
    """
    if record.get("suppressed") or record.get("status") == "ignored":
        return None
    definition = record.get("finding")
    finding = definition if isinstance(definition, dict) else record
    kind = finding.get("kind")
    if kind in {"violation", "warning", "diagnostic"}:
        return str(kind)
    code = str(record.get("code", finding.get("code", "")))
    return CATALOG[code].kind if code in CATALOG else "diagnostic"


def unfinished(chart: Mapping[str, object]) -> bool:
    """
    Identify unfinished selected work without treating ordinary sampling as a timeout.

    Args:
        chart (Mapping[str, object]): Chart status, selected-path ledger and recorded phases.

    Returns:
        bool: Whether meaningful test results are absent or selected work remains unfinished.
    """
    if chart.get("status") not in FINISHED or str(chart.get("coverage", "")).endswith("only"):
        return True
    traversal = mapping(chart.get("traversal", {}))
    if any((measured_seconds(traversal.get(key)) or 0) > 0 for key in ("remaining_paths", "incomplete_paths")):
        return True
    if (measured_seconds(chart.get("remaining_iterations")) or 0) > 0:
        return True
    return any(
        mapping(phase).get("status") in {"interrupted", "time-limit", "timeout", "error", "generation-error", "pending"}
        for phase in sequence(chart.get("phases", []))
    )


def summarize(report: Mapping[str, object]) -> Overview:
    """
    Classify chart findings and keep unknown timings separate from measured zeroes.

    Args:
        report (Mapping[str, object]): Scan summary after diagnostic deduplication.

    Returns:
        Overview: One cell per chart with the highest observed finding kind and a plain-language caption.
    """
    charts = [mapping(item) for item in sequence(report.get("charts", []))]
    groups = {str(mapping(item)["id"]): mapping(item) for item in sequence(report.get("error_groups", []))}
    testing = any(measured_seconds(chart.get("testing_seconds")) is not None for chart in charts)
    timing_key = "testing_seconds" if testing else "elapsed_seconds"
    cells = []
    for chart in charts:
        audit = mapping(chart.get("audit", {}))
        observations = [mapping(item) for key in ("findings", "unresolved") for item in sequence(audit.get(key, []))]
        observations.extend(groups.get(str(reference), {}) for reference in sequence(chart.get("error_refs", [])))
        kinds = {finding_kind(item) for item in observations}
        incomplete = unfinished(chart)
        level: Level
        if "violation" in kinds:
            level = "violation"
        elif "warning" in kinds:
            level = "warning"
        elif "diagnostic" in kinds or chart.get("status") in {"failed", "baseline-failed", "error"}:
            level = "diagnostic"
        elif chart.get("status") in UNTESTED:
            level = "untested"
        elif incomplete:
            level = "incomplete"
        else:
            level = "clean"
        cells.append(ChartCell(str(chart["chart"]), level, incomplete, measured_seconds(chart.get(timing_key))))
    unknown = sum(cell.seconds is None for cell in cells)
    caption = (
        "Each cell is one chart; both grids follow chart-section order. Click a cell in the PDF for details. "
        "Colors show the highest observed finding kind, not a security or business-impact score. "
        "Hatching marks unfinished or unavailable testing, even when a finding was recorded. "
        "No findings means none in the completed sample, not exhaustive coverage. "
        + ("Testing time excludes dependency preparation. " if testing else "Elapsed chart time includes dependency preparation. ")
        + (f"Timing is unavailable for {unknown} of {len(charts)} charts; -- is not zero." if unknown else "")
    )
    return Overview(tuple(cells), "Testing time" if testing else "Elapsed chart time", caption)


def grid_shape(count: int) -> tuple[int, int]:
    """
    Arrange charts row by row in a bounded-width matrix without dropping any entries.

    Args:
        count (int): Number of chart records.

    Returns:
        tuple[int, int]: Row and column counts, with at least one cell for an empty report.
    """
    columns = min(12, max(1, math.ceil(math.sqrt(count * 2))))
    columns = min(max(count, 1), columns)
    return max(1, math.ceil(count / columns)), columns


def write_overview(overview: Overview, destination: Path) -> tuple[CellLink, ...]:
    """
    Draw two aligned chart matrices and return their PDF navigation rectangles.

    Args:
        overview (Overview): Classified findings and measurement scopes to display.
        destination (Path): PNG beside the Markdown report, also embedded in its PDF.

    Returns:
        tuple[CellLink, ...]: Figure-relative chart rectangles for both panels, including incomplete charts.
    """
    from matplotlib import colormaps
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.colors import Normalize
    from matplotlib.figure import Figure
    from matplotlib.patches import Patch, Rectangle

    figure = Figure(figsize=(10, 9), dpi=240, facecolor="white")
    FigureCanvasAgg(figure)
    finding_axis = figure.add_axes((0.045, 0.56, 0.88, 0.33))
    time_axis = figure.add_axes((0.045, 0.075, 0.88, 0.33))
    axes = (finding_axis, time_axis)
    rows, columns = grid_shape(len(overview.charts))
    seconds = [cell.seconds for cell in overview.charts if cell.seconds is not None]
    maximum = max(seconds, default=0)
    normalize = Normalize(vmin=0, vmax=max(maximum, 1))
    colors = colormaps["Blues"]
    links = []
    labels = [
        ("Findings by chart", "Which charts have violations, warnings, or unresolved diagnostics?"),
        (f"{overview.timing_label} by chart", "Which charts used the most time? Cells match the chart grid above."),
    ]
    for axis, (title, question) in zip(axes, labels, strict=True):
        axis.set_title(title, loc="left", fontsize=14, weight="bold", pad=30)
        axis.text(0, 1.035, question, transform=axis.transAxes, fontsize=9.5, color="#53616b")
        axis.set_xlim(-0.5, columns - 0.5)
        axis.set_ylim(rows - 0.5, -0.5)
        axis.set_axis_off()
        if not overview.charts:
            axis.text(0.5, 0.5, "No chart results recorded", ha="center", va="center", transform=axis.transAxes)
        position = axis.get_position()
        for index, cell in enumerate(overview.charts):
            row, column = divmod(index, columns)
            is_findings = axis is finding_axis
            color = LEVELS[cell.level][1] if is_findings else "#f1f3f5" if cell.seconds is None else colors(normalize(cell.seconds))
            axis.add_patch(Rectangle((column - 0.48, row - 0.48), 0.96, 0.96, facecolor=color, edgecolor="white", linewidth=0.6))
            if is_findings and cell.unfinished:
                axis.add_patch(
                    Rectangle((column - 0.48, row - 0.48), 0.96, 0.96, fill=False, hatch="/", edgecolor="#697887", linewidth=0.35)
                )
            dark = cell.level == "violation" if is_findings else cell.seconds is not None and normalize(cell.seconds) > 0.65
            number = str(index + 1).zfill(2)
            if is_findings:
                name = " ".join(cell.name.rsplit("/", 1)[-1].split())
                limit = 12 if columns >= 10 else 18
                side = (limit - 3) // 2
                name = name if len(name) <= limit else name[:side] + "..." + name[-side:]
                text = f"{number}\n{name}" if len(overview.charts) <= 180 else number
            else:
                value = "--" if cell.seconds is None else f"{cell.seconds:,.1f}s" if cell.seconds < 60 else f"{cell.seconds / 60:,.1f}m"
                text = f"{number}\n{value}" if len(overview.charts) <= 180 else value
            axis.text(
                column,
                row,
                text,
                ha="center",
                va="center",
                color="white" if dark else "#23313d",
                fontsize=min(10, max(3, min(95 / columns, 85 / rows))),
                linespacing=1.25,
                parse_math=False,
            )
            links.append(
                CellLink(
                    index,
                    (
                        position.x0 + column / columns * position.width,
                        position.y0 + (rows - row - 1) / rows * position.height,
                        position.x0 + (column + 1) / columns * position.width,
                        position.y0 + (rows - row) / rows * position.height,
                    ),
                )
            )
    handles = [Patch(facecolor=color, label=label, edgecolor="#bdc6ce") for label, color in LEVELS.values()]
    handles.append(Patch(facecolor="white", hatch="/", edgecolor="#697887", label="Testing unfinished / unavailable"))
    figure.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.04, 0.548), ncol=4, frameon=False, fontsize=8.3)
    if seconds:
        from matplotlib.cm import ScalarMappable
        from matplotlib.ticker import MaxNLocator

        bar = figure.colorbar(ScalarMappable(norm=normalize, cmap=colors), cax=figure.add_axes((0.94, 0.075, 0.014, 0.33)))
        bar.set_label("Seconds", fontsize=8)
        bar.ax.tick_params(labelsize=8, length=2)
        bar.locator = MaxNLocator(nbins=4)
        bar.update_ticks()
    figure.text(
        0.045,
        0.025,
        "Read left to right, then down. Cell numbers match the chart sections; -- means timing unavailable.",
        fontsize=8.5,
        color="#53616b",
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination)
    figure.clear()
    return tuple(links)
