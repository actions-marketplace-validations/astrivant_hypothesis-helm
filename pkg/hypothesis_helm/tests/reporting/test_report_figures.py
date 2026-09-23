"""
Keep report diagrams tied to their charts and separate limitations from actual findings.
"""

import json
import re
from pathlib import Path

import pytest
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from hypothesis_helm.reporting.evidence.errors import chart_errors, deduplicate_errors
from hypothesis_helm.reporting.reports.figures import SENSITIVITY_FIELDS_KEY, study_figures
from hypothesis_helm.reporting.reports.repository import write_reports
from hypothesis_helm.reporting.reports.topology import published_metrics


@pytest.mark.parametrize("historical", [False, True])
def test_unsupported_work_has_no_numbered_error(tmp_path: Path, historical: bool) -> None:
    """
    Omit unsupported work from error groups without erasing its testing limitation.

    Args:
        tmp_path (Path): Isolated report destination.
        historical (bool): Republish previously serialized diagnostics or classify raw results.

    Returns:
        None: No E001 entry is fabricated and genuine failures still receive numbers.
    """
    limitation: dict[str, object] = {"status": "unsupported-schema", "phase": "chart", "error": "permutations need closed objects at ()"}
    chart: dict[str, object] = {"chart": "limited", **limitation}
    if historical:
        chart["error_diagnostics"] = [limitation]
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 2,
        "charts_discovered": 1,
        "counts": {"unsupported-schema": 1},
        "settings": {},
        "charts": [chart],
    }
    markdown, _ = write_reports(report, tmp_path / "report")
    assert "E001" not in markdown.read_text()
    assert "Testing limitation: permutations need closed objects" in markdown.read_text()
    assert report["error_groups"] == []
    # An actual diagnostic nested below an unsupported phase must survive.
    failure = {"status": "failed", "error": "[HH1101] Invalid YAML", "phase": "$.name"}
    assert len(chart_errors({**chart, "findings": [failure]})) == 1
    chart["error_diagnostics"] = [limitation, failure]
    deduplicate_errors(report)
    assert len(report["error_groups"]) == 1


def test_diagram_pages_and_pairs_include_charts_without_errors(tmp_path: Path) -> None:
    """
    Put aggregate graphs in an appendix while keeping chart panels below their headings.

    Args:
        tmp_path (Path): Project containing uniquely colored chart-specific images.

    Returns:
        None: Contents and graph destinations resolve, with a side-by-side pair for a chart without errors.
    """
    studies = tmp_path / "studies/chart-topologies"
    chart_dir = studies / "vendor/clean"
    chart_dir.mkdir(parents=True)
    (studies / "README.md").write_text("| vendor | [vendor/clean](vendor/clean/README.md) | rendered | 10 | 15 | 2 | 7 |\n")
    for path, color in (
        (studies / "graph-invariants.png", "red"),
        (chart_dir / "topology.png", "green"),
        (chart_dir / "sensitivity.png", "blue"),
    ):
        metadata = PngInfo()
        if path.name == "sensitivity.png":
            metadata.add_text(SENSITIVITY_FIELDS_KEY, json.dumps(["$.first.enabled", "$.pods[2].replicas"]))
        Image.new("RGB", (400, 240), color).save(path, pnginfo=metadata)
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 2,
        "charts_discovered": 1,
        "counts": {"passed": 1},
        "settings": {},
        "charts": [{"chart": "vendor/clean", "status": "passed"}],
    }
    markdown, pdf = write_reports(report, tmp_path / "docs/reports/report")
    text = markdown.read_text()
    assert text.startswith("# Scan results: charts\n")
    assert "E001" not in text
    assert "![Topology: vendor/clean]" in text and "![Sensitivity: vendor/clean]" in text
    assert text.index("### vendor/clean") < text.index("![Topology:") < text.index("Status: passed")
    assert text.index("![Sensitivity:") < text.index("[Sensitivity field key](#vendorclean-1)") < text.index("Status: passed")
    assert "- **1**: `$.first.enabled`\n- **2**: `$.pods[2].replicas`" in text
    assert text.index("Status: passed") < text.index("## Appendix: sensitivity field keys") < text.index("- **1**: `$.first.enabled`")
    assert "$.first.enabled" not in text.split("## Appendix: sensitivity field keys")[0]
    assert "[Back to chart](#vendorclean)" in text
    assert "1 of 1 report charts" in text
    objects = dict(re.findall(rb"(\d+) 0 obj\s*(.*?)\s*endobj", pdf.read_bytes(), re.DOTALL))
    pages = [(number, body) for number, body in objects.items() if b"/Type /Page\n" in body]
    graph_outline = next(body for body in objects.values() if b"/Title (Appendix: graph structure)" in body)
    graph_page = next(index for index, (number, _) in enumerate(pages) if b"/Dest [ " + number + b" 0 R" in graph_outline)
    assert graph_page > 3
    assert text.index("Status: passed") < text.index("## Appendix: graph structure")
    images_per_page = [len(re.findall(rb"/FormXob\.[^\s]+ \d+ 0 R", body)) for _, body in pages]
    assert images_per_page[:3] == [1, 1, 2]  # Cover, contents, and overview, each with its header logo.
    assert images_per_page[graph_page] == 2
    summary_outline = next(body for body in objects.values() if b"/Title (Scan summary)" in body)
    assert b"/Dest [ " + pages[3][0] + b" 0 R" in summary_outline
    overview_outline = next(body for body in objects.values() if b"/Title (Overview)" in body)
    assert b"/Dest [ " + pages[2][0] + b" 0 R" in overview_outline
    assert 3 in images_per_page[3:graph_page]  # The clean chart keeps both panels together before the appendices.
    chart_outline = next(body for body in objects.values() if b"/Title (vendor/clean)" in body)
    target = re.search(rb"/Dest \[ (\d+) 0 R", chart_outline)
    assert target is not None
    assert len(re.findall(rb"/FormXob\.[^\s]+ \d+ 0 R", objects[target[1]])) == 3
    assert "Topology shows published dependency structure" not in text
    assert "Unavailable or failed measurements are not zero sensitivity" not in text
    assert "Plot guide:" not in text.split("## Charts", 1)[1].split("## Appendix:", 1)[0]
    assert "### Chart topology" in text and "### Field interactions" in text
    assert text.index("## Appendix: plot guide") < text.index("## Appendix: finding codes")
    # Plot captions remain clickable without repeating the interpretation guide;
    # sensitivity captions reach this chart's key instead of the general guide.
    chart_links = [objects[ref] for ref in re.findall(rb"(\d+) 0 R", objects[target[1]].split(b"/Annots [", 1)[1].split(b"]", 1)[0])]
    outline = next(body for body in objects.values() if b"/Title (Chart topology)" in body)
    destination = re.search(rb"/Dest \[ ([^]]+)\]", outline)
    assert destination is not None
    assert any(b"/Dest [ " + destination[1] + b"]" in link for link in chart_links)
    key_outline = [body for body in objects.values() if b"/Title (vendor/clean)" in body][-1]
    key_target = re.search(rb"/Dest \[ ([^]]+)\]", key_outline)
    assert key_target is not None
    assert not key_target[1].startswith(target[1] + b" 0 R")
    assert sum(b"/Dest [ " + key_target[1] + b"]" in link for link in chart_links) >= 2
    scan_target = re.search(rb"/Dest \[ ([^]]+)\]", chart_outline)
    overview_links = [body for body in objects.values() if b"/Contents (Chart 01: vendor/clean)" in body]
    assert scan_target is not None and len(overview_links) == 2
    # Repeating the chart title in the field appendix must never redirect
    # either the findings cell or the testing-time cell away from the scan.
    assert all(b"/Dest [ " + scan_target[1] + b"]" in link for link in overview_links)
    assert all(b"/Dest [ " + key_target[1] + b"]" not in link for link in overview_links)


def test_missing_sensitivity_does_not_use_synthetic_reference(tmp_path: Path) -> None:
    """
    Preserve missing chart measurements even when a synthetic sensitivity study exists.

    Args:
        tmp_path (Path): Project with incomplete chart study assets.

    Returns:
        None: The synthetic plot and unsafe chart paths are never substituted for chart-specific data.
    """
    root = tmp_path / "studies/chart-topologies/vendor/clean"
    root.mkdir(parents=True)
    (root / "topology.png").touch()
    synthetic = tmp_path / "studies/sensitivity"
    synthetic.mkdir()
    (synthetic / "sensitivity.png").touch()
    figures = study_figures({"charts": [{"chart": "vendor/clean"}, {"chart": "../../outside"}]}, tmp_path / "docs/report.md")
    assert figures.charts == {"vendor/clean": (root / "topology.png", None)}


def test_overview_uses_only_report_chart_metrics(tmp_path: Path) -> None:
    """
    Select this report's diagram measurements instead of copying the all-repository scatter plot.

    Args:
        tmp_path (Path): Published inventory containing both included and unrelated charts.

    Returns:
        None: Unrelated charts and missing measurements cannot enter the report's graph distribution.
    """
    root = tmp_path / "studies/chart-topologies"
    for name in ("included", "unrelated"):
        directory = root / "vendor" / name
        directory.mkdir(parents=True)
        (directory / "topology.png").touch()
    (root / "graph-invariants.png").touch()
    (root / "README.md").write_text(
        "| vendor | [vendor/included](vendor/included/README.md) | rendered | 10 | 15 | 2 | 7 |\n"
        "| vendor | [vendor/unrelated](vendor/unrelated/README.md) | rendered | 10000 | 15000 | 2000 | 7000 |\n"
    )
    figures = study_figures({"charts": [{"chart": "vendor/included"}, {"chart": "vendor/missing"}]}, tmp_path / "docs/report.md")
    assert [(row.chart, row.vertices, row.edges) for row in figures.metrics] == [("vendor/included", 10, 15)]
    assert study_figures({"charts": [{"chart": "vendor/missing"}]}, tmp_path / "docs/report.md").metrics == ()


def test_published_counts_reject_invalid_or_absent_measurements(tmp_path: Path) -> None:
    """
    Validate graph arithmetic and keep missing graph counts out of numeric plots.

    Args:
        tmp_path (Path): Study table with valid, impossible, and absent measurements.

    Returns:
        None: Only exact, consistent graph counts are available for report selection.
    """
    (tmp_path / "README.md").write_text(
        "| vendor | [valid](valid/README.md) | static-only | 1 | 0 | 1 | 0 |\n"
        "| vendor | [bad-cycle](bad-cycle/README.md) | rendered | 10 | 15 | 2 | 99 |\n"
        "| vendor | [missing](missing/README.md) | incomplete | N/A | N/A | N/A | N/A |\n"
        "| vendor | [outside](../outside/README.md) | rendered | 10 | 15 | 2 | 7 |\n"
    )
    assert set(published_metrics(tmp_path)) == {tmp_path / "valid"}
