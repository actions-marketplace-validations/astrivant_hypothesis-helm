"""
Exercise real Polyad custom resources through Helm rendering, generation, and validation.
"""

import json
import shutil
from contextlib import nullcontext
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.suites.generate import generate_tests
from hypothesis_helm.charts.suites.runtime import prepared_chart
from hypothesis_helm.charts.testing.rendering import render, validate_resources
from hypothesis_helm.charts.testing.runner import check_chart
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.cli import argument_parser
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.execution.state.render_hashes import RenderHashes
from hypothesis_helm.schemas.configuration.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.contracts import json_value, mapping
from hypothesis_helm.schemas.kubernetes import conformity
from hypothesis_helm.schemas.kubernetes.resources import strict_schemas, validate_custom
from hypothesis_helm.tests import FIXTURES

FIXTURE = FIXTURES / "polyad-gate"
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
    refresh_env()
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
@pytest.mark.parametrize("strict", [False, True])
def test_missing_custom_schemas_are_required_only_in_strict_mode(
    polyad_chart: Chart, monkeypatch: pytest.MonkeyPatch, identity: str | None, strict: bool
) -> None:
    """
    Skip unregistered custom schemas unless strict validation is requested.

    Args:
        polyad_chart (Chart): Chart containing both CRD definitions and custom-resource templates.
        monkeypatch (pytest.MonkeyPatch): Replace the supplied schema registration.
        identity (str | None): Missing registration or the wrong API version.
        strict (bool): Whether an exact registered contract is mandatory.

    Returns:
        None: Strict mode reports the missing contract; normal mode preserves the rendered resource.
    """
    schema = json.loads((polyad_chart.path / "schemas" / "gate.json").read_text())
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"resource_schemas": {identity: schema} if identity else {}, "strict": strict}))
    refresh_env()
    if strict:
        with pytest.raises(RenderFailure, match="requires an explicit JSON schema") as caught:
            render(polyad_chart, {})
        assert caught.value.code == "HH1108"
    else:
        resources = render(polyad_chart, {})
        assert resources and validate_custom(resources[0]) is None


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
    refresh_env()
    (polyad_chart.path / ".hypothesis-helm.yaml").unlink()
    (polyad_chart.path / "schemas" / "gate.json").unlink()
    hashes = RenderHashes()
    with prepared_chart(polyad_chart.path, suite) as prepared:
        resource = render(prepared, {}, hashes=hashes)[0]
        render(prepared, {}, hashes=hashes)
        assert hashes.cache_hits == 1
        with pytest.raises(RenderFailure, match="HH1108"):
            validate_resources([{**resource, "spec": {"delaySeconds": -1}}])
    validate_resources([resource])
    assert validate_custom(resource) is None
    snapshot = suite / "input-domains.json"
    document = json.loads(snapshot.read_text())
    document["resource_schemas"][IDENTITY]["properties"]["spec"]["properties"]["delaySeconds"]["minimum"] = 2
    snapshot.write_text(json.dumps(document))
    with prepared_chart(polyad_chart.path, suite) as prepared:
        with pytest.raises(RenderFailure, match="HH1108"):
            render(prepared, {}, hashes=hashes)
    assert hashes.cache_hits == 1


def test_strict_mode_survives_saved_suites_and_invalidates_render_reuse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Preserve strict schema policy across workers, saved suites, and manifest cache entries.

    Args:
        tmp_path (Path): Direct chart and generated suite directory.
        monkeypatch (pytest.MonkeyPatch): Switch the serialized worker policy between validation modes.

    Returns:
        None: Strict checks cannot reuse a schema-skipped render; explicit current settings override saved settings.
    """
    monkeypatch.setenv(ENVIRONMENT, "{}")
    refresh_env()
    chart = direct_chart(tmp_path / "chart")
    hashes = RenderHashes()
    assert len(render(chart, {}, hashes=hashes)) == 2
    render(chart, {}, hashes=hashes)
    assert hashes.cache_hits == 1
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"strict": True}))
    refresh_env()
    with pytest.raises(RenderFailure, match="requires an explicit JSON schema"):
        render(chart, {}, hashes=hashes)
    assert hashes.cache_hits == 1
    suite = tmp_path / "suite"
    generate_tests(chart, suite, max_examples=1)
    assert json.loads((suite / "input-domains.json").read_text())["strict"] is True
    monkeypatch.setenv(ENVIRONMENT, "{}")
    refresh_env()
    with prepared_chart(chart.path, suite) as prepared:
        assert strict_schemas()
        with pytest.raises(RenderFailure, match="requires an explicit JSON schema"):
            render(prepared, {})
    assert not strict_schemas()
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"strict": False}))
    refresh_env()
    with prepared_chart(chart.path, suite) as prepared:
        assert not strict_schemas()
        assert len(render(prepared, {})) == 2


def test_schema_skips_leave_builtin_validation_enabled(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Skip unknown custom resources in lists without skipping neighboring built-in checks.

    Args:
        tmp_path (Path): Local Kubernetes schema cache fixture.
        monkeypatch (pytest.MonkeyPatch): Select default or strict resource handling.

    Returns:
        None: Missing contracts skip normally, strict mode rejects them, and invalid ConfigMaps always fail.
    """
    custom = {"apiVersion": "grafana.integreatly.org/v1beta1", "kind": "Grafana", "metadata": {"name": "example"}}
    builtin = {"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": "example"}, "data": {"ready": False}}
    (tmp_path / "configmap-v1.json").write_text(
        json.dumps({"type": "object", "properties": {"data": {"type": "object", "additionalProperties": {"type": "string"}}}})
    )
    configuration = json.dumps({"version": "1.35.0", "schemas": str(tmp_path)})
    monkeypatch.setenv(ENVIRONMENT, "{}")
    refresh_env()
    validate_resources([custom])
    conformity.validate([custom], 10, configuration=configuration)
    with pytest.raises(AssertionError, match="ConfigMap.*ready"):
        conformity.validate([{"apiVersion": "v1", "kind": "List", "items": [custom, builtin]}], 10, configuration=configuration)
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"strict": True}))
    refresh_env()
    with pytest.raises(AssertionError, match="requires an explicit JSON schema"):
        conformity.validate([custom], 10, configuration=configuration)


def test_strict_cli_and_configuration(tmp_path: Path) -> None:
    """
    Keep missing-schema strictness independent from severity-based fail-fast settings.

    Args:
        tmp_path (Path): User configuration directory.

    Returns:
        None: All execution modes accept the override and reject invalid configuration types.
    """
    parser = argument_parser()
    for command in ("test", "scan", "run", "generate"):
        for option, expected in (("--strict", True), ("--no-strict", False)):
            assert parser.parse_args([command, "chart", option]).strict is expected
        assert parser.parse_args([command, "chart"]).strict is None
    config = tmp_path / "config.yaml"
    config.write_text("strict: true\n")
    assert load_policy(config)["strict"] is True
    assert load_policy(config, strict=False)["strict"] is False
    config.write_text('strict: "yes"\n')
    with pytest.raises(ValueError, match="strict must be a Boolean"):
        load_policy(config)


@pytest.mark.parametrize("saved", [False, True])
def test_mixed_bundle_keeps_builtin_validation(polyad_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, saved: bool) -> None:
    """
    Route built-ins to native schema validation while validating custom resources with their supplied contract.

    Args:
        polyad_chart (Chart): Fixture installing the custom-resource policy.
        tmp_path (Path): Mixed-resource chart and local schema location.
        monkeypatch (pytest.MonkeyPatch): Select local schema files after rendering.
        saved (bool): Restore the custom schema from a generated suite instead of current configuration.

    Returns:
        None: The native validator rejects the ConfigMap and does not request a Gate schema.
    """
    chart = direct_chart(tmp_path / "direct")
    suite = tmp_path / "suite"
    if saved:
        generate_tests(chart, suite, max_examples=1)
        monkeypatch.delenv(ENVIRONMENT)
        refresh_env()
    (tmp_path / "configmap-v1.json").write_text(
        json.dumps({"type": "object", "properties": {"data": {"properties": {"ready": {"const": "expected"}}}}})
    )
    with prepared_chart(chart.path, suite) if saved else nullcontext(chart) as prepared:
        resources = render(prepared, {})
        monkeypatch.setenv(
            conformity.ENVIRONMENT,
            json.dumps({"version": "1.35.0", "schemas": str(tmp_path)}),
        )
        refresh_env()
        with pytest.raises(AssertionError, match="ConfigMap.*ready"):
            conformity.validate("---\n".join(yamlio.dump(resource) for resource in resources), 10)
