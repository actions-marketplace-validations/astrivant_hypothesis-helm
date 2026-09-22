"""
Compare helper contract gaps with native Helm, including conservative boundary cases.
"""

import json
import shutil
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.compiler.asts import native_operations
from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contract_values import BoundValue, native
from hypothesis_helm.compiler.asts.contracts import Evaluation, expression
from hypothesis_helm.compiler.limits import DEFAULT_LIMITS
from hypothesis_helm.exceptions.compiler import Unavailable, Unknown
from hypothesis_helm.schemas.contracts import mapping
from hypothesis_helm.tests.compiler.test_contract_control_flow import control_chart as control_chart
from hypothesis_helm.tests.compiler.test_renderer_context import configured


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    "statement",
    [
        'has "" (list .Values.nested.mode)',
        'has "bad" (list .Values.nested.mode)',
        'has "bad" (ternary (splitList "," .Values.nested.mode) (list .Values.nested.mode) false)',
        'coalesce (((.Values.missing).auth).existingSecret) "fallback"',
        'coalesce (((.Values.nested.missing).auth).existingSecret) "fallback"',
        'squote "can\'t" true false nil',
        "quote 123",
        "quote (int 123)",
        'first (reverse (list .Values.nested.mode "last"))',
        'printf "%v" (default "" .Values.nested.mode)',
        "print 27017",
        "print 1 2",
        'print 1 "" 2',
        "print true false nil",
        'print .Values.enabled "-" 3',
        'print (int 2) (int64 3) (atoi "4")',
        'print (dict "port" 27017 "enabled" true)',
        "print (list 1 2 .Values.enabled)",
        'print (fromJson `{"port":27017}`)',
        'println 1 2 "end"',
        "println",
        "print",
        'quote 1 false nil "hello"',
        'printf "%08.2f %T" (float64 "2.5") (until 3)',
        'printf "%T %T %T" (until 3) (list 0 1 2) (mustToDuration "1s")',
        'printf "%v" (toDate "2006-01-02" "2026-01-02")',
        'kindIs "struct" (toDate "2006-01-02" "2026-01-02")',
        'date "2006-01-02 15:04" (dateModify "1h" (toDate "2006-01-02" "2026-01-02"))',
        'dateInZone "2006-01-02 MST" 0 "UTC"',
        '(semver "1.2.3-alpha+metadata").Major',
        '(semver "1.2.3-alpha+metadata").Prerelease',
        'printf "%T / %v" (index (until 3) 1) (index (until 3) 1)',
        "eq (index (until 3) 1) 1",
        'print (fromJson `{"port":27017}`).port',
        'typeOf (default (semver "1.2.3") nil)',
        'typeOf (get (fromJson `{"port":27017}`) "port")',
        'printf "%s" (list (toDate "2006-01-02" "2026-01-02"))',
        "deepEqual (list (int64 1)) (list (int 1))",
        'toJson (append (list 1) (float64 "1.5"))',
        'typeOf (toJson (dict "x" 1))',
        "slice (until 6) 1 4",
        'durationSeconds (durationRoundTo "1h2m" "1h")',
        'typeIs "string" .Values.nested.mode',
        'typeIs "string" .Values.items',
        "eq .Values.missing false",
        'ne .Values.missing ""',
        "eq .Values.missing nil",
        'sha256sum "é hello"',
        'b64enc "é hello"',
        'b64dec "aGVsbG8="',
        'b64dec "invalid-base64"',
        'toYaml (dict "mode" .Values.nested.mode "items" .Values.items "none" nil "number" 3)',
        'toJson (dict "html" "<>&" "mode" .Values.nested.mode "nil" nil)',
        'get (fromYaml "mode: bad\\ncount: 2\\n") "mode"',
        'get (fromJson `{"mode":"bad","count":2}`) "mode"',
        "toJson (concat (list))",
        "toYaml (concat (list))",
        'toJson (dict "empty" (concat (list)))',
        'toYaml (dict "empty" (concat (list)))',
        'kindIs "slice" (concat (list))',
        "eq (concat (list)) nil",
        'eq (fromJson "null") nil',
        'kindIs "map" (fromJson "null")',
        'toJson (fromJson "null")',
        'toYaml (fromJson "null")',
        'regexReplaceAll `(-?[^a-z\\d\\-])+-?` "a._b--c" "-"',
        'regexReplaceAll `([a-z]+)([0-9]+)` "a12 b34" "${2}-${1}"',
        'regexReplaceAllLiteral `(a)` "a" "$1"',
        'regexReplaceAll "a*" "aba" "x"',
        'regexMatch "[[:alpha:]]+" "Hello"',
        'regexMatch `\\p{L}+` "é"',
        'regexMatch "(?i)^(abc|def)$" "ABC"',
        'mustRegexFind "(ab|cd)+" "zzabcd"',
        'regexMatch "(?=a)" "a"',
        'regexMatch "a*a*" "a"',
    ],
)
def test_concrete_helpers_match_helm(control_chart: Chart, statement: str) -> None:
    """
    Compare contract evaluation with an independent chart render of the same expression.

    Args:
        control_chart (Chart): Isolated source chart and candidate values.
        statement (str): A previously unsupported helper expression.

    Returns:
        None: Both evaluators produce the same concrete JSON-compatible value.
    """
    (control_chart.path / "templates/config.yaml").write_text(
        dedent(f"""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: comparison
        data:
          result: {{{{ {statement} | toJson | quote }}}}
        """)
    )
    values = control_chart.defaults
    evaluator = Evaluation(configured(control_chart), values, context={"Values": BoundValue(values, ())})
    observed = native(evaluator.evaluate(expression(statement), "test", 1, Scope()))
    expected = json.loads(str(mapping(render(control_chart, {})[0]["data"])["result"]))
    assert observed == expected
    # Reading one sampled list never establishes an input enum.
    assert not evaluator.enums


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("merge", ["merge", "mustMerge", "mergeOverwrite", "mustMergeOverwrite"])
def test_local_maps_and_parsed_helper_output(control_chart: Chart, merge: str) -> None:
    """
    Exercise local aliases, parsed helpers, loops and both flat-map precedence rules.

    Args:
        control_chart (Chart): Isolated chart.
        merge (str): Native merge operation to compare.

    Returns:
        None: The compiler follows the same branch as Helm without mutating chart inputs.
    """
    source = dedent(f"""
    {{{{- define "serialized" -}}}}
    {{{{- toYaml (dict "mode" .Values.nested.mode "empty" "" "bool" false "nil" nil) -}}}}
    {{{{- end -}}}}
    {{{{- $dst := dict "mode" "initial" "empty" "" "bool" false "nil" nil -}}}}
    {{{{- $alias := $dst -}}}}
    {{{{- $_ := set $alias "added" .Values.enabled -}}}}
    {{{{- range list (include "serialized" .) -}}}}
    {{{{- $dst = . | fromYaml | {merge} $dst -}}}}
    {{{{- end -}}}}
    {{{{- $_ := unset $alias "added" -}}}}
    {{{{- pick $dst "mode" "empty" "bool" "nil" | toJson -}}}}
    """)
    # Register both helpers at file scope, as required by Go templates.
    first_end = source.index("{{- end -}}") + len("{{- end -}}")
    (control_chart.path / "templates/_helpers.tpl").write_text(
        source[:first_end] + '{{ define "assemble" }}' + source[first_end:] + "{{ end }}"
    )
    (control_chart.path / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: comparison
        data:
          result: {{ include "assemble" . | quote }}
        """)
    )
    values = control_chart.defaults
    before = json.dumps(values, sort_keys=True)
    evaluator = Evaluation(configured(control_chart), values, context={"Values": BoundValue(values, ())})
    observed = evaluator.evaluate(expression('include "assemble" .'), "test", 1, Scope())
    expected = mapping(render(control_chart, {})[0]["data"])["result"]
    assert json.loads(str(observed)) == json.loads(str(expected))
    assert json.dumps(values, sort_keys=True) == before
    assert not evaluator.enums


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_included_file_registers_but_does_not_execute_definitions(control_chart: Chart) -> None:
    """
    Avoid executing declaration bodies while including a complete template file.

    Args:
        control_chart (Chart): Chart with an included configuration template.

    Returns:
        None: Uncalled rejecting definitions do not prevent the actual guard being analyzed.
    """
    (control_chart.path / "templates/fragment.yaml").write_text(
        dedent("""
        {{- define "never-called" -}}{{ fail "declarations do not run" }}{{- end -}}
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: fragment
        """)
    )
    (control_chart.path / "templates/NOTES.txt").write_text(
        dedent("""
        {{- $fragment := include (print $.Template.BasePath "/fragment.yaml") . -}}
        {{- if contains "fragment" $fragment -}}{{ fail "included body reached" }}{{- end -}}
        """)
    )
    contracts = configured(control_chart)
    result = contracts.predict(control_chart.defaults)
    assert result is not None and "included body reached" in str(result)
    assert not contracts.fallbacks


def test_local_mutation_cannot_create_a_literal_enum(control_chart: Chart) -> None:
    """
    Invalidate constant-key evidence through all aliases when a dictionary is mutated.

    Args:
        control_chart (Chart): Chart providing sampled keys and values.

    Returns:
        None: Membership remains evaluable without creating a false domain restriction.
    """
    values = control_chart.defaults
    evaluator = Evaluation(configured(control_chart), values, context={"Values": BoundValue(values, ())})
    variables = Scope()
    evaluator.pipeline('$m := dict "literal" true', "test", 1, variables)
    evaluator.pipeline("$alias := $m", "test", 2, variables)
    evaluator.evaluate(expression("set $alias .Values.nested.mode true"), "test", 3, variables)
    assert evaluator.evaluate(expression('hasKey $m "missing"'), "test", 4, variables) is False
    variables.bind("$key", BoundValue("missing", ("selected",)))
    assert evaluator.evaluate(expression("hasKey $m $key"), "test", 5, variables) is False
    assert not evaluator.enums


def test_local_aliases_do_not_own_nested_inputs(control_chart: Chart) -> None:
    """
    Reject writes to a shared child map and prevent local cyclic structures.

    Args:
        control_chart (Chart): Chart with a shared nested values map.

    Returns:
        None: Neither the input map nor the local map changes after an unsupported write.
    """
    values = control_chart.defaults
    evaluator = Evaluation(configured(control_chart), values, context={"Values": BoundValue(values, ())})
    scope = Scope()
    evaluator.pipeline('$m := dict "child" .Values.nested', "test", 1, scope)
    with pytest.raises(Unknown, match="shared context"):
        evaluator.evaluate(expression('set $m.child "mode" "changed"'), "test", 2, scope)
    assert mapping(values["nested"])["mode"] == "bad"
    with pytest.raises(Unknown, match="cyclic"):
        evaluator.evaluate(expression('set $m "self" $m'), "test", 3, scope)
    assert "self" not in mapping(native(scope.lookup("$m")))
    with pytest.raises(Unknown, match="missing parent"):
        evaluator.evaluate(expression(".Values.missing.parent.child"), "test", 4, scope)


@pytest.mark.parametrize(
    "function,arguments,limit,value",
    [
        ("regexMatch", ["aaaa", "a"], "max_regex_pattern_chars", 3),
        ("regexFind", ["a", "aaaa"], "max_regex_subject_chars", 3),
        ("regexReplaceAll", ["a*", "aaa", "xxxx"], "max_string_chars", 8),
        ("toYaml", [{"nested": {"value": "x"}}], "max_range_items", 2),
        ("print", ["abcdefgh"], "max_string_chars", 8),
        ("println", [1, 2, 3], "max_range_items", 2),
        ("repeat", [1000, "abc"], "max_string_chars", 100),
        ("until", [1000], "max_range_items", 100),
        ("untilStep", [0, 1000, 1], "max_range_items", 100),
        ("seq", [1, 1000], "max_range_items", 100),
        ("printf", ["%1000000000s", "x"], "max_string_chars", 100),
        ("printf", ["%*s", 1000000000, "x"], "max_string_chars", 100),
        ("wrapWith", [1, "x" * 100, "a b c d"], "max_string_chars", 1000),
        ("chunk", [1000000000, [1]], "max_range_items", 100),
    ],
)
def test_native_budgets_apply_before_subprocess(
    monkeypatch: pytest.MonkeyPatch, function: str, arguments: list[object], limit: str, value: int
) -> None:
    """
    Keep oversized operands from reaching a renderer process.

    Args:
        monkeypatch (pytest.MonkeyPatch): Replace the native process entry point.
        function (str): Operation exceeding a budget.
        arguments (list[object]): Concrete operands.
        limit (str): Compiler budget to reduce.
        value (int): New budget.

    Returns:
        None: An explicit budget diagnostic is raised before native evaluation.
    """
    monkeypatch.setattr(native_operations, "probe", lambda *args: pytest.fail("oversized probe was invoked"))
    with pytest.raises(Unavailable, match="compiler\\."):
        native_operations.evaluate(function, arguments, helm="helm", timeout=1, limits={**DEFAULT_LIMITS, limit: value})


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_native_errors_remain_unknown_and_cached_maps_are_private(control_chart: Chart) -> None:
    """
    Preserve native failure boundaries and avoid sharing parsed mutable cache entries.

    Args:
        control_chart (Chart): Isolated configured renderer.

    Returns:
        None: Invalid required regex evaluation stays unknown; later parsed maps stay unchanged.
    """
    evaluator = Evaluation(configured(control_chart), {})
    with pytest.raises(Unknown, match="native Helm"):
        evaluator.evaluate(expression('mustRegexMatch "(?=a)" "a"'), "test", 1, Scope())
    with pytest.raises(Unknown, match="non-UTF-8"):
        evaluator.evaluate(expression('b64dec "/w=="'), "test", 1, Scope())
    first = native(evaluator.evaluate(expression('fromYaml "key: old"'), "test", 2, Scope()))
    assert isinstance(first, dict)
    first["key"] = "mutated"
    second = native(evaluator.evaluate(expression('fromYaml "key: old"'), "test", 3, Scope()))
    assert second == {"key": "old"}


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("function", ["merge", "mustMerge", "mergeOverwrite", "mustMergeOverwrite"])
def test_local_merge_scalar_precedence_matrix(control_chart: Chart, function: str) -> None:
    """
    Compare every supported empty/nonempty scalar pair with Go's merge implementation.

    Args:
        control_chart (Chart): Chart collecting the comparison outputs in one render.
        function (str): Sprig merge operation.

    Returns:
        None: Every local merge agrees with Helm, including changes of scalar type.
    """
    scalars = ["nil", "false", "true", "0", "1", '""', '"value"']
    statements = [f'{function} (dict "value" {left}) (dict "value" {right})' for left in scalars for right in scalars]
    body = dedent("""
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: precedence
    data:
    """)
    body += "".join(f"  case{index}: {{{{ {statement} | toJson | quote }}}}\n" for index, statement in enumerate(statements))
    (control_chart.path / "templates/config.yaml").write_text(body)
    expected = mapping(render(control_chart, {})[0]["data"])
    for index, statement in enumerate(statements):
        evaluator = Evaluation(configured(control_chart), {})
        result = evaluator.evaluate(expression(statement), "test", 1, Scope())
        observed = native_operations.plain(result, DEFAULT_LIMITS)
        assert observed == json.loads(str(expected[f"case{index}"])), statement
