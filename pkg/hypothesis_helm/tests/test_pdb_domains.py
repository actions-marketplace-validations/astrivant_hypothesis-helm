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
from hypothesis_helm.charts.testing.rendering import RenderFailure, render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.domains import InputDomains
from hypothesis_helm.schemas.resources import destination


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
def test_airflow_pdb_generation_and_native_render(tmp_path: Path) -> None:
    """
    Reproduce the reported malformed YAML and keep generated PDB subtrees inside guarded field domains.

    Args:
        tmp_path (Path): Isolated Airflow chart and installed local dependencies.

    Returns:
        None: Both bad strings are excluded; valid counts, percentages and defaults still render.
    """
    source = Path(__file__).resolve().parents[3] / "third_party/bitnami-charts/bitnami"
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
