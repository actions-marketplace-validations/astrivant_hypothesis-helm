"""
Plot compiler graph measurements for exactly the charts included in a report.
"""

import re
from pathlib import Path
from urllib.parse import unquote

from attrs import frozen

__all__ = ("GraphMetrics", "published_metrics", "write_graph_overview")


@frozen
class GraphMetrics:
    """
    Describe one published dependency multigraph without inferring missing measurements.

    Attributes:
        chart (str): Exact chart identity in the study inventory.
        status (str): Whether the exported graph includes a rendered baseline.
        vertices (int): Number of exported vertices.
        edges (int): Number of exported edges, including parallel references.
        components (int): Number of weakly connected components.
    """

    chart: str
    status: str
    vertices: int
    edges: int
    components: int


def published_metrics(root: Path) -> dict[Path, GraphMetrics]:
    """
    Read the published measurement table when disposable raw study data is absent.

    Args:
        root (Path): Published chart-topology study directory.

    Returns:
        dict[Path, GraphMetrics]: Verified counts keyed by the corresponding chart diagram directory.
    """
    index = root / "README.md"
    if not index.is_file():
        return {}
    rows: dict[Path, GraphMetrics] = {}
    for line in index.read_text().splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            continue
        link = re.fullmatch(r"\[([^\]]+)\]\(<?([^>)]+)>?\)", cells[1])
        if link is None or not all(value.isdigit() for value in cells[3:]):
            continue
        vertices, edges, components, cycles = map(int, cells[3:])
        if components > vertices or cycles != edges - vertices + components or (vertices > 0 and components == 0):
            continue
        directory = (root / unquote(link[2])).resolve().parent
        if not directory.is_relative_to(root.resolve()) or directory in rows:
            continue
        rows[directory] = GraphMetrics(link[1], cells[2], vertices, edges, components)
    return rows


def write_graph_overview(rows: tuple[GraphMetrics, ...], destination: Path, total: int) -> str:
    """
    Draw graph size and independent-cycle counts for this report's selected charts.

    Args:
        rows (tuple[GraphMetrics, ...]): Matching published measurements, in report order.
        destination (Path): Report-specific PNG destination.
        total (int): Number of chart sections, including those without measurements.

    Returns:
        str: Caption identifying measurement coverage and the meaning of both panels.
    """
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    figure = Figure(figsize=(12, 5.5), layout="constrained")
    FigureCanvasAgg(figure)
    axes = figure.subplots(1, 2)
    for rendered, label, marker, color in (
        (True, "Rendered baseline", "o", "#0072B2"),
        (False, "Static graph only", "D", "#D55E00"),
    ):
        selected = [row for row in rows if (row.status == "rendered") == rendered]
        if not selected:
            continue
        vertices = [row.vertices for row in selected]
        style = {"label": f"{label} ({len(selected)})", "marker": marker, "color": color, "alpha": 0.7}
        axes[0].scatter(vertices, [row.edges for row in selected], **style)
        axes[1].scatter(vertices, [row.edges - row.vertices + row.components for row in selected], **style)
    axes[0].set(title="Graph size", xlabel=r"Vertices $|V|$", ylabel=r"Connections $|E|$")
    axes[1].set(
        title="Graph connectivity",
        xlabel=r"Vertices $|V|$",
        ylabel=r"Independent undirected cycles $|E| - |V| + C$",
    )
    for axis in axes:
        # Symmetric-log axes retain literal zeroes instead of moving them to one.
        axis.set_xscale("symlog", linthresh=1)
        axis.set_yscale("symlog", linthresh=1)
        axis.set_xlim(left=0)
        axis.set_ylim(bottom=0)
        axis.grid(alpha=0.2)
        axis.tick_params(labelsize=12)
        axis.xaxis.label.set_fontsize(14)
        axis.yaxis.label.set_fontsize(14)
        axis.title.set_fontsize(15)
        axis.legend(fontsize=12)
    figure.suptitle(f"Compiler graph structure: {len(rows)} of {total} report charts\nEach point is one chart in this report", fontsize=13)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=170)
    return (
        f"Published graph measurements are available for {len(rows)} of {total} report charts. "
        "Vertices represent inputs, conditions, templates and manifest fields; edges connect them. "
        "The right panel counts independent loops after ignoring edge direction; C is the number of disconnected groups. "
        "Parallel edges count separately. These are structural measurements from the published chart diagrams, not bug counts."
    )
