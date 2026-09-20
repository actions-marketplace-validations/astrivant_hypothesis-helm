"""
Check collection provenance against native Helm without chart-specific input bindings.
"""

import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import json_value, mapping


@pytest.fixture
def collection_chart(tmp_path: Path) -> Chart:
    """
    Create renamed helper layers forwarding two arrays through an append accumulator.

    Args:
        tmp_path (Path): Isolated chart source.

    Returns:
        Chart: Empty array defaults with no declared element constraints.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "collections", "version": "1.0.0"}))
    defaults: dict[str, object] = {"enabled": True, "first": [], "second": [], "matrix": [[1, 2], [3, 4]]}
    schema: dict[str, object] = {
        "type": "object",
        "properties": {
            "enabled": {"type": "boolean"},
            "first": {"type": "array"},
            "second": {"type": "array"},
            "matrix": {"type": "array"},
        },
    }
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "values.schema.json").write_text(json.dumps(schema))
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "collect.references" -}}
          {{- $names := list -}}
          {{- range .sources -}}
            {{- range . -}}
              {{- if kindIs "map" . -}}
                {{- $names = append $names .name -}}
              {{- else -}}
                {{- $names = append $names . -}}
              {{- end -}}
            {{- end -}}
          {{- end -}}
          {{- if not (empty $names) }}
        imagePullSecrets:
          {{- range $names | uniq }}
          - name: {{ . }}
          {{- end }}
          {{- end -}}
        {{- end -}}
        {{- define "forward.references" -}}
          {{- include "collect.references" (dict "sources" (list .Values.first .Values.second)) -}}
        {{- end -}}
        """)
    )
    (tmp_path / "templates/pod.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: Pod
        metadata:
          name: example
        spec:
          containers:
            - name: app
              image: example
          {{- if .Values.enabled }}
          {{- include "forward.references" . | nindent 2 }}
          {{- end }}
        """)
    )
    return Chart(tmp_path, schema, defaults)


@pytest.mark.parametrize("field", ["first", "second"])
def test_collection_item_branches_are_constrained_independently(collection_chart: Chart, field: str) -> None:
    """
    Accept both supported representations, including mixed lists, and reject invalid item shapes.

    Args:
        collection_chart (Chart): Generic helper and accumulation fixture.
        field (str): Caller array to vary independently.

    Returns:
        None: Item conditions constrain each element and do not affect unrelated nested arrays.
    """
    schema = collection_chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    valid: list[object] = [[], ["registry-secret"], [{"name": "registry-secret"}], ["first", {"name": "second"}], ["same", "same"]]
    invalid: list[object] = [[[{}]], [{}], [False], [{"name": []}], ["valid", [{}]], [{"name": "valid"}, {"name": []}]]
    for value in valid:
        assert validator.is_valid(json_value({**collection_chart.defaults, field: value})), value
    for value in invalid:
        assert not validator.is_valid(json_value({**collection_chart.defaults, field: value})), value
        assert validator.is_valid(json_value({**collection_chart.defaults, field: value, "enabled": False})), value
    assert validator.is_valid(json_value({**collection_chart.defaults, "matrix": [[{}]]}))
    rules = collection_chart.input_domains().rules
    assert any(rule["path"] == [field] for rule in rules)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_collection_guidance_matches_native_rendering(collection_chart: Chart) -> None:
    """
    Verify helper selections and deduplication with the real renderer.

    Args:
        collection_chart (Chart): Fixture with two merged secret-reference arrays.

    Returns:
        None: Allowed forms render and the original malformed nested list reproduces the YAML defect.
    """
    documents = render(collection_chart, {"first": ["alpha", {"name": "beta"}], "second": ["alpha"]})
    assert mapping(documents[0]["spec"])["imagePullSecrets"] == [{"name": "alpha"}, {"name": "beta"}]
    with pytest.raises(RenderFailure, match="YAML parse error"):
        render(collection_chart, {"first": [[{}]]})


def test_overwriting_loop_does_not_invent_an_accumulation(collection_chart: Chart) -> None:
    """
    Leave arbitrary recurrences unresolved instead of pretending one iteration is the whole loop.

    Args:
        collection_chart (Chart): Fixture whose helper will replace its outer binding.

    Returns:
        None: Unsupported replacement is diagnosed without constraining its discarded inputs.
    """
    helper = collection_chart.path / "templates/_helpers.tpl"
    helper.write_text(helper.read_text().replace("append $names .name", "list .name").replace("append $names .", "list ."))
    rules, notes = project(collection_chart.path, collection_chart.schema)
    assert not any(rule["path"] in [["first"], ["second"]] for rule in rules)
    assert any("non-append loop assignment" in str(note) for note in notes)


def test_authored_element_type_conflict_remains_visible(collection_chart: Chart) -> None:
    """
    Preserve an authored integer domain even when the template sends it to a string field.

    Args:
        collection_chart (Chart): Fixture whose first array explicitly admits integers.

    Returns:
        None: Schema contradictions are diagnosed rather than silently narrowing away the examples.
    """
    mapping(collection_chart.schema["properties"])["first"] = {"type": "array", "items": {"type": "integer"}}
    (collection_chart.path / "values.schema.json").write_text(json.dumps(collection_chart.schema))
    (collection_chart.path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "forward.references" -}}
        imagePullSecrets:
          {{- range .Values.first }}
          - name: {{ . }}
          {{- end }}
        {{- end -}}
        """)
    )
    schema = collection_chart.generation_schema()
    assert validators.validator_for(schema)(schema).is_valid(json_value({**collection_chart.defaults, "first": [1]}))
    assert any("declared element domain" in str(note) for note in collection_chart.input_domains().diagnostics)


def test_quoted_items_do_not_imply_an_input_string_type(collection_chart: Chart) -> None:
    """
    Keep coercible input shapes when the template explicitly converts them to strings.

    Args:
        collection_chart (Chart): Fixture whose selected item is now quoted.

    Returns:
        None: Destination string types are not confused with pre-conversion input types.
    """
    helper = collection_chart.path / "templates/_helpers.tpl"
    helper.write_text(helper.read_text().replace("- name: {{ . }}", "- name: {{ . | quote }}"))
    validator = validators.validator_for(collection_chart.generation_schema())(collection_chart.generation_schema())
    assert validator.is_valid(json_value({**collection_chart.defaults, "first": [[{}]]}))
