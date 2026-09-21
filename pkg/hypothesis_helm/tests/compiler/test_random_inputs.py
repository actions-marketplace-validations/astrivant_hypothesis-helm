"""
Compare synthetic random inputs, native Helm scopes, shrinking, and exact replay.
"""

import json
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import given, seed, settings
from hypothesis import strategies as st
from hypothesis.strategies import DataObject

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.testing.runner import check_chart
from hypothesis_helm.compiler.randomness.model import CURRENT, RandomInputs, domain
from hypothesis_helm.compiler.randomness.rendering import enabled
from hypothesis_helm.compiler.randomness.toolchain import build
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.exceptions.rendering import RandomInputUnavailable, RenderFailure
from hypothesis_helm.schemas.configuration.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.contracts import mapping, sequence


@pytest.fixture
def random_chart(tmp_path: Path) -> Chart:
    """
    Prepare the pinned renderer and a closed-schema chart containing no synthetic values keys.

    Args:
        tmp_path (Path): Chart and test artifact directory.

    Returns:
        Chart: Native chart with a configurable random-string length.
    """
    try:
        build()
    except ValueError:
        pytest.skip("Build the optional renderer with hypothesis-helm-renderer --build before running native random-input tests")
    chart = tmp_path / "chart"
    chart.mkdir()
    (chart / "templates").mkdir()
    (chart / "Chart.yaml").write_text("apiVersion: v2\nname: random-test\nversion: 0.1.0\n")
    (chart / "values.yaml").write_text("count: 3\n")
    (chart / "values.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {"count": {"type": "integer", "minimum": 0, "maximum": 8}},
            }
        )
    )
    return Chart.load(chart)


def template(chart: Chart, expression: str) -> None:
    """
    Place a template expression in a ConfigMap data field for native validation.

    Args:
        chart (Chart): Source fixture.
        expression (str): Go template expression or literal YAML field content.

    Returns:
        None: One renderable resource exists.
    """
    (chart.path / "templates/output.yaml").write_text(
        dedent(f"""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: random-test
        data:
          token: {expression}
        """).lstrip()
    )


def configure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, text: str = "hypothesis:\n  random_inputs: true\n") -> None:
    """
    Install an explicit generation policy for one integration test.

    Args:
        tmp_path (Path): Configuration directory.
        monkeypatch (pytest.MonkeyPatch): Restore policy after testing.
        text (str): Local configuration content.

    Returns:
        None: Subsequent source and worker reads see the selected policy.
    """
    config = tmp_path / "random-policy.yaml"
    config.write_text(text)
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(config)))
    refresh_env()


def test_independent_calls_and_variable_reuse(random_chart: Chart) -> None:
    """
    Preserve helper and loop scopes while each invocation receives its own draw.

    Args:
        random_chart (Chart): Prepared native renderer fixture.

    Returns:
        None: Reused variables remain identical, separate calls differ, and replay reproduces every manifest.
    """
    (random_chart.path / "templates/output.yaml").write_text(
        dedent("""
        {{- define "token" -}}{{ randAlphaNum . }}{{- end -}}
        {{- $token := randAlphaNum (.Values.count | int) -}}
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: random-test
        data:
          first: {{ $token | quote }}
          again: {{ $token | quote }}
        {{ range $i := until 2 }}
          loop{{ $i }}: {{ include "token" 3 | quote }}
        {{ end }}
          left: {{ randAlphaNum 3 | quote }}
          right: {{ randAlphaNum 3 | quote }}
        """).lstrip()
    )
    original = (random_chart.path / "templates/output.yaml").read_bytes()
    draws = iter(["0Az", "B11", "c22", "D33", "e44"])
    case = RandomInputs(lambda strategy, label: next(draws))
    with case:
        result = render(random_chart, {}, stream=False)
    assert mapping(result[0]["data"]) == {
        "first": "0Az",
        "again": "0Az",
        "loop0": "B11",
        "loop1": "c22",
        "left": "D33",
        "right": "e44",
    }
    assert len(case.records) == len({str(row["path"]) for row in case.records}) == 5
    assert any("output.yaml" in str(row["path"]) for row in case.records)
    with RandomInputs.from_document(case.document()):
        assert render(random_chart, {}, stream=False) == result
    assert (random_chart.path / "templates/output.yaml").read_bytes() == original
    assert CURRENT.get() is None


@pytest.mark.parametrize("count", [0, -1])
def test_nonpositive_native_counts(random_chart: Chart, count: int) -> None:
    """
    Preserve Sprig's empty result for zero and negative counts without requesting an impossible draw.

    Args:
        random_chart (Chart): Native renderer fixture.
        count (int): Nonpositive literal argument.

    Returns:
        None: Native and controlled results agree with no synthetic input consumed.
    """
    template(random_chart, "{{ randAlphaNum " + str(count) + " | quote }}")
    native = render(random_chart, {}, stream=False)
    with RandomInputs() as case:
        assert render(random_chart, {}, stream=False) == native
    assert case.records == []


@pytest.mark.parametrize("expression", ['{{ randAlphaNum "3" }}', "{{ randAlphaNum }}", "{{ randAlphaNum 1 2 }}"])
def test_argument_errors_are_not_hidden(random_chart: Chart, expression: str) -> None:
    """
    Retain native arity and integer argument validation after assigning synthetic call identities.

    Args:
        random_chart (Chart): Native renderer fixture.
        expression (str): Invalid call accepted by the template parser but rejected during execution.

    Returns:
        None: Both renderers retain the chart failure.
    """
    template(random_chart, expression)
    with pytest.raises(RenderFailure):
        render(random_chart, {}, stream=False)
    with pytest.raises(RenderFailure), RandomInputs():
        render(random_chart, {}, stream=False)


def test_tpl_calls_are_recorded(random_chart: Chart) -> None:
    """
    Instrument generated template code through Helm's inherited function map.

    Args:
        random_chart (Chart): Native renderer fixture.

    Returns:
        None: A dynamic call is independent and honestly labeled when no static source position is available.
    """
    template(random_chart, '{{ tpl "{{ randAlphaNum 3 }}" . | quote }}')
    with RandomInputs(lambda strategy, label: "Ab1") as case:
        result = render(random_chart, {}, stream=False)
    assert mapping(result[0]["data"])["token"] == "Ab1"
    assert "dynamic:randAlphaNum" in str(case.records[0]["path"])


def test_replay_rejects_wrong_domain_and_control_flow(random_chart: Chart) -> None:
    """
    Reject changed lengths, missing draws, extra draws and impossible characters as replay errors.

    Args:
        random_chart (Chart): Native renderer fixture.

    Returns:
        None: None of these mismatches becomes a confirmed chart defect.
    """
    template(random_chart, "{{ randAlphaNum (.Values.count | int) | quote }}")
    with RandomInputs() as case:
        render(random_chart, {}, stream=False)
    for draws in ([], [{**case.records[0], "value": "!00"}], [*case.records, *case.records]):
        with pytest.raises(ValueError), RandomInputs(replay=draws):
            render(random_chart, {}, stream=False)
    with pytest.raises(ValueError), RandomInputs(replay=case.records):
        render(random_chart, {"count": 4}, stream=False)


def test_seeded_shrinkable_draws(random_chart: Chart) -> None:
    """
    Let Hypothesis own generation and replay across repeated seeds without changing the function's domain.

    Args:
        random_chart (Chart): Native renderer fixture.

    Returns:
        None: Fixed seeds reproduce the same sampled output sequence and every length remains exact.
    """
    template(random_chart, "{{ randAlphaNum 3 | quote }}")

    def collect() -> list[str]:
        """
        Replay one seed into its own result collection.

        Returns:
            list[str]: Observed native outputs in generation order.
        """
        observed: list[str] = []

        @seed(13)
        @settings(max_examples=5, deadline=None, database=None)
        @given(data=st.data())
        def exercise(data: DataObject) -> None:
            """
            Draw inside the active property example.

            Args:
                data (DataObject): Replayable Hypothesis draw context.

            Returns:
                None: The renderer consumed this example's exact draw.
            """
            with RandomInputs(lambda strategy, label: data.draw(strategy, label=label)):
                observed.append(str(mapping(render(random_chart, {}, stream=False)[0]["data"])["token"]))

        exercise()
        return observed

    results = [collect(), collect()]
    assert results[0] == results[1]
    assert len(set(results[0])) > 1
    assert all(len(value) == 3 for value in results[0])


def test_scan_failures_save_synthetic_replay(random_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Find and shrink a chart defect driven only by random output and preserve replay data beside values.

    Args:
        random_chart (Chart): Native renderer fixture.
        tmp_path (Path): Policy and artifact directory.
        monkeypatch (pytest.MonkeyPatch): Install the opt-in renderer policy.

    Returns:
        None: Reported synthetic inputs reproduce the failure with no invented values keys.
    """
    template(
        random_chart, '{{ $token := randAlphaNum 1 }}{{ if ne $token "0" }}{{ fail "random branch defect" }}{{ end }}{{ $token | quote }}'
    )
    config = tmp_path / "policy.yaml"
    config.write_text("hypothesis:\n  random_inputs: true\n")
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(config)))
    refresh_env()
    result = check_chart(random_chart, max_examples=12, random_seed=4, artifact_dir=tmp_path / "artifacts")
    assert result["status"] == "failed"
    assert "random branch defect" in str(result["error"])
    artifact = tmp_path / "artifacts/random-inputs.json"
    replay = json.loads(artifact.read_text())
    assert replay == result["random_inputs"]
    assert mapping(sequence(replay["draws"])[0])["value"] != "0"
    with pytest.raises(RenderFailure, match="random branch defect"), RandomInputs.from_document(replay):
        render(random_chart, mapping(result["values"]), stream=False)


@given(data=st.data(), length=st.integers(min_value=-2, max_value=6))
def test_native_domain_has_no_character_policy_restrictions(data: DataObject, length: int) -> None:
    """
    Retain all source outputs even when a user's ordinary values-string policy would restrict them.

    Args:
        data (DataObject): Property draw context.
        length (int): Native source length argument.

    Returns:
        None: The source domain permits uppercase and digits and handles the empty boundary.
    """
    value = data.draw(domain(length))
    assert len(value) == max(0, length)
    assert value.isascii()
    assert not value or value.isalnum()


@pytest.mark.parametrize("jobs", [1, 2])
def test_empty_values_chart_has_a_random_property(random_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int) -> None:
    """
    Reach random-only failures in serial and multi-process path scans with no ordinary paths.

    Args:
        random_chart (Chart): Native chart fixture.
        tmp_path (Path): Artifact directory.
        monkeypatch (pytest.MonkeyPatch): Scoped renderer mode.
        jobs (int): Local path worker count.

    Returns:
        None: The synthetic root property is scheduled and preserves a replayable counterexample.
    """
    from hypothesis_helm.charts.testing.paths import check_paths

    template(random_chart, '{{ $v := randAlphaNum 1 }}{{ if ne $v "0" }}{{ fail "random-only defect" }}{{ end }}{{ $v | quote }}')
    (random_chart.path / "values.yaml").write_text("{}\n")
    (random_chart.path / "values.schema.json").write_text('{"type":"object","additionalProperties":false}')
    configure(tmp_path, monkeypatch)
    result = check_paths(
        Chart.load(random_chart.path), budget=45, max_examples=10, seed=4, helm="helm", timeout=10, artifacts=tmp_path / "scan", jobs=jobs
    )
    assert result["status"] == "failed", result
    assert mapping(result["traversal"])["visited_paths"] == 1
    phases = [mapping(row) for row in sequence(result["phases"]) if mapping(row).get("random_inputs")]
    assert phases and "random-only defect" in str(phases[0]["error"])
    assert sequence(mapping(phases[0]["random_inputs"])["draws"])


def test_saved_suite_preserves_renderer_mode(random_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep synthetic properties and settings when a generated suite runs without its original config.

    Args:
        random_chart (Chart): Native chart fixture.
        tmp_path (Path): Generated suite destination.
        monkeypatch (pytest.MonkeyPatch): Remove the original policy after generation.

    Returns:
        None: Frozen suite policy still enables the renderer and exposes the root property.
    """
    from hypothesis_helm.charts.suites.generate import generate_tests
    from hypothesis_helm.charts.suites.runtime import prepared_chart

    template(random_chart, "{{ randAlphaNum 3 | quote }}")
    configure(tmp_path, monkeypatch)
    directory = tmp_path / "suite"
    generate_tests(random_chart, directory, max_examples=5)
    inventory = json.loads((directory / "paths.json").read_text())
    assert any(row["path"] == [] and row["origin"] == "renderer-randomness" for row in inventory["paths"])
    monkeypatch.delenv(ENVIRONMENT)
    refresh_env()
    with prepared_chart(random_chart.path, directory) as chart:
        assert enabled(chart)
        assert mapping(render(chart, {}, stream=False)[0]["data"])["token"] == "000"


@pytest.mark.parametrize("jobs", [1, 2])
def test_finite_failures_retain_random_inputs(random_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int) -> None:
    """
    Preserve worker draw tapes when later manifest validation fails on the coordinator.

    Args:
        random_chart (Chart): Finite fixture with count 0 through 8.
        tmp_path (Path): Policy and artifacts.
        monkeypatch (pytest.MonkeyPatch): Opt into deterministic representatives for finite plans.
        jobs (int): Number of parallel render workers.

    Returns:
        None: Serial and parallel plans produce a replayable failure without claiming random-space exhaustion.
    """
    template(random_chart, "{{ randAlphaNum (.Values.count | int) | quote }}")
    configure(tmp_path, monkeypatch)

    def reject_output(resources: list[dict[str, object]]) -> None:
        """
        Fail after rendering so the coordinator must retain the worker's tape.

        Args:
            resources (list[dict[str, object]]): Validated native manifests.

        Returns:
            None: This assertion always fails for a recorded nonempty token.
        """
        if len(str(mapping(resources[0]["data"])["token"])) not in (0, 3):
            raise AssertionError("coordinator assertion")

    result = check_chart(random_chart, exhaustive=True, jobs=jobs, properties=(reject_output,), artifact_dir=tmp_path / "finite")
    assert result["status"] == "failed", result
    tape = mapping(result["random_inputs"])
    assert sequence(tape["draws"])
    assert mapping(result["renderer_randomness"])["random_space_exhaustive"] is False
    with RandomInputs.from_document(tape):
        assert mapping(render(random_chart, mapping(result["values"]), stream=False)[0]["data"])["token"]


@pytest.mark.parametrize("expression", ["{{ now | quote }}", "{{ randAlpha 3 | quote }}", "{{ randAlphaNum 5 | quote }}"])
def test_unsupported_effects_and_budgets_are_not_chart_defects(
    random_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, expression: str
) -> None:
    """
    Report instrumentation limits as unavailable, distinct from a broken chart.

    Args:
        random_chart (Chart): Native fixture.
        tmp_path (Path): Policy and scan destination.
        monkeypatch (pytest.MonkeyPatch): Set the optional mode and a small character limit.
        expression (str): External effect or over-budget random source.

    Returns:
        None: Whole-document and path scans retain an explicit unavailable result.
    """
    from hypothesis_helm.charts.testing.paths import check_paths

    template(random_chart, expression)
    configure(tmp_path, monkeypatch, "hypothesis:\n  random_inputs: true\ncompiler:\n  max_string_chars: 4\n")
    result = check_chart(random_chart, max_examples=2)
    assert result["status"] == "unavailable", result
    assert "error" not in result
    scanned = check_paths(random_chart, budget=20, max_examples=2, seed=0, helm="helm", timeout=10, artifacts=tmp_path / "unavailable")
    assert scanned["status"] == "unavailable", scanned


def test_replay_verifies_source_and_values(random_chart: Chart) -> None:
    """
    Refuse replay against different source or inputs even when draw lengths would still match.

    Args:
        random_chart (Chart): Native chart fixture.

    Returns:
        None: Context fingerprints detect changes independently of the draw tape.
    """
    template(random_chart, "{{ randAlphaNum 3 | quote }}")
    with RandomInputs() as case:
        render(random_chart, {}, stream=False)
    with pytest.raises(RandomInputUnavailable, match="context changed"), RandomInputs.from_document(case.document()):
        render(random_chart, {"count": 3}, stream=False)
    template(random_chart, "{{ randAlphaNum 3 | lower | quote }}")
    with pytest.raises(RandomInputUnavailable, match="context changed"), RandomInputs.from_document(case.document()):
        render(random_chart, {}, stream=False)


def test_chart_scoped_configuration(random_chart: Chart, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Resolve chart-level overrides and reject invalid or field-level instrumentation settings.

    Args:
        random_chart (Chart): Named test chart.
        tmp_path (Path): Configuration directory.
        monkeypatch (pytest.MonkeyPatch): Scoped configuration environment.

    Returns:
        None: Optional mode respects inheritance and validation rather than leaking across fields.
    """
    configure(
        tmp_path,
        monkeypatch,
        dedent("""
        hypothesis:
          random_inputs: true
        input_constraints:
          - charts: [random-test]
            path: $
            hypothesis:
              random_inputs: false
        """),
    )
    assert not enabled(random_chart)
    for invalid in (
        "hypothesis:\n  random_inputs: 1\n",
        "input_constraints:\n  - path: $.count\n    hypothesis:\n      random_inputs: true\n",
    ):
        with pytest.raises(ValueError):
            configure(tmp_path, monkeypatch, invalid)


def test_random_inputs_are_visible_in_reports() -> None:
    """
    Show synthetic call paths and exact strings beside the ordinary triggering values.

    Returns:
        None: A random-only counterexample is understandable without opening raw artifacts.
    """
    from hypothesis_helm.reporting.evidence.reproductions import failing_input, input_summary

    source: dict[str, object] = {
        "values": {},
        "random_inputs": {"draws": [{"path": '$render.random["output.yaml@1:3"][0]', "length": 3, "value": "00A"}]},
    }
    summary = "\n".join(input_summary(failing_input(source)))
    assert "Renderer random inputs" in summary and "output.yaml@1:3" in summary and '"00A"' in summary


def test_renderer_cli_replays_and_rejects_mismatches(random_chart: Chart, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Exercise the public replay command with success and actionable context mismatch output.

    Args:
        random_chart (Chart): Prepared chart fixture.
        tmp_path (Path): Saved artifact directory.
        capsys (pytest.CaptureFixture[str]): CLI output capture.

    Returns:
        None: Success emits YAML and a changed release produces a setup error without a traceback.
    """
    from hypothesis_helm.compiler.randomness.cli import main

    template(random_chart, "{{ randAlphaNum 3 | quote }}")
    with RandomInputs() as case:
        render(random_chart, {}, stream=False)
    values = tmp_path / "values.json"
    tape = tmp_path / "random-inputs.json"
    values.write_text("{}")
    tape.write_text(json.dumps(case.document()))
    arguments = [str(random_chart.path), "--values", str(values), "--random-inputs", str(tape)]
    assert main(arguments) == 0
    assert 'token: "000"' in capsys.readouterr().out
    assert main([*arguments, "--release", "changed"]) == 2
    diagnostic = capsys.readouterr().err
    assert "context changed" in diagnostic and "Traceback" not in diagnostic


def test_dependency_loading_order_does_not_change_replay(random_chart: Chart) -> None:
    """
    Fingerprint dependency sources independently of Helm loader map iteration order.

    Args:
        random_chart (Chart): Parent with four independently rendered child charts.

    Returns:
        None: Repeated fresh native processes reproduce five draws and all resources exactly.
    """
    template(random_chart, "{{ randAlphaNum 1 | quote }}")
    schema = json.loads((random_chart.path / "values.schema.json").read_text())
    for index in range(4):
        schema["properties"][f"child-{index}"] = {"type": "object"}
        child = random_chart.path / "charts" / f"child-{index}"
        (child / "templates").mkdir(parents=True)
        (child / "Chart.yaml").write_text(f"apiVersion: v2\nname: child-{index}\nversion: 0.1.0\n")
        (child / "values.yaml").write_text("{}\n")
        (child / "templates/output.yaml").write_text(
            dedent("""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: {{ .Chart.Name }}
            data:
              token: {{ randAlphaNum 1 | quote }}
            """).lstrip()
        )
    (random_chart.path / "values.schema.json").write_text(json.dumps(schema))
    random_chart = Chart.load(random_chart.path)
    with RandomInputs() as case:
        expected = render(random_chart, {}, stream=False)
    assert len(expected) == len(case.records) == 5
    for _ in range(8):
        with RandomInputs.from_document(case.document()):
            assert render(random_chart, {}, stream=False) == expected
