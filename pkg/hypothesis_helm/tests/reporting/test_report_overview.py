"""
Verify compact report measurements, partial results, and navigable PDF front matter.
"""

import base64
import re
import zlib
from pathlib import Path

import pytest
from PIL import Image

from hypothesis_helm.reporting.documentation.contents import heading_inventory
from hypothesis_helm.reporting.evidence.errors import deduplicate_errors
from hypothesis_helm.reporting.reports.links import Publication
from hypothesis_helm.reporting.reports.overview import grid_shape, measured_seconds, summarize, unfinished, write_overview
from hypothesis_helm.reporting.reports.references import APPENDIX_TITLE, with_finding_reference
from hypothesis_helm.reporting.reports.repository import write_reports


@pytest.mark.parametrize("nested", [False, True])
def test_failure_at_deadline_keeps_incomplete_marker(nested: bool) -> None:
    """
    Keep the report's incomplete-work marker when a confirmed failure survives a deadline.

    Args:
        nested (bool): Read a direct chart result or a retained property phase.

    Returns:
        None: Failure severity does not conceal unfinished sampling or minimization.
    """
    failure: dict[str, object] = {"status": "failed", "stop_reason": "time-limit", "error": "observed error"}
    assert unfinished({"status": "failed", "phases": [failure]} if nested else failure)


def test_chart_findings_and_unknown_times_stay_separate() -> None:
    """
    Classify shared diagnostics and audit warnings while preserving partial measurements.

    Returns:
        None: Audit warnings have their own category; dependency time and unknown durations are not mixed into testing.
    """
    report: dict[str, object] = {
        "charts": [
            {
                "chart": "first",
                "status": "failed",
                "testing_seconds": 20,
                "elapsed_seconds": 90,
                "dependency_preparation_seconds": 70,
                "phases": [{"phase": f"path-{index}", "status": "failed", "error": "dependency failed"} for index in range(3)],
            },
            {"chart": "second", "status": "failed", "testing_seconds": 0, "error": "dependency failed"},
            {"chart": "unknown-time", "status": "incomplete", "elapsed_seconds": 200},
            {"chart": "audit-only", "status": "passed", "audit": {"findings": [{"code": "HH2001"}]}},
        ]
    }
    deduplicate_errors(report)
    overview = summarize(report)
    assert [(cell.name, cell.level) for cell in overview.charts] == [
        ("first", "diagnostic"),
        ("second", "diagnostic"),
        ("unknown-time", "incomplete"),
        ("audit-only", "warning"),
    ]
    assert [cell.seconds for cell in overview.charts] == [20, 0, None, None]
    assert overview.timing_label == "Testing time"
    assert "unavailable for 2 of 4" in overview.caption
    assert "excludes dependency preparation" in overview.caption


def test_historical_report_keeps_elapsed_scope() -> None:
    """
    Label historical wall-clock durations without pretending they measure testing alone.

    Returns:
        None: Known elapsed time remains usable and missing measurements remain unknown.
    """
    overview = summarize({"charts": [{"chart": "old", "elapsed_seconds": "12.5"}, {"chart": "missing"}]})
    assert [cell.seconds for cell in overview.charts] == [12.5, None]
    assert overview.timing_label == "Elapsed chart time"
    assert "includes dependency preparation" in overview.caption
    assert "unavailable for 1 of 2" in overview.caption


@pytest.mark.parametrize("value", [None, True, -1, float("nan"), float("inf"), "unknown", 10**1000])
def test_unknown_duration_is_never_shown_as_zero(value: object) -> None:
    """
    Reject unusable durations without inventing zero-length scans.

    Args:
        value (object): Invalid or unavailable historical measurement.

    Returns:
        None: Invalid timing is omitted from measured totals.
    """
    assert measured_seconds(value) is None


def test_grid_keeps_every_chart_in_report_order(tmp_path: Path) -> None:
    """
    Keep all charts, including unknown results, and expose matching PDF targets in both grids.

    Args:
        tmp_path (Path): Overview image destination.

    Returns:
        None: Every chart appears exactly once per panel, with bounded and disjoint navigation regions.
    """
    charts = [{"chart": f"chart-{index}", "status": "pending"} for index in range(150)]
    overview = summarize({"charts": charts})
    assert [cell.name for cell in overview.charts] == [chart["chart"] for chart in charts]
    rows, columns = grid_shape(len(charts))
    assert rows == columns and rows * columns >= len(charts) > (rows - 1) ** 2
    links = write_overview(overview, tmp_path / "matrix.png")
    assert [cell.chart for cell in links] == list(range(150)) * 2
    assert len({cell.bounds for cell in links}) == len(links)
    assert all(0 <= left < right <= 1 and 0 <= bottom < top <= 1 for cell in links for left, bottom, right, top in [cell.bounds])
    assert links[0].bounds[2] < links[150].bounds[0]
    with Image.open(tmp_path / "matrix.png") as image:
        width, height = image.size
    for cell in links:
        left, bottom, right, top = cell.bounds
        assert (right - left) * width == pytest.approx((top - bottom) * height)


def test_severity_uses_finding_kinds_without_concealing_incomplete_work() -> None:
    """
    Keep violations above audit warnings while separating execution diagnostics and partial coverage.

    Returns:
        None: Code categories control colors; status and remaining work independently control hatching.
    """
    charts = [
        {"chart": "violation", "status": "failed", "error": "[HH1101] Invalid YAML", "audit": {"findings": [{"code": "HH2001"}]}},
        {"chart": "warning", "status": "passed", "audit": {"findings": [{"code": "HH2001"}, {"code": "HH2006"}]}},
        {"chart": "diagnostic", "status": "failed", "error": "[HH1001] Custom rejection"},
        {"chart": "timeout", "status": "time-limit", "error": "[HH1201] Timeout"},
        {"chart": "unfinished", "status": "time-limit"},
        {"chart": "pending", "status": "pending"},
        {"chart": "clean", "status": "passed", "coverage_complete": False},
        {"chart": "ignored", "status": "passed", "audit": {"findings": [{"code": "HH2001", "suppressed": True}]}},
        {"chart": "failure-and-timeout", "status": "failed", "error": "[HH3001] Missing object", "traversal": {"remaining_paths": 4}},
    ]
    report: dict[str, object] = {"charts": charts}
    deduplicate_errors(report)
    overview = summarize(report)
    assert [cell.level for cell in overview.charts] == [
        "violation",
        "warning",
        "diagnostic",
        "diagnostic",
        "incomplete",
        "untested",
        "clean",
        "clean",
        "violation",
    ]
    assert [cell.unfinished for cell in overview.charts] == [False, False, False, True, True, True, False, False, True]
    assert "not a security or business-impact score" in overview.caption


@pytest.mark.parametrize("chart_count", [0, 2, 45])
def test_report_front_matter_and_internal_destinations(tmp_path: Path, chart_count: int) -> None:
    """
    Reserve the cover and contents pages before the overview, even for large scans.

    Args:
        tmp_path (Path): Paired report destination.
        chart_count (int): Empty, short, or multipage chart inventory.

    Returns:
        None: Embedded figures and internal links refer to real pages with duplicate-safe bookmarks.
    """
    charts = [{"chart": "repeated/name", "status": "passed", "testing_seconds": index} for index in range(chart_count)]
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 100,
        "charts_discovered": chart_count,
        "counts": {"passed": chart_count},
        "settings": {},
        "charts": charts,
    }
    markdown, pdf = write_reports(report, tmp_path / "report")
    content = pdf.read_bytes()
    objects = dict(re.findall(rb"(\d+) 0 obj\s*(.*?)\s*endobj", content, re.DOTALL))
    pages = [(number, body) for number, body in objects.items() if b"/Type /Page\n" in body]
    assert len(pages) >= 4
    # The header logo appears on every page; only the overview page has a second image.
    image_counts = [len(re.findall(rb"/FormXob\.[^\s]+ \d+ 0 R", body)) for _, body in pages]
    assert image_counts[0] == 1
    assert image_counts[1] == 1
    assert image_counts[2] == 2
    assert all(count == 1 for count in image_counts[3:])
    for index, (_, page) in enumerate(pages):
        annotations = re.search(rb"/Annots \[(.*?)\]", page, re.DOTALL)
        links = [objects[number] for number in re.findall(rb"(\d+) 0 R", annotations[1])] if annotations else []
        assert any(b"/URI (https://github.com/HypothesisWorks/hypothesis/)" in link for link in links) == (index > 0)
    assert b"/Outlines" in content
    destinations = re.findall(rb"/Dest \[ (\d+) 0 R", content)
    assert set(destinations) <= {number for number, _ in pages}
    assert pages[0][0] in destinations  # The title-page bookmark retains its own destination.
    assert pages[1][0] in destinations  # Footer links return to contents.
    assert pages[2][0] in destinations  # Contents links to the overview.
    chart_links = [body for body in objects.values() if re.search(rb"/Contents \(Chart ", body)]
    assert len(chart_links) == chart_count * 2
    chart_outlines = [body for body in objects.values() if b"/Title (repeated/name)" in body]
    for index, link in enumerate(chart_links):
        # Both matrices must reach the specific scan section, even when many
        # charts share a title and several sections occupy the same PDF page.
        actual = re.search(rb"/Dest \[ ([^]]+)\]", link)
        expected = re.search(rb"/Dest \[ ([^]]+)\]", chart_outlines[index % chart_count])
        assert actual is not None and expected is not None
        assert actual[1] == expected[1]
    assert "Overview cell: 01" in markdown.read_text() if chart_count else "Overview cell:" not in markdown.read_text()
    assert "[Overview](#overview)" in markdown.read_text()
    assert "![Chart severity and scan-time matrices](<report-overview.png>)" in markdown.read_text()
    if chart_count > 1:
        assert "[repeated/name](#repeatedname-1)" in markdown.read_text()
        assert content.count(b"/Title (repeated/name)") == chart_count


def test_code_appendix_keeps_literal_inputs_and_unique_targets() -> None:
    """
    Link findings to one definition each without altering reproducing values or external links.

    Returns:
        None: References survive repeated publication, unknown codes are explained, and duplicate headings have unique anchors.
    """
    document = "\n".join(
        [
            "# Report",
            "## Charts",
            "### HH1101 - Invalid YAML in rendered output",
            "#### E001 (HH1101)",
            "- `HH2006` at `$.settings`",
            "Disabled: HH2006; future finding: HH9999.",
            "[External HH1101](https://example.org/HH1101)",
            '`$.value = "HH3001"`',
            "~~~yaml",
            "name: HH3002",
            "~~~",
            "```text",
            "[HH1101] Raw diagnostic",
            "```",
        ]
    )
    content = with_finding_reference(document)
    assert "[HH1101](#hh1101---invalid-yaml-in-rendered-output-1)" in content
    assert "[HH2006](#hh2006---opaque-object-schema)" in content
    assert "[External HH1101](https://example.org/HH1101)" in content
    assert '`$.value = "HH3001"`' in content
    assert "~~~yaml\nname: HH3002\n~~~" in content
    assert "```text\n[HH1101] Raw diagnostic\n```" in content
    assert "### HH3001" not in content and "### HH3002" not in content
    assert "### HH9999 - Unknown finding code" in content
    assert content.count(f"## {APPENDIX_TITLE}") == 1
    assert with_finding_reference(content) == content
    targets = {anchor for _, _, _, anchor in heading_inventory(content)}
    assert set(re.findall(r"\]\(#([^)]*)\)", content)) <= targets


def test_report_heading_sizes_and_code_links_in_pdf(tmp_path: Path) -> None:
    """
    Render chart headings above diagnostics in size and route code links to the final appendix page.

    Args:
        tmp_path (Path): Compact public report destination.

    Returns:
        None: Both formats link finding codes; the PDF contains distinct heading sizes and real internal destinations.
    """
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1,
        "elapsed_seconds": 2,
        "charts_discovered": 1,
        "counts": {"failed": 1},
        "settings": {},
        "ignored_rules": ["HH2006"],
        "charts": [
            {
                "chart": "readable-chart",
                "status": "failed",
                "error": "[HH1101] Invalid YAML",
                "testing_seconds": 2,
                "audit": {"findings": [{"code": "HH2001", "path": ["name"]}]},
            }
        ],
    }
    markdown, pdf = write_reports(
        report, tmp_path / "report", publication=Publication(tmp_path, "https://github.com/example/charts", "main")
    )
    text = markdown.read_text()
    assert "#### E001 ([HH1101](<#hh1101---invalid-yaml-in-rendered-output>))" in text
    assert "[HH2001](<#hh2001---undocumented-values-path>)" in text
    assert text.index(f"## {APPENDIX_TITLE}") > text.index("### readable-chart")
    assert "Default severity: **error**" in text
    content = pdf.read_bytes()
    objects = dict(re.findall(rb"(\d+) 0 obj\s*(.*?)\s*endobj", content, re.DOTALL))
    pages = [number for number, body in objects.items() if b"/Type /Page\n" in body]
    definition = next(body for body in objects.values() if b"/Title (HH1101 - Invalid YAML in rendered output)" in body)
    target = re.search(rb"/Dest \[ (\d+) 0 R", definition)
    assert target is not None and target[1] == pages[-1]
    assert sum(b"/Subtype /Link" in body and b"/Dest [ " + target[1] + b" 0 R" in body for body in objects.values()) >= 4
    streams = []
    for body in objects.values():
        if b"/Filter [ /ASCII85Decode /FlateDecode ]" in body and (match := re.search(rb"stream\s*\n(.*?)endstream", body, re.DOTALL)):
            streams.append(zlib.decompress(base64.a85decode(match[1].strip(), adobe=True)))
    drawn = b"\n".join(streams)
    assert re.search(rb"/F\d+ 12 Tf[^\n]*\(readable-chart\)", drawn)
    assert re.search(rb"/F\d+ 10 Tf[^\n]*\(E001 ", drawn)
    assert re.search(rb"/F\d+ 8 Tf", drawn)
