"""
Compare bounded collection and branch discovery with native Helm behavior.
"""

import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.inspection.templates import discover
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.schemas.contracts import mapping
from hypothesis_helm.tests.test_templates import scan


@pytest.mark.parametrize(
    ("body", "expected", "required"),
    [
        (
            '{{ $ctx := dict "context" $ }}{{ if hasKey $ctx "context" }}ok{{ else }}{{ $ctx.Release.Name }}{{ end }}',
            "ok",
            set(),
        ),
        (
            "{{ $ctx := dict }}{{ range default (list) $ctx.extraTerms }}{{ .topologyKey }}{{ else }}empty{{ end }}",
            "empty",
            set(),
        ),
        (
            '{{ $ctx := omit .Values.security "enabled" }}{{ $ctx.privileged }}',
            "false",
            {("security", "privileged")},
        ),
        (
            '{{ $ctx := pick .Values.security "privileged" }}{{ $ctx.privileged }}',
            "false",
            {("security", "privileged")},
        ),
        (
            '{{ $map := dict "normal" true }}{{ if index $map "*" }}wrong{{ else }}missing{{ end }}',
            "missing",
            set(),
        ),
        (
            "{{ $items := list }}{{ range .Values.names }}{{ $items = append $items . }}{{ end }}{{ range $items }}{{ . }}{{ end }}",
            "ab",
            {("names", "*")},
        ),
        (
            '{{ $key := first (reverse (list "security.enabled" "security.privileged")) }}'
            '{{ $obj := .Values }}{{ range splitList "." $key }}{{ $obj = index $obj . }}{{ end }}{{ $obj }}',
            "false",
            {("security", "privileged")},
        ),
        (
            '{{ $presets := dict "small" (dict "value" .Values.left) "large" (dict "value" .Values.right) }}'
            "{{ if hasKey $presets .Values.preset }}{{ $chosen := index $presets .Values.preset }}{{ $chosen.value }}{{ end }}",
            "left",
            {("left",), ("right",), ("preset",)},
        ),
        (
            "{{ range.Values.names }}{{ . }}{{ end }}",
            "ab",
            {("names", "*")},
        ),
        (
            '{{ range split "." "a.b" }}{{ . }}{{ end }}',
            "ab",
            set(),
        ),
        (
            '{{ range concat (list "a") (list "b") }}{{ . }}{{ end }}',
            "ab",
            set(),
        ),
        (
            '{{ include "scalar" (printf "%s-%s" "a" "b") }}',
            "A-B",
            set(),
        ),
        (
            '{{ $value := .Values }}{{ range splitList "." (trim " security.enabled ") }}'
            "{{ $value = index $value . }}{{ end }}{{ $value }}",
            "true",
            {("security", "enabled")},
        ),
        (
            '{{ range splitn "." 2 "a.b.c" }}{{ . }}{{ end }}',
            "ab.c",
            set(),
        ),
    ],
)
@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_supported_shapes_match_helm(tmp_path: Path, body: str, expected: str, required: set[tuple[str, ...]]) -> None:
    """
    Verify discovered input origins and actual output for each newly supported shape.

    Args:
        tmp_path (Path): Isolated native Helm chart.
        body (str): Helper body exercising one analysis gap.
        expected (str): Native Helm output from the supplied values.
        required (set[tuple[str, ...]]): Input dependencies that discovery must retain.

    Returns:
        None: Supported patterns render correctly without unresolved-context diagnostics.
    """
    defaults = mapping(
        {"security": {"enabled": True, "privileged": False}, "names": ["a", "b"], "preset": "small", "left": "left", "right": "right"}
    )
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "discovery", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/_helpers.tpl").write_text(
        '{{ define "scalar" }}{{ . | upper }}{{ end }}{{ define "probe" }}' + body + "{{ end }}"
    )
    (tmp_path / "templates/result.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: example
        data:
          value: {{ include "probe" . | quote }}
        """)
    )
    refs, warnings = discover(tmp_path)
    assert not warnings
    assert required <= {ref.path for ref in refs}
    chart = Chart(tmp_path, {"type": "object"}, defaults)
    assert mapping(render(chart, {})[0]["data"])["value"] == expected


def test_empty_optional_branches_and_input_controlled_branches(tmp_path: Path) -> None:
    """
    Eliminate only syntax-proven empty contexts while retaining every input-controlled branch.

    Args:
        tmp_path (Path): Chart with optional helper fields and mutable values defaults.

    Returns:
        None: Impossible branches disappear; defaults never prove general unreachability.
    """
    (tmp_path / "values.yaml").write_text(yamlio.dump({"enabled": False, "items": []}))
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ define "helper" }}
        {{ if and (hasKey . "customLabels") (hasKey . "context") }}
          {{ .context.Release.Name }}
        {{ else }}{{ .Release.Name }}{{ $.context.Values.impossible }}{{ end }}
        {{ if .chart }}{{ .chart.AppVersion }}{{ end }}
        {{ range default (list) .terms }}{{ .namespaces }}{{ .weight }}{{ end }}
        {{ end }}
        {{ include "helper" (dict "customLabels" (dict) "context" $) }}
        {{ if .Values.enabled }}{{ .Values.yes }}{{ else }}{{ .Values.no }}{{ end }}
        {{ range .Values.items }}{{ .name }}{{ end }}
        """),
    )
    found = {ref.path for ref in refs}
    assert {("yes",), ("no",), ("items", "*", "name")} <= found
    assert ("impossible",) not in found
    assert not warnings


@pytest.mark.parametrize("guard", ["hasKey $presets .Values.mode", "not (not (hasKey $presets .Values.mode))"])
def test_guarded_lookup_preserves_all_table_members(tmp_path: Path, guard: str) -> None:
    """
    Bound table lookups with proven membership without turning accepted keys into a global input enum.

    Args:
        tmp_path (Path): Finite helper table with values-backed entries.
        guard (str): Supported positive key-membership condition.

    Returns:
        None: Every member's nested path remains visible and unsupported keys remain testable.
    """
    refs, warnings = scan(
        tmp_path,
        '{{ $presets := dict "a" .Values.first "b" .Values.second }}'
        + "{{ if "
        + guard
        + " }}{{ $v := index $presets .Values.mode }}{{ $v.name }}{{ end }}",
    )
    assert not warnings
    assert {("first", "name"), ("second", "name"), ("mode",)} <= {ref.path for ref in refs}


def test_map_mutations_invalidate_shared_facts_and_cached_helpers(tmp_path: Path) -> None:
    """
    Retain branches that unsupported map mutations may make reachable, including memoized helper calls.

    Args:
        tmp_path (Path): Chart with aliases and repeated structurally identical mutable contexts.

    Returns:
        None: Cached helper effects and mutations cannot turn old key facts into unsafe pruning.
    """
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ define "mutate" }}{{ $_ := set . "added" true }}{{ end }}
        {{ $a := dict }}{{ include "mutate" $a }}
        {{ if hasKey $a "added" }}{{ $.Values.afterFirst }}{{ end }}
        {{ $b := dict }}{{ include "mutate" $b }}
        {{ if hasKey $b "added" }}{{ $.Values.afterCached }}{{ end }}
        {{ $c := dict "present" true }}{{ $alias := $c }}
        {{ $_ := unset $alias "present" }}
        {{ if not (hasKey $c "present") }}{{ $.Values.afterAlias }}{{ end }}
        """),
    )
    assert {("afterFirst",), ("afterCached",), ("afterAlias",)} <= {ref.path for ref in refs}
    assert any("mutation requires review" in item.message for item in warnings)


def test_unknown_and_unguarded_sources_remain_diagnostic(tmp_path: Path) -> None:
    """
    Preserve uncertainty where collections, transformations or table membership are not proven.

    Args:
        tmp_path (Path): Chart mixing unsupported and partially supported expressions.

    Returns:
        None: Supported operations do not silently turn unknown input into empty or valid input.
    """
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ $terms := default (list) (mystery .Values.source) }}
        {{ range $terms }}{{ .name }}{{ end }}
        {{ $presets := dict "a" .Values.first }}
        {{ $selected := index $presets .Values.mode }}{{ $selected.name }}
        {{ $ctx := omit (mystery .Values.security) "enabled" }}{{ $ctx.privileged }}
        """),
    )
    assert ("first", "name") in {ref.path for ref in refs}
    assert {
        "unresolved dot context: .name",
        "unresolved variable context: $selected.name",
        "unresolved variable context: $ctx.privileged",
    } <= {item.message for item in warnings}


def test_tpl_sources_survive_aliases_coalesce_and_conversion(tmp_path: Path) -> None:
    """
    Inspect every available template source while reporting unresolved alternatives.

    Args:
        tmp_path (Path): Chart supplying two concrete scripts and one unsupported alternative.

    Returns:
        None: Aliased templates retain their hidden inputs and unknown source code remains diagnostic.
    """
    (tmp_path / "values.yaml").write_text(yamlio.dump({"first": "{{ .Values.left }}", "second": "{{ .Values.right }}"}))
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ $source := coalesce .Values.first .Values.second "literal fallback" }}
        {{ tpl ($source | toString) . }}
        {{ $partial := default "{{ .Values.available }}" (mystery .Values.script) }}
        {{ tpl $partial . }}
        {{ tpl "{{ .value.child }}" (dict "value" .Values.context) }}
        """),
    )
    assert {("left",), ("right",), ("available",), ("context", "child")} <= {ref.path for ref in refs}
    assert any("source is dynamic" in item.message for item in warnings)


def test_literal_key_walk_is_not_limited_to_eight_components(tmp_path: Path) -> None:
    """
    Traverse finite key sequences exactly under the normal statement budget.

    Args:
        tmp_path (Path): Chart constructing a ten-component values key.

    Returns:
        None: Exact paths are recovered without wildcard growth or convergence warnings.
    """
    components = tuple(f"level{index}" for index in range(10))
    refs, warnings = scan(
        tmp_path,
        '{{ $value := .Values }}{{ range splitList "." "' + ".".join(components) + '" }}{{ $value = index $value . }}{{ end }}{{ $value }}',
    )
    assert components in {ref.path for ref in refs}
    assert not any("*" in ref.path for ref in refs)
    assert not warnings


def test_invalid_tpl_alternative_does_not_hide_valid_sources(tmp_path: Path) -> None:
    """
    Continue inspecting known source alternatives after one contains malformed template code.

    Args:
        tmp_path (Path): Chart with one broken script and one valid fallback.

    Returns:
        None: The malformed script is reported and the valid script's input remains discoverable.
    """
    (tmp_path / "values.yaml").write_text(yamlio.dump({"first": "{{ if", "second": "{{ .Values.hidden }}"}))
    refs, warnings = scan(tmp_path, '{{ $script := coalesce .Values.first .Values.second "fallback" }}{{ tpl $script . }}')
    assert ("hidden",) in {ref.path for ref in refs}
    assert warnings


def test_unsupported_numeric_spelling_does_not_prove_a_branch(tmp_path: Path) -> None:
    """
    Avoid interpreting Go octal constants as Python decimal integers during branch folding.

    Args:
        tmp_path (Path): Chart using an octal literal in a condition.

    Returns:
        None: Both alternatives remain discoverable until the numeric syntax is modeled.
    """
    refs, _ = scan(tmp_path, "{{ if eq 010 8 }}{{ .Values.octal }}{{ else }}{{ .Values.other }}{{ end }}")
    assert {("octal",), ("other",)} <= {ref.path for ref in refs}


def test_dynamic_code_and_helpers_invalidate_known_map_keys(tmp_path: Path) -> None:
    """
    Account for side effects of unresolved helpers and template strings supplied as values.

    Args:
        tmp_path (Path): Chart whose future template source can add a key to its context.

    Returns:
        None: A benign default script cannot hide input paths reachable after another script mutates the map.
    """
    (tmp_path / "values.yaml").write_text(yamlio.dump({"script": "no mutation in this default"}))
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ $first := dict }}{{ tpl .Values.script $first }}
        {{ if hasKey $first "added" }}{{ $.Values.afterScript }}{{ end }}
        {{ $second := dict }}{{ include .Values.helper $second }}
        {{ if hasKey $second "added" }}{{ $.Values.afterHelper }}{{ end }}
        {{ $third := dict }}{{ $_ := mustMerge $third (dict "added" true) }}
        {{ if hasKey $third "added" }}{{ $.Values.afterMerge }}{{ end }}
        """),
    )
    assert {("afterScript",), ("afterHelper",), ("afterMerge",)} <= {ref.path for ref in refs}
    assert any("helper name or call context is dynamic" in item.message for item in warnings)
    assert any("mutation requires review: mustMerge" in item.message for item in warnings)
