from hypothesis_helm.templates import discover, parse


def scan(tmp_path, text):
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "test.yaml").write_text(text)
    return discover(tmp_path)


def test_scopes_aliases_and_lookups(tmp_path):
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


def test_comments_strings_and_delimiters(tmp_path):
    refs, warnings = scan(
        tmp_path, '{{/* .Values.fake }} */}}{{ "}} .Values.fake" }}{{ .Values.real }}'
    )
    assert {r.path for r in refs} == {("real",)}
    assert not warnings


def test_unresolved_is_visible(tmp_path):
    _, warnings = scan(
        tmp_path,
        '{{ index .Values $key }}{{ tpl .Values.content . }}{{ define "x" }}{{ .thing }}{{ end }}',
    )
    assert any("dynamic key" in w.message for w in warnings)
    assert any("named template" in w.message for w in warnings)
    assert any("unresolved dot" in w.message for w in warnings)


def test_invalid_blocks():
    import pytest

    for source in ("{{ if .Values.x }}", "{{ end }}", '{{ "unterminated }}'):
        with pytest.raises(ValueError):
            parse(source)
