"""
Verify stable run tracing and execution timestamps in saved and republished reports.
"""

import copy
import json
import shlex
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from unittest.mock import Mock

import pytest

from hypothesis_helm.environment import env
from hypothesis_helm.reporting.evidence.invocation import record_invocation
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
        {"execution": {"versions": {"hypothesis": "6.0.0"}, "command": "hypothesis-helm test charts"}},
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
    assert "Hypothesis not recorded" in text
    assert "Not recorded for this run" in text
    assert "execution" not in report
    snapshot = copy.deepcopy(report)
    write_reports(report, tmp_path / "republished")
    assert report == snapshot
    assert pdf.read_bytes().startswith(b"%PDF")


@pytest.mark.parametrize("plugin", [False, True])
def test_recorded_invocation_keeps_literal_arguments(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: bool) -> None:
    """
    Preserve spaces and shell metacharacters when capturing either CLI entry point.

    Args:
        monkeypatch (pytest.MonkeyPatch): Isolate plugin detection and installed package versions.
        tmp_path (Path): Invocation working directory.
        plugin (bool): Whether Helm supplied the plugin environment.

    Returns:
        None: Shell splitting exactly reproduces the original arguments and version lookup occurs at capture time.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setitem(env, "HELM_PLUGIN_DIR", "/plugins/hypothesis" if plugin else "")
    monkeypatch.setattr(
        "hypothesis_helm.reporting.evidence.invocation.version", lambda name: "6.123.0" if name == "hypothesis" else "0.1.2"
    )
    arguments = ["test", "charts with spaces/$(literal)", "--report", "reports/a'quoted`name", "--fail"]
    execution = record_invocation(arguments)
    prefix = ["helm", "hypothesis"] if plugin else ["hypothesis-helm"]
    assert execution["argv"] == [*prefix, *arguments]
    assert shlex.split(str(execution["command"])) == execution["argv"]
    assert execution["versions"] == {"hypothesis": "6.123.0", "hypothesis-helm": "0.1.2"}
    assert execution["working_directory"] == str(tmp_path)
    arguments.clear()
    assert execution["argv"] == [*prefix, "test", "charts with spaces/$(literal)", "--report", "reports/a'quoted`name", "--fail"]


def test_library_invocation_does_not_borrow_process_arguments(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep absent CLI and package metadata explicitly unknown for source-tree library callers.

    Args:
        monkeypatch (pytest.MonkeyPatch): Simulate running uninstalled code under another application's process.

    Returns:
        None: No pytest or host-application command is misreported as the scan invocation.
    """
    monkeypatch.setattr("hypothesis_helm.reporting.evidence.invocation.version", Mock(side_effect=PackageNotFoundError("missing")))
    execution = record_invocation()
    assert execution["command"] is None
    assert execution["argv"] is None
    assert execution["versions"] == {"hypothesis": None, "hypothesis-helm": None}


def test_republished_cover_preserves_versions_and_command(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Publish the saved versions and complete command immediately after the source commit.

    Args:
        tmp_path (Path): Markdown and PDF destinations.
        monkeypatch (pytest.MonkeyPatch): Capture the cover details without relying on installed versions.

    Returns:
        None: Republishing preserves original provenance and a shell-quoted command is emitted verbatim.
    """
    covers: list[tuple[tuple[str, str], ...]] = []

    def pdf(content: str, destination: Path, **kwargs: object) -> None:
        """
        Capture PDF cover metadata.

        Args:
            content (str): Markdown report.
            destination (Path): PDF destination.
            **kwargs (object): PDF layout and cover options.

        Returns:
            None: Record cover fields for checking their order and contents.
        """
        details = kwargs["cover_details"]
        assert isinstance(details, tuple)
        covers.append(details)

    command = shlex.join(["helm", "hypothesis", "test", "charts/a space", "--report", "reports/`literal`", "--seed", "42"])
    report: dict[str, object] = {
        "directory": "charts",
        "started_epoch": 1_700_000_000,
        "elapsed_seconds": 2,
        "settings": {},
        "charts_discovered": 0,
        "counts": {},
        "charts": [],
        "source": {"kind": "git", "revision": "abc123"},
        "execution": {
            "versions": {"hypothesis": "6.100.0", "hypothesis-helm": "0.0.9"},
            "command": command,
            "working_directory": "/original/checkout",
        },
    }
    monkeypatch.setattr("hypothesis_helm.reporting.reports.repository.write_pdf", pdf)
    markdown, _ = write_reports(report, tmp_path / "first")
    saved = json.dumps(report, sort_keys=True)
    write_reports(report, tmp_path / "second")
    assert json.dumps(report, sort_keys=True) == saved
    assert covers[0] == covers[1]
    assert covers[0][2:] == (
        ("Source commit", "abc123"),
        ("Versions", "Hypothesis 6.100.0; hypothesis-helm 0.0.9"),
        ("Working directory", "/original/checkout"),
        ("Scan command", command),
    )
    text = markdown.read_text()
    assert command in text
    assert "Hypothesis 6.100.0; hypothesis-helm 0.0.9" in text
