"""
Measure bounded, chart-specific sensitivity panels for an existing repository report.
"""

import argparse
import hashlib
import json
import math
import shutil
import tempfile
import textwrap
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from jsonschema import validators

from hypothesis_helm.analysis.sensitivity import Mutation, analyze
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.inputs import load_input_chart
from hypothesis_helm.compiler.randomness.model import RandomInputs
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.execution.runtime.budget import parse_time_limit
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.reporting.console.progress import format_path
from hypothesis_helm.reporting.reports.figures import SENSITIVITY_FIELDS_KEY
from hypothesis_helm.reporting.reports.links import Publication
from hypothesis_helm.reporting.reports.repository import write_reports
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence

__all__ = ("main", "measure_chart", "mutations", "plot_panel", "prepare_figures")


def mutations(values: dict[str, object], schema: dict[str, object], limit: int, seed: int) -> list[Mutation]:
    """
    Select reproducible scalar changes without inventing arbitrary strings or collection shapes.

    Args:
        values (dict[str, object]): Supplied baseline values.
        schema (dict[str, object]): Authored acceptance contract.
        limit (int): Maximum distinct input paths to measure.
        seed (int): Stable path-order seed.

    Returns:
        list[Mutation]: Schema-valid Boolean flips and adjacent integer changes on unique existing paths.
    """
    if limit < 1:
        raise ValueError("mutation limit must be positive")
    candidates: list[Mutation] = []
    pending: list[tuple[object, tuple[str | int, ...]]] = [(values, ())]
    while pending:
        value, path = pending.pop()
        if isinstance(value, dict):
            pending.extend((child, (*path, str(key))) for key, child in value.items())
        elif isinstance(value, list):
            pending.extend((child, (*path, index)) for index, child in enumerate(value))
        elif type(value) is bool:
            candidates.append(Mutation(format_path(path), path, not value))
        elif type(value) is int:
            candidates.extend(Mutation(format_path(path), path, value + delta) for delta in (1, -1))
    candidates.sort(key=lambda mutation: hashlib.sha256(f"{seed}:{mutation.name}".encode()).digest())
    validator = validators.validator_for(schema)(schema)
    selected: list[Mutation] = []
    paths: set[tuple[str | int, ...]] = set()
    for candidate in candidates:
        if candidate.path not in paths and validator.is_valid(json_value(candidate.apply(values))):
            selected.append(candidate)
            paths.add(candidate.path)
            if len(selected) == limit:
                break
    return selected


def measure_chart(source: Path, *, helm: str, limit: int, seed: int, seconds: float, stopped: threading.Event) -> dict[str, object]:
    """
    Prepare a private source copy and compare only outputs with a repeatable baseline.

    Args:
        source (Path): Original chart directory, never modified.
        helm (str): Helm executable.
        limit (int): Mutation-path budget; all unordered pairs within it are measured.
        seed (int): Reproducible path-selection seed.
        seconds (float): Sensitivity budget excluding dependency preparation.
        stopped (threading.Event): Coordinator cancellation signal checked before each render.

    Returns:
        dict[str, object]: Actual measurements or an explicit reason measurements were unavailable.
    """
    empty: dict[str, object] = {"status": "unavailable", "mutations": [], "interactions": [], "sequence": [], "renders": 0}
    try:
        with tempfile.TemporaryDirectory(prefix="hypothesis-helm-sensitivity-") as temporary:
            target = Path(temporary) / "chart"
            shutil.copytree(source, target)
            metadata = mapping(yamlio.load((target / "Chart.yaml").read_text()))
            if metadata.get("type") == "library":
                return {**empty, "reason": "Library chart: no standalone rendered baseline."}
            if stopped.is_set():
                return {**empty, "reason": "Analysis cancelled."}
            if metadata.get("dependencies"):
                prepared = Processes().run([helm, "dependency", "build", str(target)], capture_output=True, timeout=60)
                if prepared.returncode:
                    return {**empty, "reason": "Dependency preparation failed.", "diagnostic": prepared.stderr}
            chart = load_input_chart(target)
            validators.validator_for(chart.schema)(chart.schema).validate(json_value(chart.defaults))
            selected = mutations(chart.defaults, chart.schema, limit, seed)
            if not selected:
                return {**empty, "reason": "No schema-valid Boolean or integer mutations were available."}
            deadline = time.monotonic() + seconds

            def invoke(values: dict[str, object]) -> object:
                """
                Render one configuration within the remaining measurement budget.

                Args:
                    values (dict[str, object]): Complete selected input.

                Returns:
                    object: Validated manifests with supported randomness controlled.
                """
                remaining = deadline - time.monotonic()
                if stopped.is_set() or remaining <= 0:
                    raise TimeoutError("Sensitivity measurement stopped")
                with RandomInputs() as draws:
                    output = render(chart, values, helm=helm, timeout=min(30, remaining), stream=False)
                    if draws.fallback_reason:
                        raise ValueError("Uncontrolled renderer effects: " + draws.fallback_reason)
                    return output

            baseline = invoke(chart.defaults)
            if baseline != invoke(chart.defaults):
                return {
                    **empty,
                    "renders": 2,
                    "reason": "Repeated baseline renders differed; output changes cannot be attributed to inputs.",
                }
            result = analyze(
                chart.defaults,
                chart.schema,
                selected,
                invoke,
                max_mutations=limit,
                max_pairs=math.comb(len(selected), 2),
                time_limit=max(0.001, deadline - time.monotonic()),
            )
            result["baseline_verification_renders"] = 2
            return result
    except Exception as error:
        return {**empty, "reason": str(error), "error_type": type(error).__name__}


def _field_path(row: dict[str, object]) -> str:
    """
    Preserve the exact field identity for the numbered figure caption.

    Args:
        row (dict[str, object]): Measured mutation with its path or a legacy name.

    Returns:
        str: Full field path, including array indices and quoted keys.
    """
    return (
        format_path(tuple(part if isinstance(part, int) else str(part) for part in sequence(row["path"])))
        if "path" in row
        else str(row["name"])
    )


def plot_panel(document: dict[str, object], destination: Path, title: str) -> None:
    """
    Save a compact chart-specific interaction panel without fabricating missing measurements.

    Args:
        document (dict[str, object]): Sensitivity observations or an unavailable status.
        destination (Path): Published PNG path.
        title (str): Exact chart identity.

    Returns:
        None: An interaction heatmap with a numbered field key is written.
    """
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    rows = [mapping(row) for row in sequence(document.get("mutations", []))]
    # Embed the key in the PNG so republishing a report cannot pair these
    # numbers with a different run's paths or require a separate data file.
    fields = [_field_path(row) for row in rows]
    figure = Figure(figsize=(8, 6.5), layout="constrained")
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    # Rows and columns represent the same field set, so preserve equal scales.
    axis.set_box_aspect(1)
    measured = sum("distance" in row for row in rows)
    positions = {str(row["name"]): index for index, row in enumerate(rows)}
    matrix = np.full((max(1, len(rows)), max(1, len(rows))), np.nan)
    pairs = [mapping(row) for row in sequence(document.get("interactions", [])) if "mixed_difference_l1" in mapping(row)]
    for pair in pairs:
        a, b = [positions[str(name)] for name in sequence(pair["mutations"])]
        matrix[a, b] = matrix[b, a] = int(str(pair["mixed_difference_l1"]))
    if pairs:
        image = axis.imshow(
            np.ma.masked_invalid(matrix),
            origin="lower",
            aspect="equal",
            cmap="viridis",
            vmin=0,
            vmax=max(1, float(np.nanmax(matrix))),
            extent=(0.5, len(rows) + 0.5, 0.5, len(rows) + 0.5),
        )
        colorbar = figure.colorbar(image, ax=axis, shrink=0.5)
        colorbar.set_label(r"$\|\Delta_i\Delta_j f\|_1$", fontsize=16)
        colorbar.ax.tick_params(labelsize=14)
    else:
        axis.text(0.5, 0.5, "No comparable\npairs", ha="center", va="center", fontsize=16, transform=axis.transAxes)
        axis.set(xticks=[], yticks=[])
    axis.set(
        title="Field interactions",
        xlabel="Field number (see caption)" if rows else "",
        ylabel="Field number" if rows else "",
    )
    axis.title.set_fontsize(16)
    axis.xaxis.label.set_fontsize(16)
    axis.yaxis.label.set_fontsize(16)
    axis.tick_params(labelsize=14)
    if rows:
        ticks = range(1, len(rows) + 1)
        axis.set_xticks(ticks)
        axis.set_yticks(ticks)
        axis.set(xlim=(0.5, len(rows) + 0.5), ylim=(0.5, len(rows) + 0.5))
    heading = textwrap.fill(title, width=60, break_on_hyphens=False)
    figure.suptitle(f"{heading}\n{measured} measured changes; {len(pairs)} pairs ({document['status']})", fontsize=18)
    if document.get("reason"):
        # Explain missing evidence in the published image, not only in the local JSON.
        reason = textwrap.shorten(" ".join(str(document["reason"]).split()), width=210, placeholder="...")
        figure.supxlabel("\n".join(textwrap.wrap(reason, 65)), fontsize=14)
    # Lay out the full-width heading first, then shrink only the plotted data.
    # Freezing the layout keeps savefig from stretching the heatmap back again.
    figure.canvas.draw()
    figure.set_layout_engine(None)
    position = axis.get_position()
    axis.set_position(
        (position.x0 + position.width * 0.1, position.y0 + position.height * 0.1, position.width * 0.8, position.height * 0.8)
    )
    if pairs:
        bar_position = colorbar.ax.get_position()
        colorbar.ax.set_position(
            (axis.get_position().x1 + 0.025, bar_position.y0 + bar_position.height * 0.1, bar_position.width, bar_position.height * 0.8)
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=170, metadata={SENSITIVITY_FIELDS_KEY: json.dumps(fields)})


def prepare_figures(
    report: dict[str, object],
    *,
    output: Path,
    cache: Path,
    source_root: Path,
    jobs: int = 6,
    limit: int = 8,
    seed: int = 0,
    seconds: float = 180,
    helm: str = "helm",
    repository: str | None = None,
) -> None:
    """
    Measure chart jobs concurrently and publish figures serially to avoid Matplotlib thread races.

    Args:
        report (dict[str, object]): Scan whose chart sections will receive these figures.
        output (Path): Published chart-topology study root, with chart-relative subdirectories.
        cache (Path): Local raw measurement directory.
        source_root (Path): Local chart repository matching the recorded scan revision.
        jobs (int): Maximum concurrent chart measurements.
        limit (int): Maximum measured paths per chart.
        seed (int): Reproducible input path ordering.
        seconds (float): Per-chart measurement limit, excluding dependency preparation.
        helm (str): Helm executable.
        repository (str | None): Published study namespace, such as bitnami or prometheus.

    Returns:
        None: Each chart receives actual sensitivity evidence or an explicit unavailable panel.
    """
    if jobs < 1 or limit < 1:
        raise ValueError("jobs and mutation limit must be positive")
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("measurement time must be finite and positive")
    source = mapping(report.get("source", {}))
    if source.get("kind") == "git" and source.get("revision"):
        revision = Processes().run(["git", "-C", str(source_root), "rev-parse", "HEAD"], capture_output=True, check=True, timeout=10)
        if revision.stdout.strip() != source["revision"]:
            raise ValueError("Chart checkout differs from the scan revision; use the recorded source before measuring sensitivity")
        changes = Processes().run(["git", "-C", str(source_root), "status", "--porcelain"], capture_output=True, check=True, timeout=10)
        if changes.stdout.strip():
            raise ValueError("Chart checkout has unrecorded changes; use a clean copy of the scan revision")
    charts = [mapping(chart) for chart in sequence(report["charts"])]
    stopped = threading.Event()
    pool = ThreadPoolExecutor(max_workers=jobs)
    futures = {}
    try:
        for chart in charts:
            name = str(chart["chart"])
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"Unsafe chart path: {name}")
            futures[
                pool.submit(measure_chart, source_root / relative, helm=helm, limit=limit, seed=seed, seconds=seconds, stopped=stopped)
            ] = chart
        for index, future in enumerate(as_completed(futures), 1):
            chart = futures[future]
            name = str(chart["chart"])
            document = future.result()
            document["context"] = {
                "chart": name,
                "source": report.get("source"),
                "seed": seed,
                "maximum_mutations": limit,
                "seconds": seconds,
                "measured_epoch": time.time(),
            }
            directory = cache / name
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "sensitivity.json").write_text(json.dumps(document, indent=2) + "\n")
            # Existing studies use bitnami/name and prometheus/name, while the
            # source checkouts use bitnami/name and charts/name respectively.
            source_path = Path(name)
            relative = Path(*source_path.parts[1:]) if source_path.parts and source_path.parts[0] in {repository, "charts"} else source_path
            study_path = Path(repository) / relative if repository else source_path
            destination = output / study_path / "sensitivity.png"
            plot_panel(document, destination, name)
            chart["report_figures"] = {"sensitivity": str(destination.resolve())}
            topology = output / study_path / "topology.png"
            if topology.is_file():
                mapping(chart["report_figures"])["topology"] = str(topology.resolve())
            print(f"[{index}/{len(charts)}] {name}: {document['status']}; {document.get('renders', 0)} renders", flush=True)
    except BaseException:
        stopped.set()
        raise
    finally:
        pool.shutdown(wait=True, cancel_futures=True)


def main(argv: list[str] | None = None) -> int:
    """
    Enrich saved scan reports without rerunning the scan or changing its findings.

    Args:
        argv (list[str] | None): Explicit command-line arguments.

    Returns:
        int: Zero after publication, or 130 after graceful interruption.
    """
    refresh_env()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan", type=Path, help="existing scan.json")
    parser.add_argument("--report", required=True, type=Path, help="Markdown/PDF output stem")
    parser.add_argument("--source-root", type=Path, help="local chart repository; defaults to the scan directory")
    parser.add_argument("--output", type=Path, default=Path("studies/chart-topologies"))
    parser.add_argument("--cache", type=Path, default=Path(".cache/report-figures"))
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--max-mutations", type=int, default=8)
    parser.add_argument("--time-limit", type=parse_time_limit, default=180)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--helm", default="helm")
    parser.add_argument("--repository", choices=("bitnami", "prometheus"), help="namespace used by the published topology study")
    parser.add_argument("--publication-url", help="optional public GitHub repository for links")
    args = parser.parse_args(argv)
    report = mapping(json.loads(args.scan.read_text()))
    try:
        prepare_figures(
            report,
            output=args.output,
            cache=args.cache / str(report["started_epoch"]),
            source_root=args.source_root or Path(str(report["directory"])),
            jobs=args.jobs,
            limit=args.max_mutations,
            seconds=args.time_limit,
            seed=args.seed,
            helm=args.helm,
            repository=args.repository,
        )
    except KeyboardInterrupt:
        return 130
    enriched = args.cache / str(report["started_epoch"]) / "report.json"
    enriched.parent.mkdir(parents=True, exist_ok=True)
    enriched.write_text(json.dumps(report, indent=2) + "\n")
    publication = Publication(Path.cwd(), args.publication_url, "main") if args.publication_url else None
    write_reports(report, args.report, publication=publication, artifact_links=False)
    return 0
