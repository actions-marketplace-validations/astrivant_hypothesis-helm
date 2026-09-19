"""
Verify severity inheritance across chart selectors, branches, workers and saved property suites.
"""

import json
from pathlib import Path

import pytest

from hypothesis_helm.charts.inspection.audit import audit_findings
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.paths import check_paths
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.cli import main
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.findings.policy import RuleScope
from hypothesis_helm.findings.severity import attributes, for_paths, policy
from hypothesis_helm.reporting.errors import chart_errors
from hypothesis_helm.rules import RenderFailure
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.selectors import SourceScope
from hypothesis_helm.tests.test_severity import severity_chart as severity_chart


def configure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, document: dict[str, object]) -> Path:
    """
    Resolve and inherit a user policy without changing the caller's global environment permanently.

    Args:
        tmp_path (Path): Configuration directory.
        monkeypatch (pytest.MonkeyPatch): Restore inherited settings after the test.
        document (dict[str, object]): User-facing YAML configuration.

    Returns:
        Path: Config file usable by both library calls and the CLI.
    """
    path = tmp_path / "policy.yaml"
    path.write_text(yamlio.dump(document))
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(path)))
    return path


def test_severity_inherits_per_setting_and_matches_sources(severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Merge partial settings at the chart and branch levels while retaining unrelated inherited codes.

    Args:
        severity_chart (Chart): Chart selected by its metadata name.
        tmp_path (Path): Config location.
        monkeypatch (pytest.MonkeyPatch): Isolate the worker environment.

    Returns:
        None: Deep overrides and wildcard paths apply only to matching source/name selectors.
    """
    config = configure(
        tmp_path,
        monkeypatch,
        {
            "findings": {"fail_on": "error", "severity": {"HH2001": "error", "HH1101": "warning"}},
            "input_constraints": [
                {"charts": ["severity"], "path": "$", "findings": {"severity": {"HH2003": "warning"}}},
                {"charts": ["severity"], "path": "$.items[*]", "findings": {"fail_on": "warning"}},
                {"charts": ["severity"], "path": "$.items[*].name", "findings": {"severity": {"HH1101": "info"}}},
                {
                    "charts": [{"sources": ["https://example.test/charts.git"], "names": ["severity"]}],
                    "path": "$.flag",
                    "findings": {"severity": {"HH1101": "error"}},
                },
            ],
        },
    )
    first = mapping(sequence(load_policy(config)["input_constraints"])[0])
    assert first["findings"] == {"severity": {"HH2003": "warning"}}
    root = for_paths(severity_chart.path)
    assert root["severity"] == {"HH2001": "error", "HH1101": "warning", "HH2003": "warning"}
    settings = for_paths(severity_chart.path, (("items", 0, "name"),))
    assert settings["fail_on"] == "warning"
    assert attributes("HH1101", settings=settings) == {"severity": "info", "blocking": False, "fail_fast": False}
    assert attributes("HH1101", settings=for_paths(severity_chart.path, (("flag",),)))["severity"] == "warning"
    with SourceScope("https://example.test/charts.git"):
        assert attributes("HH1101", settings=for_paths(severity_chart.path, (("flag",),)))["severity"] == "error"


def test_multiple_paths_and_nested_scopes_do_not_weaken_errors(
    severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Require all affected paths to fall below their own threshold before treating a joint finding as nonfatal.

    Args:
        severity_chart (Chart): Two independently mutable paths.
        tmp_path (Path): Config directory.
        monkeypatch (pytest.MonkeyPatch): Restore policy after the scope exits.

    Returns:
        None: Unrelated changes remain blocking and nested contexts restore their parent's decision.
    """
    configure(
        tmp_path,
        monkeypatch,
        {
            "findings": {"fail_on": "error"},
            "input_constraints": [{"charts": ["severity"], "path": "$.flag", "findings": {"severity": {"HH1101": "info"}}}],
        },
    )
    original = policy()
    with RuleScope.for_values(severity_chart, {"flag": True}):
        assert not attributes("HH1101")["blocking"]
        with pytest.raises(RuntimeError), RuleScope.for_values(severity_chart, {"flag": True, "other": True}):
            assert attributes("HH1101")["blocking"]
            raise RuntimeError("leave nested candidate")
        assert not attributes("HH1101")["blocking"]
    assert policy() == original


def test_equal_depth_conflicts_are_rejected(severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Reject contradictory matches instead of resolving them by YAML order.

    Args:
        severity_chart (Chart): Matching chart.
        tmp_path (Path): Conflicting configuration location.
        monkeypatch (pytest.MonkeyPatch): Inherited policy.

    Returns:
        None: A conflicting severity is reported when its branch is evaluated.
    """
    configure(
        tmp_path,
        monkeypatch,
        {
            "input_constraints": [
                {"charts": ["severity"], "path": "$.flag", "findings": {"severity": {"HH1101": value}}} for value in ("warning", "error")
            ]
        },
    )
    with pytest.raises(ValueError, match="Conflicting input constraints for findings.HH1101"):
        for_paths(severity_chart.path, (("flag",),))


@pytest.mark.parametrize("settings", [None, {"fail_on": "fatal"}, {"severity": {"HH9999": "error"}}, {"severity": {"HH1101": "off"}}])
def test_invalid_branch_findings(tmp_path: Path, settings: object) -> None:
    """
    Apply the global findings validator to each scoped override.

    Args:
        tmp_path (Path): Invalid config directory.
        settings (object): Malformed findings settings.

    Returns:
        None: Invalid scoped policies fail during config loading, before chart execution.
    """
    config = tmp_path / "policy.yaml"
    config.write_text(yamlio.dump({"input_constraints": [{"charts": ["severity"], "path": "$", "findings": settings}]}))
    with pytest.raises(ValueError, match="findings"):
        load_policy(config)


def test_chart_compiler_finding_threshold(severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Resolve chart overrides for compiler diagnostics outside a candidate's render scope.

    Args:
        severity_chart (Chart): Chart with an unsupported time-dependent expression.
        tmp_path (Path): Policy directory.
        monkeypatch (pytest.MonkeyPatch): Isolate the inherited policy.

    Returns:
        None: Chart-level severity and fail-fast decisions survive the raised diagnostic.
    """
    configure(
        tmp_path,
        monkeypatch,
        {"input_constraints": [{"charts": ["severity"], "path": "$", "findings": {"fail_on": "error", "severity": {"HH2007": "error"}}}]},
    )
    (severity_chart.path / "templates/NOTES.txt").write_text("{{ now }}")
    contracts = Contracts.build(severity_chart.path)
    with pytest.raises(RenderFailure, match="HH2007") as error:
        contracts.predict(severity_chart.defaults)
    assert error.value.controls == {"severity": "error", "blocking": True, "fail_fast": True}


def test_chart_threshold_applies_to_empty_baseline(
    severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """
    Honor a chart-level severity for the nonempty check that follows baseline rendering.

    Args:
        severity_chart (Chart): Chart whose only template is replaced with empty output.
        tmp_path (Path): Policy and report directory.
        monkeypatch (pytest.MonkeyPatch): Isolate inherited settings.
        caplog (pytest.LogCaptureFixture): Baseline log records after leaving the finding scope.

    Returns:
        None: The baseline finding retains its scoped severity and later path checks run.
    """
    configure(
        tmp_path,
        monkeypatch,
        {
            "findings": {"fail_on": "error"},
            "input_constraints": [{"charts": ["severity"], "path": "$", "findings": {"severity": {"HH1107": "info"}}}],
        },
    )
    (severity_chart.path / "templates/config.yaml").write_text("")
    result = check_paths(
        severity_chart, budget=45, max_examples=3, seed=0, helm="helm", timeout=5, artifacts=tmp_path / "reports", fail_fast=True
    )
    assert result["status"] == "findings"
    baseline = mapping(result["baseline"])
    assert baseline["severity"] == "info" and baseline["blocking"] is False
    recorded = next(record for record in caplog.records if "Baseline finding" in record.getMessage())
    assert getattr(recorded, "finding_severity", None) == "info"
    traversal = mapping(result["traversal"])
    assert traversal["completed_paths"] == traversal["selected_paths"]


def test_branch_audit_enables_its_own_threshold(severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Apply a local audit gate without requiring a global --fail or fail_on setting.

    Args:
        severity_chart (Chart): Paths with informational missing descriptions.
        tmp_path (Path): Configuration directory.
        monkeypatch (pytest.MonkeyPatch): Isolate policy discovery.

    Returns:
        None: Only the promoted path blocks; ordinary audit findings remain visible.
    """
    monkeypatch.chdir(tmp_path)
    config = configure(
        tmp_path,
        monkeypatch,
        {
            "input_constraints": [
                {"charts": ["severity"], "path": "$.flag", "findings": {"fail_on": "error", "severity": {"HH2003": "error"}}}
            ]
        },
    )
    report = audit_findings(severity_chart)
    findings = {tuple(str(part) for part in sequence(mapping(row)["path"])): mapping(row) for row in sequence(report["findings"])}
    assert findings[("flag",)]["fail_fast"] is True
    assert findings[("other",)]["fail_fast"] is False
    assert main(["audit", str(severity_chart.path), "--config", str(config)]) == 1
    assert main(["audit", str(severity_chart.path), "--config", str(config), "--ignore", "HH2003"]) == 0


@pytest.mark.parametrize("jobs", [1, 2])
def test_branch_runtime_threshold_reaches_path_workers(
    severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int
) -> None:
    """
    Apply per-path severity during serial and subprocess execution.

    Args:
        severity_chart (Chart): The flag path emits malformed YAML.
        tmp_path (Path): Policy and reports directory.
        monkeypatch (pytest.MonkeyPatch): Inherited worker settings.
        jobs (int): Number of path workers.

    Returns:
        None: The demoted finding is recorded and all selected paths are visited.
    """
    configure(
        tmp_path,
        monkeypatch,
        {
            "findings": {"fail_on": "error"},
            "input_constraints": [{"charts": ["severity"], "path": "$.flag", "findings": {"severity": {"HH1101": "info"}}}],
        },
    )
    result = check_paths(
        severity_chart, budget=45, max_examples=3, seed=0, helm="helm", timeout=5, artifacts=tmp_path / "reports", jobs=jobs, fail_fast=True
    )
    assert result["status"] == "findings"
    traversal = mapping(result["traversal"])
    assert traversal["completed_paths"] == traversal["selected_paths"]
    finding = next(row for row in chart_errors(result) if row["code"] == "HH1101")
    assert finding["severity"] == "info"
    assert finding["blocking"] is False


@pytest.mark.parametrize("jobs", [1, 2])
@pytest.mark.parametrize("cleared", [False, True])
def test_saved_suite_respects_branch_thresholds(
    severity_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int, cleared: bool
) -> None:
    """
    Retain severity decisions in JUnit and continue unaffected properties when a branch clears fail-fast.

    Args:
        severity_chart (Chart): Two generated path properties with one invalid render.
        tmp_path (Path): Suite and policy output directory.
        monkeypatch (pytest.MonkeyPatch): Isolate local configuration.
        jobs (int): Serial or parallel pytest executor.
        cleared (bool): Restore legacy non-fail-fast behavior for the failing branch.

    Returns:
        None: Both properties execute and the report preserves the branch decision after its scope exits.
    """
    monkeypatch.chdir(tmp_path)
    config = configure(
        tmp_path,
        monkeypatch,
        {
            "findings": {"fail_on": "error"},
            "input_constraints": [
                {"charts": ["severity"], "path": "$.flag", "findings": {"fail_on": None} if cleared else {"severity": {"HH1101": "info"}}}
            ],
        },
    )
    suite = tmp_path / "suite"
    assert main(["generate", str(severity_chart.path), "--output", str(suite), "--max-examples", "3", "--config", str(config)]) == 0
    assert main(["run", str(suite), "--config", str(config), "--jobs", str(jobs), "--traversal-strategy", "linear"]) == (
        1 if cleared else 0
    )
    report = json.loads((suite / "report.json").read_text())
    import xml.etree.ElementTree as ET

    cases = list(ET.fromstring(report["junit_xml"]).iter("testcase"))
    assert len(cases) == 2
    if cleared:
        assert sum(case.find("failure") is not None for case in cases) == 1
        assert sum(case.find("skipped") is not None for case in cases) == 0
    else:
        assert report["findings"][0]["severity"] == "info"
        assert report["findings"][0]["fail_fast"] is False
