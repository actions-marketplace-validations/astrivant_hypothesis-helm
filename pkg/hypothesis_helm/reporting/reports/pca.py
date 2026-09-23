"""
Draw one comparable before/after output projection for the charts in a scan report.
"""

import math
from colorsys import hsv_to_rgb
from pathlib import Path

from hypothesis_helm.analysis.output_space import ENCODING, project
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("PCA_LABEL", "write_pca")

PCA_LABEL = "Output-space PCA before and after selection"


def write_pca(report: dict[str, object], destination: Path) -> str | None:
    """
    Publish paired PCA panels using one fit, common axes and stable chart colors.

    Args:
        report (dict[str, object]): Scan records with optional measured reference observations.
        destination (Path): PNG beside the report.

    Returns:
        str | None: Caption reporting measurement coverage, or None for a legacy report with no reference data.
    """
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.colors import to_hex
    from matplotlib.figure import Figure
    from matplotlib.lines import Line2D

    charts = [mapping(row) for row in sequence(report["charts"])]
    if not any("output_space" in chart for chart in charts):
        return None
    vectors = []
    owners = []
    retained = []
    measured = set()
    failures = 0
    for index, chart in enumerate(charts):
        reference = mapping(chart.get("output_space", {}))
        failures += int(str(reference.get("render_failures", 0)))
        if reference.get("encoding") != ENCODING:
            continue
        for item in sequence(reference.get("observations", [])):
            observation = mapping(item)
            vectors.append([float(str(value)) for value in sequence(observation["vector"])])
            owners.append(index)
            retained.append(observation.get("retained"))
            measured.add(index)
    scores, basis = project(vectors)
    variance = sequence(basis["explained_variance_ratio"])
    colors = [
        to_hex(hsv_to_rgb((index * 0.61803398875) % 1, 0.55 + (index % 3) * 0.1, 0.7 + (index % 2) * 0.2)) for index in range(len(charts))
    ]
    figure = Figure(figsize=(12, 8), dpi=220, facecolor="white")
    FigureCanvasAgg(figure)
    # Reserve a bounded legend area; numbered entries refer to the chart key
    # instead of squeezing long chart paths around the scatter plots.
    axes = [figure.add_axes((left, 0.37, 0.34, 0.51)) for left in (0.09, 0.58)]
    for panel, axis in enumerate(axes):
        for index in sorted(measured):
            positions = [position for position, owner in enumerate(owners) if owner == index and (panel == 0 or retained[position] is True)]
            if positions:
                axis.scatter(scores[positions, 0], scores[positions, 1], color=colors[index], s=12, alpha=0.6, linewidths=0)
        axis.set_title("Before selection (reference sample)" if panel == 0 else "After recorded selection", fontsize=14)
        axis.set_xlabel(rf"$\mathrm{{PC}}_1$ ({float(str(variance[0])):.1%})", fontsize=12)
        axis.set_ylabel(rf"$\mathrm{{PC}}_2$ ({float(str(variance[1])):.1%})", fontsize=12)
        axis.tick_params(labelsize=10)
        axis.grid(alpha=0.15)
        if len(scores):
            for dimension, setter in ((0, axis.set_xlim), (1, axis.set_ylim)):
                low, high = float(scores[:, dimension].min()), float(scores[:, dimension].max())
                pad = max((high - low) * 0.08, 0.5)
                setter(low - pad, high + pad)
        else:
            axis.text(0.5, 0.5, "No comparable outputs", transform=axis.transAxes, ha="center", fontsize=13)
        if panel and scores.size and not any(value is True for value in retained):
            note = "Selection unavailable" if any(value is None for value in retained) else "No reference outputs retained"
            axis.text(0.5, 0.5, note, transform=axis.transAxes, ha="center", fontsize=13)
    columns = min(16, max(1, math.ceil(len(charts) / 6)))
    handles = [
        Line2D(
            [],
            [],
            marker="o",
            linestyle="",
            color=colors[index],
            markerfacecolor=colors[index] if index in measured else "none",
            markersize=5,
        )
        for index in range(len(charts))
    ]
    figure.legend(
        handles,
        [f"{index + 1:02d}" for index in range(len(charts))],
        loc="lower center",
        ncol=columns,
        fontsize=11,
        frameon=False,
        columnspacing=0.8,
        handletextpad=0.3,
        bbox_to_anchor=(0.5, 0.02),
    )
    figure.text(0.5, 0.285, "Chart numbers match the Overview; hollow markers mean no measured output", ha="center", fontsize=10)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=220)
    report["output_pca"] = {
        **basis,
        "charts_measured": len(measured),
        "charts_total": len(charts),
        "reference_observations": len(vectors),
        "retained_observations": sum(value is True for value in retained),
        "unknown_selection_observations": sum(value is None for value in retained),
        "render_failures": failures,
    }
    return (
        f"Bounded reference: {len(vectors):,} outputs from {len(measured)} of {len(charts)} charts; "
        f"{sum(value is True for value in retained):,} retained. Both panels share one PCA fit."
    )
