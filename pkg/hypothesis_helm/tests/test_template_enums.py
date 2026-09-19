"""
Verify source-backed allowlists, helper scopes, and native Helm rejection witnesses.
"""

import itertools
import json
import shutil
import tarfile
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import strategies as st

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.runner import RenderFailure, check_chart, render
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.passes.rejections import matches_rejection
from hypothesis_helm.schemas.contracts import mapping


@pytest.fixture
def preset_chart(tmp_path: Path) -> Chart:
    """
    Create a chart with a conditional, dictionary-backed resource preset helper.

    Args:
        tmp_path (Path): Isolated fixture directory.

    Returns:
        Chart: Valid defaults and an enum contract behind optional configuration branches.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "preset", "version": "1.0.0"}))
    defaults: dict[str, object] = {"enabled": True, "resources": {}, "preset": "none"}
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "preset.resources" -}}
        {{- $presets := dict "nano" (dict "cpu" "100m") "small" (dict "cpu" "500m") "large" (dict "cpu" "1") -}}
        {{- if hasKey $presets .type -}}
        {{- index $presets .type | toYaml -}}
        {{- else -}}
        {{- printf "ERROR: Preset key '%s' invalid. Allowed values are %s" .type (join "," (keys $presets)) | fail -}}
        {{- end -}}
        {{- end -}}
        """)
    )
    (tmp_path / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: preset
        data:
          status: ready
        {{- if .Values.enabled }}
        {{- if .Values.resources }}
          custom: "true"
        {{- else if ne .Values.preset "none" }}
          selected: {{ include "preset.resources" (dict "type" .Values.preset) | quote }}
        {{- end }}
        {{- end }}
        """)
    )
    return Chart(tmp_path, {"type": "object"}, defaults)


def test_map_enum_guards_and_message_order(preset_chart: Chart) -> None:
    """
    Recover an allowlist only on its rejecting branch and verify every key exactly once.

    Args:
        preset_chart (Chart): Conditional map-backed preset fixture.

    Returns:
        None: Bypassed presets stay unrestricted and message matching tolerates only key order.
    """
    contracts = Contracts.build(preset_chart.path)
    invalid = {**preset_chart.defaults, "preset": "invalid"}
    rejection = contracts.predict(invalid)
    assert rejection is not None
    assert rejection.enums == {"$.preset": ("large", "nano", "small")}
    for overrides in ({"enabled": False}, {"resources": {"cpu": "2"}}, {"preset": "none"}):
        assert contracts.predict({**invalid, **overrides}) is None
    prefix = "Error: execution error at (preset/templates/config.yaml:13:27): ERROR: Preset key 'invalid' invalid. Allowed values are "
    for order in itertools.permutations(("large", "nano", "small")):
        assert matches_rejection(prefix + ",".join(order), rejection)
    assert not matches_rejection(prefix + "large,nano,nano", rejection)
    assert not matches_rejection(prefix + "large,nano,small,extra", rejection)
    assert not matches_rejection(prefix.replace("'invalid'", "'different'") + "large,nano,small", rejection)
    another = contracts.predict({**invalid, "preset": "another"})
    assert another is not None and another.key == rejection.key


@pytest.mark.parametrize("membership", ["has", "mustHas"])
def test_literal_lists_nested_arguments_and_aliases(preset_chart: Chart, membership: str) -> None:
    """
    Follow nested dictionary contexts and local aliases into literal-list membership.

    Args:
        preset_chart (Chart): Chart whose helper and caller are replaced for this pattern.
        membership (str): Supported Sprig list membership function.

    Returns:
        None: Helper-local dollar refers to the argument map and provenance retains the input path.
    """
    (preset_chart.path / "templates/_helpers.tpl").write_text(
        dedent(f"""
        {{{{- define "preset.resources" -}}}}
        {{{{- $allowed := list "small" "large" -}}}}
        {{{{- $selected := $.nested.type -}}}}
        {{{{- if not ({membership} $selected $allowed) -}}}}{{{{ fail "unsupported preset" }}}}{{{{- end -}}}}
        {{{{- end -}}}}
        """)
    )
    (preset_chart.path / "templates/config.yaml").write_text(
        dedent("""
        {{ $selected := .Values.preset }}
        {{ include "preset.resources" (dict "nested" (dict "type" $selected)) }}
        """)
    )
    contracts = Contracts.build(preset_chart.path)
    rejection = contracts.predict({"preset": "bad"})
    assert rejection is not None and rejection.enums == {"$.preset": ("large", "small")}
    assert contracts.predict({"preset": "small"}) is None


@pytest.mark.parametrize(
    "guard",
    [
        'hasKey (dict "small" true) (lower .type)',
        'eq (tpl .type $) "bad"',
    ],
)
def test_unsupported_expressions_remain_unknown(preset_chart: Chart, guard: str) -> None:
    """
    Retain ordinary testing when a guard needs unsupported transformations or dynamic templates.

    Args:
        preset_chart (Chart): Chart with a replaceable helper.
        guard (str): Guard whose semantics remain outside the supported contract subset.

    Returns:
        None: No rejection or inferred allowlist is claimed.
    """
    (preset_chart.path / "templates/_helpers.tpl").write_text(
        dedent(f"""
        {{{{- define "preset.resources" -}}}}
        {{{{- if {guard} -}}}}{{{{ fail "unknown semantics" }}}}{{{{- end -}}}}
        {{{{- end -}}}}
        """)
    )
    assert Contracts.build(preset_chart.path).predict({**preset_chart.defaults, "preset": "bad"}) is None


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_native_enum_guidance_and_schema_conflicts(preset_chart: Chart) -> None:
    """
    Verify rejection with Helm before choosing an enum member and preserve authored-schema failures.

    Args:
        preset_chart (Chart): Renderable chart with an explicit preset allowlist.

    Returns:
        None: Inferred inputs receive tested replacements; authored inputs still expose their contract conflict.
    """
    invalid = {**preset_chart.defaults, "preset": '*a"/?U'}
    rejection = Contracts.build(preset_chart.path).predict(invalid)
    assert rejection is not None
    with pytest.raises(RenderFailure) as failure:
        render(preset_chart, invalid)
    assert matches_rejection(str(failure.value), rejection)
    report = check_chart(
        preset_chart, input_strategy=st.just(invalid), max_examples=1, filter_rejections=True, protected_paths=(("preset",),)
    )
    assert report["status"] == "passed", report
    evidence = mapping(report["configuration_rejections"])
    assert evidence["verification_renders"] == evidence["adjusted_candidates"] == 1
    assert evidence["classifier_disagreements"] == 0
    (preset_chart.path / "values.schema.json").write_text(json.dumps({"type": "object", "properties": {"preset": {"type": "string"}}}))
    report = check_chart(preset_chart, input_strategy=st.just(invalid), max_examples=1, filter_rejections=True)
    assert report["status"] == "failed"
    assert int(str(mapping(report["configuration_rejections"])["schema_conflicts"])) > 0


@pytest.mark.parametrize("archived", [False, True])
def test_aliased_dependency_contracts(preset_chart: Chart, tmp_path: Path, archived: bool) -> None:
    """
    Inspect dependency sources before temporary extraction ends and respect their activation controls.

    Args:
        preset_chart (Chart): Child chart with a helper-backed allowlist.
        tmp_path (Path): Parent chart and optional child archive destination.
        archived (bool): Package the child as a tgz instead of using an unpacked directory.

    Returns:
        None: Active aliases map to parent values paths; disabled children cannot reject parent inputs.
    """
    parent = tmp_path / "parent"
    (parent / "charts").mkdir(parents=True)
    metadata = {
        "apiVersion": "v2",
        "name": "parent",
        "version": "1.0.0",
        "dependencies": [{"name": "preset", "alias": "db", "version": "1.0.0", "condition": "db.active"}],
    }
    (parent / "Chart.yaml").write_text(yamlio.dump(metadata))
    if archived:
        with tarfile.open(parent / "charts/preset-1.0.0.tgz", "w:gz") as archive:
            for name in ("Chart.yaml", "values.yaml", "templates"):
                archive.add(preset_chart.path / name, arcname="preset/" + name)
    else:
        child = parent / "charts/preset"
        child.mkdir()
        for name in ("Chart.yaml", "values.yaml"):
            shutil.copy2(preset_chart.path / name, child / name)
        shutil.copytree(preset_chart.path / "templates", child / "templates")
    contracts = Contracts.build(parent)
    invalid: dict[str, object] = {"db": {"active": True, "preset": "bad"}}
    rejection = contracts.predict(invalid)
    assert rejection is not None and rejection.enums == {"$.db.preset": ("large", "nano", "small")}
    assert contracts.predict({"db": {"active": False, "preset": "bad"}}) is None
