"""
Verify lexical branch scopes and helper input origins against native template behavior.
"""

import json
import shutil
import tarfile
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.templates import discover, parse
from hypothesis_helm.tests.test_templates import scan


def test_chained_branches_have_bodies_and_preserve_scope(tmp_path: Path) -> None:
    """
    Bind chained branches to their bodies and retain the caller's dot through else-if.

    Args:
        tmp_path (Path): Isolated chart sources.

    Returns:
        None: Branch bodies retain their paths and literal pruning removes only unreachable branches.
    """
    text = dedent("""
        {{ with .Values.worker }}
          {{ if .custom }}{{ .custom.value }}
          {{ else if .livenessProbe.enabled }}{{ .livenessProbe }}
          {{ else if .readinessProbe.enabled }}{{ .readinessProbe }}
          {{ else }}{{ .resourcesPreset }}{{ end }}
        {{ end }}
        {{ if $chosen := .Values.selected }}{{ $chosen.yes }}{{ else }}{{ $chosen.no }}{{ end }}
        {{ if false }}{{ .Values.deadA }}
        {{ else if true }}{{ .Values.live }}
        {{ else }}{{ .Values.deadB }}{{ end }}
        """)
    first = parse(text)[0].children[0]
    assert first.otherwise[0].tokens == ["if", ".livenessProbe.enabled"]
    assert first.otherwise[0].children[0].tokens == [".livenessProbe"]
    assert first.otherwise[0].otherwise[0].children[0].tokens == [".readinessProbe"]
    scan(tmp_path, text)
    refs, warnings = discover(tmp_path, prune_literals=True)
    paths = {ref.path for ref in refs}
    assert {
        ("worker", "livenessProbe", "enabled"),
        ("worker", "livenessProbe"),
        ("worker", "readinessProbe", "enabled"),
        ("worker", "readinessProbe"),
        ("worker", "resourcesPreset"),
        ("selected", "yes"),
        ("selected", "no"),
        ("live",),
    } <= paths
    assert ("deadA",) not in paths and ("deadB",) not in paths
    assert not warnings


def test_else_with_restores_outer_dot(tmp_path: Path) -> None:
    """
    Enter each with branch from the outer dot and restore that dot in the final else.

    Args:
        tmp_path (Path): Isolated chart sources.

    Returns:
        None: Alternate contexts do not inherit the preceding with branch's dot.
    """
    refs, warnings = scan(
        tmp_path,
        dedent("""
            {{ with .Values.first }}{{ .name }}
            {{ else with .Values.second }}{{ .name }}
            {{ else }}{{ .Values.fallback }}{{ end }}
            """),
    )
    assert {(ref.path) for ref in refs} == {("first",), ("first", "name"), ("second",), ("second", "name"), ("fallback",)}
    assert not warnings


@pytest.mark.parametrize("call", ["include", "template", "block"])
def test_helper_dictionary_contexts_and_source_locations(tmp_path: Path, call: str) -> None:
    """
    Follow known helpers with fresh dollar bindings and nested literal dictionary contexts.

    Args:
        tmp_path (Path): Isolated chart with a separate helper source.
        call (str): Helm's named helper invocation forms.

    Returns:
        None: Helper-only fields are found in each calling scope and retain definition source lines.
    """
    templates = tmp_path / "templates"
    templates.mkdir()
    helpers = dedent("""
        {{ define "inner" }}{{ .context.Values.globalField }}{{ $.value.hidden }}{{ end }}
        {{ define "outer" }}{{ include "inner" . }}{{ end }}
        {{ define "unused" }}{{ .Values.neverRead }}{{ end }}
        """).lstrip()
    (templates / "_helpers.tpl").write_text(helpers)
    invocation = call + ' "outer" (dict "context" $ "value" .Values.first)'
    suffix = "{{ end }}" if call == "block" else ""
    if call == "block":
        # A block defines its default body as well as invoking the named helper.
        invocation += ' }}{{ include "inner" .'
    (templates / "resource.yaml").write_text(
        "{{ " + invocation + " }}" + suffix + '{{ include "outer" (dict "context" $ "value" .Values.second) | quote }}'
    )
    refs, warnings = discover(tmp_path)
    paths = {ref.path for ref in refs}
    assert {("globalField",), ("first", "hidden"), ("second", "hidden")} <= paths
    assert ("neverRead",) not in paths
    assert all(ref.file == "templates/_helpers.tpl" and ref.line == 1 for ref in refs if ref.path[-1:] == ("hidden",))
    assert not warnings


@pytest.mark.parametrize("packaged", [False, True])
def test_installed_dependency_helpers(tmp_path: Path, packaged: bool) -> None:
    """
    Resolve helpers supplied by installed library dependencies in directories or archives.

    Args:
        tmp_path (Path): Parent chart with an installed library.
        packaged (bool): Whether the dependency is stored in a tar archive.

    Returns:
        None: Child-defined helpers use the parent's explicitly passed values context.
    """
    library = tmp_path / "charts/library"
    (library / "templates").mkdir(parents=True)
    (library / "templates/_helpers.tpl").write_text('{{ define "library.read" }}{{ $.hidden }}{{ end }}')
    if packaged:
        with tarfile.open(tmp_path / "charts/library.tgz", "w:gz") as archive:
            archive.add(library, arcname="library")
        shutil.rmtree(library)
    refs, warnings = scan(tmp_path, '{{ include "library.read" .Values.parent }}')
    found = next(ref for ref in refs if ref.path == ("parent", "hidden"))
    assert found.file.startswith("charts/library") and found.file.endswith("templates/_helpers.tpl")
    assert not warnings


def test_dynamic_ambiguous_recursive_and_transformed_calls_stay_unknown(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Bound helper discovery and retain unknown context instead of inventing input paths.

    Args:
        tmp_path (Path): Sources exercising unsupported calls.
        monkeypatch (pytest.MonkeyPatch): Small compiler depth limit.

    Returns:
        None: Unsupported calls retain diagnostics and caller-local variables never leak into helpers.
    """
    monkeypatch.setattr("hypothesis_helm.charts.templates.call_depth", lambda: 2)
    refs, warnings = scan(
        tmp_path,
        dedent("""
            {{ define "same" }}{{ .wrongA }}{{ end }}
            {{ define "same" }}{{ .wrongB }}{{ end }}
            {{ define "recursive" }}{{ include "recursive" . }}{{ end }}
            {{ define "first" }}{{ include "second" . }}{{ end }}
            {{ define "second" }}{{ include "third" . }}{{ end }}
            {{ define "third" }}{{ .tooDeep }}{{ end }}
            {{ define "local" }}{{ $caller.secret }}{{ .valid }}{{ end }}
            {{ $caller := .Values.outside }}
            {{ include "same" .Values.ambiguous }}
            {{ include .Values.helper . }}
            {{ include "missing" . }}
            {{ include "recursive" . }}
            {{ include "first" . }}
            {{ include "local" .Values.inside }}
            {{ include "local" ((dict "valid" .Values.wrong) | toJson) }}
            """),
    )
    messages = [warning.message for warning in warnings]
    assert any("ambiguous: same" in message for message in messages)
    assert any("dynamic:" in message for message in messages)
    assert any("missing or ambiguous: missing" in message for message in messages)
    assert any("recursive or exceeds" in message for message in messages)
    assert any("unresolved variable context: $caller.secret" in message for message in messages)
    assert any("unresolved dot context: .valid" in message for message in messages)
    paths = {ref.path for ref in refs}
    assert ("inside", "valid") in paths
    assert ("outside", "secret") not in paths
    assert ("tooDeep",) not in paths
    assert ("ambiguous", "wrongA") not in paths and ("ambiguous", "wrongB") not in paths
    assert all(warning.file == "templates/test.yaml" and warning.line > 0 for warning in warnings)


def test_repeated_helper_contexts_leave_budget_for_other_templates(tmp_path: Path) -> None:
    """
    Reuse identical helper discoveries so repeated includes do not hide later template inputs.

    Args:
        tmp_path (Path): Chart with many calls to one helper and a final distinct calling context.

    Returns:
        None: Both contexts and the final root field are discovered without exhausting the action budget.
    """
    templates = tmp_path / "templates"
    templates.mkdir()
    body = "".join("{{ .field" + str(index) + " }}" for index in range(100))
    (templates / "_helpers.tpl").write_text('{{ define "fields" }}' + body + "{{ end }}")
    (templates / "first.yaml").write_text('{{ include "fields" .Values.first }}' * 200)
    (templates / "last.yaml").write_text('{{ include "fields" .Values.second }}{{ .Values.finalField }}')
    refs, warnings = discover(tmp_path)
    assert {("first", "field99"), ("second", "field99"), ("finalField",)} <= {ref.path for ref in refs}
    assert not warnings


@pytest.mark.integration
@pytest.mark.skipif(not shutil.which("helm"), reason="Helm is required")
def test_discovered_helper_branches_match_native_helm(tmp_path: Path) -> None:
    """
    Change helper-only values in chained branches and confirm native Helm reads those exact paths.

    Args:
        tmp_path (Path): Complete chart used for native rendering.

    Returns:
        None: Every discovered branch field changes the manifest in its matching configuration.
    """
    from hypothesis_helm.charts.model import Chart
    from hypothesis_helm.charts.rendering import render
    from hypothesis_helm.schemas.contracts import mapping

    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "helper-test", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(
        yamlio.dump({"worker": {"custom": "", "enabled": False, "probe": "ready", "fallback": "disabled"}})
    )
    (tmp_path / "values.schema.json").write_text(json.dumps({"type": "object"}))
    refs, warnings = scan(
        tmp_path,
        dedent("""
            {{ define "probe" }}
            {{- if .custom }}{{ .custom }}
            {{- else if .enabled }}{{ .probe }}
            {{- else }}{{ .fallback }}{{ end -}}
            {{ end }}
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: helper-test
            data:
              probe: {{ include "probe" .Values.worker | trim | quote }}
            """),
    )
    assert {("worker", "custom"), ("worker", "enabled"), ("worker", "probe"), ("worker", "fallback")} <= {ref.path for ref in refs}
    assert not warnings
    chart = Chart.load(tmp_path)
    for overrides, expected in (({}, "disabled"), ({"enabled": True}, "ready"), ({"custom": "custom"}, "custom")):
        assert mapping(render(chart, {"worker": overrides})[0]["data"])["probe"] == expected
