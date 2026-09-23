"""
Verify branch-specific finding controls, fail-fast audits, and isolated validation caches.
"""

import json
import os
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.inspection.audit import audit_findings
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.cli import argument_parser, main
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.execution.state.render_hashes import RenderHashes
from hypothesis_helm.execution.suite import run_suite
from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.findings.policy import RuleScope, candidate_paths, resolve_codes
from hypothesis_helm.reporting.reports.repository import write_reports
from hypothesis_helm.rules import ENVIRONMENT as RULE_ENVIRONMENT
from hypothesis_helm.rules import ignored, may_check
from hypothesis_helm.schemas.configuration.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests.fixtures.cli import result_text
from hypothesis_helm.tests.generation.test_input_domains import fixture_chart


def configure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, rules: list[dict[str, object]], ignored_codes: list[str] | None = None
) -> Path:
    """
    Resolve a real configuration and install its worker environment.

    Args:
        tmp_path (Path): Policy destination.
        monkeypatch (pytest.MonkeyPatch): Restore environment after each test.
        rules (list[dict[str, object]]): Unresolved input constraints.
        ignored_codes (list[str] | None): Optional global exclusions.

    Returns:
        Path: Configuration reusable by the CLI.
    """
    path = tmp_path / "policy.yaml"
    path.write_text(yamlio.dump({"ignored": ignored_codes or [], "downstream_inputs": False, "input_constraints": rules}))
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(path)))
    refresh_env()
    monkeypatch.setenv(RULE_ENVIRONMENT, json.dumps(ignored_codes or []))
    refresh_env()
    return path


@pytest.mark.parametrize(
    "extra",
    [
        {"ignored": "HH2001"},
        {"enabled": ["HH9999"]},
        {"ignored": [1]},
        {"ignored": ["HH2001"], "enabled": ["HH2001"]},
        {"ignored": [], "allow_empty": True},
        {},
    ],
)
def test_invalid_scoped_policy(tmp_path: Path, extra: dict[str, object]) -> None:
    """
    Reject malformed finding controls before they can change test coverage.

    Args:
        tmp_path (Path): Policy destination.
        extra (dict[str, object]): Invalid code configuration.

    Returns:
        None: Validation reports a configuration error.
    """
    path = tmp_path / "policy.yaml"
    path.write_text(yamlio.dump({"input_constraints": [{"charts": ["demo"], "path": "$.missing", **extra}]}))
    with pytest.raises(ValueError):
        load_policy(path)


@pytest.mark.parametrize(
    ("paths", "disabled"),
    [
        ((("credentials", "name"),), True),
        ((("credentials", "token"),), False),
        ((("credentials", "name"), ("other",)), False),
        ((("items", 0, "name"),), True),
        ((("items", 0, "name"), ("items", 1, "token")), False),
        (((),), False),
        ((), False),
    ],
)
def test_branch_precedence(paths: tuple[tuple[str | int, ...], ...], disabled: bool) -> None:
    """
    Require all changed fields to permit suppression and honor deeper exceptions.

    Args:
        paths (tuple[tuple[str | int, ...], ...]): Audit or candidate paths.
        disabled (bool): Expected effective policy.

    Returns:
        None: Siblings, collection entries and baselines remain independently checked.
    """
    rules: list[dict[str, object]] = [
        {"path": "$.credentials", "ignored": ["HH2001"]},
        {"path": "$.credentials.token", "enabled": ["HH2001"]},
        {"path": "$.items[*].name", "ignored": ["HH2001"]},
    ]
    assert ("HH2001" in resolve_codes(rules, paths, [])) is disabled
    assert resolve_codes(rules, paths, []) == resolve_codes(list(reversed(rules)), paths, [])
    assert "HH2001" not in resolve_codes([*rules, {"path": "$.credentials", "enabled": ["HH2001"]}], (("credentials", "name"),), [])


def test_missing_paths_can_have_code_only_rules(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Target absent schema paths without manufacturing a generation schema for them.

    Args:
        tmp_path (Path): Chart and policy fixture.
        monkeypatch (pytest.MonkeyPatch): Inherited policy.

    Returns:
        None: Audit evidence is suppressed locally while unrelated findings remain visible.
    """
    chart = fixture_chart(tmp_path)
    mapping(chart.schema["properties"]).pop("secretName")
    configure(tmp_path, monkeypatch, [{"charts": ["demo"], "path": "$.secretName", "ignored": ["HH2001"]}])
    result = audit_findings(chart)
    assert any(mapping(row)["code"] == "HH2001" for row in sequence(result["ignored_findings"]))
    assert not any(mapping(row)["code"] == "HH2001" for row in sequence(result["findings"]))
    assert chart.input_domains().rules == []
    assert result["findings"]  # Other documentation findings are still active.
    configure(tmp_path, monkeypatch, [{"charts": ["other"], "path": "$.secretName", "ignored": ["HH2001"]}])
    assert any(mapping(row)["code"] == "HH2001" for row in sequence(audit_findings(chart)["findings"]))


def test_global_exclusion_can_be_enabled_locally(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Re-enable a globally ignored validator and restore policy after nested failures.

    Args:
        tmp_path (Path): Chart and policy fixture.
        monkeypatch (pytest.MonkeyPatch): Global and scoped policies.

    Returns:
        None: Validator preparation and candidate checking agree, without scope leakage.
    """
    chart = fixture_chart(tmp_path)
    configure(tmp_path, monkeypatch, [{"charts": ["demo"], "path": "$.secretName", "enabled": ["HH1108"]}], ["HH1108"])
    assert ignored("HH1108") and may_check("HH1108")
    with pytest.raises(RuntimeError), RuleScope.for_values(chart, {"secretName": "changed"}):
        assert not ignored("HH1108")
        with RuleScope.for_values(chart, {}):
            assert ignored("HH1108")
        assert not ignored("HH1108")
        raise RuntimeError("restore")
    assert ignored("HH1108")


def test_fail_uses_scoped_audit_controls(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Fail only when a path-specific exception leaves an audit finding enabled.

    Args:
        tmp_path (Path): Chart with an undocumented template input.
        monkeypatch (pytest.MonkeyPatch): Isolated global exclusions.
        capsys (pytest.CaptureFixture[str]): CLI reports.

    Returns:
        None: Enabling wins over a global CLI exclusion and scoped ignoring restores success.
    """
    chart = fixture_chart(tmp_path)
    mapping(chart.schema["properties"]).pop("secretName")
    (tmp_path / "values.schema.json").write_text(json.dumps(chart.schema))
    for key, expected in (("enabled", 1), ("ignored", 0)):
        policy = configure(tmp_path, monkeypatch, [{"charts": ["demo"], "path": "$.secretName", key: ["HH2001"]}], sorted(CATALOG))
        assert (
            main(["audit", str(tmp_path), "--fail", "--config", str(policy), "--disable-codes", "HH2001", "--log-file", "/dev/stderr"])
            == expected
        )
        report = json.loads(result_text(capsys.readouterr().out))
        assert bool(report["findings"]) is bool(expected)
        assert report["ignored_findings"]


def test_effective_changes_include_deletions_and_array_entries(tmp_path: Path) -> None:
    """
    Compute concrete changed paths without counting unchanged baseline fields.

    Args:
        tmp_path (Path): Original chart fixture.

    Returns:
        None: Null deletion, array edits and added leaves have distinct paths.
    """
    chart = fixture_chart(tmp_path)
    chart.defaults["items"] = [{"name": "old", "same": True}]
    values = {**chart.defaults, "secretName": None, "items": [{"name": "new", "same": True}], "new": {"nested": 1}}
    assert set(candidate_paths(chart, values)) == {("secretName",), ("items", 0, "name"), ("new", "nested")}
    assert candidate_paths(chart, {}) == ()


def test_identical_output_cannot_cross_check_policies(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Validate identical manifests again when another input branch requires more checks.

    Args:
        tmp_path (Path): Chart fixture.
        monkeypatch (pytest.MonkeyPatch): Enable a single branch exception.

    Returns:
        None: A scoped ignored duplicate does not become an enabled branch's success witness.
    """
    chart = fixture_chart(tmp_path)
    configure(tmp_path, monkeypatch, [{"charts": ["demo"], "path": "$.secretName", "ignored": ["HH1106"]}])
    resource = {"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": "same"}}
    output = yamlio.dump(resource) + "---\n" + yamlio.dump(resource)
    hashes = RenderHashes()
    render(chart, {"secretName": "changed"}, rendered_output=output, hashes=hashes, stream=False)
    cases: list[dict[str, object]] = [{"port": 42}, {"secretName": "changed", "port": 42}, {}]
    for overrides in cases:
        with pytest.raises(RenderFailure, match="HH1106"):
            render(chart, overrides, rendered_output=output, hashes=hashes, stream=False)
    assert hashes.cache_hits == 0
    assert not ignored("HH1106")


def test_symbolic_pruning_respects_enabled_checks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Prevent a pruned input from inheriting a witness validated under weaker checks.

    Args:
        tmp_path (Path): Finite chart with equivalent output for both flag values.
        monkeypatch (pytest.MonkeyPatch): In-memory rendering and branch policy.

    Returns:
        None: Re-enabling the duplicate-resource check exposes the otherwise equivalent failure.
    """
    from hypothesis_helm.charts.model import Chart
    from hypothesis_helm.charts.testing.runner import check_chart

    fixture_chart(tmp_path)
    schema: dict[str, object] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["enabled"],
        "properties": {"enabled": {"type": "boolean"}},
    }
    chart = Chart(tmp_path, schema, {"enabled": False})
    resource = {"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": "same"}}
    output = yamlio.dump(resource) + "---\n" + yamlio.dump(resource)
    (tmp_path / "templates/pod.yaml").write_text(output)
    configure(tmp_path, monkeypatch, [{"charts": ["demo"], "path": "$.enabled", "enabled": ["HH1106"]}], ["HH1106"])

    def rendered(chart: Chart, values: dict[str, object], **options: object) -> list[dict[str, object]]:
        """
        Validate fixed output without launching external Helm.

        Args:
            chart (Chart): Original finite chart.
            values (dict[str, object]): Current overrides.
            **options (object): Unused external rendering settings.

        Returns:
            list[dict[str, object]]: Validated resources or a finding when checks are enabled.
        """
        return render(chart, values, rendered_output=output, stream=False)

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", rendered)
    result = check_chart(chart, exhaustive=True, prune_equivalent=True, time_limit=10, max_examples=2)
    assert result["status"] == "failed" and "HH1106" in str(result["error"])


def test_opaque_warning_can_be_enabled_for_one_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """
    Apply the same branch policy to audit records and live opaque-object warnings.

    Args:
        tmp_path (Path): Chart metadata and scoped policy.
        monkeypatch (pytest.MonkeyPatch): Globally ignored HH2006 with a local exception.
        caplog (pytest.LogCaptureFixture): Warning evidence.

    Returns:
        None: Only the explicitly enabled opaque field emits a warning and a visible finding.
    """
    chart = fixture_chart(tmp_path)
    chart.schema = {"type": "object", "properties": {"first": {"type": "object"}, "second": {"type": "object"}}}
    configure(tmp_path, monkeypatch, [{"charts": ["demo"], "path": "$.first", "enabled": ["HH2006"]}], ["HH2006"])
    report = audit_findings(chart)
    opaque = [mapping(item) for item in sequence(report["findings"]) if mapping(item)["code"] == "HH2006"]
    assert [finding["path"] for finding in opaque] == [["first"]]
    warnings = [record.message for record in caplog.records if "[HH2006]" in record.message]
    assert len(warnings) == 1 and "$.first" in warnings[0]


@pytest.mark.parametrize("fail", [False, True])
def test_scan_audit_findings_continue_or_fail_fast(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], fail: bool
) -> None:
    """
    Stop all subsequent chart work only when fail-fast is requested.

    Args:
        tmp_path (Path): Two independent charts.
        monkeypatch (pytest.MonkeyPatch): Replace testing after the real audit.
        capsys (pytest.CaptureFixture[str]): Structured CLI output.
        fail (bool): Requested fail-fast behavior.

    Returns:
        None: Findings appear in both reports, and --fail returns one before testing either chart.
    """
    for name in ("a", "b"):
        fixture_chart(tmp_path / name)
    executed: list[Path] = []

    def exercise(path: Path, args: object, artifacts: Path) -> dict[str, object]:
        """
        Record a test job after audit handling has completed.

        Args:
            path (Path): Prepared chart.
            args (object): Unused command options.
            artifacts (Path): Unused artifact directory.

        Returns:
            dict[str, object]: A passing run independent of documentation warnings.
        """
        executed.append(path)
        return {"status": "passed", "attempts": 1}

    monkeypatch.setattr("hypothesis_helm.charts.repositories.scan._exercise_chart", exercise)
    arguments = [
        "test",
        str(tmp_path),
        "--no-build-dependencies",
        "--no-cache",
        "--helm",
        "/usr/bin/true",
        "--log-file",
        "/dev/stderr",
        "--artifact-dir",
        str(tmp_path / "results"),
    ]
    assert main([*arguments, *(["--fail"] if fail else [])]) == (1 if fail else 0)
    report = json.loads(result_text(capsys.readouterr().out))
    assert len(executed) == (0 if fail else 2)
    assert report["charts"][0]["audit"]["findings"]
    assert report["charts"][1]["status"] == ("pending" if fail else "passed")
    markdown, _ = write_reports(report, tmp_path / "report")
    assert "HH2003" in markdown.read_text() and "Audit findings:" in markdown.read_text()


@pytest.mark.parametrize("command", ["audit", "generate", "test", "scan", "run"])
def test_fail_replaces_strict(command: str) -> None:
    """
    Expose one failure switch and reject the removed spelling.

    Args:
        command (str): Finding-producing CLI command.

    Returns:
        None: --fail is accepted and --strict is an argument error.
    """
    assert argument_parser().parse_args([command, "chart", "--fail"]).fail
    with pytest.raises(SystemExit) as error:
        argument_parser().parse_args([command, "chart", "--strict"])
    assert error.value.code == 2


@pytest.mark.parametrize("code", sorted(CATALOG))
def test_fail_honors_every_observed_code(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, code: str) -> None:
    """
    Apply the same fail-fast decision to every finding category.

    Args:
        tmp_path (Path): Chart fixture.
        monkeypatch (pytest.MonkeyPatch): Inject classified detector output before tests start.
        code (str): Every current catalog code.

    Returns:
        None: No category is exempt from an explicit --fail request.
    """
    from hypothesis_helm.charts.repositories.scan import exercise_chart

    chart = fixture_chart(tmp_path)
    monkeypatch.setattr(
        "hypothesis_helm.charts.repositories.scan.audit_findings", lambda chart: {"findings": [{"code": code}], "unresolved": []}
    )
    args = argument_parser().parse_args(["scan", "remote", "--fail"])
    result = exercise_chart(chart.path, args, tmp_path / "results")
    assert result["status"] == "failed" and result["code"] == code


@pytest.mark.parametrize("jobs", [1, 2])
def test_suite_fail_fast_joins_workers(tmp_path: Path, jobs: int) -> None:
    """
    Stop scheduled properties after a failure and join any running sibling processes.

    Args:
        tmp_path (Path): Editable saved suite and worker artifacts.
        jobs (int): Serial or parallel execution.

    Returns:
        None: Later work never starts, children exit, and the preserved report returns one.
    """
    (tmp_path / "test_chart_values.py").write_text(
        dedent("""
        import os
        import time
        from pathlib import Path

        def test_a():
            assert False, "first finding"

        def test_b():
            Path("sibling.pid").write_text(str(os.getpid()))
            time.sleep(60)

        def test_c():
            Path("unexpected").touch()
        """)
    )
    assert run_suite(tmp_path, jobs=jobs, cache=False, fail_fast=True, traversal_strategy="linear") == 1
    assert not (tmp_path / "unexpected").exists()
    assert json.loads((tmp_path / "report.json").read_text())["exit_code"] == 1
    if (tmp_path / "sibling.pid").exists():
        with pytest.raises(ProcessLookupError):
            os.kill(int((tmp_path / "sibling.pid").read_text()), 0)
    if jobs > 1:
        concurrency = json.loads((tmp_path / "concurrency.json").read_text())
        assert concurrency["failed_early"] is True and concurrency["interrupted"] is False
        assert len(concurrency["not_started"]) == 1


def test_path_workers_inherit_scoped_checks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Exercise real Helm workers with a rule that applies to only one input branch.

    Args:
        tmp_path (Path): Chart and worker results.
        monkeypatch (pytest.MonkeyPatch): Inherited scoped policy.

    Returns:
        None: Both workers finish and a disabled blocking render failure remains explicitly ignored.
    """
    from hypothesis_helm.charts.model import Chart
    from hypothesis_helm.charts.testing.paths import check_paths

    chart = fixture_chart(tmp_path)
    chart.schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {"left": {"type": "boolean"}, "right": {"type": "boolean"}},
        "required": ["left", "right"],
    }
    chart.defaults = {"left": False, "right": False}
    (tmp_path / "values.schema.json").write_text(json.dumps(chart.schema))
    (tmp_path / "values.yaml").write_text(yamlio.dump(chart.defaults))
    (tmp_path / "templates/pod.yaml").write_text(
        dedent("""
        {{- if .Values.left }}{{ fail "deliberate rejection" }}{{ end }}
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: example
        data:
          right: {{ .Values.right | quote }}
        """)
    )
    (tmp_path / ".helmignore").write_text("results/\n")
    configure(tmp_path, monkeypatch, [{"charts": ["demo"], "path": "$.left", "ignored": ["HH1001"]}])
    chart = Chart.load(tmp_path)
    result = check_paths(chart, budget=30, max_examples=3, seed=0, helm="helm", timeout=5, artifacts=tmp_path / "results", jobs=2)
    phases = [mapping(item) for item in sequence(result["phases"]) if mapping(item).get("kind") == "value-path"]
    assert len(phases) == 2
    assert all(phase["status"] in {"passed", "ignored"} for phase in phases)
    left = next(phase for phase in phases if phase["path"] == ["left"])
    assert int(str(mapping(left["ignored_failures"])["HH1001"])) > 0
