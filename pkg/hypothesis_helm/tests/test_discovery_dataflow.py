"""
Exercise optional helper fields, computed records, file includes and branch-origin joins.
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


def test_missing_helper_keys_are_distinct_from_unknown_arguments(tmp_path: Path) -> None:
    """
    Treat omitted literal-dictionary keys as absent without treating unknown supplied values as absent.

    Args:
        tmp_path (Path): Chart receiving a known dictionary and one unknown argument.

    Returns:
        None: Optional reads are quiet; unresolved and invalid nested contexts remain visible.
    """
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ define "helper" }}
          {{ .skipQuote }}{{ .secret }}{{ .defaultValue }}
          {{ .unknown.field }}{{ .missing.field }}
        {{ end }}
        {{ include "helper" (dict "secret" "existing" "unknown" (mystery .Values.source)) }}
        """),
    )
    assert ("source",) in {ref.path for ref in refs}
    messages = {warning.message for warning in warnings}
    assert messages == {"unresolved dot context: .unknown.field", "unresolved dot context: .missing.field"}


def test_parenthesized_fields_are_resolved_as_whole_expressions(tmp_path: Path) -> None:
    """
    Bind selector receivers before emitting references or diagnosing unresolved dot access.

    Args:
        tmp_path (Path): Chart using Bitnami's capabilities expression shape.

    Returns:
        None: Both fallback inputs are found and a separate argument after parentheses remains visible.
    """
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ define "versions" }}
          {{ $versions := default .context.Values.apiVersions ((.context.Values.global).apiVersions) }}
          {{ $versions }}
        {{ end }}
        {{ include "versions" (dict "context" $) }}
        {{ printf "%s%s" (printf "%s" .Values.first) .Values.second }}
        {{ printf "%s%s" ((.Values.left).name) ((.Values.right).name) }}
        {{ if false }}{{ .Values.dead }}{{ else if ((.Values.global).enabled) }}{{ .Values.live }}{{ end }}
        """),
    )
    assert {("apiVersions",), ("global", "apiVersions"), ("first",), ("second",), ("global", "enabled"), ("live",)} <= {
        ref.path for ref in refs
    }
    assert not warnings
    assert {("left", "name"), ("right", "name")} <= {ref.path for ref in refs}


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_template_basepath_includes_preserve_caller_context(tmp_path: Path) -> None:
    """
    Resolve file-template includes using chart metadata and compare their input paths with native Helm.

    Args:
        tmp_path (Path): Directory whose name deliberately differs from the Helm chart name.

    Returns:
        None: An included partial reads the supplied values subtree and dynamic filenames remain diagnostic.
    """
    templates = tmp_path / "templates"
    templates.mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "named-chart", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump({"nested": {"hidden": "default"}}))
    (templates / "_fragment.tpl").write_text("{{ .hidden }}")
    (templates / "config.yaml").write_text(
        dedent("""
        {{ $file := print $.Template.BasePath "/_fragment.tpl" }}
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: example
        data:
          value: {{ include $file .Values.nested | quote }}
        """)
    )
    refs, warnings = discover(tmp_path)
    assert not warnings
    ref = next(ref for ref in refs if ref.path == ("nested", "hidden"))
    assert ref.file == "templates/_fragment.tpl"
    chart = Chart(tmp_path, {"type": "object"}, {"nested": {"hidden": "default"}})
    assert mapping(render(chart, {"nested": {"hidden": "changed"}})[0]["data"])["value"] == "changed"
    (templates / "config.yaml").write_text("{{ include (print $.Template.BasePath .Values.filename) . }}")
    _, warnings = discover(tmp_path)
    assert any("dynamic" in warning.message for warning in warnings)


@pytest.mark.parametrize(
    ("statements", "expected"),
    [
        ("{{ if .Values.flag }}{{ $v = .Values.second }}{{ else }}{{ $v = .Values.third }}{{ end }}", {"second", "third"}),
        ("{{ if .Values.flag }}{{ $v := .Values.second }}{{ end }}", {"first"}),
        ("{{ if .Values.flag }}{{ $v = .Values.second }}{{ $v := .Values.third }}{{ end }}", {"first", "second"}),
        ("{{ with .Values.context }}{{ $v = $.Values.second }}{{ end }}", {"first", "second"}),
        ("{{ range .Values.items }}{{ $v.name }}{{ $v = $.Values.second }}{{ end }}", {"first", "second"}),
        ("{{ range $v := .Values.items }}{{ end }}", {"first"}),
        ("{{ range $item := .Values.items }}{{ $v = $item }}{{ end }}", {"first", "items"}),
    ],
)
def test_branch_and_loop_assignments_join_origins(tmp_path: Path, statements: str, expected: set[str]) -> None:
    """
    Preserve assignments to enclosing variables while excluding shadow declarations.

    Args:
        tmp_path (Path): Chart with a variable surviving branches or iterations.
        statements (str): Structured mutations of the lexical binding.
        expected (set[str]): Root input names that can supply the selected name field.

    Returns:
        None: All possible source fields are discovered without reassignment warnings or leaked shadows.
    """
    refs, warnings = scan(tmp_path, "{{ $v := .Values.first }}" + statements + "{{ $v.name }}")
    assert not warnings
    assert {ref.path[0] for ref in refs if ref.path[-1:] == ("name",)} == expected


def test_nonconverging_loop_origins_remain_visible(tmp_path: Path) -> None:
    """
    Bound loops that can grow symbolic paths indefinitely without declaring discovery complete.

    Args:
        tmp_path (Path): Chart whose assignment follows a deeper path on every iteration.

    Returns:
        None: The loop budget produces a diagnostic and retains discovered paths alongside uncertainty.
    """
    refs, warnings = scan(tmp_path, "{{ $v := .Values.tree }}{{ range .Values.items }}{{ $v = $v.next }}{{ end }}{{ $v.name }}")
    assert any("did not converge" in warning.message for warning in warnings)
    assert any("unresolved variable context: $v.name" == warning.message for warning in warnings)
    assert ("tree", "name") in {ref.path for ref in refs}


def test_unknown_alternatives_and_malformed_helper_arguments_remain_visible(tmp_path: Path) -> None:
    """
    Keep unsupported alternatives and malformed dictionaries diagnostic after resolving supported cases.

    Args:
        tmp_path (Path): Chart mixing supported sources with an unresolved transformation.

    Returns:
        None: Discovery retains known inputs without treating unknown branches as fully resolved.
    """
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ $value := .Values.known }}
        {{ if .Values.enabled }}{{ $value = mystery .Values.other }}{{ end }}
        {{ $value.name }}
        {{ (mystery .Values.other).unknown }}
        {{ define "merge" }}{{ .values.name }}{{ end }}
        {{ include "merge" (dict "values" .Values.first .Values.second "context" .) }}
        """),
    )
    assert {("known", "name"), ("other",), ("first",), ("second",)} <= {ref.path for ref in refs}
    messages = {warning.message for warning in warnings}
    assert "unresolved variable context: $value.name" in messages
    assert any(message.startswith("unresolved parenthesized context:") for message in messages)
    assert any("dict has an unpaired key" in message for message in messages)
    assert "helper context is dynamic or unsupported: merge" not in messages


def test_derived_records_and_external_results_keep_input_dependencies(tmp_path: Path) -> None:
    """
    Recognize semver and certificate result fields without inventing corresponding values paths.

    Args:
        tmp_path (Path): Chart combining derived records and a cluster lookup.

    Returns:
        None: Derived selectors resolve, source inputs remain visible, and external operations warn at their call sites.
    """
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ $tag := .Values.image.tag | toString }}
        {{ $version := semver $tag }}
        {{ $version.Major }}{{ $version.Minor }}{{ $version.Patch }}
        {{ $ca := genCA "ca" 365 }}
        {{ $cert := genSignedCert .Values.hostname nil (list .Values.hostname) 365 $ca }}
        {{ $cert.Cert }}{{ $cert.Key }}
        {{ define "secret" }}
          {{ $secretData := (lookup "v1" "Secret" .context.Release.Namespace .secret).data }}
          {{ $value := index $secretData .key }}
          {{ if not $value }}{{ $value = .defaultValue | toString | b64enc }}{{ end }}
          {{ $value }}{{ .skipQuote }}
        {{ end }}
        {{ $secretName := printf "%s-tls" .Values.secretName }}
        {{ include "secret" (dict "secret" $secretName "key" "tls.crt" "defaultValue" $cert.Cert "context" $) }}
        """),
    )
    found = {ref.path for ref in refs}
    assert {("image", "tag"), ("hostname",), ("secretName",)} <= found
    assert not any(part in {"Major", "Minor", "Patch", "Cert", "Key", "data"} for path in found for part in path)
    assert len(warnings) == 3
    assert all("result left to Helm" in warning.message for warning in warnings)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_assignment_discovery_matches_native_branches(tmp_path: Path) -> None:
    """
    Compare joined symbolic origins with the values selected by each real Helm branch.

    Args:
        tmp_path (Path): Renderable chart with branch-dependent reassignment.

    Returns:
        None: Both discovered source fields affect the output in the corresponding configuration.
    """
    defaults = {"enabled": False, "left": {"name": "left"}, "right": {"name": "right"}}
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "branches", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    refs, warnings = scan(
        tmp_path,
        dedent("""
        {{ $chosen := .Values.left }}
        {{ if .Values.enabled }}{{ $chosen = .Values.right }}{{ end }}
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: example
        data:
          selected: {{ $chosen.name | quote }}
        """),
    )
    assert not warnings
    assert {("left", "name"), ("right", "name")} <= {ref.path for ref in refs}
    chart = Chart(tmp_path, {"type": "object"}, mapping(defaults))
    for enabled, expected in ((False, "left"), (True, "right")):
        assert mapping(render(chart, {"enabled": enabled})[0]["data"])["selected"] == expected
