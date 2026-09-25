"""
Exercise report sensitivity through the public local and remote scan commands.
"""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest
from PIL import Image

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.repositories.repository import RepositorySource
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.cli import main
from hypothesis_helm.reporting.reports.figures import SENSITIVITY_FIELDS_KEY
from hypothesis_helm.tests.fixtures.cli import result_text


@pytest.mark.parametrize("remote", [False, True])
def test_scan_measures_requested_fields_and_preserves_results(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    remote: bool,
) -> None:
    """
    Measure all 48 requested Boolean paths through the same command that tests charts.

    Args:
        tmp_path (Path): Chart checkout and report destinations.
        monkeypatch (pytest.MonkeyPatch): Replace fetching and Helm calls with repeatable output.
        capsys (pytest.CaptureFixture[str]): Capture the machine-readable scan result.
        remote (bool): Select test or scan without making network requests.

    Returns:
        None: Both commands publish a 48-field panel, 1,128 pairs, and the unchanged scan findings.
    """
    root = tmp_path / "source"
    root.mkdir()
    (root / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "example", "version": "1.0.0"}))
    defaults = {f"field{index}": False for index in range(48)}
    (root / "values.yaml").write_text(yamlio.dump(defaults))
    selected = {**defaults, "field0": True}
    (root / "alternate.yaml").write_text(yamlio.dump(selected))
    observed: list[dict[str, object]] = []

    def render(chart: Chart, values: dict[str, object], **kwargs: object) -> object:
        """
        Return a stable manifest and record which baseline the measurement used.

        Args:
            chart (Chart): Private chart copy.
            values (dict[str, object]): Selected candidate configuration.
            **kwargs (object): Renderer options forwarded by the measurement.

        Returns:
            object: A valid deterministic ConfigMap.
        """
        if not observed:
            observed.append(dict(values))
        return [
            {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {"name": "example"},
                "data": {"total": str(sum(bool(value) for value in values.values()))},
            }
        ]

    monkeypatch.setattr("hypothesis_helm.analysis.repository.render", render)
    monkeypatch.setattr("hypothesis_helm.charts.repositories.scan.exercise_chart", lambda *args: {"status": "passed", "attempts": 10})
    source = "https://example.org/charts.git" if remote else str(root)
    if remote:
        monkeypatch.setattr(
            "hypothesis_helm.charts.repositories.scan.prepare_helm_source",
            lambda *args, **kwargs: RepositorySource(source, root, "charts", True, revision="abc123"),
        )
    arguments = [
        "scan" if remote else "test",
        source,
        "--filter",
        "--jobs",
        "6",
        "--chart-timeout",
        "120s",
        "--max-examples",
        "10",
        "--seed",
        "0",
        "--no-cache",
        "--no-build-dependencies",
        "--helm",
        "/usr/bin/true",
        "--values",
        "alternate.yaml",
        "--artifact-dir",
        str(tmp_path / "artifacts"),
        "--report",
        str(tmp_path / "report.md"),
        "--log-file",
        "/dev/stderr",
        "--max-mutations",
        "48",
        "--sensitivity-timeout",
        "30s",
    ]
    assert main(arguments) == 0
    report = json.loads(result_text(capsys.readouterr().out))
    saved = next((tmp_path / "artifacts").glob("*/scan.json"))
    assert json.loads(saved.read_text()) == report
    assert report["counts"] == {"passed": 1}
    assert report["figure_generation"]["status"] == "complete"
    assert report["settings"]["report_max_mutations"] == 48
    assert report["settings"]["chart_timeout_seconds"] == 120
    assert report["settings"]["scan_timeout_seconds"] is None
    assert report["figure_generation"]["time_limit_seconds_per_chart"] == 30
    assert report["figure_generation"]["pca_sample_limit"] == 64
    assert report["output_pca"]["reference_observations"] == 64
    assert report["output_pca"]["charts_measured"] == 1
    assert (tmp_path / "report-pca.png").is_file()
    evidence = json.loads((saved.parent / "figures/sensitivity.json").read_text())
    assert evidence["context"]["maximum_mutations"] == 48
    assert evidence["context"]["values"] == "alternate.yaml"
    assert evidence["context"]["seconds"] == 30
    assert len(evidence["mutations"]) == 48
    assert len(evidence["interactions"]) == 1128
    assert observed == [selected]
    image = Path(report["charts"][0]["report_figures"]["sensitivity"])
    with Image.open(image) as panel:
        assert len(json.loads(panel.info[SENSITIVITY_FIELDS_KEY])) == 48
    assert (tmp_path / "report.pdf").is_file()
    assert "Sensitivity field key" in (tmp_path / "report.md").read_text()
    assert "Full input and diagnostic" not in (tmp_path / "report.md").read_text()


@pytest.mark.parametrize(
    ("error", "expected", "status"), [(KeyboardInterrupt(), 130, "interrupted"), (ValueError("plot failed"), 2, "failed")]
)
def test_figure_failure_keeps_scan_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    error: BaseException,
    expected: int,
    status: str,
) -> None:
    """
    Save completed scan results even when the optional measurement stage cannot finish.

    Args:
        tmp_path (Path): Single chart and retained evidence directory.
        monkeypatch (pytest.MonkeyPatch): Replace testing and figure work with controlled outcomes.
        capsys (pytest.CaptureFixture[str]): Capture saved JSON.
        error (BaseException): Interruption or publication failure.
        expected (int): CLI exit status.
        status (str): Figure-stage status without rewriting chart findings.

    Returns:
        None: Scan outcomes and reports remain available after figure cleanup.
    """
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "example", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text("enabled: true\n")
    monkeypatch.setattr("hypothesis_helm.charts.repositories.scan.exercise_chart", lambda *args: {"status": "passed", "attempts": 1})
    monkeypatch.setattr("hypothesis_helm.analysis.scan_figures.prepare_figures", Mock(side_effect=error))
    assert (
        main(
            [
                "test",
                str(tmp_path),
                "--helm",
                "/usr/bin/true",
                "--no-build-dependencies",
                "--log-file",
                "/dev/stderr",
                "--artifact-dir",
                str(tmp_path / "artifacts"),
                "--report",
                str(tmp_path / "report"),
                "--max-mutations",
                "48",
            ]
        )
        == expected
    )
    report = json.loads(result_text(capsys.readouterr().out))
    assert report["counts"] == {"passed": 1}
    assert report["scan_status"] == "completed"
    assert report["figure_generation"]["status"] == status
    assert json.loads(next((tmp_path / "artifacts").glob("*/scan.json")).read_text()) == report
    assert (tmp_path / "report.pdf").is_file()


@pytest.mark.parametrize("arguments", [["--max-mutations", "0", "--report"], ["--max-mutations", "48"]])
def test_invalid_measurement_options_fail_before_testing(arguments: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    """
    Reject missing report destinations and nonpositive measurement limits before starting a scan.

    Args:
        arguments (list[str]): Invalid report measurement options.
        capsys (pytest.CaptureFixture[str]): Capture the parser explanation.

    Returns:
        None: The CLI exits with usage status and identifies the invalid option.
    """
    with pytest.raises(SystemExit) as error:
        main(["test", *arguments])
    assert error.value.code == 2
    assert "--max-mutations" in capsys.readouterr().err
