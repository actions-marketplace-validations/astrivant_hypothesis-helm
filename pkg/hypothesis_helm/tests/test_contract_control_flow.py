"""
Compare lexical control-flow predictions with native Helm execution.
"""

import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.rendering import RenderFailure, render
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.passes.rejections import matches_rejection


@pytest.fixture
def control_chart(tmp_path: Path) -> Chart:
    """
    Create a chart whose notes can exercise control flow without emitting resources.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        Chart: Small chart with nested values and a valid independent resource.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "control", "version": "1.0.0"}))
    defaults: dict[str, object] = {"enabled": True, "nested": {"mode": "bad"}, "items": ["first", "second"], "empty": []}
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: control
        """)
    )
    return Chart(tmp_path, {"type": "object"}, defaults)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    ("body", "rejected"),
    [
        ('{{ with .Values.nested }}{{ if and $.Values.enabled (eq .mode "bad") }}{{ fail "with root" }}{{ end }}{{ end }}', True),
        (
            '{{ with .Values.empty }}{{ fail "wrong branch" }}{{ else }}{{ if .Values.enabled }}{{ fail "empty with" }}{{ end }}{{ end }}',
            True,
        ),
        (
            '{{ with .Values.empty }}{{ fail "wrong" }}{{ else with .Values.nested }}'
            '{{ if eq .mode "bad" }}{{ fail "chain" }}{{ end }}{{ end }}',
            True,
        ),
        ('{{ $x := false }}{{ if .Values.enabled }}{{ $x = true }}{{ end }}{{ if $x }}{{ fail "assignment" }}{{ end }}', True),
        ('{{ $x := false }}{{ if .Values.enabled }}{{ $x := true }}{{ end }}{{ if $x }}{{ fail "shadow leaked" }}{{ end }}', False),
        ('{{ $x := false }}{{ with $x = .Values.enabled }}{{ end }}{{ if $x }}{{ fail "with assignment" }}{{ end }}', True),
        ('{{ if $x := .Values.empty }}{{ fail "wrong" }}{{ else }}{{ if not $x }}{{ fail "else scope" }}{{ end }}{{ end }}', True),
        ('{{ range $i, $v := .Values.items }}{{ if and (eq $i 1) (eq $v "second") }}{{ fail "indexed" }}{{ end }}{{ end }}', True),
        ('{{ range .Values.items }}{{ if and $.Values.enabled (eq . "second") }}{{ fail "dot" }}{{ end }}{{ end }}', True),
        ('{{ range .Values.empty }}{{ fail "wrong" }}{{ else }}{{ if .Values.enabled }}{{ fail "range else" }}{{ end }}{{ end }}', True),
        ('{{ $x := "" }}{{ range $v := .Values.items }}{{ $x = $v }}{{ end }}{{ if eq $x "second" }}{{ fail "last" }}{{ end }}', True),
        ('{{ $x := "" }}{{ range $x = .Values.items }}{{ end }}{{ if eq $x "second" }}{{ fail "assigned iterator" }}{{ end }}', True),
        ('{{ range .Values.items }}{{ break }}{{ fail "unreachable" }}{{ end }}', False),
        ('{{ range .Values.items }}{{ continue }}{{ fail "unreachable" }}{{ end }}', False),
        (
            "{{ range .Values.items }}{{ range $.Values.items }}{{ break }}{{ end }}"
            '{{ if eq . "second" }}{{ fail "outer continues" }}{{ end }}{{ end }}',
            True,
        ),
        ('{{ range $k, $v := dict "z" "last" "a" "first" }}{{ if eq $k "a" }}{{ break }}{{ end }}{{ fail "wrong order" }}{{ end }}', False),
        ('{{ template "reject" .Values.nested }}', True),
        ('{{ template "empty" }}', True),
        ('{{ block "local" .Values.nested }}{{ if eq $.mode "bad" }}{{ fail "block root" }}{{ end }}{{ end }}', True),
        ('{{ if ne (len .Values.items) 1 }}{{ fail "cardinality" }}{{ end }}', True),
        ('{{ if eq (len "é") 2 }}{{ fail "utf8 bytes" }}{{ end }}', True),
        ('{{ template "length" .Values.items | len }}', True),
        ('{{ include "messages" . | fail }}', True),
    ],
)
def test_control_flow_matches_helm(control_chart: Chart, body: str, rejected: bool) -> None:
    """
    Check predictions, rejection text, branch selection and native success together.

    Args:
        control_chart (Chart): Valid fixture with independent manifest output.
        body (str): Go-template control-flow example.
        rejected (bool): Whether the selected configuration reaches an explicit rejection.

    Returns:
        None: Predictions agree with Helm for each tested scope and loop rule.
    """
    (control_chart.path / "templates/NOTES.txt").write_text(body)
    (control_chart.path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{ define "reject" }}
        {{ with .mode }}{{ if eq $.mode . }}{{ end }}{{ end }}
        {{ if eq $.mode "bad" }}{{ fail "helper root" }}{{ end }}{{ end }}
        {{ define "empty" }}{{ if not . }}{{ fail "nil context" }}{{ end }}{{ end }}
        {{ define "length" }}{{ if eq . 2 }}{{ fail "argument pipeline" }}{{ end }}{{ end }}
        {{ define "messages" }}{{ range .Values.items }}before{{ if eq . "first" }}{{ continue }}{{ end }}after{{ break }}{{ end }}{{ end }}
        """)
    )
    rejection = Contracts.build(control_chart.path).predict(control_chart.defaults)
    assert (rejection is not None) is rejected
    if rejected:
        assert rejection is not None
        with pytest.raises(RenderFailure) as failure:
            render(control_chart, {})
        assert matches_rejection(str(failure.value), rejection)
    else:
        render(control_chart, {})


@pytest.mark.parametrize(
    "body",
    [
        '{{ $x := false }}{{ if true }}{{ $x := tpl "{{ now }}" . }}{{ if $x }}{{ fail "unknown shadow" }}{{ end }}{{ end }}',
        '{{ range keys (dict "a" 1 "b" 2) }}{{ fail "unordered" }}{{ end }}',
        '{{ range .Values.items }}{{ fail "oversized" }}{{ end }}',
        '{{ block "ambiguous" . }}{{ fail "one" }}{{ end }}',
    ],
)
def test_unsupported_control_flow_stays_unknown(control_chart: Chart, body: str) -> None:
    """
    Refuse guesses after unknown assignments, mutation, ambiguous blocks and work limits.

    Args:
        control_chart (Chart): Chart with replaceable note and helper sources.
        body (str): Unsupported or bounded-out contract.

    Returns:
        None: Unsupported behavior cannot authorize pruning.
    """
    (control_chart.path / "templates/NOTES.txt").write_text(body)
    (control_chart.path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{ define "mutate" }}{{ $_ := set .Values "enabled" false }}{{ end }}
        {{ define "ambiguous" }}{{ fail "two" }}{{ end }}
        """)
    )
    assert Contracts.build(control_chart.path).predict({**control_chart.defaults, "items": ["x"] * 4097}) is None


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_joint_repair_keeps_enabled_branch_and_authored_failures(control_chart: Chart) -> None:
    """
    Supply two jointly required fields without changing the selected activation flag.

    Args:
        control_chart (Chart): Renderable chart shell with mutable defaults.

    Returns:
        None: Inferred fields receive a tested joint candidate; authored contradictions stay findings.
    """
    import json

    from hypothesis import strategies as st

    from hypothesis_helm.charts.runner import check_chart
    from hypothesis_helm.schemas.contracts import mapping

    control_chart.defaults.update(enabled=False, repository="", branch="")
    (control_chart.path / "values.yaml").write_text(yamlio.dump(control_chart.defaults))
    (control_chart.path / "templates/NOTES.txt").write_text(
        dedent("""
        {{ if and .Values.enabled (or (not .Values.repository) (not .Values.branch)) }}
        {{ fail "enabled cloning needs repository and branch" }}
        {{ end }}
        """)
    )
    candidate = {**control_chart.defaults, "enabled": True}
    report = check_chart(
        control_chart, input_strategy=st.just(candidate), max_examples=1, filter_rejections=True, protected_paths=(("enabled",),)
    )
    assert report["status"] == "passed", report
    evidence = mapping(report["configuration_rejections"])
    assert evidence["adjusted_candidates"] == 1 and evidence["verification_renders"] == 1
    schema: dict[str, object] = {
        "type": "object",
        "properties": {"enabled": {"type": "boolean"}, "repository": {"type": "string"}, "branch": {"type": "string"}},
    }
    (control_chart.path / "values.schema.json").write_text(json.dumps(schema))
    control_chart.schema = schema
    report = check_chart(
        control_chart, input_strategy=st.just(candidate), max_examples=1, filter_rejections=True, protected_paths=(("enabled",),)
    )
    assert report["status"] == "failed", report
    assert int(str(mapping(report["configuration_rejections"])["schema_conflicts"])) > 0
