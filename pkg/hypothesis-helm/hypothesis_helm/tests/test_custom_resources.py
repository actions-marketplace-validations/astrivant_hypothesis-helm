"""
Exercise real Polyad custom resources through Helm rendering, generation, and validation.
"""

import json
import shutil
import subprocess
from contextlib import nullcontext
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from jsonschema import validators

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.generate import generate_tests
from hypothesis_helm.charts.generated import prepared_chart
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.rendering import RenderFailure, render, validate_resources
from hypothesis_helm.charts.runner import check_chart
from hypothesis_helm.execution.render_hashes import RenderHashes
from hypothesis_helm.schemas import conformity
from hypothesis_helm.schemas.contracts import json_value, mapping
from hypothesis_helm.schemas.policy import ENVIRONMENT, load_policy

FIXTURE = Path(__file__).parent / "fixtures" / "polyad-gate"
IDENTITY = "polyad.astrivant.com/v1alpha1/Gate"
pytestmark = [pytest.mark.integration, pytest.mark.skipif(shutil.which("helm") is None, reason="Helm is required")]


@pytest.fixture
def polyad_chart(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Chart:
    """
    Load the pinned Polyad renderer and resolve its explicit resource schema.

    Args:
        tmp_path (Path): Isolated chart and artifact directory.
        monkeypatch (pytest.MonkeyPatch): Restore the caller's generation policy.

    Returns:
        Chart: Local snapshot with the real Gate schema and helper templates.
    """
    path = tmp_path / "polyad"
    shutil.copytree(FIXTURE, path)
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(path / ".hypothesis-helm.yaml")))
    return Chart.load(path)


def direct_chart(path: Path) -> Chart:
    """
    Map a deliberately broad integer input directly to the real Gate's delay field.

    Args:
        path (Path): New chart directory.

    Returns:
        Chart: Conditional custom resource alongside a built-in ConfigMap.
    """
    (path / "templates").mkdir(parents=True)
    (path / "Chart.yaml").write_text(
        dedent("""
        apiVersion: v2
        name: gate-direct
        version: 0.1.0
        """).lstrip()
    )
    (path / "values.yaml").write_text(yamlio.dump({"enabled": True, "delay": 1}))
    (path / "values.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["enabled", "delay"],
                "properties": {"enabled": {"type": "boolean"}, "delay": {"type": "integer"}},
            }
        )
    )
    (path / "templates" / "gate.yaml").write_text(
        dedent("""
        {{ if .Values.enabled }}
        apiVersion: polyad.astrivant.com/v1alpha1
        kind: Gate
        metadata:
          name: wait
        spec:
          delaySeconds: {{ .Values.delay }}
        {{ end }}
        """).lstrip()
    )
    (path / "templates" / "configmap.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: companion
        data:
          ready: "true"
        """).lstrip()
    )
    return Chart.load(path)


@pytest.mark.parametrize("delay, expected", [(0, 0), (0.5, 0.5), (315360000, 315360000), ("{{ .Values.variables.delay }}", 7)])
def test_polyad_helpers_render_valid_resources(polyad_chart: Chart, delay: object, expected: float) -> None:
    """
    Render real helpers and tpl references at both accepted numeric boundaries.

    Args:
        polyad_chart (Chart): Pinned real chart and resource contract.
        delay (object): Literal or templated input to the upstream renderer.
        expected (float): Resolved delay in the rendered Gate.

    Returns:
        None: The custom resource passes validation with the expected identity and value.
    """
    resources = render(polyad_chart, {"variables": {"delay": 7}, "gates": {"wait": {"spec": {"delaySeconds": delay}}}})
    assert len(resources) == 1
    resource = resources[0]
    assert f"{resource['apiVersion']}/{resource['kind']}" == IDENTITY
    assert mapping(resource["metadata"]) == {"name": "wait", "namespace": "default"}
    assert mapping(resource["spec"])["delaySeconds"] == expected
    assert isinstance(mapping(resource["spec"])["delaySeconds"], (int, float))


@pytest.mark.parametrize("identity", [None, "polyad.astrivant.com/v1beta1/Gate"])
def test_crd_files_do_not_replace_explicit_resource_schemas(
    polyad_chart: Chart, monkeypatch: pytest.MonkeyPatch, identity: str | None
) -> None:
    """
    Reject missing and wrong-version contracts even when the chart bundles the CRD.

    Args:
        polyad_chart (Chart): Chart containing both CRD definitions and custom-resource templates.
        monkeypatch (pytest.MonkeyPatch): Replace the supplied schema registration.
        identity (str | None): Missing registration or the wrong API version.

    Returns:
        None: Successful Helm rendering cannot hide a missing output contract.
    """
    schema = json.loads((polyad_chart.path / "schemas" / "gate.json").read_text())
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"resource_schemas": {identity: schema} if identity else {}}))
    with pytest.raises(RenderFailure, match="requires an explicit JSON schema") as caught:
        render(polyad_chart, {})
    assert caught.value.code == "HH1108"


def test_custom_resource_constraints_guide_generated_values(polyad_chart: Chart, tmp_path: Path) -> None:
    """
    Narrow direct input mappings and render generated candidates against the real schema.

    Args:
        polyad_chart (Chart): Fixture installing the Gate resource policy.
        tmp_path (Path): Direct-mapping chart directory.

    Returns:
        None: Active Gate delays stay bounded while disabled branches keep their input freedom.
    """
    chart = direct_chart(tmp_path / "direct")
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid({"enabled": True, "delay": 0})
    assert validator.is_valid({"enabled": True, "delay": 315360000})
    assert not validator.is_valid({"enabled": True, "delay": -1})
    assert not validator.is_valid({"enabled": True, "delay": 315360001})
    assert validator.is_valid({"enabled": False, "delay": -1})
    assert any(rule["source"] == "supplied-resource-schema" for rule in chart.input_domains().rules)

    @settings(max_examples=12, deadline=None, database=None, derandomize=True)
    @given(chart.strategy())
    def check(values: dict[str, object]) -> None:
        """
        Exercise generation and Helm's actual output with the same resource policy.

        Args:
            values (dict[str, object]): Generated configuration after destination constraints.

        Returns:
            None: All rendered resources validate and disabled Gates disappear.
        """
        assert validator.is_valid(json_value(values))
        resources = render(chart, values)
        gates = [resource for resource in resources if resource["kind"] == "Gate"]
        assert len(gates) == int(bool(values["enabled"]))
        if gates:
            assert mapping(gates[0]["spec"])["delaySeconds"] == values["delay"]

    check()


@pytest.mark.parametrize("delay", [-1, 315360001])
def test_invalid_rendered_custom_resources_fail(polyad_chart: Chart, tmp_path: Path, delay: int) -> None:
    """
    Catch output-contract violations even when values satisfy the chart's input schema.

    Args:
        polyad_chart (Chart): Fixture installing the Gate resource policy.
        tmp_path (Path): Direct-mapping chart directory.
        delay (int): Out-of-range value permitted by the deliberately broad input schema.

    Returns:
        None: Downstream validation reports HH1108 with the offending field.
    """
    chart = direct_chart(tmp_path / "direct")
    with pytest.raises(RenderFailure, match="delaySeconds") as caught:
        render(chart, {"delay": delay})
    assert caught.value.code == "HH1108"


def test_custom_resource_failure_records_reproducible_values(polyad_chart: Chart, tmp_path: Path) -> None:
    """
    Detect a template defect that turns a valid input into an invalid custom resource.

    Args:
        polyad_chart (Chart): Fixture installing the Gate resource policy.
        tmp_path (Path): Deliberately defective chart and failure artifacts.

    Returns:
        None: The runner records the schema error and exact input that produces it.
    """
    chart = direct_chart(tmp_path / "direct")
    template = chart.path / "templates" / "gate.yaml"
    template.write_text(template.read_text().replace("{{ .Values.delay }}", "{{ sub .Values.delay 1 }}"))
    chart = Chart.load(chart.path)
    values: dict[str, object] = {"enabled": True, "delay": 0}
    artifacts = tmp_path / "failure"
    result = check_chart(chart, input_strategy=st.just(values), max_examples=1, random_seed=0, artifact_dir=artifacts)
    assert result["status"] == "failed"
    assert result["code"] == "HH1108"
    assert result["values"] == values
    assert "delaySeconds" in str(result["error"])
    assert json.loads((artifacts / "values.json").read_text()) == values


def test_saved_suite_preserves_custom_resource_schema(polyad_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep the registered contract available after the caller's config and schema disappear.

    Args:
        polyad_chart (Chart): Pinned chart with a supplied resource schema.
        tmp_path (Path): Saved suite output.
        monkeypatch (pytest.MonkeyPatch): Remove the parent process policy.

    Returns:
        None: Saved schemas survive source removal, remain scoped, and invalidate reused validation when changed.
    """
    suite = tmp_path / "suite"
    generate_tests(polyad_chart, suite, max_examples=1)
    monkeypatch.delenv(ENVIRONMENT)
    (polyad_chart.path / ".hypothesis-helm.yaml").unlink()
    (polyad_chart.path / "schemas" / "gate.json").unlink()
    hashes = RenderHashes()
    with prepared_chart(polyad_chart.path, suite) as prepared:
        resource = render(prepared, {}, hashes=hashes)[0]
        render(prepared, {}, hashes=hashes)
        assert hashes.cache_hits == 1
        with pytest.raises(RenderFailure, match="HH1108"):
            validate_resources([{**resource, "spec": {"delaySeconds": -1}}])
    with pytest.raises(RenderFailure, match="requires an explicit JSON schema"):
        validate_resources([resource])
    snapshot = suite / "input-domains.json"
    document = json.loads(snapshot.read_text())
    document["resource_schemas"][IDENTITY]["properties"]["spec"]["properties"]["delaySeconds"]["minimum"] = 2
    snapshot.write_text(json.dumps(document))
    with prepared_chart(polyad_chart.path, suite) as prepared:
        with pytest.raises(RenderFailure, match="HH1108"):
            render(prepared, {}, hashes=hashes)
    assert hashes.cache_hits == 1


@pytest.mark.parametrize("saved", [False, True])
def test_mixed_bundle_keeps_builtin_validation(polyad_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, saved: bool) -> None:
    """
    Route built-ins to kubeconform while validating custom resources with their supplied contract.

    Args:
        polyad_chart (Chart): Fixture installing the custom-resource policy.
        tmp_path (Path): Mixed-resource chart and local schema location.
        monkeypatch (pytest.MonkeyPatch): Replace only the external validator boundary after rendering.
        saved (bool): Restore the custom schema from a generated suite instead of current configuration.

    Returns:
        None: Kubeconform receives the ConfigMap, rejects it, and does not request a Gate schema.
    """
    chart = direct_chart(tmp_path / "direct")
    suite = tmp_path / "suite"
    if saved:
        generate_tests(chart, suite, max_examples=1)
        monkeypatch.delenv(ENVIRONMENT)
    calls: list[str] = []

    def execute(self: object, command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """
        Observe validator stdin and simulate a failing built-in API check.

        Args:
            self (object): Process owner at the patched boundary.
            command (list[str]): Kubeconform invocation.
            **kwargs (object): Validator process options and manifest input.

        Returns:
            subprocess.CompletedProcess[str]: A built-in resource rejection.
        """
        assert command[0] == "kubeconform" and "-ignore-missing-schemas" not in command
        documents = list(yamlio.load_all(str(kwargs["input"])))
        assert len(documents) == 1 and mapping(documents[0])["kind"] == "ConfigMap"
        calls.append(str(kwargs["input"]))
        return subprocess.CompletedProcess(command, 1, "invalid ConfigMap", "")

    with prepared_chart(chart.path, suite) if saved else nullcontext(chart) as prepared:
        resources = render(prepared, {})
        monkeypatch.setenv(
            conformity.ENVIRONMENT,
            json.dumps({"version": "1.35.0", "schemas": str(tmp_path), "executable": "kubeconform"}),
        )
        monkeypatch.setattr("hypothesis_helm.schemas.conformity.Processes.run", execute)
        with pytest.raises(AssertionError, match="invalid ConfigMap"):
            conformity.validate("---\n".join(yamlio.dump(resource) for resource in resources), 10)
    assert len(calls) == 1
