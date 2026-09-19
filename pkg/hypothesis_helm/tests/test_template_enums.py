"""
Verify source-backed allowlists, helper scopes, and native Helm rejection witnesses.
"""

import itertools
import json
import shutil
import tarfile
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import strategies as st

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.runner import RenderFailure, check_chart, render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.contracts import Contracts, declares_path
from hypothesis_helm.compiler.passes.rejections import RejectionPolicy, matches_rejection
from hypothesis_helm.schemas.contracts import mapping


@pytest.fixture
def preset_chart(tmp_path: Path) -> Chart:
    """
    Create a chart with a conditional, dictionary-backed resource preset helper.

    Args:
        tmp_path (Path): Isolated fixture directory.

    Returns:
        Chart: Valid defaults and an enum contract behind optional configuration branches.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "preset", "version": "1.0.0"}))
    defaults: dict[str, object] = {"enabled": True, "resources": {}, "preset": "none"}
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "preset.resources" -}}
        {{- $presets := dict "nano" (dict "cpu" "100m") "small" (dict "cpu" "500m") "large" (dict "cpu" "1") -}}
        {{- if hasKey $presets .type -}}
        {{- index $presets .type | toYaml -}}
        {{- else -}}
        {{- printf "ERROR: Preset key '%s' invalid. Allowed values are %s" .type (join "," (keys $presets)) | fail -}}
        {{- end -}}
        {{- end -}}
        """)
    )
    (tmp_path / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: preset
        data:
          status: ready
        {{- if .Values.enabled }}
        {{- if .Values.resources }}
          custom: "true"
        {{- else if ne .Values.preset "none" }}
          selected: {{ include "preset.resources" (dict "type" .Values.preset) | quote }}
        {{- end }}
        {{- end }}
        """)
    )
    return Chart(tmp_path, {"type": "object"}, defaults)


def test_map_enum_guards_and_message_order(preset_chart: Chart) -> None:
    """
    Recover an allowlist only on its rejecting branch and verify every key exactly once.

    Args:
        preset_chart (Chart): Conditional map-backed preset fixture.

    Returns:
        None: Bypassed presets stay unrestricted and message matching tolerates only key order.
    """
    contracts = Contracts.build(preset_chart.path)
    invalid = {**preset_chart.defaults, "preset": "invalid"}
    rejection = contracts.predict(invalid)
    assert rejection is not None
    assert rejection.enums == {"$.preset": ("large", "nano", "small")}
    for overrides in ({"enabled": False}, {"resources": {"cpu": "2"}}, {"preset": "none"}):
        assert contracts.predict({**invalid, **overrides}) is None
    prefix = "Error: execution error at (preset/templates/config.yaml:13:27): ERROR: Preset key 'invalid' invalid. Allowed values are "
    for order in itertools.permutations(("large", "nano", "small")):
        assert matches_rejection(prefix + ",".join(order), rejection)
    assert not matches_rejection(prefix + "large,nano,nano", rejection)
    assert not matches_rejection(prefix + "large,nano,small,extra", rejection)
    assert not matches_rejection(prefix.replace("'invalid'", "'different'") + "large,nano,small", rejection)
    another = contracts.predict({**invalid, "preset": "another"})
    assert another is not None and another.key == rejection.key


@pytest.mark.parametrize("membership", ["has", "mustHas"])
def test_literal_lists_nested_arguments_and_aliases(preset_chart: Chart, membership: str) -> None:
    """
    Follow nested dictionary contexts and local aliases into literal-list membership.

    Args:
        preset_chart (Chart): Chart whose helper and caller are replaced for this pattern.
        membership (str): Supported Sprig list membership function.

    Returns:
        None: Helper-local dollar refers to the argument map and provenance retains the input path.
    """
    (preset_chart.path / "templates/_helpers.tpl").write_text(
        dedent(f"""
        {{{{- define "preset.resources" -}}}}
        {{{{- $allowed := list "small" "large" -}}}}
        {{{{- $selected := $.nested.type -}}}}
        {{{{- if not ({membership} $selected $allowed) -}}}}{{{{ fail "unsupported preset" }}}}{{{{- end -}}}}
        {{{{- end -}}}}
        """)
    )
    (preset_chart.path / "templates/config.yaml").write_text(
        dedent("""
        {{ $selected := .Values.preset }}
        {{ include "preset.resources" (dict "nested" (dict "type" $selected)) }}
        """)
    )
    contracts = Contracts.build(preset_chart.path)
    rejection = contracts.predict({"preset": "bad"})
    assert rejection is not None and rejection.enums == {"$.preset": ("large", "small")}
    assert contracts.predict({"preset": "small"}) is None


@pytest.mark.parametrize(
    "guard",
    [
        'hasKey (dict "small" true) (snakecase .type)',
        'eq (tpl "{{ now }}" $) "bad"',
    ],
)
def test_unsupported_expressions_remain_unknown(preset_chart: Chart, guard: str) -> None:
    """
    Retain ordinary testing when a guard needs unsupported transformations or dynamic templates.

    Args:
        preset_chart (Chart): Chart with a replaceable helper.
        guard (str): Guard whose semantics remain outside the supported contract subset.

    Returns:
        None: No rejection or inferred allowlist is claimed.
    """
    (preset_chart.path / "templates/_helpers.tpl").write_text(
        dedent(f"""
        {{{{- define "preset.resources" -}}}}
        {{{{- if {guard} -}}}}{{{{ fail "unknown semantics" }}}}{{{{- end -}}}}
        {{{{- end -}}}}
        """)
    )
    assert Contracts.build(preset_chart.path).predict({**preset_chart.defaults, "preset": "bad"}) is None


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_native_enum_guidance_and_schema_conflicts(preset_chart: Chart) -> None:
    """
    Verify rejection with Helm before choosing an enum member and preserve authored-schema failures.

    Args:
        preset_chart (Chart): Renderable chart with an explicit preset allowlist.

    Returns:
        None: Inferred inputs receive tested replacements; authored inputs still expose their contract conflict.
    """
    invalid = {**preset_chart.defaults, "preset": '*a"/?U'}
    rejection = Contracts.build(preset_chart.path).predict(invalid)
    assert rejection is not None
    with pytest.raises(RenderFailure) as failure:
        render(preset_chart, invalid)
    assert matches_rejection(str(failure.value), rejection)
    observed: list[dict[str, object]] = []
    report = check_chart(
        preset_chart,
        input_strategy=st.just(invalid),
        max_examples=1,
        filter_rejections=True,
        protected_paths=(("preset",),),
        properties=(lambda resources: observed.extend(resources),),
    )
    assert report["status"] == "passed", report
    evidence = mapping(report["configuration_rejections"])
    assert evidence["verification_renders"] == evidence["adjusted_candidates"] == 1
    assert evidence["classifier_disagreements"] == 0
    assert "selected" in mapping(observed[-1]["data"]), "Repair must exercise the preset, not disable its surrounding resource"
    (preset_chart.path / "values.schema.json").write_text(json.dumps({"type": "object", "properties": {"enabled": {"type": "boolean"}}}))
    report = check_chart(preset_chart, input_strategy=st.just(invalid), max_examples=1, filter_rejections=True)
    assert report["status"] == "passed", report
    assert mapping(report["configuration_rejections"])["adjusted_candidates"] == 1
    (preset_chart.path / "values.schema.json").write_text(json.dumps({"type": "object", "properties": {"preset": {"type": "string"}}}))
    report = check_chart(preset_chart, input_strategy=st.just(invalid), max_examples=1, filter_rejections=True)
    assert report["status"] == "failed"
    assert int(str(mapping(report["configuration_rejections"])["schema_conflicts"])) > 0


@pytest.mark.parametrize("archived", [False, True])
@pytest.mark.parametrize("declared", [False, True])
def test_aliased_dependency_contracts(preset_chart: Chart, tmp_path: Path, archived: bool, declared: bool) -> None:
    """
    Inspect dependency sources before temporary extraction ends and respect their activation controls.

    Args:
        preset_chart (Chart): Child chart with a helper-backed allowlist.
        tmp_path (Path): Parent chart and optional child archive destination.
        archived (bool): Package the child as a tgz instead of using an unpacked directory.
        declared (bool): Author the preset field in the child's own schema.

    Returns:
        None: Active aliases map to parent values paths; disabled children cannot reject parent inputs.
    """
    parent = tmp_path / "parent"
    (parent / "charts").mkdir(parents=True)
    metadata = {
        "apiVersion": "v2",
        "name": "parent",
        "version": "1.0.0",
        "dependencies": [{"name": "preset", "alias": "db", "version": "1.0.0", "condition": "db.active"}],
    }
    (parent / "Chart.yaml").write_text(yamlio.dump(metadata))
    names = ["Chart.yaml", "values.yaml"]
    if declared:
        (preset_chart.path / "values.schema.json").write_text(json.dumps({"type": "object", "properties": {"preset": {"type": "string"}}}))
        names.append("values.schema.json")
    if archived:
        with tarfile.open(parent / "charts/preset-1.0.0.tgz", "w:gz") as archive:
            for name in (*names, "templates"):
                archive.add(preset_chart.path / name, arcname="preset/" + name)
    else:
        child = parent / "charts/preset"
        child.mkdir()
        for name in names:
            shutil.copy2(preset_chart.path / name, child / name)
        shutil.copytree(preset_chart.path / "templates", child / "templates")
    contracts = Contracts.build(parent)
    invalid: dict[str, object] = {"db": {"active": True, "preset": "bad"}}
    rejection = contracts.predict(invalid)
    assert rejection is not None and rejection.enums == {"$.db.preset": ("large", "nano", "small")}
    assert rejection.declared_schema is declared
    assert contracts.predict({"db": {"active": False, "preset": "bad"}}) is None


@pytest.mark.parametrize(
    ("schema", "expected"),
    [
        ({"type": "object", "properties": {"unrelated": {"type": "boolean"}}}, False),
        ({"properties": {"preset": {"type": "string"}}}, True),
        ({"properties": {"preset": {}}}, True),
        ({"additionalProperties": {"type": "string"}}, True),
        ({"additionalProperties": False}, True),
        ({"patternProperties": {".*": {"type": "string"}}}, True),
        ({"allOf": [{"properties": {"preset": {"enum": ["bad"]}}}]}, True),
        ({"$ref": "#/definitions/preset"}, True),
        ({"enum": [{"preset": "bad"}]}, True),
    ],
)
def test_authored_domain_boundaries(schema: dict[str, object], expected: bool) -> None:
    """
    Guide only omitted fields and conservatively preserve unresolved schema relationships.

    Args:
        schema (dict[str, object]): Original partial or composed values schema.
        expected (bool): Whether this schema must prevent automatic enum replacement.

    Returns:
        None: Open omitted fields differ from authored and ambiguous domains.
    """
    assert declares_path(schema, ("preset",)) is expected


@pytest.mark.parametrize("access", ['index .Values "preset"', 'get .Values "preset"'])
def test_indexed_input_provenance(preset_chart: Chart, access: str) -> None:
    """
    Retain direct values provenance across supported map lookup calls.

    Args:
        preset_chart (Chart): Literal preset helper fixture.
        access (str): Supported lookup passed as the helper argument.

    Returns:
        None: The inferred choices refer to the actual input path.
    """
    (preset_chart.path / "templates/config.yaml").write_text('{{ include "preset.resources" (dict "type" (' + access + ")) }}")
    rejection = Contracts.build(preset_chart.path).predict({"preset": "bad"})
    assert rejection is not None and "$.preset" in rejection.enums


def test_candidate_defined_choices_are_not_static_enums(preset_chart: Chart) -> None:
    """
    Refuse to treat candidate-supplied map keys as template-authored enum constants.

    Args:
        preset_chart (Chart): Fixture receiving a dynamic allowed map.

    Returns:
        None: An explicit rejection can be predicted without inventing a fixed enum.
    """
    (preset_chart.path / "templates/config.yaml").write_text(
        '{{ if not (hasKey .Values.allowed .Values.preset) }}{{ fail "unsupported preset" }}{{ end }}'
    )
    rejection = Contracts.build(preset_chart.path).predict({"preset": "bad", "allowed": {"small": {}}})
    assert rejection is not None and not rejection.enums


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_finite_enum_assignments_are_not_repaired(preset_chart: Chart) -> None:
    """
    Keep finite-plan assignments fixed even when a supported enum replacement exists.

    Args:
        preset_chart (Chart): Fixture with one explicit invalid alternative to its defaults.

    Returns:
        None: Rejected assignments are counted separately and never replaced or marked successful.
    """
    preset_chart.schema = {"enum": [preset_chart.defaults, {**preset_chart.defaults, "preset": "bad"}]}
    report = check_chart(preset_chart, exhaustive=True, filter_rejections=True)
    evidence = mapping(report["configuration_rejections"])
    assert evidence["filtered_candidates"] == 1 and evidence["adjusted_candidates"] == 0
    assert report["remaining_iterations"] == 0 and not report["coverage_complete"]


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_bitnami_resource_helper(preset_chart: Chart) -> None:
    """
    Validate the retained Bitnami helper source without needing a repository scan or network access.

    Args:
        preset_chart (Chart): Isolated chart shell using the real common resource helper.

    Returns:
        None: The full preset map yields a matching native rejection and a tested resource choice.
    """
    source = Path(__file__).resolve().parents[3] / "third_party/bitnami-charts/bitnami/common/templates/_resources.tpl"
    if not source.is_file():
        pytest.skip("Bitnami submodule is not present")
    (preset_chart.path / "templates/_helpers.tpl").write_text(source.read_text())
    template = preset_chart.path / "templates/config.yaml"
    template.write_text(template.read_text().replace('"preset.resources"', '"common.resources.preset"'))
    invalid = {**preset_chart.defaults, "preset": '*a"/?U'}
    rejection = Contracts.build(preset_chart.path).predict(invalid)
    assert rejection is not None
    assert rejection.enums == {"$.preset": ("2xlarge", "large", "medium", "micro", "nano", "small", "xlarge")}
    with pytest.raises(RenderFailure) as failure:
        render(preset_chart, invalid)
    assert matches_rejection(str(failure.value), rejection)
    report = check_chart(
        preset_chart, input_strategy=st.just(invalid), max_examples=1, filter_rejections=True, protected_paths=(("preset",),)
    )
    assert report["status"] == "passed", report
    assert mapping(report["configuration_rejections"])["adjusted_candidates"] == 1


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_postgresql_partial_schema_and_ordered_effects(tmp_path: Path) -> None:
    """
    Reproduce the actual backup preset failure under PostgreSQL's partial authored schema.

    Args:
        tmp_path (Path): Isolated chart copy and installed local common dependency.

    Returns:
        None: Quoted scalars and later dynamic output do not hide the earlier verified enum contract.
    """
    source = Path(__file__).resolve().parents[3] / "third_party/bitnami-charts/bitnami"
    if not (source / "postgresql/Chart.yaml").is_file():
        pytest.skip("Bitnami submodule is not present")
    destination = tmp_path / "postgresql"
    shutil.copytree(source / "postgresql", destination, ignore=shutil.ignore_patterns("charts"))
    shutil.copytree(source / "common", destination / "charts/common")
    chart = Chart.load(destination)
    invalid = mapping(yamlio.load((destination / "values.yaml").read_text()))
    mapping(invalid["backup"])["enabled"] = True
    mapping(mapping(invalid["backup"])["cronjob"])["resourcesPreset"] = '*a"/?U'
    rejection = Contracts.build(destination).predict(invalid)
    assert rejection is not None and not rejection.declared_schema
    assert set(rejection.enums) == {"$.backup.cronjob.resourcesPreset"}
    with pytest.raises(RenderFailure) as failure:
        render(chart, invalid)
    assert matches_rejection(str(failure.value), rejection)
    report = check_chart(
        chart,
        input_strategy=st.just(invalid),
        max_examples=1,
        filter_rejections=True,
        protected_paths=(("backup", "cronjob", "resourcesPreset"),),
    )
    assert report["status"] == "passed", report
    assert mapping(report["configuration_rejections"])["adjusted_candidates"] == 1


@pytest.mark.parametrize("before", [False, True])
def test_effects_before_and_after_rejections(preset_chart: Chart, before: bool) -> None:
    """
    Refuse context mutations before a rejection while permitting unreachable later operations.

    Args:
        preset_chart (Chart): Supported helper fixture.
        before (bool): Place the mutation before the rejection instead of after it.

    Returns:
        None: Statement ordering cannot turn an unsupported earlier effect into a proved allowlist.
    """
    template = preset_chart.path / "templates/config.yaml"
    operation = '{{ $_ := set .Values "preset" "none" }}'
    template.write_text(operation + template.read_text() if before else template.read_text() + operation)
    rejection = Contracts.build(preset_chart.path).predict({**preset_chart.defaults, "preset": "bad"})
    assert (rejection is None) is before


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_enum_witnesses_never_hide_a_later_native_disagreement(preset_chart: Chart) -> None:
    """
    Verify every enum rejection even after two earlier witnesses established its source identity.

    Args:
        preset_chart (Chart): Fixture with an earlier unrelated failure for a third invalid value.

    Returns:
        None: The unrelated error remains a finding and disables the contradicted classifier.
    """
    template = preset_chart.path / "templates/config.yaml"
    template.write_text('{{ if eq .Values.preset "bad3" }}{{ .Values.missing.parent }}{{ end }}' + template.read_text())
    policy = RejectionPolicy(Contracts.build(preset_chart.path), preset_chart.defaults)
    for name in ("bad1", "bad2"):
        invalid = {**preset_chart.defaults, "preset": name}
        rejection = policy.predict(invalid)
        assert rejection is not None
        with pytest.raises(RenderFailure) as failure:
            render(preset_chart, invalid)
        assert matches_rejection(str(failure.value), rejection)
        policy.verified(rejection, invalid)
    report = check_chart(
        preset_chart,
        input_strategy=st.just({**preset_chart.defaults, "preset": "bad3"}),
        max_examples=1,
        rejection_policy=policy,
        fail_fast=True,
    )
    assert report["status"] == "failed" and "nil pointer" in str(report["error"])
    evidence = mapping(report["configuration_rejections"])
    assert evidence["classifier_disagreements"] == 1 and evidence["adjusted_candidates"] == 0
