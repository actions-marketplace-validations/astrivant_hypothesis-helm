"""
Keep working data out of published studies and preserve usable document links.
"""

from pathlib import Path

import pytest
from hypothesis_helm_benchmarking.reporting.publication import STUDIES, publish_study


def test_publication_excludes_workspaces_and_replaces_stale_figures(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Publish final documents and figures while preserving raw evidence in the run cache.

    Args:
        tmp_path (Path): Isolated project directory.
        monkeypatch (pytest.MonkeyPatch): Resolve publication paths from that project.

    Returns:
        None: Raw files remain cached; current plots replace stale plots and have valid links.
    """
    monkeypatch.chdir(tmp_path)
    source = Path(".cache/refresh/run/outputs/example")
    destination = STUDIES / "example"
    source.mkdir(parents=True)
    destination.mkdir(parents=True)
    (destination / "old.png").write_bytes(b"old")
    (source / "README.md").write_text(
        "# Example\n\n![Plot](plot.png)\n\n[Raw](results.json)\n\n[Guide](../../docs/benchmarking/README.md#runs)\n"
    )
    (source / "plot.png").write_bytes(b"new")
    (source / "results.json").write_text('{"measured": true}')
    for directory in ("runs", "cases", "reports", "chart"):
        root = source / directory
        root.mkdir()
        (root / "README.md").write_text("Run or fixture, not a published result")
        if directory == "chart":
            (root / "Chart.yaml").write_text("apiVersion: v2\nname: example\nversion: 0.1.0\n")
    # A dependency named charts inside the graph catalog is a legitimate final result.
    nested = source / "catalog/charts/dependency"
    nested.mkdir(parents=True)
    (nested / "graph.png").write_bytes(b"graph")
    published = publish_study(source, destination)
    assert set(published) == {str(destination / name) for name in ("README.md", "plot.png", "catalog/charts/dependency/graph.png")}
    assert not (destination / "old.png").exists()
    assert not (destination / "results.json").exists()
    assert (source / "results.json").read_text() == '{"measured": true}'
    document = (destination / "README.md").read_text()
    assert "![Plot](<plot.png>)" in document
    assert "Raw (local run data)" in document
    assert "[Guide](../../docs/benchmarking/README.md#runs)" in document


def test_empty_or_overlapping_publication_preserves_existing_results(tmp_path: Path) -> None:
    """
    Reject publication without finished files or with source data inside the destination.

    Args:
        tmp_path (Path): Isolated measurement and publication directories.

    Returns:
        None: Validation errors occur before changing the previous report.
    """
    destination = tmp_path / "final"
    destination.mkdir()
    report = destination / "README.md"
    report.write_text("Previous results")
    source = tmp_path / "cache"
    source.mkdir()
    (source / "results.json").write_text("{}")
    with pytest.raises(ValueError, match="No final documents"):
        publish_study(source, destination)
    with pytest.raises(ValueError, match="outside"):
        publish_study(destination, destination)
    assert report.read_text() == "Previous results"
