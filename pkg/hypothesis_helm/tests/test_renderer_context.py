"""
Compare compiler context, file and concrete tpl evaluation with native Helm outcomes.
"""

import json
import logging
import shutil
import tarfile
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import strategies as st

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.rendering import RenderFailure, render
from hypothesis_helm.charts.runner import check_chart
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.passes.rejections import RejectionPolicy, matches_rejection
from hypothesis_helm.rules import ENVIRONMENT
from hypothesis_helm.schemas.contracts import mapping
from hypothesis_helm.schemas.policy import ENVIRONMENT as INPUT_POLICY


@pytest.fixture
def context_chart(tmp_path: Path) -> Chart:
    """
    Create a chart with replaceable note templates and independent valid output.

    Args:
        tmp_path (Path): Isolated chart source.

    Returns:
        Chart: Minimal chart with real files and a safe baseline.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "context", "version": "0.1.0"}))
    defaults: dict[str, object] = {"mode": "good", "script": ""}
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates/config.yaml").write_text(
        dedent(
            """
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: context
            """
        )
    )
    (tmp_path / "allowed.txt").write_text("good\nother\n")
    (tmp_path / "hidden.txt").write_text("must not be visible")
    (tmp_path / ".helmignore").write_text("hidden.txt\n")
    return Chart(tmp_path, {"type": "object"}, defaults)


def configured(chart: Chart, kube_version: str = "1.35.0") -> Contracts:
    """
    Attach the same binary and Kubernetes version used by the native comparisons.

    Args:
        chart (Chart): Prepared source chart.
        kube_version (str): Helm capability version override.

    Returns:
        Contracts: Compiler with fixed native execution context.
    """
    contracts = Contracts.build(chart.path)
    contracts.configure(helm="helm", kube_version=kube_version, timeout=30, release="hypothesis", namespace="default", fail_fast=False)
    return contracts


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    "guard",
    [
        'and (.Capabilities.APIVersions.Has "v1") (eq .Capabilities.KubeVersion.Minor "35")',
        'semverCompare ">=1.35.0-0" .Capabilities.KubeVersion.Version',
        'not (.Capabilities.APIVersions.Has "example.invalid/v1/Missing")',
        'eq (.Files.Get "allowed.txt") "good\\nother\\n"',
        'eq (.Files.Get "hidden.txt") ""',
        'eq (.Files.Get "values.yaml") ""',
        'eq (.Files.Get "templates/config.yaml") ""',
        'eq (.Files.Get "../outside") ""',
        'not (has .Values.mode (.Files.Lines "allowed.txt"))',
        'eq (tpl "{{ .Values.mode }}" .) "bad"',
        'eq (tpl "{{ .mode }}" (dict "mode" .Values.mode)) "bad"',
        'eq (tpl "{{ include \\"read-mode\\" . }}" .) "bad"',
        'eq (tpl (.Files.Get "mode.tpl") .) "bad"',
        'eq (tpl .Values.script .) "bad"',
    ],
)
def test_context_predictions_match_helm(context_chart: Chart, guard: str) -> None:
    """
    Confirm supported guards and native witness verification agree for bad and good inputs.

    Args:
        context_chart (Chart): Chart with accessible and ignored files.
        guard (str): Supported renderer-context or concrete tpl expression.

    Returns:
        None: Rejection evidence matches Helm and remains subject to per-candidate verification.
    """
    (context_chart.path / "templates/NOTES.txt").write_text(
        '{{ if and (eq .Values.mode "bad") (' + guard + ') }}{{ fail "context guard rejects mode" }}{{ end }}'
    )
    (context_chart.path / "templates/_helpers.tpl").write_text('{{ define "read-mode" }}{{ .Values.mode }}{{ end }}')
    (context_chart.path / "mode.tpl").write_text("{{ .Values.mode }}")
    contracts = configured(context_chart)
    values: dict[str, object] = {"mode": "bad", "script": "{{ .Values.mode }}"}
    rejection = contracts.predict(values)
    assert rejection is not None, contracts.fallbacks
    assert rejection.contextual
    with pytest.raises(RenderFailure) as failure:
        render(context_chart, values, kube_version="1.35.0")
    assert matches_rejection(str(failure.value), rejection), str(failure.value)
    policy = RejectionPolicy(contracts, context_chart.defaults)
    policy.witnesses[rejection.key] = {"first", "second"}
    assert policy.needs_probe(rejection, values)
    assert contracts.predict(context_chart.defaults) is None
    render(context_chart, {}, kube_version="1.35.0")


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_capabilities_version_and_helper_context(context_chart: Chart) -> None:
    """
    Preserve native capabilities through helper dictionaries and distinguish target versions.

    Args:
        context_chart (Chart): Chart whose helper evaluates a capability guard.

    Returns:
        None: Only the version satisfying Helm's native comparison reaches the rejection.
    """
    (context_chart.path / "templates/NOTES.txt").write_text('{{ include "version-check" (dict "root" $) }}')
    (context_chart.path / "templates/_helpers.tpl").write_text(
        dedent(
            """
            {{ define "version-check" }}
            {{ if semverCompare ">=1.35.0-0" .root.Capabilities.KubeVersion.Version }}{{ fail "new API" }}{{ end }}
            {{ end }}
            """
        )
    )
    assert configured(context_chart, "1.34.0").predict(context_chart.defaults) is None
    render(context_chart, {}, kube_version="1.34.0")
    rejected = configured(context_chart).predict(context_chart.defaults)
    assert rejected is not None
    with pytest.raises(RenderFailure) as failure:
        render(context_chart, {}, kube_version="1.35.0")
    assert matches_rejection(str(failure.value), rejected)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("packed", [False, True])
def test_dependency_file_scope(context_chart: Chart, tmp_path: Path, packed: bool) -> None:
    """
    Read files from aliased child charts without leaking parent data or applying archived ignores.

    Args:
        context_chart (Chart): Parent chart containing a similarly named file.
        tmp_path (Path): Isolated dependency staging directory.
        packed (bool): Keep the child as a directory or a prebuilt dependency archive.

    Returns:
        None: Native and compiler lookups agree on the child's file namespace.
    """
    charts = context_chart.path / "charts"
    child = charts / "original"
    (child / "templates").mkdir(parents=True)
    (child / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "original", "version": "0.1.0"}))
    (child / "allowed.txt").write_text("child-only")
    (child / ".helmignore").write_text("allowed.txt\n")
    (child / "templates/NOTES.txt").write_text('{{ if eq (.Files.Get "allowed.txt") "child-only" }}{{ fail "child context" }}{{ end }}')
    metadata = mapping(yamlio.load((context_chart.path / "Chart.yaml").read_text()))
    metadata["dependencies"] = [{"name": "original", "alias": "child", "version": "0.1.0", "repository": ""}]
    (context_chart.path / "Chart.yaml").write_text(yamlio.dump(metadata))
    if packed:
        with tarfile.open(charts / "original-0.1.0.tgz", "w:gz") as bundle:
            bundle.add(child, arcname="original")
        shutil.rmtree(child)
    rejected = configured(context_chart).predict(context_chart.defaults)
    assert rejected is not None
    with pytest.raises(RenderFailure) as failure:
        render(context_chart, {}, kube_version="1.35.0")
    assert matches_rejection(str(failure.value), rejected)


@pytest.mark.parametrize("body", ["{{ now }}", '{{ lookup "v1" "Secret" "default" "example" }}', "{{ randAlphaNum 4 }}"])
def test_unknown_context_warns_once_and_can_be_suppressed(
    context_chart: Chart, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch, body: str
) -> None:
    """
    Keep unmodeled runtime behavior renderable while warning once per location and suppression state.

    Args:
        context_chart (Chart): Chart with an intentionally unsupported expression.
        caplog (pytest.LogCaptureFixture): Captured compiler warnings.
        monkeypatch (pytest.MonkeyPatch): Restore inherited suppression after this test.
        body (str): Clock, cluster-state or random expression.

    Returns:
        None: Unknown candidates never become rejection or equivalence witnesses.
    """
    (context_chart.path / "templates/NOTES.txt").write_text(body)
    contracts = Contracts.build(context_chart.path)
    with caplog.at_level(logging.WARNING):
        assert contracts.predict(context_chart.defaults) is None
        assert contracts.predict(context_chart.defaults) is None
    assert len(caplog.records) == 1
    assert "[HH2007]" in caplog.text and "retained for Helm rendering" in caplog.text
    assert contracts.fallbacks[0]["source"] == "templates/NOTES.txt"
    assert contracts.fallbacks[0]["line"] == 1
    assert contracts.incomplete_evaluations == 2
    caplog.clear()
    monkeypatch.setenv(ENVIRONMENT, json.dumps(["HH2007"]))
    contracts.fail_fast = True
    assert contracts.predict(context_chart.defaults) is None
    assert not caplog.records
    monkeypatch.setenv(ENVIRONMENT, "[]")
    with pytest.raises(RenderFailure, match="HH2007"):
        contracts.predict(context_chart.defaults)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_unknown_candidate_reaches_renderer(context_chart: Chart, caplog: pytest.LogCaptureFixture) -> None:
    """
    Exercise the executor's fallback path, not just the standalone evaluator.

    Args:
        context_chart (Chart): Valid chart using a native clock expression in its notes.
        caplog (pytest.LogCaptureFixture): Captured compiler diagnostics.

    Returns:
        None: The candidate passes native rendering and is counted as retained, not filtered out.
    """
    (context_chart.path / "templates/NOTES.txt").write_text('{{ if eq .Values.mode "bad" }}{{ now }}{{ end }}')
    with caplog.at_level(logging.WARNING):
        report = check_chart(context_chart, filter_rejections=True, input_strategy=st.just({"mode": "bad"}), max_examples=1)
    assert report["status"] == "passed", report
    evidence = mapping(report["configuration_rejections"])
    assert evidence["incomplete_evaluations"] == 1
    assert evidence["filtered_candidates"] == 0
    assert report["attempts"] == 2
    assert "[HH2007]" in caplog.text


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_analysis_fail_fast_preserves_candidate(context_chart: Chart) -> None:
    """
    Preserve the triggering values when an enabled compiler warning stops execution.

    Args:
        context_chart (Chart): Chart whose nondefault mode reaches an unmodeled clock.

    Returns:
        None: Failure evidence names the warning and the actual triggering configuration.
    """
    (context_chart.path / "templates/NOTES.txt").write_text('{{ if eq .Values.mode "bad" }}{{ now }}{{ end }}')
    report = check_chart(context_chart, filter_rejections=True, input_strategy=st.just({"mode": "bad"}), max_examples=1, fail_fast=True)
    assert report["status"] == "failed"
    assert report["code"] == "HH2007"
    assert report["values"] == {"mode": "bad"}


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_secondary_analysis_warning_preserves_native_failure(context_chart: Chart) -> None:
    """
    Keep a confirmed chart defect when follow-up rejection analysis is incomplete.

    Args:
        context_chart (Chart): Chart with native rejection and a clock outside the analysis contract.

    Returns:
        None: The native failure remains the report's primary evidence with fail-fast enabled.
    """
    (context_chart.path / "templates/NOTES.txt").write_text('{{ now }}{{ fail "confirmed chart failure" }}')
    report = check_chart(context_chart, filter_rejections=True, max_examples=1, fail_fast=True)
    assert report["status"] == "failed"
    assert report["code"] == "HH1001"
    assert "confirmed chart failure" in str(report["error"])


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_tpl_rejection_and_changed_candidate_source(context_chart: Chart) -> None:
    """
    Analyze each candidate's actual tpl source and verify failures raised inside it.

    Args:
        context_chart (Chart): Chart whose supplied string becomes template source.

    Returns:
        None: One source's rejection never contaminates a later valid string or context.
    """
    (context_chart.path / "templates/NOTES.txt").write_text("{{ tpl .Values.script . }}")
    contracts = configured(context_chart)
    values: dict[str, object] = {"mode": "bad", "script": '{{ if eq .Values.mode "bad" }}{{ fail "dynamic requirement" }}{{ end }}'}
    rejection = contracts.predict(values)
    assert rejection is not None
    assert "(tpl)" in rejection.source
    with pytest.raises(RenderFailure) as failure:
        render(context_chart, values)
    assert matches_rejection(str(failure.value), rejection), str(failure.value)
    assert contracts.predict({"mode": "bad", "script": "plain notes"}) is None
    assert contracts.predict({"mode": "good", "script": values["script"]}) is None


@pytest.mark.parametrize("source", ["{{ now }}", '{{ define "local" }}text{{ end }}', "{{ tpl .Values.script . }}", "{{ if"])
def test_tpl_uncertainty_and_recursion_are_bounded(context_chart: Chart, source: str) -> None:
    """
    Retain dynamically unsupported templates and stop recursive expansion at the configured budget.

    Args:
        context_chart (Chart): Chart passing its candidate string to tpl.
        source (str): Unmodeled, locally defining, recursive or malformed generated source.

    Returns:
        None: No rejection is inferred, and the bounded fallback records its reason.
    """
    (context_chart.path / "templates/NOTES.txt").write_text("{{ tpl .Values.script . }}")
    contracts = Contracts.build(context_chart.path)
    contracts.max_call_depth = 3
    assert contracts.predict({"mode": "bad", "script": source}) is None
    assert len(contracts.fallbacks) == 1
    if source == "{{ tpl .Values.script . }}":
        assert "limit 3" in str(contracts.fallbacks[0]["reason"])


def test_fallback_suppression_is_scoped_to_values_paths(
    context_chart: Chart, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """
    Honor branch-level enabling even when incomplete-analysis warnings are globally ignored.

    Args:
        context_chart (Chart): Chart using a values-backed dynamic template.
        monkeypatch (pytest.MonkeyPatch): Isolate input-constraint and finding configuration.
        caplog (pytest.LogCaptureFixture): Captured diagnostics for enabled and disabled branches.

    Returns:
        None: Scoped suppression changes warning visibility without changing render eligibility.
    """
    (context_chart.path / "templates/NOTES.txt").write_text("{{ tpl .Values.script . }}")
    monkeypatch.setenv(ENVIRONMENT, '["HH2007"]')
    monkeypatch.setenv(
        INPUT_POLICY, json.dumps({"input_constraints": [{"charts": ["context"], "path": "$.script", "enabled": ["HH2007"]}]})
    )
    contracts = Contracts.build(context_chart.path)
    with caplog.at_level(logging.WARNING):
        assert contracts.predict({"script": "{{ now }}"}) is None
    assert "[HH2007]" in caplog.text
    assert contracts.fallbacks[0]["suppressed"] is False
