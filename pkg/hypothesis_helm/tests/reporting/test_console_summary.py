"""
Keep scan and test completion readable without discarding saved diagnostic evidence.
"""

import json
from pathlib import Path

import pytest

from hypothesis_helm.charts.repositories.repository import RepositorySource
from hypothesis_helm.cli import main
from hypothesis_helm.reporting.console.summary import print_summary
from hypothesis_helm.tests.fixtures.cli import result_text


@pytest.mark.parametrize("command", ["test", "scan"])
@pytest.mark.parametrize("interrupted", [False, True])
def test_scan_completion_is_concise(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], command: str, interrupted: bool
) -> None:
    """
    Save complete results and emit only a short summary on normal exits and Ctrl-C.

    Args:
        tmp_path (Path): Private chart and result directory.
        monkeypatch (pytest.MonkeyPatch): Replace remote preparation and chart work.
        capsys (pytest.CaptureFixture[str]): Separate console output from finding logs.
        command (str): Recursive local testing or remote scanning.
        interrupted (bool): Raise KeyboardInterrupt during the chart's execution.

    Returns:
        None: Normal and interrupted scans preserve evidence without dumping it to the terminal.
    """
    chart = tmp_path / "chart"
    chart.mkdir()
    (chart / "Chart.yaml").write_text("apiVersion: v2\nname: example\nversion: 1.0.0\n")
    (chart / "values.yaml").write_text("enabled: true\n")
    source = str(chart) if command == "test" else "https://example.org/charts.git"
    monkeypatch.setattr(
        "hypothesis_helm.charts.repositories.scan.prepare_helm_source",
        lambda *args, **kwargs: RepositorySource(source, chart, "example", True, revision="abc"),
    )

    def exercise(*args: object) -> dict[str, object]:
        """
        Return verbose evidence or simulate Ctrl-C inside chart execution.

        Args:
            *args (object): The chart, settings and artifact location.

        Returns:
            dict[str, object]: Deliberately large evidence which belongs only in the saved report.

        Raises:
            KeyboardInterrupt: The interruption variant ends the scan gracefully.
        """
        if interrupted:
            raise KeyboardInterrupt
        return {"status": "passed", "attempts": 10, "input_domains": {"details": "PRIVATE-DIAGNOSTIC" * 10000}}

    monkeypatch.setattr("hypothesis_helm.charts.repositories.scan.exercise_chart", exercise)
    status = main(
        [
            command,
            source,
            "--helm",
            "/usr/bin/true",
            "--no-build-dependencies",
            "--no-cache",
            "--artifact-dir",
            str(tmp_path / "results"),
            "--log-file",
            "/dev/stderr",
        ]
    )
    output = capsys.readouterr().out
    assert status == (130 if interrupted else 0)
    assert f"Scan {'interrupted' if interrupted else 'completed'}" in output
    assert len(output) < 1000 and len(output.splitlines()) == 3
    assert "PRIVATE-DIAGNOSTIC" not in output and '"charts"' not in output
    report = json.loads(result_text(output))
    assert report["scan_status"] == ("interrupted" if interrupted else "completed")
    if not interrupted:
        assert len(report["charts"][0]["input_domains"]["details"]) > 100000


@pytest.mark.parametrize(("status", "exit_code"), [("passed", 0), ("failed", 1), ("time-limit", 124), ("interrupted", 130)])
def test_single_chart_completion_preserves_saved_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], status: str, exit_code: int
) -> None:
    """
    Apply concise reporting to single-chart tests, including interrupted and failed results.

    Args:
        tmp_path (Path): Schema-backed chart and output directory.
        monkeypatch (pytest.MonkeyPatch): Supply runner outcomes without invoking Helm.
        capsys (pytest.CaptureFixture[str]): Captured completion summary.
        status (str): Whole-chart execution outcome.
        exit_code (int): Expected CLI exit status.

    Returns:
        None: All outcomes save the full result and show a short terminal summary.
    """
    (tmp_path / "Chart.yaml").write_text("apiVersion: v2\nname: example\nversion: 1.0.0\n")
    (tmp_path / "values.yaml").write_text("enabled: true\n")
    (tmp_path / "values.schema.json").write_text('{"type":"object","properties":{"enabled":{"type":"boolean"}}}')
    report = {"status": status, "attempts": 3, "input_domains": {"details": "PRIVATE-DIAGNOSTIC" * 10000}}
    monkeypatch.setattr("hypothesis_helm.cli.check_chart", lambda *args, **kwargs: report)
    assert main(["test", str(tmp_path), "--whole-chart", "--shard", "none", "--artifact-dir", str(tmp_path / "results")]) == exit_code
    output = capsys.readouterr().out
    assert f"Test {status.replace('-', ' ')}; 3 test attempts." in output
    assert "PRIVATE-DIAGNOSTIC" not in output and len(output) < 1000
    assert json.loads(result_text(output)) == report


def test_summary_does_not_walk_chart_evidence(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Restrict summaries to aggregate statistics even when evidence is enormous or not serializable.

    Args:
        capsys (pytest.CaptureFixture[str]): Captured fixed-size terminal output.

    Returns:
        None: Summary generation never serializes or visits per-chart data.
    """
    print_summary(
        {"scan_status": "completed", "charts_discovered": 10000, "counts": {"passed": 10000}, "charts": object()},
        Path("results/scan.json"),
        reports=(Path("report.md"), Path("report.pdf")),
    )
    output = capsys.readouterr().out
    assert "10000 charts" in output and "report.md, report.pdf" in output
    assert len(output.splitlines()) == 4
