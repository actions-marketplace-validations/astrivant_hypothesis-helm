"""
Propagate structural destination constraints through serialized YAML fragments.
"""

import copy
import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import given, settings
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.domain_fragments import contribution, literal_region
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import json_value, mapping, schema_strategy
from hypothesis_helm.schemas.policy import ENVIRONMENT


@pytest.fixture
def fragment_chart(tmp_path: Path) -> Chart:
    """
    Create an arbitrary helper that serializes structured inputs and renders templated strings.

    Args:
        tmp_path (Path): Destination for the isolated chart.

    Returns:
        Chart: NetworkPolicy accepting either structured fragments or raw YAML strings.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "fragments", "version": "1.0.0"}))
    schema: dict[str, object] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["enabled", "rules", "legacy"],
        "properties": {"enabled": {"type": "boolean"}, "rules": {}, "legacy": {}},
    }
    defaults: dict[str, object] = {"enabled": True, "rules": [], "legacy": []}
    (tmp_path / "values.schema.json").write_text(json.dumps(schema))
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
            {{- define "render.fragment" -}}
            {{- $text := typeIs "string" .value | ternary .value (.value | toYaml) -}}
            {{- if contains "{{" (toJson .value) -}}
            {{- tpl $text .context -}}
            {{- else -}}{{- $text -}}{{- end -}}
            {{- end -}}
            """)
    )
    (tmp_path / "templates/policy.yaml").write_text(
        dedent("""
            {{ if .Values.enabled }}
            apiVersion: networking.k8s.io/v1
            kind: NetworkPolicy
            metadata:
              name: fragments
            spec:
              podSelector: {}
              policyTypes: [Ingress]
              ingress:
                - ports:
                    - port: 80
                {{- $rules := coalesce .Values.rules .Values.legacy }}
                {{- if $rules }}
                {{- include "render.fragment" (dict "value" $rules "context" $) | nindent 4 }}
                {{- end }}
            {{ end }}
            """)
    )
    return Chart(tmp_path, schema, defaults)


def test_fragment_constraints_preserve_fallbacks_strings_and_unknown_tpl(fragment_chart: Chart) -> None:
    """
    Constrain selected literal structures without coercing strings or guessing dynamic template behavior.

    Args:
        fragment_chart (Chart): Chart inserting a conditional fragment after an existing list item.

    Returns:
        None: Wrong structures are excluded only when literal serialization and activation are established.
    """
    schema = fragment_chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    valid: list[object] = [[], [{"ports": [{"port": 8080}]}], [{"from": []}], "- ports: [{port: 8080}]", '{{ "- {}" }}']
    invalid: list[object] = [{"": None}, [42], [{"ports": 7}], ["bad"]]
    for field in ("rules", "legacy"):
        for value in valid + invalid:
            candidate = {**fragment_chart.defaults, field: value}
            assert validator.is_valid(json_value(candidate)) == (value in valid), (field, value)
            assert validator.is_valid(json_value({**candidate, "enabled": False}))
    assert validator.is_valid(json_value({**fragment_chart.defaults, "rules": [{}], "legacy": {"": None}}))
    for unknown in ({"{{ something }}": None}, {"key": "{{ something }}"}):
        assert validator.is_valid(json_value({**fragment_chart.defaults, "rules": unknown}))
    assert any(rule.get("literal_fragment") for rule in fragment_chart.input_domains().rules)


def test_fragment_depth_budget_leaves_deeper_inputs_for_helm(fragment_chart: Chart, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Respect configurable literal inspection depth without rejecting candidates outside the proof region.

    Args:
        fragment_chart (Chart): Chart with a serialized fragment destination.
        monkeypatch (pytest.MonkeyPatch): Restore compiler settings after the test.

    Returns:
        None: A deeper invalid fragment stays eligible when its literal structure exceeds the configured budget.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"compiler": {"max_fragment_depth": 1}}))
    refresh_env()
    schema = fragment_chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert not validator.is_valid(json_value({**fragment_chart.defaults, "rules": {"": None}}))
    assert validator.is_valid(json_value({**fragment_chart.defaults, "rules": [{"ports": 7}]}))
    region = literal_region(100000, 32)
    assert len(json.dumps(region)) < 3000


def test_authored_fragment_type_conflict_is_reported(fragment_chart: Chart) -> None:
    """
    Preserve a conflicting authored schema instead of silently replacing its declared fragment type.

    Args:
        fragment_chart (Chart): Chart whose source contract will explicitly require an object.

    Returns:
        None: The conflict stays visible and the authored input remains eligible for native validation.
    """
    mapping(fragment_chart.schema["properties"])["rules"] = {"type": "object"}
    (fragment_chart.path / "values.schema.json").write_text(json.dumps(fragment_chart.schema))
    schema = fragment_chart.generation_schema()
    assert validators.validator_for(schema)(schema).is_valid(json_value({**fragment_chart.defaults, "rules": {"": None}}))
    assert any("conflict" in str(note) and note.get("path") == ["rules"] for note in fragment_chart.input_domains().diagnostics)


def test_fragment_domain_is_usable_by_hypothesis(fragment_chart: Chart) -> None:
    """
    Exercise generated strategies rather than only checking the resulting schema with a validator.

    Args:
        fragment_chart (Chart): Chart whose rules include a bounded no-template guard.

    Returns:
        None: Hypothesis can generate schema-valid cases from the conditional fragment constraints.
    """
    schema = fragment_chart.generation_schema()
    properties = mapping(schema["properties"])
    properties["enabled"] = {"const": True}
    properties["rules"] = {"enum": [{"": None}, [], [{"ports": [{"port": 8080}]}]]}
    properties["legacy"] = {"const": []}
    validator = validators.validator_for(schema)(schema)

    @given(schema_strategy(schema))
    @settings(max_examples=10, deadline=None, derandomize=True)
    def check(value: object) -> None:
        """
        Validate each generated case against its complete domain.

        Args:
            value (object): Generated chart input.

        Returns:
            None: Generated cases honor the guarded constraints.
        """
        assert validator.is_valid(json_value(value))

    check()


def test_fragment_keeps_item_requirements_without_whole_container_requirements() -> None:
    """
    Check partial contributions independently of fields and items supplied by surrounding template text.

    Returns:
        None: Whole-container requirements are relaxed, while nested item and field contracts remain intact.
    """
    item: dict[str, object] = {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}
    original: dict[str, object] = {"type": "array", "minItems": 2, "items": item}
    partial = contribution(original)
    validator = validators.validator_for(partial)(partial)
    assert validator.is_valid([{"name": "second"}])
    assert not validator.is_valid([{}])
    assert original["minItems"] == 2
    original = {
        "type": "object",
        "allOf": [{"required": ["suppliedByTemplate"]}],
        "oneOf": [{"required": ["first"]}, {"required": ["second"]}],
        "properties": {"added": item},
    }
    partial = contribution(original)
    validator = validators.validator_for(partial)(partial)
    assert validator.is_valid({"added": {"name": "part"}})
    assert not validator.is_valid({"added": {}})


@pytest.mark.parametrize(
    "positional",
    [
        {"items": [{"type": "string"}, {"type": "integer"}], "additionalItems": False},
        {"prefixItems": [{"type": "string"}], "items": {"type": "integer"}},
    ],
)
def test_fragment_does_not_guess_array_offset(positional: dict[str, object]) -> None:
    """
    Leave position-specific validation to the assembled array rather than assuming the fragment starts at index zero.

    Args:
        positional (dict[str, object]): Tuple or prefix-and-tail array contract.

    Returns:
        None: Either possible item type remains eligible when the template determines its position.
    """
    partial = contribution({"type": "array", **positional})
    validator = validators.validator_for(partial)(partial)
    assert validator.is_valid([1])
    assert validator.is_valid(["first"])


def test_closed_fragment_schema_preserves_yaml_strings(fragment_chart: Chart, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Avoid applying an array input type to a string that the helper inserts as YAML text.

    Args:
        fragment_chart (Chart): Chart emitting both structured and textual fragment representations.
        monkeypatch (pytest.MonkeyPatch): Restore the supplied output contract after the test.

    Returns:
        None: Structured inputs receive closed item contracts while YAML strings retain their original input type.
    """
    resource: dict[str, object] = {
        "type": "object",
        "properties": {
            "spec": {
                "type": "object",
                "properties": {"ingress": {"type": "array", "minItems": 2, "items": {"type": "object", "additionalProperties": False}}},
            }
        },
    }
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"resource_schemas": {"networking.k8s.io/v1/NetworkPolicy": resource}}))
    refresh_env()
    schema = fragment_chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value({**fragment_chart.defaults, "rules": "- {}"}))
    assert validator.is_valid(json_value({**fragment_chart.defaults, "rules": [{}]}))
    assert not validator.is_valid(json_value({**fragment_chart.defaults, "rules": [{"unexpected": 1}]}))


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("name", ["logstash", "mariadb-galera"])
def test_bitnami_fragment_counterexamples_are_excluded(tmp_path: Path, name: str) -> None:
    """
    Reproduce both saved NetworkPolicy failures and compare valid structured and string fragments with Helm.

    Args:
        tmp_path (Path): Isolated chart copy and dependency directory.
        name (str): Bitnami chart containing the previously unresolved fragment.

    Returns:
        None: The bad map is excluded; valid lists and raw YAML strings still render correctly.
    """
    source = Path(__file__).resolve().parents[3] / "third_party/bitnami-charts/bitnami"
    if not all((source / chart / "Chart.yaml").is_file() for chart in (name, "common")):
        pytest.skip("requires the pinned Bitnami submodule")
    target = tmp_path / name
    shutil.copytree(source / name, target, ignore=shutil.ignore_patterns("charts"))
    shutil.copytree(source / "common", target / "charts/common")
    chart = Chart(target, {"type": "object"}, mapping(yamlio.load((target / "values.yaml").read_text())))
    bad: dict[str, object] = {"networkPolicy": {"customRules": {"": None}}}
    with pytest.raises(RenderFailure) as error:
        render(chart, bad)
    assert error.value.code == "HH1101"
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    candidate = copy.deepcopy(chart.defaults)
    mapping(candidate["networkPolicy"])["customRules"] = {"": None}
    assert not validator.is_valid(json_value(candidate))
    for rules in ([{"ports": [{"port": 8080}]}], "- ports: [{port: 8080}]"):
        mapping(candidate["networkPolicy"])["customRules"] = rules
        assert validator.is_valid(json_value(candidate))
        assert render(chart, {"networkPolicy": {"customRules": rules}})
