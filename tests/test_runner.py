import json
import os
import shutil
from pathlib import Path

import pytest
from hypothesis import given, settings
from jsonschema import validate

from hypothesis_helm import Chart, check_chart
from hypothesis_helm.cli import main
from hypothesis_helm.runner import RenderFailure, audit, merge_values, validate_resources

ROOT = Path(__file__).resolve().parents[1]


def test_strategy_is_schema_valid():
    chart = Chart.load(ROOT / "examples/workload")

    @settings(max_examples=20)
    @given(chart.strategy())
    def valid(values):
        validate(values, chart.schema)

    valid()


def test_audit_hidden_defaults_and_types():
    report = audit(Chart.load(ROOT / "examples/hidden-levers"))
    assert {tuple(f["path"]) for f in report["findings"] if f["issue"] == "undocumented"} == {
        ("secretSwitch",),
        ("other-switch",),
    }
    assert any(r["fallback"] for r in report["references"])
    assert not audit(Chart.load(ROOT / "examples/workload"))["findings"]


def test_merge():
    assert merge_values({"a": {"x": 1, "y": 2}, "b": [1]}, {"a": {"x": None}, "b": []}) == {
        "a": {"y": 2},
        "b": [],
    }


@pytest.mark.parametrize(
    "resource",
    [
        None,
        {},
        {"apiVersion": "v1", "kind": "ConfigMap"},
        {"apiVersion": "v1", "kind": "List", "items": None},
    ],
)
def test_bad_resources(resource):
    with pytest.raises(RenderFailure):
        validate_resources([resource])


def test_cli_error(capsys, tmp_path):
    assert main(["test", str(tmp_path)]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "error"


@pytest.mark.integration
@pytest.mark.skipif(not shutil.which("helm"), reason="Helm is required")
@pytest.mark.parametrize("name", ["configmap", "workload"])
def test_real_helm(name):
    report = check_chart(ROOT / "examples" / name, max_examples=12)
    assert report["status"] == "passed", report


@pytest.mark.integration
@pytest.mark.skipif(not shutil.which("helm"), reason="Helm is required")
def test_shrinks_and_saves_counterexample(tmp_path):
    report = check_chart(ROOT / "examples/broken", max_examples=20, artifact_dir=tmp_path)
    assert report["status"] == "failed"
    assert report["values"] == {"replicas": 0}
    assert json.loads((tmp_path / "values.json").read_text()) == report["values"]


@pytest.mark.integration
@pytest.mark.skipif(not shutil.which("helm"), reason="Helm is required")
def test_custom_property():
    def property(resources):
        assert resources[0]["kind"] == "Deployment", "expected Deployment"

    report = check_chart(ROOT / "examples/configmap", properties=(property,))
    assert report["status"] == "failed"
    assert "expected Deployment" in report["error"]


@pytest.mark.astrivant
def test_neighbor_astrivant_audit():
    path = Path(os.environ.get("ASTRIVANT_CHART", ROOT.parent / "astrivant/helm/astrivant"))
    if not path.exists():
        pytest.skip("neighboring Astrivant checkout unavailable")
    report = audit(Chart.load(path))
    assert any(r["path"] == ("networkPolicy", "dns", "namespace") for r in report["references"])
    assert report["findings"]  # This real-world schema currently has documentation gaps.


@pytest.mark.astrivant
@pytest.mark.integration
def test_neighbor_astrivant_render():
    path = os.environ.get("ASTRIVANT_CHART")
    if not path or not shutil.which("helm"):
        pytest.skip("set ASTRIVANT_CHART to opt into the full dependency-backed run")
    report = check_chart(path, max_examples=5)
    assert report["status"] == "passed", report
