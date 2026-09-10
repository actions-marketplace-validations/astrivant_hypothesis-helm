"""
Verify templates.
"""

from pathlib import Path

from hypothesis_helm.charts.templates import Diagnostic, Reference, discover, parse


def scan(tmp_path: Path, text: str) -> tuple[list[Reference], list[Diagnostic]]:
    """
    Check scan.

    Args:
        tmp_path (Path): Temporary directory supplied by pytest.
        text (str): YAML or template text to process.

    Returns:
        tuple[list[Reference], list[Diagnostic]]: Result of the documented operation.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "test.yaml").write_text(text)
    return discover(tmp_path)


def test_scopes_aliases_and_lookups(tmp_path: Path) -> None:
    """
    Verify scopes aliases and lookups.

    Args:
        tmp_path (Path): Temporary directory supplied by pytest.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    refs, warnings = scan(
        tmp_path,
        """{{ $root := . }}{{ $v := .Values }}
{{ with .Values.image }}{{ .tag }}{{ $root.Values.enabled }}{{ end }}
{{ range $item := .Values.items }}{{ .name }}{{ $item.port }}{{ end }}
{{ $v.hidden | default "fallback" }}
{{ index .Values "hyphen-key" "child" }}
{{ (index .Values "other").nested }}
{{ dig "nested" "key" "default" .Values }}""",
    )
    paths = {r.path for r in refs}
    assert {
        ("image", "tag"),
        ("enabled",),
        ("items", "*", "name"),
        ("items", "*", "port"),
        ("hidden",),
        ("hyphen-key", "child"),
        ("other", "nested"),
        ("nested", "key"),
    } <= paths
    assert any(r.path == ("hidden",) and r.fallback for r in refs)
    assert not warnings


def test_comments_strings_and_delimiters(tmp_path: Path) -> None:
    """
    Verify comments strings and delimiters.

    Args:
        tmp_path (Path): Temporary directory supplied by pytest.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    refs, warnings = scan(
        tmp_path, '{{/* .Values.fake }} */}}{{ "}} .Values.fake" }}{{ .Values.real }}'
    )
    assert {r.path for r in refs} == {("real",)}
    assert not warnings


def test_unresolved_is_visible(tmp_path: Path) -> None:
    """
    Verify unresolved is visible.

    Args:
        tmp_path (Path): Temporary directory supplied by pytest.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    _, warnings = scan(
        tmp_path,
        '{{ index .Values $key }}{{ tpl .Values.content . }}{{ define "x" }}{{ .thing }}{{ end }}',
    )
    assert any("dynamic key" in w.message for w in warnings)
    assert any("named template" in w.message for w in warnings)
    assert any("unresolved dot" in w.message for w in warnings)


def test_invalid_blocks() -> None:
    """
    Verify invalid blocks.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    import pytest

    for source in ("{{ if .Values.x }}", "{{ end }}", '{{ "unterminated }}'):
        with pytest.raises(ValueError):
            parse(source)


def test_dig_pipeline_and_range_key(tmp_path: Path) -> None:
    """
    Verify dig pipeline and range key.

    Args:
        tmp_path (Path): Temporary directory supplied by pytest.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    refs, _ = scan(
        tmp_path,
        '{{ dig "nested" "key" "fallback" .Values | quote }}{{ range '
        "$key, $value := .Values.map }}{{ $key.name }}{{ $value.port "
        "}}{{ end }}",
    )
    paths = {r.path for r in refs}
    assert ("nested", "key") in paths
    assert ("map", "*", "port") in paths
    assert ("map", "*", "name") not in paths
