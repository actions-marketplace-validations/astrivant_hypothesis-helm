"""
Verify severity thresholds retain findings without suppressing tests or caching invalid output.
"""

import json
import logging
import os
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import strategies as st

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.paths import check_paths
from hypothesis_helm.charts.testing.runner import check_chart
from hypothesis_helm.cli import argument_parser, main
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.findings.generator import FindingGenerator
from hypothesis_helm.findings.severity import blocks, level, validate
from hypothesis_helm.reporting.evidence.errors import chart_errors
from hypothesis_helm.reporting.reports.shards import aggregate
from hypothesis_helm.rules import ENVIRONMENT as IGNORED
from hypothesis_helm.schemas.configuration.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.contracts import mapping, sequence


@pytest.fixture
def severity_chart(tmp_path: Path) -> Chart:
    """
    Create two Boolean paths with valid defaults and a reproducible YAML failure.

    Args:
        tmp_path (Path): Chart fixture root.

    Returns:
        Chart: Enabling flag produces invalid YAML; the other path stays independent.
    """
    chart = tmp_path / "chart"
    (chart / "templates").mkdir(parents=True)
    (chart / "Chart.yaml").write_text("apiVersion: v2\nname: severity\nversion: 1.0.0\n")
    (chart / "values.yaml").write_text("flag: false\nother: false\n")
    (chart / "values.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {name: {"type": "boolean"} for name in ("flag", "other")},
            }
        )
    )
    (chart / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: severity
        {{ if .Values.flag }}data: [{{ else }}data:
          other: {{ .Values.other | quote }}
        {{ end }}
    """)
    )
    return Chart.load(chart)


@pytest.mark.parametrize("threshold, expected", [("info", True), ("warning", True), ("error", False)])
def test_threshold_uses_effective_severity(monkeypatch: pytest.MonkeyPatch, threshold: str, expected: bool) -> None:
    """
    Compare severity independently of whether evidence proves a contract violation.

    Args:
        monkeypatch (pytest.MonkeyPatch): Isolated worker policy.
        threshold (str): Selected minimum severity.
        expected (bool): Whether a warning meets the threshold.

    Returns:
        None: Overrides affect failure decisions while preserving the evidence kind.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"findings": {"fail_on": threshold, "severity": {"HH1101": "warning"}}}))
    refresh_env()
    assert level("HH1101") == "warning"
    assert blocks("HH1101") is expected
    record = FindingGenerator.create("HH1101", "invalid YAML").record()
    assert record["kind"] == "violation"
    assert record["severity"] == "warning"
    assert record["blocking"] is expected
    assert blocks("uncategorized-worker-error")
    assert CATALOG["HH1101"].severity == "error"


@pytest.mark.parametrize(
    "settings",
    [
        None,
        [],
        {"fail_on": True},
        {"fail_on": "critical"},
        {"severity": []},
        {"severity": {"HH9999": "error"}},
        {"severity": {"HH1101": "off"}},
        {"unknown": "warning"},
    ],
)
def test_invalid_severity_configuration(settings: object) -> None:
    """
    Reject misspelled levels and codes before testing starts.

    Args:
        settings (object): Invalid findings policy.

    Returns:
        None: Every malformed policy raises a configuration error.
    """
    with pytest.raises(ValueError):
        validate(settings)


def test_report_keeps_the_original_severity_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Preserve a promoted code when reports are aggregated outside the workers' environment.

    Args:
        monkeypatch (pytest.MonkeyPatch): Remove the worker's runtime policy.

    Returns:
        None: Rendering a saved diagnostic uses its recorded policy instead of current defaults.
    """
    monkeypatch.delenv(ENVIRONMENT, raising=False)
    refresh_env()
    diagnostics = chart_errors(
        {
            "finding_policy": {"fail_on": "error", "severity": {"HH1201": "error"}},
            "phases": [{"phase": "shard 1/2", "status": "failed", "error": "[HH1201] helm exceeded 1s"}],
        }
    )
    assert diagnostics[0]["severity"] == "error"
    assert diagnostics[0]["blocking"] is True


@pytest.mark.parametrize("command", ["audit", "generate", "test", "scan", "run"])
def test_fail_threshold_keeps_boolean_scheduler_setting(command: str) -> None:
    """
    Support the same optional threshold on each command without changing scheduler argument types.

    Args:
        command (str): Public command supporting fail-fast execution.

    Returns:
        None: Bare fail means any severity and named thresholds remain explicit.
    """
    for flags, expected in [([], None), (["--fail"], "info"), (["--fail", "error"], "error")]:
        args = argument_parser().parse_args([command, "chart", *flags])
        assert args.fail is (expected is not None)
        assert getattr(args, "fail_level", None) == expected


def test_audit_cli_threshold_and_configuration_override(
    severity_chart: Chart,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Keep lower-severity audit findings visible and let explicit CLI thresholds override configuration.

    Args:
        severity_chart (Chart): Chart with informational missing descriptions.
        tmp_path (Path): Local configuration directory.
        monkeypatch (pytest.MonkeyPatch): Select the isolated working directory.
        capsys (pytest.CaptureFixture[str]): Capture audit JSON and logs.

    Returns:
        None: Thresholds, overrides and explicit suppression produce distinct exit decisions.
    """
    monkeypatch.chdir(tmp_path)
    config = tmp_path / "policy.yaml"
    config.write_text("findings:\n  fail_on: info\n")
    args = ["audit", str(severity_chart.path), "--config", str(config)]
    assert main(args) == 1
    assert main([*args, "--fail", "error"]) == 0
    assert '"severity": "info"' in capsys.readouterr().out
    config.write_text("findings:\n  fail_on: error\n  severity:\n    HH2003: error\n")
    assert main(args) == 1
    assert main([*args, "--ignore", "HH2003"]) == 0
    assert load_policy(config)["findings"] == {"fail_on": "error", "severity": {"HH2003": "error"}}
    config.write_text("findings:\n  fail_on: error\n")
    assert main(["audit", "--fail", str(severity_chart.path), "--config", str(config)]) == 1


@pytest.mark.parametrize("exhaustive", [False, True])
def test_lower_findings_do_not_stop_or_validate_candidates(
    severity_chart: Chart,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    exhaustive: bool,
) -> None:
    """
    Continue sampling after warnings while retaining evidence and excluding failed validation witnesses.

    Args:
        severity_chart (Chart): Finite chart used by both generation modes.
        tmp_path (Path): Report destination.
        monkeypatch (pytest.MonkeyPatch): Deterministic failing renderer and policy.
        exhaustive (bool): Use all finite cases or Hypothesis sampling.

    Returns:
        None: Every candidate is attempted, warnings stay visible and no output is certified.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"findings": {"fail_on": "error", "severity": {"HH1101": "warning"}}}))
    refresh_env()
    attempted = []

    def fail(chart: Chart, values: dict[str, object], **kwargs: object) -> list[dict[str, object]]:
        """
        Simulate invalid YAML for every candidate without invoking Helm.

        Args:
            chart (Chart): Chart under test.
            values (dict[str, object]): Current generated overrides.
            **kwargs (object): Renderer options.

        Returns:
            list[dict[str, object]]: Never returns output.
        """
        attempted.append(values)
        raise RenderFailure("invalid YAML", "HH1101")

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", fail)
    result = check_chart(
        severity_chart,
        max_examples=5,
        exhaustive=exhaustive,
        fail_fast=True,
        artifact_dir=tmp_path / "artifacts",
        input_strategy=None if exhaustive else st.fixed_dictionaries({"flag": st.booleans(), "other": st.booleans()}),
    )
    assert result["status"] == "findings"
    assert len(attempted) >= 4
    assert result["coverage_complete"] is False
    assert result["proof_of_totality"] is False
    assert result["ignored_failures"] == {}
    assert mapping(sequence(result["findings"])[0])["occurrences"] == len(attempted)
    assert chart_errors(result)[0]["severity"] == "warning"
    assert chart_errors(result)[0]["blocking"] is False


@pytest.mark.parametrize("jobs", [1, 2])
def test_path_workers_continue_after_lower_findings(
    severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int
) -> None:
    """
    Propagate the same severity policy through serial and real subprocess path execution.

    Args:
        severity_chart (Chart): Chart with one invalid-YAML mutation.
        tmp_path (Path): Worker and report artifacts.
        monkeypatch (pytest.MonkeyPatch): Inherited policy and installed worker entry points.
        jobs (int): Number of isolated workers for this chart.

    Returns:
        None: Both paths complete, the warning survives and no fail-fast stop is signaled.
    """
    import sys

    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}:{os.environ['PATH']}")
    refresh_env()
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"findings": {"fail_on": "error", "severity": {"HH1101": "warning"}}}))
    refresh_env()
    monkeypatch.setenv(IGNORED, "[]")
    refresh_env()
    result = check_paths(
        severity_chart, budget=45, max_examples=3, seed=0, helm="helm", timeout=5, artifacts=tmp_path / "results", jobs=jobs, fail_fast=True
    )
    assert result["status"] == "findings"
    traversal = mapping(result["traversal"])
    assert traversal["completed_paths"] == traversal["selected_paths"]
    diagnostics = chart_errors(result)
    assert any(row["code"] == "HH1101" and row["severity"] == "warning" and row["blocking"] is False for row in diagnostics)


def test_compiler_warning_threshold_retains_unknown_candidates(
    severity_chart: Chart, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """
    Keep unresolved expressions eligible for Helm instead of pruning them when their warning is nonfatal.

    Args:
        severity_chart (Chart): Chart with an added nondeterministic expression.
        monkeypatch (pytest.MonkeyPatch): Inherited severity and suppression settings.
        caplog (pytest.LogCaptureFixture): Effective compiler diagnostic levels.

    Returns:
        None: Error-only thresholds retain unknowns; promoting the warning stops the analysis.
    """
    (severity_chart.path / "templates/NOTES.txt").write_text("{{ now }}")
    monkeypatch.setenv(IGNORED, "[]")
    refresh_env()
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"findings": {"fail_on": "error"}}))
    refresh_env()
    contracts = Contracts.build(severity_chart.path)
    contracts.fail_fast = True
    assert contracts.predict(severity_chart.defaults) is None
    assert contracts.incomplete_evaluations > 0
    assert any(row["severity"] == "warning" and row["blocking"] is False for row in contracts.fallbacks)
    assert caplog.records[-1].levelno == logging.WARNING
    caplog.clear()
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"findings": {"fail_on": "error", "severity": {"HH2007": "error"}}}))
    refresh_env()
    with pytest.raises(RenderFailure, match="HH2007"):
        contracts.predict(severity_chart.defaults)
    assert caplog.records[-1].levelno == logging.ERROR


def test_warning_does_not_hide_a_later_error(severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Continue finite iteration past a downgraded finding and fail on the next blocking code.

    Args:
        severity_chart (Chart): Two independent Boolean factors.
        tmp_path (Path): Durable failure evidence.
        monkeypatch (pytest.MonkeyPatch): Replace rendering with deterministic classified outcomes.

    Returns:
        None: Both findings survive, and the blocking reproducer owns the failure checkpoint.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"findings": {"fail_on": "error", "severity": {"HH1101": "warning"}}}))
    refresh_env()

    def render(chart: Chart, values: dict[str, object], **kwargs: object) -> list[dict[str, object]]:
        """
        Produce different defects in the single-factor and joint branches.

        Args:
            chart (Chart): Input chart.
            values (dict[str, object]): Selected Boolean configuration.
            **kwargs (object): Render parameters.

        Returns:
            list[dict[str, object]]: Valid defaults, otherwise a classified render failure.
        """
        if values.get("flag"):
            raise RenderFailure("missing name" if values.get("other") else "invalid YAML", "HH1105" if values.get("other") else "HH1101")
        return [{"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": "fixture"}}]

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", render)
    result = check_chart(severity_chart, exhaustive=True, traversal_strategy="linear", fail_fast=True, artifact_dir=tmp_path / "artifacts")
    assert result["status"] == "failed"
    assert result["code"] == "HH1105"
    assert result["severity"] == "error"
    assert mapping(sequence(result["findings"])[0])["code"] == "HH1101"
    assert json.loads((tmp_path / "artifacts" / "observed-failure.json").read_text())["code"] == "HH1105"


def test_shards_preserve_nonfatal_findings_and_retry_them(severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Carry severity through generated suites, warm caches and final shard publication.

    Args:
        severity_chart (Chart): A finite two-path chart with one malformed output.
        tmp_path (Path): Suite, policy, cache and report locations.
        monkeypatch (pytest.MonkeyPatch): Isolate configuration discovery.

    Returns:
        None: Nonfatal findings are retried and published; inconsistent shard policies cannot be aggregated.
    """
    monkeypatch.chdir(tmp_path)
    config = tmp_path / "policy.yaml"
    config.write_text("findings:\n  fail_on: error\n  severity:\n    HH1101: warning\n")
    suite = tmp_path / "suite"
    reports = tmp_path / "reports"
    assert main(["generate", str(severity_chart.path), "--output", str(suite), "--max-examples", "3", "--config", str(config)]) == 0
    arguments = ["run", str(suite), "--config", str(config), "--artifact-dir", str(reports), "--jobs", "2"]
    for run_id in ("cold", "warm"):
        observed = []
        for index in (1, 2):
            assert main([*arguments, "--shard", f"{index}/2", "--run-id", run_id]) == 0
            record = json.loads((reports / "shards" / f"{index}-of-2" / "report.json").read_text())
            observed.extend(record["findings"])
            assert record["audit"]["findings"]
        assert len(observed) == 1
        assert observed[0]["code"] == "HH1101"
        assert observed[0]["severity"] == "warning"
        final = tmp_path / run_id
        assert aggregate([reports], 2, run_id, final) == 0
        merged = json.loads((final / "report.json").read_text())
        assert merged["charts"][0]["status"] == "findings"
        assert merged["charts"][0]["coverage_complete"] is False
        assert merged["charts"][0]["error_diagnostics"][0]["blocking"] is False
        assert "Severity: **warning**" in (final / "report.md").read_text()
    altered = reports / "shards" / "1-of-2" / "report.json"
    record = json.loads(altered.read_text())
    record["finding_policy"]["fail_on"] = "warning"
    altered.write_text(json.dumps(record))
    with pytest.raises(ValueError, match="different finding severity policies"):
        aggregate([reports], 2, "warm", tmp_path / "inconsistent")
    assert main([*arguments, "--fail", "warning", "--match", "flag"]) == 1
