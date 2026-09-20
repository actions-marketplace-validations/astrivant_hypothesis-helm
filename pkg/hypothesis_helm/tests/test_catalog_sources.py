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
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.domains import InputDomains
from hypothesis_helm.schemas.policy import ENVIRONMENT
from hypothesis_helm.schemas.resources import destination


@pytest.mark.parametrize(
    ("field", "allowed"),
    [("type", ["ClusterIP", "NodePort", "LoadBalancer", "ExternalName"]), ("sessionAffinity", ["None", "ClientIP"])],
)
def test_service_enum_shims_preserve_defaulting_and_exact_destinations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str, allowed: list[str]
) -> None:
    """
    Rebuild Service enums without restricting unrelated strings or Kubernetes defaulting.

    Args:
        tmp_path (Path): Isolated source and schema snapshots.
        monkeypatch (pytest.MonkeyPatch): Select only the supplement under test.
        field (str): Exact ServiceSpec field.
        allowed (list[str]): Values accepted by the pinned upstream validator.

    Returns:
        None: Generated and bundled catalogs reject invalid enums with explicit shim provenance.
    """
    row = next(
        mapping(item)
        for item in sequence(json.loads((builder.DATA / "reviewed-domains.json").read_text()))
        if mapping(item)["id"] == f"servicespec.{field}"
    )
    spec = {"type": "object", "properties": {field: {"type": ["string", "null"], "description": row["description"]}}}
    service = {
        "type": "object",
        "x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Service"}],
        "properties": {"spec": {"$ref": "#/definitions/io.k8s.api.core.v1.ServiceSpec"}, "unrelated": spec},
    }
    source = tmp_path / "api/openapi-spec/swagger.json"
    source.parent.mkdir(parents=True)
    source.write_text(json.dumps({"definitions": {"io.k8s.api.core.v1.ServiceSpec": spec, "io.k8s.api.core.v1.Service": service}}))
    resources = sources.destinations(tmp_path, {"fields": {}, "profiles": {}}, reviewed=[row])
    assert set(mapping(resources["v1/Service"])) == {f"spec/{field}"}
    (tmp_path / "reviewed-domains.json").write_text(json.dumps([row]))
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    (snapshot / "servicespec.json").write_text(json.dumps(spec))
    mapping(service["properties"])["spec"] = spec
    (snapshot / "service-v1.json").write_text(json.dumps(service))
    monkeypatch.setattr(builder, "DATA", tmp_path)
    rebuilt = builder.build(snapshot, "fixture", upstream={"resources": resources, "version": "fixture", "revision": "test"})
    bundled = mapping(json.loads(builder.LIBRARY.read_text()))
    for catalog in (rebuilt, bundled):
        paths = mapping(mapping(catalog["resources"])["v1/Service"])
        record = mapping(mapping(catalog["domains"])[str(paths[f"spec/{field}"])])
        validator = validators.Draft7Validator(mapping(record["schema"]))
        for value in [*allowed, "", None]:
            assert validator.is_valid(value), value
        for invalid in ["'", "[Ma", "Unknown", 0, False]:
            assert not validator.is_valid(json_value(invalid)), invalid
        assert row["id"] in sequence(record["sources"])
        assert mapping(sequence(record["evidence"])[0])["type_field"] == row["type_field"]
    paths = mapping(mapping(rebuilt["resources"])["v1/Service"])
    unrelated = mapping(mapping(rebuilt["domains"])[str(paths[f"unrelated/{field}"])])
    assert validators.Draft7Validator(mapping(unrelated["schema"])).is_valid("'")


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


def test_reviewed_supplements_follow_type_references_not_descriptions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Rebuild identical prose at two API types without leaking the selector's name constraint.

    Args:
        tmp_path (Path): Minimal OpenAPI source and standalone schema snapshot.
        monkeypatch (pytest.MonkeyPatch): Select a small supplement inventory.

    Returns:
        None: Exact references carry supplements through arrays; unrelated same-description fields remain unrestricted.
    """
    reviewed = [
        mapping(row)
        for row in sequence(json.loads((builder.DATA / "reviewed-domains.json").read_text()))
        if mapping(row)["id"] == "secretkeyselector.name"
    ]
    row = reviewed[0]
    selector: dict[str, object] = {"type": "object", "properties": {"name": {"type": "string", "description": row["description"]}}}
    # These structurally identical definitions have different validators in Kubernetes.
    local_reference = copy.deepcopy(selector)
    definitions: dict[str, object] = {
        "io.k8s.api.core.v1.SecretKeySelector": selector,
        "io.k8s.api.core.v1.LocalObjectReference": local_reference,
        "io.k8s.api.core.v1.Pod": {
            "x-kubernetes-group-version-kind": [{"group": "", "version": "v1", "kind": "Pod"}],
            "type": "object",
            "properties": {
                "imagePullSecrets": {"type": "array", "items": {"$ref": "#/definitions/io.k8s.api.core.v1.LocalObjectReference"}},
                "secretKeys": {"type": "array", "items": {"$ref": "#/definitions/io.k8s.api.core.v1.SecretKeySelector"}},
            },
        },
    }
    source = tmp_path / "api/openapi-spec/swagger.json"
    source.parent.mkdir(parents=True)
    source.write_text(json.dumps({"definitions": definitions}))
    (tmp_path / "reviewed-domains.json").write_text(json.dumps(reviewed))
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    (snapshot / "secretkeyselector.json").write_text(json.dumps(selector))
    pod = mapping(copy.deepcopy(definitions["io.k8s.api.core.v1.Pod"]))
    mapping(pod["properties"]).update(
        imagePullSecrets={"type": "array", "items": local_reference}, secretKeys={"type": "array", "items": selector}
    )
    (snapshot / "pod.json").write_text(json.dumps(pod))
    monkeypatch.setattr(builder, "DATA", tmp_path)
    extracted: dict[str, object] = {"fields": {}, "profiles": {"dns1123-subdomain": {"schema": row["schema"]}}}
    before = copy.deepcopy(extracted)
    resources = sources.destinations(tmp_path, extracted, reviewed=reviewed)
    assert extracted == before
    assert set(mapping(resources["v1/Pod"])) == {"secretKeys/*/name"}
    catalog = builder.build(snapshot, "fixture", upstream={"resources": resources, "version": "fixture", "revision": "test"})
    paths = mapping(mapping(catalog["resources"])["v1/Pod"])
    domains = mapping(catalog["domains"])
    reference = mapping(domains[str(paths["imagePullSecrets/*/name"])])
    secret = mapping(domains[str(paths["secretKeys/*/name"])])
    assert reference == {"schema": {"type": "string"}, "sources": ["json-schema"]}
    assert row["id"] in sequence(secret["sources"])
    validator = validators.Draft7Validator(mapping(secret["schema"]))
    assert validator.is_valid("config.v1")
    assert not validator.is_valid("")
    assert not validator.is_valid(">0")
    assert mapping(sequence(secret["evidence"])[0])["type_field"] == row["type_field"]
    # Flattened schemas alone cannot establish API type identity, even with identical prose and shape.
    plain = builder.build(snapshot, "fixture")
    plain_paths = mapping(mapping(plain["resources"])["v1/Pod"])
    assert mapping(mapping(plain["domains"])[str(plain_paths["secretKeys/*/name"])])["schema"] == {"type": "string"}
    mapping(mapping(selector["properties"])["name"])["description"] = "Changed upstream description"
    source.write_text(json.dumps({"definitions": definitions}))
    with pytest.raises(ValueError, match="Source description changed"):
        sources.destinations(tmp_path, extracted, reviewed=reviewed)
    del definitions["io.k8s.api.core.v1.SecretKeySelector"]
    source.write_text(json.dumps({"definitions": definitions}))
    with pytest.raises(ValueError, match="Reviewed API field missing"):
        sources.destinations(tmp_path, extracted, reviewed=reviewed)


@pytest.mark.parametrize(
    ("identity", "prefix"),
    [("v1/Pod", "spec"), ("apps/v1/Deployment", "spec/template/spec"), ("batch/v1/CronJob", "spec/jobTemplate/spec/template/spec")],
)
def test_bundled_catalog_preserves_windows_mounts_and_reference_types(identity: str, prefix: str) -> None:
    """
    Check released domains across Pod resources and embedded Pod templates.

    Args:
        identity (str): Resource API identity.
        prefix (str): Resource path to the Pod spec.

    Returns:
        None: Windows and Unix mounts pass, empty mounts fail, and Secret bounds stay on their API types.
    """
    catalog = mapping(json.loads(builder.LIBRARY.read_text()))
    paths = mapping(mapping(catalog["resources"])[identity])
    domains = mapping(catalog["domains"])
    mount = mapping(domains[str(paths[f"{prefix}/containers/*/volumeMounts/*/mountPath"])])
    schema = mapping(mount["schema"])
    validators.Draft7Validator.check_schema(schema)
    validator = validators.Draft7Validator(schema)
    for value in ("/var/run/config", r"C:\data", "C:/data"):
        assert validator.is_valid(value), value
    assert not validator.is_valid("")
    assert "volumemount.mountPath" in sequence(mount["sources"])
    for path, valid_empty in (("imagePullSecrets/*/name", True), ("containers/*/env/*/valueFrom/secretKeyRef/name", False)):
        record = mapping(domains[str(paths[f"{prefix}/{path}"])])
        assert validators.Draft7Validator(mapping(record["schema"])).is_valid("") == valid_empty
        assert ("secretkeyselector.name" in sequence(record["sources"])) != valid_empty


@pytest.mark.parametrize("version", ["1.35.0", "1.34.0"])
def test_live_schema_cache_never_matches_supplements_by_description(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, version: str) -> None:
    """
    Apply exact catalog destinations only for the selected Kubernetes version during runtime lookup.

    Args:
        tmp_path (Path): Local schema cache containing deliberately repeated descriptions.
        monkeypatch (pytest.MonkeyPatch): Activate the cache without source downloads or catalog rebuilding.
        version (str): Matching or different Kubernetes schema version.

    Returns:
        None: Reference-name bounds do not leak to unrelated fields or across versions; Windows paths remain usable.
    """
    reviewed = {str(mapping(row)["id"]): mapping(row) for row in sequence(json.loads((builder.DATA / "reviewed-domains.json").read_text()))}
    paths = {
        "spec/imagePullSecrets/*/name": "secretkeyselector.name",
        "spec/containers/*/env/*/valueFrom/secretKeyRef/name": "secretkeyselector.name",
        "spec/containers/*/volumeMounts/*/mountPath": "volumemount.mountPath",
        "unrelated": "secretkeyselector.name",
    }
    root: dict[str, object] = {}
    for path, supplement in paths.items():
        node = root
        for part in path.split("/"):
            if part == "*":
                node["type"] = "array"
                node = mapping(node.setdefault("items", {}))
            else:
                node["type"] = "object"
                node = mapping(mapping(node.setdefault("properties", {})).setdefault(part, {}))
        node.update(type="string", description=reviewed[supplement]["description"])
    (tmp_path / "pod-v1.json").write_text(json.dumps(root))
    monkeypatch.setenv("HYPOTHESIS_HELM_CONFORMITY", json.dumps({"version": version, "schemas": str(tmp_path)}))
    for path in paths:
        found = destination("v1/Pod", tuple(path.split("/")))
        assert found is not None
        schema, provenance = found
        assert "+reviewed:" not in provenance
        validator = validators.Draft7Validator(schema)
        bound = version == "1.35.0" and path not in {"spec/imagePullSecrets/*/name", "unrelated"}
        assert validator.is_valid("") is not bound
        if path.endswith("mountPath"):
            assert validator.is_valid(r"C:\data")
        elif bound:
            assert not validator.is_valid(">0")
        else:
            assert validator.is_valid(">0")


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
