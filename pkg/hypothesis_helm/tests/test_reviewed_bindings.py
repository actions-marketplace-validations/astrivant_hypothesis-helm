"""
Check versioned destination bindings through chart dependencies and native rendering.
"""

import hashlib
import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import given, settings
from hypothesis_helm_catalog.builder import DATA
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.suites.generate import coalesce
from hypothesis_helm.charts.testing.rendering import RenderFailure, render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.passes.input_bindings import reviewed_bindings
from hypothesis_helm.schemas.contracts import json_value, mapping, schema_strategy
from hypothesis_helm.schemas.domains import InputDomains


@pytest.fixture
def reviewed_chart(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Provide two reviewed source versions with one serialized destination mapping.

    Args:
        tmp_path (Path): Isolated source and catalog files.
        monkeypatch (pytest.MonkeyPatch): Select only the fixture's reviewed bindings.

    Returns:
        Path: Chart whose unrelated dynamic expression prevents full-file projection.
    """
    chart = tmp_path / "chart"
    (chart / "templates").mkdir(parents=True)
    (chart / "Chart.yaml").write_text("apiVersion: v2\nname: reviewed\nversion: 1.0.0\n")
    (chart / "values.yaml").write_text("annotations: {}\n")
    source = dedent("""
        {{- $clock := now }}
        apiVersion: v1
        kind: Service
        metadata:
          name: reviewed
          annotations: {{- .Values.annotations | toYaml | nindent 4 }}
        spec:
          ports:
            - port: 80
        """)
    (chart / "templates/service.yaml").write_text(source)
    binding = {
        "chart": "reviewed",
        "path": ["annotations"],
        "destination": "v1/Service:$.metadata.annotations",
        "quoted": False,
        "serialized": True,
        "reference": "reviewed test fixture",
    }
    records = [
        {**binding, "files": {"templates/service.yaml": digest}}
        for digest in ("outdated source", hashlib.sha256(source.encode()).hexdigest())
    ]
    (tmp_path / "chart-bindings.json").write_text(json.dumps(records))
    monkeypatch.setattr("hypothesis_helm.compiler.passes.input_bindings.DATA", tmp_path)
    return chart


def test_reviewed_versions_and_schema_availability(reviewed_chart: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Apply the matching version and decline changed source or unavailable destination schemas.

    Args:
        reviewed_chart (Path): Source with both stale and matching catalog records.
        monkeypatch (pytest.MonkeyPatch): Simulate a missing configured schema.

    Returns:
        None: Only verified source and available schema pairs constrain generated cases.
    """
    bindings, notes = reviewed_bindings(reviewed_chart)
    assert len(bindings) == 1 and not notes
    schema = mapping(bindings[0]["schema"])
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid({"note": "multiline\nconfiguration"})
    assert not validator.is_valid({"note": []})
    assert not validator.is_valid({"note": True})
    with monkeypatch.context() as patch:
        patch.setattr("hypothesis_helm.compiler.passes.input_bindings.destination", lambda *_: None)
        bindings, notes = reviewed_bindings(reviewed_chart)
        assert not bindings and any("schema unavailable" in str(note) for note in notes)
    template = reviewed_chart / "templates/service.yaml"
    template.write_text(template.read_text().replace("annotations:", "labels:"))
    bindings, notes = reviewed_bindings(reviewed_chart)
    assert not bindings and all("source changed" in str(note) for note in notes)


def test_reviewed_collection_domain_reaches_aliased_dependencies(reviewed_chart: Path, tmp_path: Path) -> None:
    """
    Constrain an entire generated dependency subtree without altering supplied defaults.

    Args:
        reviewed_chart (Path): Child with an opaque output helper and reviewed annotations.
        tmp_path (Path): Root chart destination.

    Returns:
        None: Annotations remain strings even when the parent selects the whole dependency map.
    """
    root = tmp_path / "parent"
    (root / "charts").mkdir(parents=True)
    shutil.copytree(reviewed_chart, root / "charts/reviewed")
    (root / "Chart.yaml").write_text(
        yamlio.dump(
            {
                "apiVersion": "v2",
                "name": "parent",
                "version": "1.0.0",
                "dependencies": [{"name": "reviewed", "alias": "backend", "version": "1.0.0"}],
            }
        )
    )
    (root / "values.yaml").write_text("{}\n")
    chart = Chart(root, {"type": "object"}, {})
    domains = InputDomains.build(chart)
    assert any(rule["path"] == ["backend", "annotations"] and rule.get("serialized") for rule in domains.rules)
    schema = domains.apply(coalesce(chart).schema)

    @settings(max_examples=30, deadline=None, database=None, derandomize=True)
    @given(schema_strategy(schema))
    def check(values: object) -> None:
        """
        Check dependency map values independently of the rule implementation.

        Args:
            values (object): One generated parent configuration.

        Returns:
            None: No array, Boolean or object is generated as an annotation value.
        """
        backend = mapping(mapping(values).get("backend", {}))
        annotations = mapping(backend.get("annotations") or {})
        assert all(value is None or isinstance(value, str) for value in annotations.values())

    check()
    assert chart.defaults == {}


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_annotation_shape_failure_matches_helm(reviewed_chart: Path) -> None:
    """
    Retain the native failure for supplied bad values while constraining generated values.

    Args:
        reviewed_chart (Path): Chart serializing annotations with toYaml.

    Returns:
        None: Arrays reproduce HH1109; ordinary multiline annotation text still renders.
    """
    chart = Chart(reviewed_chart, {"type": "object"}, {"annotations": {}})
    with pytest.raises(RenderFailure) as observed:
        render(chart, {"annotations": {"note": []}})
    assert observed.value.code == "HH1109"
    assert render(chart, {"annotations": {"note": "two\nlines"}})
    domains = InputDomains.build(chart)
    schema = domains.apply(coalesce(chart).schema)
    validator = validators.validator_for(schema)(schema)
    assert not validator.is_valid(json_value({"annotations": {"note": []}}))


def test_catalog_covers_scan_destinations() -> None:
    """
    Retain the source-backed bindings for the concrete scan regressions.

    Returns:
        None: Each reported destination has a reviewed binding, including MongoDB's older dependency release.
    """
    records = json.loads((DATA / "chart-bindings.json").read_text())
    paths = {(record["chart"], tuple(record["path"])) for record in records}
    assert {
        ("apache", ("service", "annotations")),
        ("redis", ("sentinel", "service", "headless", "annotations")),
        ("apisix", ("controlPlane", "extraConfigExistingConfigMap")),
        ("etcd", ("pdb", "minAvailable")),
    } <= paths
    assert any(record["chart"] == "mongodb" and "16.5.45" in record["reference"] for record in records)
