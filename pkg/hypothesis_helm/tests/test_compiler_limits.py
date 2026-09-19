"""
Keep helper analysis configurable, conservative at its boundary, and consistent across workers.
"""

import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.rendering import RenderFailure, render
from hypothesis_helm.cli import argument_parser, main
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.compiler.passes.rejections import matches_rejection
from hypothesis_helm.execution.cache import fingerprint
from hypothesis_helm.schemas.policy import ENVIRONMENT, load_policy


def helper_chart(directory: Path, depth: int) -> Chart:
    """
    Build independent rejection and direct-output chains of exactly the requested depth.

    Args:
        directory (Path): Temporary chart directory.
        depth (int): Number of nested helper invocations, including the first call.

    Returns:
        Chart: Chart exercising both analyses without external dependencies.
    """
    (directory / "templates").mkdir()
    (directory / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "helpers", "version": "1.0.0"}))
    (directory / "values.yaml").write_text(yamlio.dump({"name": "example", "enabled": True}))
    (directory / "values.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {"name": {"type": "string"}, "enabled": {"type": "boolean"}},
            }
        )
    )
    helpers = []
    for kind, terminal in (
        ("output", "{{ .Values.name }}"),
        ("reject", '{{ if eq .Values.name "reject" }}{{ fail "rejected name" }}{{ end }}'),
    ):
        for index in range(depth):
            body = terminal if index == depth - 1 else '{{ include "' + kind + str(index + 1) + '" . }}'
            helpers.append('{{ define "' + kind + str(index) + '" }}' + body + "{{ end }}")
    (directory / "templates/_helpers.tpl").write_text("\n".join(helpers))
    (directory / "templates/NOTES.txt").write_text('{{ include "reject0" . }}')
    (directory / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: Pod
        metadata:
          name: helpers
          annotations:
            enabled: {{ .Values.enabled | quote }}
        spec:
          containers:
            - name: app
              image: example
          volumes:
            - name: credentials
              secret:
                secretName: {{ include "output0" . | quote }}
        """)
    )
    return Chart.load(directory)


@pytest.mark.parametrize(("depth", "limit", "supported"), [(16, None, True), (17, None, False), (20, 32, True), (2, 1, False)])
def test_analysis_depth_boundary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, depth: int, limit: int | None, supported: bool) -> None:
    """
    Apply one budget to rejection prediction and destination projection without dropping unknown cases.

    Args:
        tmp_path (Path): Chart directory.
        monkeypatch (pytest.MonkeyPatch): Isolate the inherited compiler policy.
        depth (int): Actual helper chain depth.
        limit (int | None): Requested override or the default budget.
        supported (bool): Whether the complete chain fits within that budget.

    Returns:
        None: Both analyses agree at the exact boundary, with native Helm confirming rejections.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"compiler": {} if limit is None else {"max_call_depth": limit}}))
    chart = helper_chart(tmp_path, depth)
    model = Contracts.build(chart.path)
    rejection = model.predict({**chart.defaults, "name": "reject"})
    assert (rejection is not None) is supported
    assert model.predict(chart.defaults) is None
    rules, diagnostics = project(chart.path, chart.schema)
    assert any(rule["path"] == ["name"] for rule in rules) is supported
    if not supported:
        assert f"helper call depth exceeds compiler limit {limit or 16}" in str(diagnostics)
    if shutil.which("helm") is not None:
        render(chart, {})
        with pytest.raises(RenderFailure) as failure:
            render(chart, {"name": "reject"})
        if rejection is not None:
            assert matches_rejection(str(failure.value), rejection)


def test_recursive_helpers_remain_unresolved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep cycle safety and unrelated limits when raising the helper budget.

    Args:
        tmp_path (Path): Chart directory.
        monkeypatch (pytest.MonkeyPatch): Raise the analysis depth.

    Returns:
        None: An infinite call cycle cannot establish a constraint or rejection.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"compiler": {"max_call_depth": 64}}))
    chart = helper_chart(tmp_path, 1)
    (chart.path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{ define "output0" }}{{ include "output0" . }}{{ end }}
        {{ define "reject0" }}{{ include "reject0" . }}{{ fail "unreachable" }}{{ end }}
        """)
    )
    assert Contracts.build(chart.path).predict(chart.defaults) is None
    rules, diagnostics = project(chart.path, chart.schema)
    assert rules == []
    assert "recursive" in str(diagnostics)


@pytest.mark.parametrize(
    "compiler",
    [
        None,
        [],
        32,
        {"typo": 32},
        {"max_call_depth": 0},
        {"max_call_depth": -1},
        {"max_call_depth": True},
        {"max_call_depth": 1.5},
        {"max_call_depth": "32"},
    ],
)
def test_invalid_compiler_configuration(tmp_path: Path, compiler: object) -> None:
    """
    Reject malformed or unbounded compiler settings before any chart work starts.

    Args:
        tmp_path (Path): Config directory.
        compiler (object): Unsupported settings or invalid depth.

    Returns:
        None: Invalid policy raises an actionable configuration error.
    """
    config = tmp_path / "policy.yaml"
    config.write_text(yamlio.dump({"compiler": compiler}))
    with pytest.raises(ValueError, match="compiler"):
        load_policy(config)


@pytest.mark.parametrize("command", ["audit", "generate", "test", "scan", "run"])
def test_compiler_option_available(command: str) -> None:
    """
    Expose the same override on every command accepting an input policy.

    Args:
        command (str): Command performing or scheduling compiler analysis.

    Returns:
        None: Parser accepts an explicit depth for each entry point.
    """
    args = argument_parser().parse_args([command, "example", "--compiler-call-depth", "32"])
    assert args.compiler_call_depth == 32


def test_policy_precedence_and_cache_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Freeze each chart's budget and prevent cache reuse after a configuration change.

    Args:
        tmp_path (Path): Config and chart directory.
        monkeypatch (pytest.MonkeyPatch): Apply resolved policies as the coordinator does.

    Returns:
        None: Overrides win, old models retain their budget, and newly built models use the new setting.
    """
    config = tmp_path / "policy.yaml"
    config.write_text(yamlio.dump({"compiler": {"max_call_depth": 24}}))
    chart = helper_chart(tmp_path, 20)
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(config)))
    original = Contracts.build(chart.path)
    previous = fingerprint(tmp_path, 0, None, "none")
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(config, compiler_call_depth=32)))
    assert original.max_call_depth == 24
    assert Contracts.build(chart.path).max_call_depth == 32
    assert fingerprint(tmp_path, 0, None, "none") != previous
    with pytest.raises(ValueError, match="positive integer"):
        load_policy(config, compiler_call_depth=0)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_parallel_workers_inherit_compiler_override(tmp_path: Path, capfd: pytest.CaptureFixture[str]) -> None:
    """
    Exercise the real CLI, inherited policy, and path-worker interpreters together.

    Args:
        tmp_path (Path): Chart and artifact directories.
        capfd (pytest.CaptureFixture[str]): Capture the machine-readable CLI report.

    Returns:
        None: Worker rejection reports retain the CLI override instead of their own default.
    """
    chart = helper_chart(tmp_path, 20)
    config = tmp_path / "policy.yaml"
    config.write_text(yamlio.dump({"compiler": {"max_call_depth": 1}}))
    assert (
        main(
            [
                "test",
                str(chart.path),
                "--filter",
                "--config",
                str(config),
                "--compiler-call-depth",
                "32",
                "--jobs",
                "2",
                "--max-examples",
                "2",
                "--chart-timeout",
                "30s",
                "--no-cache",
                "--artifact-dir",
                str(tmp_path / "results"),
                "--log-file",
                "/dev/stderr",
            ]
        )
        == 0
    )
    report = json.loads(capfd.readouterr().out)
    assert report["settings"]["input_policy"]["compiler"] == {"max_call_depth": 32}
    phases = [phase for phase in report["charts"][0]["phases"] if "worker_pid" in phase]
    assert len(phases) == 2
    assert all(phase["configuration_rejections"]["max_call_depth"] == 32 for phase in phases)
