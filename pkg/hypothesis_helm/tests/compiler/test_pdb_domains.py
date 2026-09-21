"""
Constrain PDB input generation using destination types and source-derived helper mappings.
"""

import copy
import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis_helm_catalog.builder import scalar_domain
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.suites.generate import coalesce
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.generation.domains import InputDomains
from hypothesis_helm.schemas.kubernetes.resources import destination
from hypothesis_helm.tests import PROJECT_ROOT


def test_scalar_composition_retains_types_without_unresolved_references() -> None:
    """
    Preserve complete union alternatives and decline partially understood exclusive alternatives.

    Returns:
        None: Scalar oneOf bounds survive extraction without making an unresolved branch unconditional.
    """
    source: dict[str, object] = {"oneOf": [{"type": "integer", "minimum": 0}, {"type": "string", "pattern": "^[0-9]+%$"}]}
    assert scalar_domain(source) == source
    assert scalar_domain({"oneOf": [{"type": "string"}, {"$ref": "#/definitions/integer"}]}) == {}
    assert scalar_domain({"oneOf": [{"type": "string"}, {"allOf": [{"$ref": "#/definitions/integer"}]}]}) == {}


@pytest.mark.parametrize("field", ["minAvailable", "maxUnavailable"])
def test_pdb_catalog_bounds(field: str) -> None:
    """
    Check destination-derived PDB limits at both count and percentage boundaries.

    Args:
        field (str): PDB spec limit selected from the bundled destination catalog.

    Returns:
        None: Invalid syntax, negative counts and excessive percentages are excluded.
    """
    result = destination("policy/v1/PodDisruptionBudget", ("spec", field))
    assert result is not None
    schema, _ = result
    validator = validators.validator_for(schema)(schema)
    for value in (0, 1, 2**31 - 1, "0%", "1%", "99%", "100%", "0001%", "000100%"):
        assert validator.is_valid(value), value
    for invalid in (-1, 2**31, 0.5, True, "", "#", "[Ma", "1", "101%", "-1%", "1.5%", "100%\n", "é"):
        assert not validator.is_valid(invalid), invalid


@pytest.mark.parametrize("union", [False, True])
def test_direct_pdb_mapping_constrains_arbitrary_input_names(tmp_path: Path, union: bool) -> None:
    """
    Apply PDB rules by manifest destination while retaining inactive branches and unrelated text.

    Args:
        tmp_path (Path): Simple chart with a direct PDB destination.
        union (bool): Declare the source type as a mixed type array or scalar alternatives.

    Returns:
        None: Both integer and percentage inputs are constrained without a field-name heuristic.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "example", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump({"enabled": True, "limit": 1, "notes": "#"}))
    limit = {"anyOf": [{"type": "integer"}, {"type": "string"}]} if union else {"type": ["integer", "string"]}
    (tmp_path / "values.schema.json").write_text(
        json.dumps({"type": "object", "properties": {"enabled": {"type": "boolean"}, "limit": limit, "notes": {"type": "string"}}})
    )
    (tmp_path / "templates/pdb.yaml").write_text(
        dedent("""
            {{ if .Values.enabled }}
            apiVersion: policy/v1
            kind: PodDisruptionBudget
            metadata:
              name: example
            spec:
              maxUnavailable: {{ .Values.limit }}
              selector:
                matchLabels:
                  app: example
            {{ end }}
            """)
    )
    chart = Chart.load(tmp_path)
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    for value in (0, 1, "50%", "100%"):
        assert validator.is_valid({"enabled": True, "limit": value, "notes": "#"})
    for value in ("#", "[Ma", -1, "101%"):
        assert not validator.is_valid({"enabled": True, "limit": value})
        assert validator.is_valid({"enabled": False, "limit": value})
    assert any(rule["path"] == ["limit"] for rule in chart.input_domains().rules)


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_mariadb_galera_coalesced_pdb_generation_and_native_render(tmp_path: Path) -> None:
    """
    Trace PDB fields through the map alias and verify the reported quote failure with Helm.

    Args:
        tmp_path (Path): Isolated chart and its locally available common dependency.

    Returns:
        None: Selected limits receive destination constraints while defaults and inactive inputs remain available.
    """
    source = PROJECT_ROOT / "third_party/bitnami-charts/bitnami"
    if not all((source / name / "Chart.yaml").is_file() for name in ("mariadb-galera", "common")):
        pytest.skip("requires the pinned Bitnami submodule")
    target = tmp_path / "mariadb-galera"
    shutil.copytree(source / "mariadb-galera", target, ignore=shutil.ignore_patterns("charts"))
    shutil.copytree(source / "common", target / "charts/common")
    chart = Chart(target, {"type": "object"}, mapping(yamlio.load((target / "values.yaml").read_text())))
    with pytest.raises(RenderFailure) as error:
        render(chart, {"pdb": {"maxUnavailable": "'"}})
    assert error.value.code == "HH1101"
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value(chart.defaults))
    for field in ("minAvailable", "maxUnavailable"):
        for value in ("", 0, 1, "50%", "100%", "'", "[", -1, "101%"):
            candidate = copy.deepcopy(chart.defaults)
            mapping(candidate["pdb"])[field] = value
            assert validator.is_valid(json_value(candidate)) == (value in ("", 0, 1, "50%", "100%")), (field, value)
            mapping(candidate["pdb"])["create"] = False
            assert validator.is_valid(json_value(candidate)), (field, value)
    valid_overrides: list[dict[str, object]] = [{}, {"pdb": {"maxUnavailable": "50%"}}, {"pdb": {"minAvailable": 1}}]
    for overrides in valid_overrides:
        assert render(chart, overrides)


@pytest.mark.parametrize(
    "selection",
    [
        "coalesce .Values.primary .Values.secondary .Values.fallback",
        "default (default .Values.fallback .Values.secondary) .Values.primary",
        "ternary .Values.primary (coalesce .Values.secondary .Values.fallback) (not (empty .Values.primary))",
    ],
)
def test_pdb_map_selection_preserves_whole_map_precedence(tmp_path: Path, selection: str) -> None:
    """
    Follow nested map choices without incorrectly selecting fallback fields from an unused map.

    Args:
        tmp_path (Path): Generic chart with arbitrary input names.
        selection (str): Equivalent map selection written using different Helm functions.

    Returns:
        None: Only emitted limits are constrained, including empty and missing fallback maps.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "choices", "version": "1.0.0"}))
    defaults: dict[str, object] = {"primary": {}, "secondary": {}, "fallback": {"active": True, "limit": ""}}
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates/pdb.yaml").write_text(
        "{{ $selected := "
        + selection
        + " }}\n"
        + dedent("""
            {{ if $selected.active }}
            apiVersion: policy/v1
            kind: PodDisruptionBudget
            metadata:
              name: choices
            spec:
              maxUnavailable: {{ $selected.limit | default 1 }}
              selector:
                matchLabels:
                  app: choices
            {{ end }}
            """)
    )
    properties = {"active": {"type": "boolean"}, "limit": {"type": ["integer", "string"]}}
    source_schema: dict[str, object] = {
        "type": "object",
        "properties": {name: {"type": "object", "properties": properties} for name in defaults},
    }
    chart = Chart(tmp_path, source_schema, defaults)
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    for selected in ("primary", "secondary", "fallback"):
        for value in ("", 0, 1, "50%", "'", -1, "101%"):
            candidate: dict[str, object] = {"fallback": {"active": True, "limit": "'"}}
            candidate[selected] = {"active": True, "limit": value}
            assert validator.is_valid(json_value(candidate)) == (value in ("", 0, 1, "50%")), (selected, value)
            mapping(candidate[selected])["active"] = False
            assert validator.is_valid(json_value(candidate)), (selected, value)
    for primary in ({}, {"active": False}, {"limit": "'"}, {"active": True}):
        candidate = {"primary": primary, "fallback": {"active": True, "limit": "'"}}
        assert validator.is_valid(json_value(candidate)) == bool(primary), primary


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_airflow_pdb_generation_and_native_render(tmp_path: Path) -> None:
    """
    Reproduce the reported malformed YAML and keep generated PDB subtrees inside guarded field domains.

    Args:
        tmp_path (Path): Isolated Airflow chart and installed local dependencies.

    Returns:
        None: Both bad strings are excluded; valid counts, percentages and defaults still render.
    """
    source = PROJECT_ROOT / "third_party/bitnami-charts/bitnami"
    if not all((source / name / "Chart.yaml").is_file() for name in ("airflow", "common", "redis", "postgresql")):
        pytest.skip("requires the pinned Bitnami submodule")
    target = tmp_path / "airflow"
    shutil.copytree(source / "airflow", target, ignore=shutil.ignore_patterns("charts"))
    for name in ("common", "redis", "postgresql"):
        shutil.copytree(source / name, target / "charts" / name, ignore=shutil.ignore_patterns("charts"))
    for name in ("redis", "postgresql"):
        shutil.copytree(source / "common", target / "charts" / name / "charts/common")
    chart = Chart(target, {"type": "object"}, mapping(yamlio.load((target / "values.yaml").read_text())))
    original = copy.deepcopy(chart.defaults)
    rules = [
        rule for rule in chart.input_domains().rules if sequence(rule["path"])[-2:] in (["pdb", "minAvailable"], ["pdb", "maxUnavailable"])
    ]
    schema = InputDomains(rules, [], "test").apply({})
    validator = validators.validator_for(schema)(schema)
    for component in ("worker", "web", "scheduler", "dagProcessor", "triggerer"):
        for field in ("minAvailable", "maxUnavailable"):
            for value in ("", 0, 1, "0%", "50%", "100%", "#", "[Ma", "101%", -1):
                candidate = copy.deepcopy(chart.defaults)
                section = mapping(candidate[component])
                section["enabled"] = True
                limits = mapping(section["pdb"])
                limits.update(create=True, minAvailable="", maxUnavailable="")
                limits[field] = value
                assert validator.is_valid(json_value(candidate)) == (value in ("", 0, 1, "0%", "50%", "100%")), candidate
    model = coalesce(chart)
    with pytest.raises(RenderFailure) as error:
        render(chart, {"worker": {"pdb": {"minAvailable": "#", "maxUnavailable": "[Ma"}}})
    assert error.value.code == "HH1101"
    for valid_limits in ({"minAvailable": "", "maxUnavailable": "50%"}, {"minAvailable": 1, "maxUnavailable": ""}, {}):
        assert render(chart, {"worker": {"pdb": valid_limits}})
    assert chart.defaults == original
    pdb_template = target / "templates/worker/poddisruptionbudget.yaml"
    pdb_template.write_text(pdb_template.read_text() + "\n{{/* changed comment */}}\n")
    rules, _ = project(target, model.schema, chart.dependency_model)
    assert any(sequence(rule["path"]) == ["worker", "pdb", "minAvailable"] for rule in rules)
