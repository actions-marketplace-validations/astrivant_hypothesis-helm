"""
Verify destination-aware generation, explicit overrides, shrinking and reproducible catalogs.
"""

import copy
import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import find, given, settings
from hypothesis import strategies as st
from hypothesis_helm_catalog.builder import DATA, build
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.suites.generate import generate_tests
from hypothesis_helm.charts.suites.runtime import prepared_chart
from hypothesis_helm.charts.testing.paths import path_strategy
from hypothesis_helm.charts.testing.rendering import validate_resources
from hypothesis_helm.charts.testing.runner import check_chart
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.execution.cache import fingerprint
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.finite import enumerate_values
from hypothesis_helm.schemas.paths import enumerate_paths
from hypothesis_helm.schemas.policy import ENVIRONMENT, PROFILES, intersect, load_policy, restrict
from hypothesis_helm.schemas.resources import destination, library


def fixture_chart(tmp_path: Path, *, guarded: bool = False) -> Chart:
    """
    Create a directly mapped Secret reference and an independently varied activation flag.

    Args:
        tmp_path (Path): Isolated chart destination.
        guarded (bool): Put the Pod behind a Boolean condition.

    Returns:
        Chart: Chart with broad string inputs and a known downstream Secret-name contract.
    """
    (tmp_path / "templates").mkdir(parents=True)
    (tmp_path / "Chart.yaml").write_text("apiVersion: v2\nname: demo\nversion: 0.1.0\n")
    schema: dict[str, object] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["enabled", "secretName", "port"],
        "properties": {"enabled": {"type": "boolean"}, "secretName": {"type": "string"}, "port": {"type": "integer"}},
    }
    defaults = {"enabled": True, "secretName": "example", "port": 8080}
    (tmp_path / "values.schema.json").write_text(json.dumps(schema))
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    template = dedent("""
        apiVersion: v1
        kind: Pod
        metadata:
          name: example
        spec:
          containers:
            - name: app
              image: example
              ports:
                - containerPort: {{ .Values.port }}
          volumes:
            - name: credentials
              secret:
                secretName: {{ .Values.secretName | quote }}
        """).lstrip()
    if guarded:
        template = "{{ if .Values.enabled }}\n" + template + "{{ end }}\n"
    (tmp_path / "templates" / "pod.yaml").write_text(template)
    return Chart.load(tmp_path)


def explicit_policy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, empty: bool = True) -> dict[str, object]:
    """
    Resolve a user policy exactly as the CLI does before workers start.

    Args:
        tmp_path (Path): Local configuration directory.
        monkeypatch (pytest.MonkeyPatch): Restore inherited policy after the test.
        empty (bool): Preserve an intentional empty-string input.

    Returns:
        dict[str, object]: Resolved policy inherited by generation and shrinking.
    """
    config = tmp_path / "policy.yaml"
    config.write_text(
        yamlio.dump(
            {
                "downstream_inputs": False,
                "input_constraints": [
                    {"charts": ["demo"], "path": "$.secretName", "profile": "kubernetes-secret-name", "allow_empty": empty}
                ],
            }
        )
    )
    policy = load_policy(config)
    monkeypatch.setenv(ENVIRONMENT, json.dumps(policy))
    return policy


def test_downstream_defaults_and_shrinking(tmp_path: Path) -> None:
    """
    Generate and shrink within reviewed Secret-name and port constraints by default.

    Args:
        tmp_path (Path): Chart directory.

    Returns:
        None: All generated and shrinking candidates stay inside the destination domain.
    """
    chart = fixture_chart(tmp_path)
    original = copy.deepcopy(chart.schema)
    secret = validators.validator_for(PROFILES["kubernetes-secret-name"])(PROFILES["kubernetes-secret-name"])

    def acceptable(values: dict[str, object]) -> bool:
        """
        Assert validity on every candidate evaluated by the shrinker.

        Args:
            values (dict[str, object]): Complete generated values.

        Returns:
            bool: Whether this candidate reaches the chosen failure condition.
        """
        assert secret.is_valid(json_value(values["secretName"]))
        assert 1 <= int(str(values["port"])) <= 65535
        return values["enabled"] is True

    smallest = find(chart.strategy(), acceptable, settings=settings(max_examples=100, deadline=None, database=None))
    assert smallest["enabled"] is True
    assert chart.schema == original
    assert chart.defaults == {"enabled": True, "secretName": "example", "port": 8080}
    assert len(chart.input_domains().rules) == 2


def test_conditional_domain_preserves_disabled_region(tmp_path: Path) -> None:
    """
    Keep otherwise-invalid values available when their destination resource is absent.

    Args:
        tmp_path (Path): Conditional chart directory.

    Returns:
        None: Constraints apply only to the supported branch that actually emits the value.
    """
    chart = fixture_chart(tmp_path, guarded=True)
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid({"enabled": False, "secretName": ">0", "port": -1})
    assert not validator.is_valid({"enabled": True, "secretName": ">0", "port": 8080})
    assert validator.is_valid({"enabled": True, "secretName": "valid", "port": 1})
    finite = copy.deepcopy(schema)
    properties = mapping(finite["properties"])
    properties["secretName"] = {"enum": ["good", ">0"]}
    properties["port"] = {"enum": [0, 1]}
    values = enumerate_values(finite)
    assert len(values) == 5


def test_manual_policy_parent_paths_and_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Apply explicit restrictions during path draws and retain optional empty names.

    Args:
        tmp_path (Path): Chart and policy files.
        monkeypatch (pytest.MonkeyPatch): Inherited coordinator policy.

    Returns:
        None: Root draws, path draws and their shrinking share one restricted domain.
    """
    chart = fixture_chart(tmp_path)
    explicit_policy(tmp_path, monkeypatch)
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value({**chart.defaults, "secretName": ""}))
    assert not validator.is_valid(json_value({**chart.defaults, "secretName": ">0"}))
    entry = next(entry for entry in enumerate_paths(schema) if entry.path == ("secretName",))

    @settings(max_examples=30, deadline=None, database=None)
    @given(path_strategy(chart, entry, schema))
    def check(values: dict[str, object]) -> None:
        """
        Check every path candidate after baseline and dependent-context assembly.

        Args:
            values (dict[str, object]): Assembled path candidate.

        Returns:
            None: The final merged context satisfies the generation restriction.
        """
        assert validator.is_valid(json_value(values))

    check()


def test_policy_intersection_and_chart_scope(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Never broaden existing enum constraints or apply one chart's rules to another chart.

    Args:
        tmp_path (Path): Chart and configuration files.
        monkeypatch (pytest.MonkeyPatch): Inherited explicit policy.

    Returns:
        None: Enum intersection is exact and unmatched chart names remain unaffected.
    """
    chart = fixture_chart(tmp_path)
    explicit_policy(tmp_path, monkeypatch, empty=False)
    mapping(chart.schema["properties"])["secretName"] = {"type": "string", "enum": [">0", "good"]}
    assert mapping(mapping(chart.generation_schema()["properties"])["secretName"])["enum"] == ["good"]
    (tmp_path / "Chart.yaml").write_text("apiVersion: v2\nname: unrelated\nversion: 0.1.0\n")
    assert Chart.load(tmp_path).input_domains().rules == []
    with pytest.raises(ValueError, match="excludes every"):
        intersect({"enum": [">0"]}, PROFILES["kubernetes-secret-name"])
    with pytest.raises(ValueError, match="contradictory"):
        intersect({"type": "integer", "maximum": 0}, {"minimum": 1})


def test_supplied_defaults_are_not_rewritten(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Retain and actually test a source default outside the user's generated domain.

    Args:
        tmp_path (Path): Chart and policy.
        monkeypatch (pytest.MonkeyPatch): Capture render attempts without invoking Helm.

    Returns:
        None: Baseline remains present and the conflict appears in the report.
    """
    chart = fixture_chart(tmp_path)
    explicit_policy(tmp_path, monkeypatch, empty=False)
    chart.defaults["secretName"] = ">0"
    observed: list[dict[str, object]] = []

    def render(unused: Chart, values: dict[str, object], **kwargs: object) -> list[dict[str, object]]:
        """
        Capture the exact overrides submitted to rendering.

        Args:
            unused (Chart): Original chart identity.
            values (dict[str, object]): Submitted overrides.
            **kwargs (object): Renderer settings.

        Returns:
            list[dict[str, object]]: A fixed valid resource.
        """
        observed.append(copy.deepcopy(values))
        return [{"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": "ok"}}]

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", render)
    report = check_chart(chart, input_strategy=st.just({**chart.defaults, "secretName": "good"}), max_examples=1)
    assert report["status"] == "passed"
    assert observed[0] == {}
    assert chart.defaults["secretName"] == ">0"
    assert mapping(report["input_domains"])["diagnostics"]


def test_opaque_helpers_are_not_guessed(tmp_path: Path) -> None:
    """
    Refuse automatic input inversion when a helper may transform or replace its value.

    Args:
        tmp_path (Path): Chart fixture directory.

    Returns:
        None: Unsupported output remains visible as a limitation without narrowing.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates" / "pod.yaml"
    template.write_text(template.read_text().replace(".Values.secretName | quote", 'include "secretName" .'))
    domains = chart.input_domains()
    assert domains.rules == []
    assert "helper" in str(domains.diagnostics)


def test_custom_schema_required_and_used(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Require a custom API contract and reuse it for input domains and manifest validation.

    Args:
        tmp_path (Path): Configuration directory.
        monkeypatch (pytest.MonkeyPatch): Worker policy environment.

    Returns:
        None: Missing or invalid custom schemas cannot produce a successful validation witness.
    """
    resource = {"apiVersion": "example.org/v1", "kind": "Widget", "metadata": {"name": "ok"}, "spec": {"size": 2}}
    with pytest.raises(RenderFailure, match="requires an explicit JSON schema"):
        validate_resources([resource])
    schema = {"type": "object", "properties": {"spec": {"type": "object", "properties": {"size": {"type": "integer", "minimum": 1}}}}}
    (tmp_path / "widget.json").write_text(json.dumps(schema))
    config = tmp_path / "policy.yaml"
    config.write_text(yamlio.dump({"resource_schemas": {"example.org/v1/Widget": "widget.json"}}))
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(config)))
    validate_resources([resource])
    with pytest.raises(RenderFailure, match="HH1108"):
        validate_resources([{**resource, "spec": {"size": 0}}])
    assert destination("example.org/v1/Widget", ("spec", "size")) == ({"type": "integer", "minimum": 1}, "supplied-resource-schema")
    assert destination("another.org/v1/Widget", ("spec", "size")) is None


def test_cache_and_generated_snapshot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Persist reviewed generation restrictions and invalidate successes on policy changes.

    Args:
        tmp_path (Path): Chart, suite and policy files.
        monkeypatch (pytest.MonkeyPatch): Change the coordinator policy.

    Returns:
        None: A standalone generated suite retains its restrictions after leaving the original directory.
    """
    chart = fixture_chart(tmp_path / "chart")
    original_key = fingerprint(chart.path, 0, None, "none")
    explicit_policy(tmp_path, monkeypatch)
    assert fingerprint(chart.path, 0, None, "none") != original_key
    suite = tmp_path / "suite"
    generate_tests(chart, suite, max_examples=3)
    monkeypatch.delenv(ENVIRONMENT)
    with prepared_chart(chart.path, suite) as prepared:
        validator = validators.validator_for(prepared.generation_schema())(prepared.generation_schema())
        assert not validator.is_valid(json_value({**chart.defaults, "secretName": ">0"}))
        assert prepared.schema == chart.schema


def test_reviewed_library_rebuild_and_stale_descriptions(tmp_path: Path) -> None:
    """
    Rebuild deterministically and require human review when source prose changes.

    Args:
        tmp_path (Path): Minimal schema repository snapshot.

    Returns:
        None: Same sources produce the same catalog; changed review anchors fail closed.
    """
    for raw in sequence(json.loads((DATA / "reviewed-domains.json").read_text())):
        row = mapping(raw)
        file = tmp_path / str(row["file"])
        document: dict[str, object] = mapping(json.loads(file.read_text())) if file.is_file() else {"type": "object", "properties": {}}
        key = str(sequence(row["path"])[0])
        mapping(document["properties"])[key] = {"description": row["description"], **mapping(row["schema"])}
        document["x-kubernetes-group-version-kind"] = [{"group": "example.org", "version": "v1", "kind": file.stem}]
        file.write_text(json.dumps(document))
    assert build(tmp_path, "fixture") == build(tmp_path, "fixture")
    file = tmp_path / "containerport.json"
    file.write_text(file.read_text().replace("Number of port", "Changed description of port"))
    with pytest.raises(ValueError, match="Source description changed"):
        build(tmp_path, "fixture")
    for raw in mapping(library()["domains"]).values():
        schema = mapping(mapping(raw)["schema"])
        validators.validator_for(schema).check_schema(schema)


def test_restrictions_do_not_widen_closed_objects_or_refs() -> None:
    """
    Preserve rejection of unknown properties and local-reference constraints.

    Returns:
        None: Supplemental property rules cannot open closed objects or replace referenced bounds.
    """
    original = {"type": "object", "additionalProperties": False}
    schema = restrict(original, ("new",), {"type": "string"})
    assert not validators.validator_for(schema)(schema).is_valid({"new": "hello"})
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "definitions": {"count": {"type": "integer", "minimum": 3}},
        "properties": {"count": {"$ref": "#/definitions/count"}},
    }
    restricted = restrict(schema, ("count",), {"maximum": 5})
    validator = validators.validator_for(restricted)(restricted)
    assert validator.is_valid({"count": 4})
    assert not validator.is_valid({"count": 2})
    assert not validator.is_valid({"count": 6})


def test_quoted_numeric_output_does_not_restrict_numeric_input(tmp_path: Path) -> None:
    """
    Recognize that literal YAML quotes convert a numeric input into a string destination.

    Args:
        tmp_path (Path): Chart with a quoted port expression.

    Returns:
        None: No numeric destination bounds are asserted for the transformed value.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(template.read_text().replace("{{ .Values.port }}", '"{{ .Values.port }}"'))
    domains = chart.input_domains()
    assert all(rule["path"] != ["port"] for rule in domains.rules)
    assert any(item.get("path") == ["port"] for item in domains.diagnostics)


def test_inline_references_cannot_rebind_to_chart_schema(tmp_path: Path) -> None:
    """
    Reject inline schema references before embedding can change their target document.

    Args:
        tmp_path (Path): Policy file directory.

    Returns:
        None: A local-looking reference cannot silently resolve against the chart schema.
    """
    config = tmp_path / "policy.yaml"
    config.write_text(
        yamlio.dump(
            {
                "input_constraints": [
                    {"charts": ["demo"], "path": "$.port", "schema": {"$ref": "#/$defs/port", "$defs": {"port": {"minimum": 1}}}}
                ]
            }
        )
    )
    with pytest.raises(ValueError, match="self-contained"):
        load_policy(config)


def test_unsupported_inferred_yaml_keeps_declared_domain_evidence(tmp_path: Path) -> None:
    """
    Retain supported mappings when an unrelated inferred value is not a JSON scalar.

    Args:
        tmp_path (Path): Chart with an undeclared YAML date.

    Returns:
        None: The audit gets a diagnostic and the declared numeric domain remains available.
    """
    fixture_chart(tmp_path)
    values = tmp_path / "values.yaml"
    values.write_text(values.read_text() + "generatedOn: 2024-04-01\n")
    domains = Chart.load(tmp_path).input_domains()
    assert any(rule["path"] == ["port"] for rule in domains.rules)
    assert any("declared paths only" in str(item.get("reason")) for item in domains.diagnostics)


@pytest.mark.parametrize(
    "helper",
    [
        '{{- define "secret" -}}{{- .name -}}{{- end -}}',
        '{{- define "secret" -}}{{- (.).name -}}{{- end -}}',
        '{{- define "secret" -}}{{- (dict "name" .name).name -}}{{- end -}}',
        '{{- define "secret" -}}{{- $empty := dict -}}{{- .name -}}{{- end -}}',
        '{{- define "secret" -}}{{- $empty := list -}}{{- .name -}}{{- end -}}',
        '{{- define "secret" -}}{{- $items := list .name -}}{{- .name -}}{{- end -}}',
        '{{- define "secret" -}}{{- $v := (dict "nested" .) -}}{{- ($v.nested).name -}}{{- end -}}',
        '{{- define "secret" -}}{{- $v := .name -}}{{- include "identity" (dict "value" $v) -}}{{- end -}}'
        '{{- define "identity" -}}{{- .value -}}{{- end -}}',
    ],
)
@pytest.mark.parametrize("invocation", ["include", "template"])
def test_helper_projection_preserves_input_origins(tmp_path: Path, helper: str, invocation: str) -> None:
    """
    Carry input destinations through pure helper arguments and nested aliases.

    Args:
        tmp_path (Path): Isolated chart directory.
        helper (str): Helper source retaining the original input unchanged.
        invocation (str): Function call or template action selecting the named helper.

    Returns:
        None: Generated values obey the destination contract through either helper shape.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text(helper)
    template = tmp_path / "templates/pod.yaml"
    call = f'{invocation} "secret" (dict "name" .Values.secretName)' + (" | quote" if invocation == "include" else "")
    template.write_text(template.read_text().replace(".Values.secretName | quote", call))
    validator = validators.validator_for(chart.generation_schema())(chart.generation_schema())
    assert not validator.is_valid(json_value({**chart.defaults, "secretName": ">0"}))
    assert validator.is_valid(json_value({**chart.defaults, "secretName": "valid"}))
    assert {tuple(sequence(rule["path"])) for rule in chart.input_domains().rules} >= {("secretName",), ("port",)}


def test_symbolic_root_context_constrains_tpl_to_literal_inputs(tmp_path: Path) -> None:
    """
    Constrain template-valued references to literal input without serializing the helper context.

    Args:
        tmp_path (Path): Isolated chart with a helper forwarding the root context to tpl.

    Returns:
        None: Literal names are constrained and supplied template-valued defaults remain unchanged.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text('{{- define "secret" -}}{{- tpl .Values.secretName $ -}}{{- end -}}')
    template = tmp_path / "templates/pod.yaml"
    template.write_text(template.read_text().replace(".Values.secretName | quote", 'include "secret" .'))
    domains = chart.input_domains()
    assert {tuple(sequence(rule["path"])) for rule in domains.rules} >= {("secretName",), ("port",)}
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value({**chart.defaults, "secretName": "literal-name"}))
    assert not validator.is_valid(json_value({**chart.defaults, "secretName": "{{ .Release.Name }}"}))
    assert "JSON serializable" not in str(domains.diagnostics)


def test_serialized_collections_use_destination_shapes(tmp_path: Path) -> None:
    """
    Constrain annotation maps and port arrays using their Kubernetes field schemas.

    Args:
        tmp_path (Path): Isolated Pod chart.

    Returns:
        None: Invalid collection members are excluded while valid objects remain available.
    """
    chart = fixture_chart(tmp_path)
    mapping(chart.schema["properties"])["annotations"] = {"type": "object"}
    mapping(chart.schema["properties"])["ports"] = {"type": "array"}
    chart.defaults.update(annotations={"purpose": "example"}, ports=[{"containerPort": 8080}])
    (tmp_path / "values.schema.json").write_text(json.dumps(chart.schema))
    (tmp_path / "templates/_helpers.tpl").write_text('{{- define "annotations" -}}{{- toYaml .data -}}{{- end -}}')
    template = tmp_path / "templates/pod.yaml"
    text = template.read_text().replace(
        "  name: example", '  name: example\n  annotations: {{ include "annotations" (dict "data" .Values.annotations) | nindent 4 }}'
    )
    text = text.replace("      ports:\n        - containerPort: {{ .Values.port }}", "      ports: {{ toYaml .Values.ports | nindent 8 }}")
    template.write_text(text)
    validator = validators.validator_for(chart.generation_schema())(chart.generation_schema())
    assert validator.is_valid(json_value(chart.defaults))
    assert not validator.is_valid(json_value({**chart.defaults, "annotations": {"example": []}}))
    assert not validator.is_valid(json_value({**chart.defaults, "ports": ["not-a-port-object"]}))
    assert not validator.is_valid(json_value({**chart.defaults, "ports": [{}]}))
    assert not validator.is_valid(json_value({**chart.defaults, "ports": [{"containerPort": 0}]}))


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_helper_domain_keeps_numeric_strings_and_real_encoding_failures(tmp_path: Path) -> None:
    """
    Keep legal numeric-looking names available to expose missing YAML quoting.

    Args:
        tmp_path (Path): Isolated chart with an unquoted helper result.

    Returns:
        None: The input remains eligible and native Helm output still fails manifest validation.
    """
    from hypothesis_helm.charts.testing.rendering import render

    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/_helpers.tpl").write_text('{{- define "name" -}}{{- .Values.secretName -}}{{- end -}}')
    template = tmp_path / "templates/pod.yaml"
    template.write_text(template.read_text().replace("name: example", 'name: {{ include "name" . }}'))
    candidate = {**chart.defaults, "secretName": "0"}
    validator = validators.validator_for(chart.generation_schema())(chart.generation_schema())
    assert validator.is_valid(json_value(candidate))
    with pytest.raises(RenderFailure, match="HH1105"):
        render(chart, candidate)
