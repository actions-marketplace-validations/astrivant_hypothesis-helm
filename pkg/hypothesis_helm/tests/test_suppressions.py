"""
Check generated suppression coverage, scope, worker isolation, and per-chart publication.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.cli import main
from hypothesis_helm.findings.policy import candidate_paths, resolve_codes
from hypothesis_helm.findings.suppressions import ENVIRONMENT, SuppressionCapture, observe, observed_paths
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.policy import load_policy


def rules(directory: Path) -> list[dict[str, object]]:
    """
    Load exported rules through the production configuration validator.

    Args:
        directory (Path): Chart artifact directory.

    Returns:
        list[dict[str, object]]: Validated code-only input constraints.
    """
    return [mapping(rule) for rule in sequence(load_policy(directory / "suppressions.yaml")["input_constraints"])]


def test_export_covers_all_changed_paths_and_shrinking_observations(tmp_path: Path) -> None:
    """
    Retain earlier codes and dependent fields while leaving unrelated branches enabled.

    Args:
        tmp_path (Path): Observation journal and draft destination.

    Returns:
        None: Every observed failure is covered and deleting one rule restores that check.
    """
    defaults: dict[str, object] = {"enabled": False, "secret": {"name": ""}, "unrelated": 1}
    chart = Chart(tmp_path, {}, defaults)
    values = {"enabled": True, "secret": {"name": ">0"}}
    with SuppressionCapture(tmp_path, enabled=True) as capture:
        observe("HH1101", defaults, values)
        observe("HH1101", defaults, values)
        observe("HH3001", defaults, {"secret": None})
    record: dict[str, object] = {"status": "failed", "code": "HH1101", "error": "[HH1101] YAML", "values": values}
    capture.write(record, name="demo", source="https://example.com/charts.git", defaults=defaults)
    proposals = rules(tmp_path)
    assert len(proposals) == 3
    assert "HH1101" in resolve_codes(proposals, candidate_paths(chart, values), [])
    assert "HH3001" in resolve_codes(proposals, candidate_paths(chart, {"secret": None}), [])
    assert "HH1101" not in resolve_codes(proposals, (("unrelated",),), [])
    assert "HH1101" not in resolve_codes([row for row in proposals if row["path"] != "$.enabled"], candidate_paths(chart, values), [])
    assert all(row["charts"] == [{"sources": ["https://example.com/charts.git"], "names": ["demo"]}] for row in proposals)
    text = (tmp_path / "suppressions.yaml").read_text()
    assert "Manifest" in text and "Template" in text and "HH1101: Invalid YAML" in text
    assert ">0" not in text  # Secret-bearing values are unnecessary for code/path rules.
    assert mapping(record["suppression_export"])["applied"] is False
    assert ENVIRONMENT not in os.environ


def test_audit_cover_removes_only_existing_redundant_rules(tmp_path: Path) -> None:
    """
    Remove a child covered by an observed parent without broadening sibling findings.

    Args:
        tmp_path (Path): Draft configuration destination.

    Returns:
        None: Category grouping keeps unrelated finding codes independently removable.
    """
    record: dict[str, object] = {
        "findings": [
            {"path": ["parent"], "code": "HH2001"},
            {"path": ["parent", "child"], "code": "HH2001"},
            {"path": ["sibling", "a"], "code": "HH2001"},
            {"path": ["sibling", "b"], "code": "HH2001"},
            {"path": ["sibling", "a"], "code": "HH2004"},
        ],
        "ignored_findings": [{"path": ["ignored"], "code": "HH2003"}],
    }
    SuppressionCapture(tmp_path, enabled=True).write(record, name="demo", source="remote.git")
    proposals = rules(tmp_path)
    assert {row["path"] for row in proposals} == {"$.parent", "$.sibling.a", "$.sibling.b"}
    assert next(row for row in proposals if row["path"] == "$.sibling.a")["ignored"] == ["HH2001", "HH2004"]
    assert all("HH2003" not in sequence(row["ignored"]) for row in proposals)


def test_baseline_widening_and_uncoded_failures_are_explicit(tmp_path: Path) -> None:
    """
    Label unavoidable whole-chart and wildcard rules without inventing infrastructure codes.

    Args:
        tmp_path (Path): Draft destination.

    Returns:
        None: Existing codes remain actionable, and uncoded failures remain visibly uncovered.
    """
    record: dict[str, object] = {
        "status": "failed",
        "phases": [
            {"status": "failed", "phase": "defaults", "error": "[HH1107] empty", "values": {}},
            {"status": "error", "phase": "tool", "error": "binary unavailable"},
            {"status": "failed", "phase": "items", "error": "[HH1101] bad", "values": {"items": [{"name": ">"}]}},
            {"status": "failed", "phase": "keys", "error": "[HH3002] bad", "values": {"labels": {"a.b": 1}}},
        ],
    }
    SuppressionCapture(tmp_path, enabled=True).write(record, name="demo", source="remote.git", defaults={})
    proposals = rules(tmp_path)
    assert {(row["path"], tuple(sequence(row["ignored"]))) for row in proposals} == {
        ("$", ("HH1107",)),
        ("$.items[*].name", ("HH1101",)),
        ("$.labels", ("HH3002",)),
    }
    text = (tmp_path / "suppressions.yaml").read_text()
    assert "Chart-wide:" in text and "Widened scope:" in text
    assert mapping(record["suppression_export"])["uncovered_observations"] == 1


def test_wildcard_audit_rules_cover_and_replace_redundant_descendants(tmp_path: Path) -> None:
    """
    Honor wildcard policy semantics when minimizing the exported rule set.

    Args:
        tmp_path (Path): Export destination.

    Returns:
        None: An observed wildcard covers concrete children only for its own finding code.
    """
    record: dict[str, object] = {
        "findings": [
            {"code": "HH2001", "path": ["*"]},
            {"code": "HH2001", "path": ["specific", "name"]},
            {"code": "HH2004", "path": ["specific", "name"]},
        ]
    }
    SuppressionCapture(tmp_path, enabled=True).write(record, name="demo", source="remote.git")
    proposals = rules(tmp_path)
    assert {(row["path"], tuple(sequence(row["ignored"]))) for row in proposals} == {
        ("$[*]", ("HH2001",)),
        ("$.specific.name", ("HH2004",)),
    }
    assert "HH2001" in resolve_codes(proposals, (("specific", "name"),), [])
    assert "HH2004" not in resolve_codes(proposals, (("unrelated",),), [])


def test_worker_journals_and_repeated_runs_are_isolated(tmp_path: Path) -> None:
    """
    Combine distinct worker journals without importing observations from an earlier run.

    Args:
        tmp_path (Path): Reused artifact destination.

    Returns:
        None: All workers contribute rules and a clean rerun produces an empty draft.
    """
    with SuppressionCapture(tmp_path, enabled=True) as capture:
        workers = [
            subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    "from hypothesis_helm.findings.suppressions import observe; import sys; observe('HH1101', {}, {sys.argv[1]: 1})",
                    f"field{index}",
                ]
            )
            for index in range(3)
        ]
        try:
            assert all(worker.wait(timeout=20) == 0 for worker in workers)
        finally:
            for worker in workers:
                if worker.poll() is None:
                    worker.kill()
                worker.wait()
    capture.write({"status": "interrupted"}, name="demo", source="remote.git", defaults={})
    assert {row["path"] for row in rules(tmp_path)} == {"$.field0", "$.field1", "$.field2"}
    with SuppressionCapture(tmp_path, enabled=True) as fresh:
        fresh.write({"status": "passed"}, name="demo", source="remote.git", defaults={})
    assert rules(tmp_path) == []


def test_summary_does_not_broaden_precise_phase_suppressions(tmp_path: Path) -> None:
    """
    Avoid turning a repeated scan summary into a new chart-wide finding.

    Args:
        tmp_path (Path): Draft destination.

    Returns:
        None: Phase inputs determine scope and the redundant summary introduces no root rule.
    """
    record: dict[str, object] = {
        "status": "failed",
        "error": "selected: [HH1101] bad YAML",
        "phases": [{"status": "failed", "phase": "selected", "error": "[HH1101] bad YAML", "values": {"selected": 1}}],
    }
    SuppressionCapture(tmp_path, enabled=True).write(record, name="demo", source="remote.git", defaults={})
    assert [row["path"] for row in rules(tmp_path)] == ["$.selected"]
    assert observed_paths({}, {"unserializable": object()}) == ((),)


def test_disabled_export_creates_no_artifacts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Leave ordinary tests and their filesystem footprint unchanged when export is not selected.

    Args:
        tmp_path (Path): Empty artifact location.
        monkeypatch (pytest.MonkeyPatch): Isolate any inherited observation scope.

    Returns:
        None: No rules become active and no files are written.
    """
    monkeypatch.delenv(ENVIRONMENT, raising=False)
    with SuppressionCapture(tmp_path, enabled=False) as capture:
        observe("HH1101", {}, {"name": ">"})
        capture.write({"status": "passed"}, name="demo", source="remote.git")
    assert list(tmp_path.iterdir()) == []


def test_audit_fail_fast_keeps_precise_paths(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Export input audit gaps even when --fail exits before rendering.

    Args:
        tmp_path (Path): Chart and audit artifacts.
        capsys (pytest.CaptureFixture[str]): Capture the audit report.

    Returns:
        None: The draft targets missing descriptions individually and preserves the failure exit.
    """
    from hypothesis_helm.tests.test_path_workers import fixture_chart

    chart = fixture_chart(tmp_path)
    artifacts = tmp_path / "audit"
    assert (
        main(["audit", str(chart.path), "--fail", "--export-suppressions", "--artifact-dir", str(artifacts), "--log-file", "/dev/stderr"])
        == 1
    )
    result = json.loads(capsys.readouterr().out)
    proposals = rules(artifacts)
    assert len([row for row in proposals if row["ignored"] == ["HH2003"]]) == 8
    assert all(row["path"] != "$" for row in proposals)
    for finding in [*result["findings"], *result["unresolved"]]:
        assert finding["code"] in resolve_codes(proposals, (tuple(finding.get("path", [])),), [])


@pytest.mark.parametrize("stop", ["continue", "fail", "interrupt"])
def test_recursive_export_precedes_next_chart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], stop: str
) -> None:
    """
    Export each finished chart immediately, including fail-fast and interrupted scans.

    Args:
        tmp_path (Path): Chart tree and scan results.
        monkeypatch (pytest.MonkeyPatch): Replace Helm execution with known outcomes.
        capsys (pytest.CaptureFixture[str]): Read the final scan record.
        stop (str): Continue, fail fast, or interrupt while testing the second chart.

    Returns:
        None: Every visited chart has a separate draft and pending charts do not.
    """
    source = tmp_path / "charts"
    for name in ("a", "b", "c"):
        chart = source / name
        chart.mkdir(parents=True)
        (chart / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": name, "version": "1.0.0"}))
        (chart / "values.yaml").write_text("{}")
    visited: list[Path] = []

    def exercise(path: Path, args: argparse.Namespace, artifacts: Path) -> dict[str, object]:
        """
        Check publication ordering before returning or interrupting the next result.

        Args:
            path (Path): Prepared chart copy.
            args (argparse.Namespace): Scan configuration.
            artifacts (Path): Per-chart output directory.

        Returns:
            dict[str, object]: Known coded failure with an exact input path.
        """
        if visited:
            assert (visited[-1] / "suppressions.yaml").exists()
        visited.append(artifacts)
        observe("HH1101", {}, {"key": ">"})
        if stop == "interrupt" and len(visited) == 2:
            raise KeyboardInterrupt
        return {"status": "failed", "error": "[HH1101] bad YAML", "values": {"key": ">"}}

    monkeypatch.setattr("hypothesis_helm.charts.repositories.scan.exercise_chart", exercise)
    monkeypatch.setattr("hypothesis_helm.charts.repositories.scan.shutil.which", lambda name: "/bin/true")
    arguments = [
        "test",
        str(source),
        "--no-build-dependencies",
        "--no-cache",
        "--export-suppressions",
        "--artifact-dir",
        str(tmp_path / "artifacts"),
        "--log-file",
        "/dev/stderr",
    ]
    if stop == "fail":
        arguments.append("--fail")
    assert main(arguments) == (130 if stop == "interrupt" else 1)
    result = json.loads(capsys.readouterr().out)
    assert len(visited) == {"continue": 3, "fail": 1, "interrupt": 2}[stop]
    for directory in visited:
        assert {row["path"] for row in rules(directory)} == {"$.key"}
    assert all("suppression_export" not in row for row in result["charts"] if row["status"] == "pending")


@pytest.mark.skipif(not shutil.which("helm"), reason="Helm is required")
def test_generated_suite_export_can_suppress_observed_failure(tmp_path: Path) -> None:
    """
    Exercise real generated workers and replay their draft through the normal policy loader.

    Args:
        tmp_path (Path): Real Helm chart, generated suite, and report directories.

    Returns:
        None: Export leaves the first failure intact; explicit reuse suppresses it.
    """
    chart = tmp_path / "chart"
    (chart / "templates").mkdir(parents=True)
    (chart / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "draft", "version": "1.0.0"}))
    (chart / "values.yaml").write_text("name: safe\n")
    (chart / "values.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {"name": {"enum": ["safe", ">0"], "description": "Config value"}},
            }
        )
    )
    (chart / "templates/config.yaml").write_text(
        dedent(
            """
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: demo
        data:
          value: {{ .Values.name }}
        """
        )
    )
    first = tmp_path / "first"
    command = ["test", str(chart), "--paths", "--jobs", "2", "--max-examples", "10", "--no-cache", "--artifact-dir", str(first)]
    assert main([*command, "--export-suppressions"]) == 1
    assert any("HH1101" in sequence(row["ignored"]) for row in rules(first))
    assert main([*command, "--config", str(first / "suppressions.yaml")]) == 0
