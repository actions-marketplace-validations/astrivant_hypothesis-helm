"""
Verify stable run tracing and execution timestamps in saved and republished reports.
"""

import copy
import json
from pathlib import Path

from hypothesis_helm.reporting.evidence.provenance import finish_epoch, trace_run
from hypothesis_helm.reporting.reports.repository import write_reports


def test_run_fingerprint_survives_republication_and_changes_with_run_metadata() -> None:
    """
    Keep publication edits outside run identity while tracking source, timing, and configuration changes.

    Returns:
        None: JSON round trips preserve identity; another source, setting, or execution interval changes it.
    """
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1_700_000_000,
        "elapsed_seconds": 60,
        "settings": {"seed": 1},
        "source": {"revision": "abc"},
    }
    trace_run(report, finished_epoch=1_700_000_061)
    assert report["finished_at"] == "2023-11-14T22:14:21.000+00:00"
    assert finish_epoch(report) == 1_700_000_061
    original = report["run_hash"]
    assert len(str(original)) == 64
    republished = json.loads(json.dumps(report))
    republished.update(title="Republished", summary=["New prose"], artifact_checksums={"report.pdf": "changed"})
    trace_run(republished)
    assert republished["run_hash"] == original
    assert republished["finished_at"] == report["finished_at"]
    for change in (
        {"settings": {"seed": 2}},
        {"source": {"revision": "def"}},
        {"started_epoch": 1_700_000_001},
        {"finished_epoch": 1_700_000_065},
    ):
        changed = {**report, **change}
        trace_run(changed)
        assert changed["run_hash"] != original


def test_legacy_finish_time_is_derived_and_labeled(tmp_path: Path) -> None:
    """
    Report the historical execution interval rather than the current publication date.

    Args:
        tmp_path (Path): Markdown and PDF destinations.

    Returns:
        None: Incomplete scans retain their status, and their estimated finish time and fingerprint survive republication.
    """
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1_700_000_000,
        "elapsed_seconds": 60.5,
        "settings": {},
        "charts_discovered": 0,
        "counts": {},
        "charts": [],
        "scan_status": "interrupted",
    }
    markdown, pdf = write_reports(report, tmp_path / "report")
    assert report["finished_at"] == "2023-11-14T22:14:20.500+00:00"
    assert report["finish_time_source"] == "derived-start-plus-elapsed"
    text = markdown.read_text()
    assert "Finished (UTC): 2023-11-14T22:14:20.500+00:00 (estimated from recorded timing)" in text
    assert "Scan status: interrupted" in text
    assert f"Run fingerprint (SHA-256): `{report['run_hash']}`" in text
    snapshot = copy.deepcopy(report)
    write_reports(report, tmp_path / "republished")
    assert report == snapshot
    assert pdf.read_bytes().startswith(b"%PDF")
