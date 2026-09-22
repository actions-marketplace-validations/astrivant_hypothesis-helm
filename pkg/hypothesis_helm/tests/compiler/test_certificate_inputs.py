"""
Exercise native certificate generation, stable retries and exact replay through Helm.
"""

import copy
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render, render_output
from hypothesis_helm.charts.testing.runner import check_chart
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.randomness.certificates import CERTIFICATE_FUNCTIONS, CertificateInputs, CertificateStore
from hypothesis_helm.compiler.randomness.model import RandomInputs
from hypothesis_helm.compiler.randomness.toolchain import SOURCE, build
from hypothesis_helm.environment import env
from hypothesis_helm.exceptions.rendering import RandomInputUnavailable, RenderFailure
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.reporting.evidence.reproductions import failing_input, input_summary
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests.compiler.test_random_inputs import configure, template


@pytest.fixture
def certificate_chart(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Chart:
    """
    Prepare a strict native chart with finite certificate arguments.

    Args:
        tmp_path (Path): Source and artifact directory.
        monkeypatch (pytest.MonkeyPatch): Restore the renderer policy after testing.

    Returns:
        Chart: Isolated chart whose crypto results are retained for the current test.
    """
    try:
        build()
    except ValueError:
        pytest.skip("Go is required for certificate renderer integration tests")
    configure(tmp_path, monkeypatch)
    chart = tmp_path / "chart"
    (chart / "templates").mkdir(parents=True)
    (chart / "Chart.yaml").write_text("apiVersion: v2\nname: certificates\nversion: 0.1.0\n")
    (chart / "values.yaml").write_text("name: first\ndays: 1\n")
    (chart / "values.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {"name": {"enum": ["first", "second"]}, "days": {"enum": [0, 1, 2]}},
            }
        )
    )
    return Chart.load(chart)


def test_all_generators_and_native_certificate_type(certificate_chart: Chart) -> None:
    """
    Keep native objects compatible across signing, custom-certificate loading and reflection.

    Args:
        certificate_chart (Chart): Prepared strict chart.

    Returns:
        None: Every generator executes once and the complete manifest replays byte for byte.
    """
    (certificate_chart.path / "templates/output.yaml").write_text(
        dedent("""
        {{- $key := genPrivateKey "ecdsa" -}}
        {{- $token := randAlphaNum 3 -}}
        {{- $ca := genCA .Values.name (.Values.days | int) -}}
        {{- $caWithKey := genCAWithKey "second" 2 $key -}}
        {{- $imported := buildCustomCert ($ca.Cert | b64enc) ($ca.Key | b64enc) -}}
        {{- $leaf := genSignedCert "leaf" (list "127.0.0.1") (list "service.local") 1 $imported -}}
        {{- $leafWithKey := genSignedCertWithKey "leaf" nil nil 1 $caWithKey $key -}}
        {{- $self := genSelfSignedCert "self" nil nil 1 -}}
        {{- $selfWithKey := genSelfSignedCertWithKey "self" nil nil 1 $key -}}
        apiVersion: v1
        kind: Secret
        metadata:
          name: certificates
        stringData:
          token: {{ $token | quote }}
          ca: {{ $ca.Cert | quote }}
          leaf: {{ $leaf.Cert | quote }}
          key: {{ $key | quote }}
          sameKey: {{ eq $key $leafWithKey.Key | quote }}
          type: {{ typeOf $ca | quote }}
        """).lstrip()
    )
    with RandomInputs() as case:
        original = render_output(certificate_chart, {})
    assert {row["function"] for row in case.records if "function" in row} == CERTIFICATE_FUNCTIONS
    assert case.records[1]["value"] == "000"
    assert "sprig.certificate" in original
    assert 'sameKey: "true"' in original
    assert case.document()["format"] == "helm-random-inputs-v2"
    # Replay on a fresh Chart proves it does not depend on the live observation cache.
    with RandomInputs.from_document(case.document()) as replay:
        assert render_output(Chart.load(certificate_chart.path), {}) == original
    assert replay.records == case.records


def test_retries_are_stable_but_new_arguments_generate(certificate_chart: Chart) -> None:
    """
    Retain the same native outcome through retries without ignoring changed certificate arguments.

    Args:
        certificate_chart (Chart): Prepared strict chart.

    Returns:
        None: Retries match, fresh chart runs differ, and changed names or validity create distinct records.
    """
    template(certificate_chart, "{{ (genCA .Values.name (.Values.days | int)).Cert | quote }}")
    with RandomInputs() as original:
        first = render(certificate_chart, {})
    with RandomInputs() as retry:
        assert render(certificate_chart, {}) == first
    assert original.records == retry.records
    changes: list[dict[str, object]] = [{"name": "second"}, {"days": 2}]
    for values in changes:
        with RandomInputs() as changed:
            assert render(certificate_chart, values) != first
        assert changed.records[0]["arguments"] != original.records[0]["arguments"]
        with pytest.raises(RandomInputUnavailable, match="diverged"), RandomInputs(replay=original.records):
            render(certificate_chart, values)
    assert render(Chart.load(certificate_chart.path), {}) != first


def test_helpers_loops_and_dynamic_templates(certificate_chart: Chart) -> None:
    """
    Distinguish repeated calls and preserve variable reuse, including generated template code.

    Args:
        certificate_chart (Chart): Prepared strict chart.

    Returns:
        None: Independent calls receive different key material, while loop occurrences and dynamic calls replay.
    """
    (certificate_chart.path / "templates/output.yaml").write_text(
        dedent("""
        {{- define "key" -}}{{ genPrivateKey "ecdsa" }}{{- end -}}
        {{- $first := include "key" . -}}
        {{- $second := include "key" . -}}
        {{- range until 2 }}{{ $unused := genPrivateKey "ecdsa" }}{{ end -}}
        {{- $dynamic := tpl "{{ genPrivateKey \\"ecdsa\\" }}" . -}}
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: keys
        data:
          token: {{ list (eq $first $first) (ne $first $second) (ne $second $dynamic) | toJson | quote }}
        """).lstrip(),
    )
    with RandomInputs() as case:
        output = render(certificate_chart, {})
    assert mapping(output[0]["data"])["token"] == "[true,true,true]"
    assert len(case.records) == len({row["path"] for row in case.records}) == 5
    assert "dynamic:genPrivateKey" in str(case.records[-1]["path"])
    with RandomInputs.from_document(case.document()):
        assert render(certificate_chart, {}) == output


@pytest.mark.parametrize(
    "expression",
    [
        '{{ genCA "name" }}',
        '{{ genCA "name" "days" }}',
        '{{ genCAWithKey "name" 1 "invalid" }}',
        '{{ genSelfSignedCert "name" (list "invalid-ip") nil 1 }}',
        '{{ genSelfSignedCert "name" nil (list 42) 1 }}',
        '{{ genSignedCert "name" nil nil 1 (dict "Cert" "x" "Key" "y") }}',
    ],
)
def test_native_errors_replay(certificate_chart: Chart, expression: str) -> None:
    """
    Preserve native argument checking and cryptographic errors instead of inventing replacement values.

    Args:
        certificate_chart (Chart): Prepared strict chart.
        expression (str): Invalid native call.

    Returns:
        None: The chart failure and any partial native tape reproduce exactly.
    """
    template(certificate_chart, expression)
    with pytest.raises(RenderFailure) as failure, RandomInputs() as case:
        render_output(certificate_chart, {})
    with pytest.raises(RenderFailure) as replayed, RandomInputs.from_document(case.document()):
        render_output(certificate_chart, {})
    assert str(replayed.value) == str(failure.value)


def test_damaged_missing_and_unused_certificates(certificate_chart: Chart) -> None:
    """
    Refuse damaged material and changed replay control flow as tooling errors.

    Args:
        certificate_chart (Chart): Prepared strict chart.

    Returns:
        None: Invalid tapes never fall back or become chart findings.
    """
    template(certificate_chart, '{{ genPrivateKey "ecdsa" | quote }}')
    with RandomInputs() as case:
        render(certificate_chart, {})
    damaged = copy.deepcopy(case.records)
    damaged[0]["result"] = "corrupted"
    for records in ([], damaged, [*case.records, *case.records]):
        with pytest.raises(RandomInputUnavailable), RandomInputs(replay=records):
            render(certificate_chart, {})


def test_concurrent_same_call_uses_one_observation(certificate_chart: Chart) -> None:
    """
    Keep retry outcomes identical when two threads first reach the same native call.

    Args:
        certificate_chart (Chart): Shared prepared chart.

    Returns:
        None: Publication chooses one retained result for concurrent requests.
    """
    template(certificate_chart, '{{ genPrivateKey "ecdsa" | quote }}')
    with ThreadPoolExecutor(max_workers=2) as pool:
        outputs = list(pool.map(lambda _: render_output(certificate_chart, {}), range(2)))
    assert outputs[0] == outputs[1]
    assert len(certificate_chart.certificate_records.records) == 1


def test_scan_failure_artifact_and_report(certificate_chart: Chart, tmp_path: Path) -> None:
    """
    Save real key material for replay while keeping PEM blocks out of report prose.

    Args:
        certificate_chart (Chart): Prepared strict chart.
        tmp_path (Path): Failure artifacts.

    Returns:
        None: Hypothesis produces a stable finding and the exported tape reproduces it.
    """
    template(certificate_chart, '{{ $key := genPrivateKey "ecdsa" }}{{ if $key }}{{ fail "certificate branch" }}{{ end }}')
    result = check_chart(certificate_chart, max_examples=3, artifact_dir=tmp_path / "artifacts")
    assert result["status"] == "failed", result
    tape = json.loads((tmp_path / "artifacts/random-inputs.json").read_text())
    assert tape == result["random_inputs"]
    with pytest.raises(RenderFailure, match="certificate branch"), RandomInputs.from_document(tape):
        render(certificate_chart, mapping(result["values"]))
    summary = "\n".join(input_summary(failing_input(result)))
    assert "genPrivateKey" in summary and "SHA-256" in summary
    assert "PRIVATE KEY" not in summary
    assert sequence(tape["draws"])


@pytest.mark.parametrize("jobs", [1, 2])
def test_parallel_validation_failure_keeps_certificate_tape(certificate_chart: Chart, tmp_path: Path, jobs: int) -> None:
    """
    Preserve native material across worker output and coordinator-side manifest assertions.

    Args:
        certificate_chart (Chart): Prepared strict chart with finite values.
        tmp_path (Path): Saved failure evidence.
        jobs (int): Concurrent render workers.

    Returns:
        None: Serial and parallel findings retain identical replay semantics.
    """
    template(certificate_chart, '{{ $key := genPrivateKey "ecdsa" }}{{ .Values.days | quote }}')

    def reject(resources: list[dict[str, object]]) -> None:
        """
        Reject a changed value only after native rendering has completed.

        Args:
            resources (list[dict[str, object]]): Rendered resources on the coordinator.

        Returns:
            None: The baseline passes; another configuration deliberately fails.
        """
        assert mapping(resources[0]["data"])["token"] == "1", "downstream assertion"

    result = check_chart(certificate_chart, exhaustive=True, jobs=jobs, properties=(reject,), artifact_dir=tmp_path / "parallel")
    assert result["status"] == "failed", result
    tape = mapping(result["random_inputs"])
    assert mapping(sequence(tape["draws"])[0])["function"] == "genPrivateKey"
    with pytest.raises(AssertionError, match="downstream assertion"), RandomInputs.from_document(tape):
        reject(render(certificate_chart, mapping(result["values"])))


def test_certificate_observations_do_not_prove_rejections(certificate_chart: Chart) -> None:
    """
    Keep sampled certificate contents outside static rejection proofs.

    Args:
        certificate_chart (Chart): Prepared strict chart.

    Returns:
        None: Rendering can fail while the compiler correctly retains an unknown prediction.
    """
    template(certificate_chart, '{{ if (genCA "name" 1).Cert }}{{ fail "generated" }}{{ end }}')
    contracts = Contracts.build(certificate_chart.path)
    with RandomInputs() as case:
        assert contracts.predict(certificate_chart.defaults) is None
        assert not case.records
        with pytest.raises(RenderFailure, match="generated"):
            render(certificate_chart, {})


def test_recording_budget_does_not_evict_retry_material() -> None:
    """
    Stop bounded retention without replacing a previous native outcome.

    Returns:
        None: Exhaustion keeps the original record usable and does not silently rerandomize retries.
    """
    store = CertificateStore()
    inputs = CertificateInputs(store, {}, 10000, 1)
    call: dict[str, object] = {"path": "first", "function": "genPrivateKey", "arguments": []}
    assert inputs.exchange(call, None)["generate"] is True
    record = inputs.exchange({**call, "result": "native test key"}, None)
    assert inputs.exchange(call, None) == record
    second = {**call, "path": "second"}
    assert inputs.exchange(second, None)["generate"] is True
    with pytest.raises(RandomInputUnavailable, match="compiler.max"):
        inputs.exchange({**second, "result": "another key"}, None)
    assert inputs.exchange(call, None) == record


def test_native_certificate_chain() -> None:
    """
    Validate signatures, names, validity, SANs and matching keys using Go's X.509 implementation.

    Returns:
        None: Native crypto contract checks run in the ordinary test suite and repository refresh.
    """
    go = shutil.which("go")
    if go is None:
        pytest.skip("Go is required for native certificate contract tests")
    cache = Path(".cache/random-renderer/go").resolve()
    Processes().run(
        [go, "test", "-mod=readonly", "-count=1", "."],
        cwd=SOURCE,
        env={**env, "GOMODCACHE": str(cache / "modules"), "GOCACHE": str(cache / "build"), "GOTOOLCHAIN": "auto", "GOWORK": "off"},
        capture_output=True,
        check=True,
        timeout=120,
    )
