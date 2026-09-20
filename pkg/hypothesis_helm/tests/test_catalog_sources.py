"""
Verify source-derived bounds, exact destination bindings, and immutable rebuild comparisons.
"""

import copy
import json
import shutil
import tarfile
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis_helm_catalog import builder, sources
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import RenderFailure, render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.domains import InputDomains
from hypothesis_helm.schemas.policy import ENVIRONMENT


def test_upstream_destinations_use_api_types_not_field_names(tmp_path: Path) -> None:
    """
    Apply reference-name bounds only at reviewed API types reached through OpenAPI references.

    Args:
        tmp_path (Path): Minimal upstream OpenAPI checkout.

    Returns:
        None: An unrelated field called name remains unrestricted and recursive definitions terminate.
    """
    source = tmp_path / "api/openapi-spec/swagger.json"
    source.parent.mkdir(parents=True)
    source.write_text(
        json.dumps(
            {
                "definitions": {
                    "io.k8s.api.core.v1.ConfigMapVolumeSource": {"properties": {"name": {"type": "string"}}},
                    "io.k8s.api.core.v1.Pod": {
                        "x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Pod"}],
                        "properties": {
                            "name": {"type": "string"},
                            "volumes": {"items": {"$ref": "#/definitions/io.k8s.api.core.v1.ConfigMapVolumeSource"}},
                            "recursive": {"$ref": "#/definitions/io.k8s.api.core.v1.Pod"},
                        },
                    },
                }
            }
        )
    )
    schema = {"type": "string", "pattern": "^[a-z]+$"}
    result = sources.destinations(tmp_path, {"fields": {}, "profiles": {"dns1123-subdomain": {"schema": schema}}})
    pod = mapping(result["v1/Pod"])
    assert set(pod) == {"volumes/*/name"}
    assert mapping(mapping(pod["volumes/*/name"])["schema"])["pattern"] == schema["pattern"]


def test_check_never_overwrites_the_catalog_under_comparison(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Detect stale cached catalogs without replacing them before the comparison.

    Args:
        tmp_path (Path): Fake source snapshot and output cache.
        monkeypatch (pytest.MonkeyPatch): Replace only the expensive upstream rebuild.

    Returns:
        None: Check mode reports staleness and a normal rebuild atomically replaces it.
    """
    monkeypatch.setattr(sources, "rebuild", lambda *args, **kwargs: {})
    monkeypatch.setattr(builder, "build", lambda *args, **kwargs: {"resources": {"v1/Pod": {}}})
    target = tmp_path / "catalogs/1.35.0/input-domains.json"
    target.parent.mkdir(parents=True)
    target.write_text("stale\n")
    arguments = [
        "--schema-dir",
        str(tmp_path),
        "--kubernetes-source-dir",
        str(tmp_path),
        "--cache-dir",
        str(tmp_path),
        "--output",
        str(target),
    ]
    assert builder.main([*arguments, "--check"]) == 1
    assert target.read_text() == "stale\n"
    assert builder.main(arguments) == 0
    assert builder.main([*arguments, "--check"]) == 0


@pytest.fixture
def bound_chart(tmp_path: Path) -> Path:
    """
    Create a source-analyzable ConfigMap helper without relying on an external chart checkout.

    Args:
        tmp_path (Path): Chart directory.

    Returns:
        Path: Chart with a broad declared string and a helper-derived destination.
    """
    chart = tmp_path / "mongodb"
    (chart / "templates").mkdir(parents=True)
    (chart / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "mongodb", "version": "1.0.0"}))
    (chart / "values.yaml").write_text(yamlio.dump({"existingConfigmap": ""}))
    (chart / "values.schema.json").write_text(json.dumps({"type": "object", "properties": {"existingConfigmap": {"type": "string"}}}))
    template = chart / "templates/helper.tpl"
    template.write_text(
        dedent("""
        {{- define "configmapName" -}}
        {{- if .Values.existingConfigmap -}}
        {{- tpl .Values.existingConfigmap $ -}}
        {{- else -}}fallback{{- end -}}
        {{- end -}}
        """)
    )
    (chart / "templates/pod.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: Pod
        metadata:
          name: example
        spec:
          containers:
            - name: app
              image: example
          volumes:
            - name: config
              configMap:
                name: {{ include "configmapName" . }}
        """)
    )
    return chart


@pytest.mark.parametrize("packaged", [False, True])
def test_helper_constraints_follow_dependency_aliases(tmp_path: Path, bound_chart: Path, packaged: bool) -> None:
    """
    Preserve source-derived reference constraints across unpacked and packaged dependency aliases.

    Args:
        tmp_path (Path): Parent chart root.
        bound_chart (Path): Child chart with a helper-derived destination.
        packaged (bool): Package the child as a tgz before analysis.

    Returns:
        None: Empty fallbacks and meaningful names pass, invalid references fail, and supplied values remain unchanged.
    """
    root_rules, diagnostics = project(bound_chart, Chart.load(bound_chart).schema)
    assert len(root_rules) == 1 and not diagnostics
    parent = tmp_path / "parent"
    (parent / "charts").mkdir(parents=True)
    (parent / "Chart.yaml").write_text(
        yamlio.dump(
            {
                "apiVersion": "v2",
                "name": "parent",
                "version": "1.0.0",
                "dependencies": [{"name": "mongodb", "alias": "database", "version": "1.0.0"}],
            }
        )
    )
    (parent / "values.yaml").write_text(yamlio.dump({"database": {"existingConfigmap": ""}}))
    (parent / "values.schema.json").write_text(json.dumps({"type": "object"}))
    if packaged:
        with tarfile.open(parent / "charts/mongodb-1.0.0.tgz", "w:gz") as archive:
            archive.add(bound_chart, arcname="mongodb")
    else:
        shutil.copytree(bound_chart, parent / "charts/mongodb")
    chart = Chart.load(parent)
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    for value in ("", "my-config", "my.config"):
        assert validator.is_valid(json_value({"database": {"existingConfigmap": value}}))
    for value in ("I\n&", ">0", "invalid\tname", "a\n", "é"):
        assert not validator.is_valid(json_value({"database": {"existingConfigmap": value}}))
    assert chart.defaults == {"database": {"existingConfigmap": ""}}
    assert any(rule["path"] == ["database", "existingConfigmap"] for rule in chart.input_domains().rules)


def test_changed_helper_is_reanalyzed_and_opt_out_is_respected(bound_chart: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Reanalyze edited helpers and respect an explicit domain-analysis opt-out.

    Args:
        bound_chart (Path): Source-derived input helper.
        monkeypatch (pytest.MonkeyPatch): Install an explicit downstream-input opt-out.

    Returns:
        None: Edited helper behavior is reanalyzed, and user policy can disable automatic domains.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"downstream_inputs": False}))
    assert not Chart.load(bound_chart).input_domains().rules
    monkeypatch.delenv(ENVIRONMENT)
    file = bound_chart / "templates/helper.tpl"
    file.write_text(file.read_text() + "\n{{/* changed */}}\n")
    rules, _ = project(bound_chart, Chart.load(bound_chart).schema)
    assert any(rule["path"] == ["existingConfigmap"] for rule in rules)
    file.write_text(file.read_text().replace("tpl .Values.existingConfigmap $", 'printf "fixed-%s" .Values.existingConfigmap'))
    rules, notes = project(bound_chart, Chart.load(bound_chart).schema)
    assert not any(rule["path"] == ["existingConfigmap"] for rule in rules)
    assert "unsupported output transformation" in str(notes)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_bitnami_cilium_configmap_domains_and_native_render(tmp_path: Path) -> None:
    """
    Reproduce the Cilium reference failure and constrain its four ConfigMap inputs from source.

    Args:
        tmp_path (Path): Isolated chart copy and locally supplied dependencies.

    Returns:
        None: Invalid names are outside generation; real names and empty fallbacks retain native behavior.
    """
    source = Path(__file__).resolve().parents[3] / "third_party/bitnami-charts/bitnami"
    if not all((source / name / "Chart.yaml").is_file() for name in ("cilium", "common", "etcd")):
        pytest.skip("requires the pinned Bitnami submodule")
    target = tmp_path / "cilium"
    shutil.copytree(source / "cilium", target)
    for dependency in ("common", "etcd"):
        shutil.copytree(source / dependency, target / "charts" / dependency)
    chart = Chart(target, {"type": "object"}, mapping(yamlio.load((target / "values.yaml").read_text())))
    before = yamlio.dump(chart.defaults)
    domains = chart.input_domains()
    paths = {
        ("existingConfigmap",),
        ("envoy", "existingConfigmap"),
        ("hubble", "relay", "existingConfigmap"),
        ("hubble", "ui", "frontend", "existingServerBlockConfigmap"),
    }
    assert paths <= {tuple(sequence(rule["path"])) for rule in domains.rules}
    targeted = [rule for rule in domains.rules if tuple(sequence(rule["path"])) in paths]
    restriction = InputDomains(targeted, [], "test").apply({})
    validator = validators.validator_for(restriction)(restriction)
    for path in paths:
        for value in ("", "existing-config", "config.v1", "0", "I\n&", ">0", "invalid\tname", "a\n", "A"):
            candidate = copy.deepcopy(chart.defaults)
            hubble = mapping(candidate["hubble"])
            hubble["enabled"] = True
            mapping(hubble["relay"])["enabled"] = True
            mapping(hubble["ui"])["enabled"] = True
            current = candidate
            for key in path[:-1]:
                current = mapping(current.setdefault(key, {}))
            current[path[-1]] = value
            assert validator.is_valid(json_value(candidate)) == (value in {"", "existing-config", "config.v1", "0"}), (path, value)
    assert validator.is_valid({"unrelatedConfig": "I\n&"})
    assert yamlio.dump(chart.defaults) == before
    with pytest.raises(RenderFailure) as failure:
        render(chart, {"envoy": {"existingConfigmap": "I\n&"}})
    assert failure.value.code == "HH1101"
    resources = render(chart, {"envoy": {"existingConfigmap": "existing-config"}})
    assert "existing-config" in yamlio.dump(resources)
    assert render(chart, {})
