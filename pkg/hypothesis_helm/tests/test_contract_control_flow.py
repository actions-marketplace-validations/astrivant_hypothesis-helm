"""
Compare lexical control-flow predictions with native Helm execution.
"""

import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.rendering import RenderFailure, render
from hypothesis_helm.compiler.asts.contract_values import BoundValue
from hypothesis_helm.compiler.asts.contracts import Contracts, Evaluation, FieldAccess, Unknown, calls, expression
from hypothesis_helm.compiler.passes.dependencies import Dependencies
from hypothesis_helm.compiler.passes.rejections import RejectionPolicy, matches_rejection
from hypothesis_helm.schemas.contracts import mapping


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
        ('{{ if eq ((.Values).nested).mode "bad" }}{{ fail "parenthesized input" }}{{ end }}', True),
        ('{{ if eq (dict "mode" .Values.nested.mode).mode "bad" }}{{ fail "dictionary field" }}{{ end }}', True),
        ('{{ $v := .Values }}{{ if eq (($v.nested).mode) "bad" }}{{ fail "alias field" }}{{ end }}', True),
        ('{{ if eq (.Values.nested).mode "good" }}{{ fail "wrong branch" }}{{ end }}', False),
        ('{{ with (.Values).nested }}{{ if eq (.).mode "bad" }}{{ fail "nested dot" }}{{ end }}{{ end }}', True),
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


def test_parenthesized_selectors_preserve_calls_and_argument_boundaries() -> None:
    """
    Distinguish adjacent field selectors from a separate dot argument and retain nested effects.

    Returns:
        None: Selectors keep their receiver calls visible to rejection and mutation analysis.
    """
    selected = expression("(($context.Values.global).imagePullSecrets)")
    assert selected == FieldAccess("$context.Values.global", ("imagePullSecrets",))
    assert expression("(.Values.nested) .mode") == (".Values.nested", ".mode")
    assert calls(expression('(dict "data" (include "validate" .)).data')) == {"dict", "include", "include:validate"}
    assert "set" in calls(expression('(set .Values "mode" "bad").mode'))


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_unresolved_aliases_keep_the_original_diagnostic(control_chart: Chart, caplog: pytest.LogCaptureFixture) -> None:
    """
    Report one unsupported helper operation instead of cascading errors for every variable use.

    Args:
        control_chart (Chart): Chart with repeated uses of one helper-derived value.
        caplog (pytest.LogCaptureFixture): Captured compiler warning messages.

    Returns:
        None: Alias chains retain the cause; native rendering and independent rejection checks still run.
    """
    (control_chart.path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{ define "opaque" }}{{ .Values.nested | toYaml }}{{ end }}
        {{ define "consume" }}{{ tpl .value .context }}{{ end }}
        """)
    )
    (control_chart.path / "templates/NOTES.txt").write_text(
        dedent("""
        {{ $labels := include "opaque" . }}
        {{ include "consume" (dict "value" $labels "context" $) }}
        {{ $alias := $labels }}
        {{ include "consume" (dict "value" $alias "context" $) }}
        {{ include "consume" (dict "value" $labels "context" $) }}
        {{ if not .Values.enabled }}{{ fail "independent rejection" }}{{ end }}
        """)
    )
    contracts = Contracts.build(control_chart.path)
    assert contracts.predict(control_chart.defaults) is None
    assert len(contracts.fallbacks) == 1
    assert contracts.fallbacks[0]["source"] == "templates/_helpers.tpl"
    assert contracts.fallbacks[0]["reason"] == "unsupported function: toYaml"
    assert caplog.text.count("[HH2007]") == 1
    assert "unbound" not in caplog.text
    render(control_chart, {})
    rejection = contracts.predict({**control_chart.defaults, "enabled": False})
    assert rejection is not None and rejection.contextual
    with pytest.raises(RenderFailure) as failure:
        render(control_chart, {"enabled": False})
    assert matches_rejection(str(failure.value), rejection)
    assert len(contracts.fallbacks) == 1
    contracts.fail_fast = True
    with pytest.raises(RenderFailure, match="HH2007"):
        contracts.predict(control_chart.defaults)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("access", ["(.Values.global).mode", 'get .Values.global "mode"', 'index .Values.global "mode"'])
@pytest.mark.parametrize("owner", ["root", "parent", "child"])
def test_forwarded_global_origins_match_helm(control_chart: Chart, access: str, owner: str) -> None:
    """
    Trace scalar globals through nested aliased dependencies while preserving native verification.

    Args:
        control_chart (Chart): Root chart receiving two nested child charts.
        access (str): Equivalent direct or indexed global field access.
        owner (str): Highest-priority ancestor providing the rejecting field.

    Returns:
        None: Predicted evidence names the supplying input and Helm confirms each tested precedence case.
    """
    root = control_chart.path
    parent = root / "charts/database"
    child = parent / "charts/leaf"
    for path, name, dependency in ((root, "control", "database"), (parent, "database", "leaf"), (child, "leaf", None)):
        (path / "templates").mkdir(parents=True, exist_ok=True)
        metadata: dict[str, object] = {"apiVersion": "v2", "name": name, "version": "1.0.0"}
        if dependency:
            metadata["dependencies"] = [{"name": dependency, "alias": "db" if dependency == "database" else "worker", "version": "1.0.0"}]
        (path / "Chart.yaml").write_text(yamlio.dump(metadata))
        if path != root:
            defaults = {"global": {"mode": "good"}} if path == child else {"global": {"parentOnly": "retained"}}
            (path / "values.yaml").write_text(yamlio.dump(defaults))
    candidate: dict[str, object] = {
        "global": {"rootOnly": "retained"},
        "db": {"global": {"parentOnly": "retained"}, "worker": {"global": {"mode": "bad"}}},
    }
    if owner == "root":
        candidate["global"] = {"mode": "bad"}
    elif owner == "parent":
        candidate["db"] = {"global": {"mode": "bad"}, "worker": {"global": {"mode": "good"}}}
    (root / "values.yaml").write_text(yamlio.dump(candidate))
    (child / "templates/NOTES.txt").write_text(
        "{{ $value := " + access + ' }}{{ if not (has $value (list "good")) }}{{ fail "invalid global mode" }}{{ end }}'
    )
    chart = Chart(root, {"type": "object"}, candidate)
    contracts = Contracts.build(root)
    rejection = contracts.predict(candidate)
    assert rejection is not None, contracts.fallbacks
    source = {"root": "$.global.mode", "parent": "$.db.global.mode", "child": "$.db.worker.global.mode"}[owner]
    assert rejection.enums == {source: ("good",)}
    assert rejection.inputs[source] == "bad"
    assert not contracts.fallbacks
    assert rejection.contextual
    policy = RejectionPolicy(contracts, candidate)
    policy.witnesses[rejection.key] = {"first", "second"}
    assert policy.needs_probe(rejection, candidate)
    with pytest.raises(RenderFailure) as failure:
        render(chart, {})
    assert matches_rejection(str(failure.value), rejection)
    render(chart, {"global": {"mode": "good"}})
    (child / "values.schema.json").write_text(
        json.dumps({"type": "object", "properties": {"global": {"type": "object", "properties": {"mode": {"type": "string"}}}}})
    )
    authored = Contracts.build(root).predict(candidate)
    assert authored is not None and authored.declared_schema


def test_unbound_helper_variables_still_report_their_name(control_chart: Chart) -> None:
    """
    Keep real scope violations visible rather than hiding them as previously diagnosed aliases.

    Args:
        control_chart (Chart): Chart with a helper attempting to use a caller-local variable.

    Returns:
        None: Fresh helper scope rejects the leaked binding and reports the variable name.
    """
    (control_chart.path / "templates/NOTES.txt").write_text('{{ $caller := "bad" }}{{ include "reject" . }}')
    (control_chart.path / "templates/_helpers.tpl").write_text(
        '{{ define "reject" }}{{ if eq $caller "bad" }}{{ fail "leaked caller scope" }}{{ end }}{{ end }}'
    )
    contracts = Contracts.build(control_chart.path)
    assert contracts.predict(control_chart.defaults) is None
    assert [row["reason"] for row in contracts.fallbacks] == ["unbound variable: $caller"]


def test_incompatible_global_origins_stay_unknown(control_chart: Chart) -> None:
    """
    Decline global provenance when an ancestor map disagrees with the selected child value.

    Args:
        control_chart (Chart): Root receiving a locally installed dependency.

    Returns:
        None: Mixed container shapes and absent origins cannot establish a pruning proof.
    """
    child = control_chart.path / "charts/child"
    child.mkdir(parents=True)
    (child / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "child", "version": "1.0.0"}))
    (child / "values.yaml").write_text("{}")
    contracts = Contracts(dependencies=Dependencies.build(control_chart.path))
    for globals in ({"nested": "wrong shape"}, {"nested": {"mode": "different"}}, {}):
        evaluator = Evaluation(contracts, {"global": globals})
        with pytest.raises(Unknown):
            evaluator.observe(BoundValue("bad", ("child", "global", "nested", "mode")))
        assert not evaluator.inputs


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_airflow_contract_warnings_resolve_causes(tmp_path: Path) -> None:
    """
    Exercise the reported PostgreSQL and common-helper expressions in their real dependency context.

    Args:
        tmp_path (Path): Isolated chart with locally copied dependencies.

    Returns:
        None: Original cascade and global-method warnings disappear while unsupported operations stay explicit.
    """
    source = Path(__file__).resolve().parents[3] / "third_party/bitnami-charts/bitnami"
    if not all((source / name / "Chart.yaml").is_file() for name in ("airflow", "common", "postgresql", "redis")):
        pytest.skip("requires the pinned Bitnami submodule")
    chart = tmp_path / "airflow"
    shutil.copytree(source / "airflow", chart, ignore=shutil.ignore_patterns("charts"))
    for name in ("common", "postgresql", "redis"):
        shutil.copytree(source / name, chart / "charts" / name, ignore=shutil.ignore_patterns("charts"))
    for name in ("postgresql", "redis"):
        shutil.copytree(source / "common", chart / "charts" / name / "charts/common")
    values = mapping(yamlio.load((chart / "values.yaml").read_text()))
    contracts = Contracts.build(chart)
    assert contracts.predict(values) is None
    assert contracts.fallbacks  # Unsupported helpers remain visible instead of being silently accepted.
    assert not any("unbound" in str(row["reason"]) or "unresolved variable" in str(row["reason"]) for row in contracts.fallbacks)
    assert not any("unsupported context method: global" == row["reason"] for row in contracts.fallbacks)
    assert not any("forwarded global input origins are unresolved" == row["reason"] for row in contracts.fallbacks)
    render(Chart(chart, {"type": "object"}, values), {})


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
