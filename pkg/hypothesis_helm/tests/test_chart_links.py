"""
Keep chart source and artifact links portable without guessing missing provenance.
"""

from pathlib import Path

import pytest

from hypothesis_helm.reporting.contents import heading_inventory, with_contents
from hypothesis_helm.reporting.links import chart_source_url, repository_url
from hypothesis_helm.reporting.repository import chart_heading, write_reports


@pytest.mark.parametrize(
    ("remote", "expected"),
    [
        ("git@github.com:team/charts.git", "https://github.com/team/charts/tree/release%2F1.0/charts/nested%20app"),
        ("ssh://git@gitlab.com/team/charts.git", "https://gitlab.com/team/charts/-/tree/release%2F1.0/charts/nested%20app"),
        ("https://bitbucket.org/team/charts", "https://bitbucket.org/team/charts/src/release%2F1.0/charts/nested%20app"),
    ],
)
def test_chart_source_links_use_recorded_revision(remote: str, expected: str) -> None:
    """
    Preserve nested paths and encode ref names for each supported browser route.

    Args:
        remote (str): Recorded Git remote spelling.
        expected (str): Chart browser URL for the exact recorded ref.

    Returns:
        None: The source link and internal report anchor remain independent.
    """
    chart: dict[str, object] = {"chart": "nested app", "source_url": "https://example.org/declared"}
    source: dict[str, object] = {"url": remote, "revision": "release/1.0", "path": "charts"}
    assert chart_source_url(chart, source) == expected
    heading = chart_heading(chart, source, Path("report.md"))
    assert heading == f"### [nested app](<{expected}>)"
    assert heading_inventory(heading)[0][2:] == ("nested app", "nested-app")
    assert "[nested app](#nested-app)" in with_contents("# Report\n\n" + heading)


@pytest.mark.parametrize(
    "remote",
    ["https://token@github.com/team/charts", "ssh://git:token@github.com/team/charts", "ssh://[broken", "file:///private/chart"],
)
def test_chart_links_reject_credentials_and_invalid_urls(remote: str) -> None:
    """
    Avoid leaking credentials or converting local-only sources into public links.

    Args:
        remote (str): Unsafe or malformed remote.

    Returns:
        None: Source lookup falls back without aborting report generation.
    """
    assert repository_url(remote) is None
    assert chart_source_url({"chart": "demo", "source_url": remote}, {"url": remote, "revision": "abc"}) is None


def test_chart_links_preserve_declared_sources_and_artifact_fallback(tmp_path: Path) -> None:
    """
    Use declared package sources and omit unpublished artifacts from standalone reports.

    Args:
        tmp_path (Path): Report and retained run destinations.

    Returns:
        None: Unknown source revisions never produce guessed browser paths.
    """
    chart: dict[str, object] = {"chart": "demo", "artifacts": str(tmp_path / "saved inputs")}
    source: dict[str, object] = {"url": "https://github.com/example/charts"}
    report = tmp_path / "report.md"
    assert chart_heading(chart, source, report) == "### [demo](<saved%20inputs>)"
    assert chart_heading(chart, source, report, artifact_links=False) == "### demo"
    chart["artifacts"] = "https://example.org/runs/123/demo"
    assert chart_heading(chart, source, report) == "### [demo](<https://example.org/runs/123/demo>)"
    chart["source_url"] = "https://example.org/chart-code"
    assert chart_heading(chart, source, report, artifact_links=False) == "### [demo](<https://example.org/chart-code>)"
    source.update(kind="helm", revision="1.2.3")
    assert chart_source_url(chart, source) == chart["source_url"]
    source.update(kind="git", chart_paths=["different-chart"])
    assert chart_source_url(chart, source) == chart["source_url"]
    source.pop("chart_paths")
    chart["chart"] = "../escape"
    assert chart_source_url(chart, source) == chart["source_url"]


def test_standalone_report_links_chart_code_in_markdown_and_pdf(tmp_path: Path) -> None:
    """
    Publish clickable chart names without enabling private run-artifact links.

    Args:
        tmp_path (Path): Final report output directory.

    Returns:
        None: Both formats contain the public source URL and retain internal section navigation.
    """
    report: dict[str, object] = {
        "directory": "charts",
        "source": {"url": "git@github.com:example/charts.git", "revision": "abc123"},
        "started_epoch": 1,
        "elapsed_seconds": 1,
        "charts_discovered": 1,
        "counts": {"passed": 1},
        "settings": {},
        "charts": [{"chart": "demo", "status": "passed", "artifacts": "/private/unpublished"}],
    }
    markdown, pdf = write_reports(report, tmp_path / "report", artifact_links=False)
    expected = "https://github.com/example/charts/tree/abc123/demo"
    assert f"### [demo](<{expected}>)" in markdown.read_text()
    assert "[demo](#demo)" in markdown.read_text()
    assert f"/URI ({expected})".encode() in pdf.read_bytes()
    assert "/private/unpublished" not in markdown.read_text()
    assert b"/private/unpublished" not in pdf.read_bytes()
