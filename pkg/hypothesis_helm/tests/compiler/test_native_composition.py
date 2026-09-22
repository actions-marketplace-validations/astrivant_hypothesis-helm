"""
Keep native builtin composition deterministic without losing types, aliases or resource limits.
"""

import json
import shutil
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.compiler.asts import native_operations
from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contract_values import BoundValue, NativeValue, native
from hypothesis_helm.compiler.asts.contracts import Evaluation, expression
from hypothesis_helm.compiler.limits import DEFAULT_LIMITS
from hypothesis_helm.environment import env
from hypothesis_helm.exceptions.compiler import Unavailable, Unknown
from hypothesis_helm.schemas.contracts import mapping
from hypothesis_helm.tests.compiler.test_contract_control_flow import control_chart as control_chart
from hypothesis_helm.tests.compiler.test_renderer_context import configured


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    "statement",
    [
        'date "2006" "not a date"',
        'date "2006" .Values.enabled',
        'durationRound (toDate "2006" "2026")',
        'durationRound (default (toDate "2006" "2026") nil)',
        'values (dict "a" 1 "b" 2)',
        'print (keys (dict "a" 1 "b" 2))',
        'eq (semver "1.2.3") "1.2.3"',
        'fail (semver "1.2.3")',
        'b32dec "74======"',
    ],
)
def test_uncertain_native_results_cannot_become_concrete(control_chart: Chart, statement: str) -> None:
    """
    Keep implicit clocks, order dependence, incompatible Go types and binary strings unresolved.

    Args:
        control_chart (Chart): Isolated chart supplying a renderer context.
        statement (str): Operand case which cannot establish a concrete static result.

    Returns:
        None: No sampled order, clock result or JSON coercion is accepted as a proof.
    """
    evaluator = Evaluation(configured(control_chart), control_chart.defaults, context={"Values": BoundValue(control_chart.defaults, ())})
    with pytest.raises(Unknown):
        evaluator.evaluate(expression(statement), "composition", 1, Scope())


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_native_copy_preserves_local_aliases_without_changing_inputs(control_chart: Chart) -> None:
    """
    Mutate aliases to a deep copy while preserving the original chart values.

    Args:
        control_chart (Chart): Chart containing nested input values.

    Returns:
        None: The local aliases share the write, input values do not, and stale native recipes defer.
    """
    original = json.dumps(control_chart.defaults, sort_keys=True)
    evaluator = Evaluation(configured(control_chart), control_chart.defaults, context={"Values": BoundValue(control_chart.defaults, ())})
    scope = Scope()
    copied = evaluator.pipeline("$copy := deepCopy .Values.nested", "composition", 1, scope)
    evaluator.pipeline("$alias := $copy", "composition", 2, scope)
    evaluator.pipeline('$_ := set $alias "mode" "changed"', "composition", 3, scope)
    assert mapping(native(copied))["mode"] == "changed"
    assert native(evaluator.pipeline("$copy.mode", "composition", 4, scope)) == "changed"
    assert json.dumps(control_chart.defaults, sort_keys=True) == original
    with pytest.raises(Unknown, match="mutated"):
        evaluator.pipeline("toJson $copy", "composition", 5, scope)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_native_recipes_freeze_input_arguments_and_never_execute_input_text(control_chart: Chart) -> None:
    """
    Preserve an evaluated snapshot even when the caller later changes the original values.

    Args:
        control_chart (Chart): Private chart used to evaluate a native map copy.

    Returns:
        None: Template-looking text stays data and recipe inputs remain frozen.
    """
    values: dict[str, object] = {"text": '{{ fail "must stay data" }}'}
    evaluator = Evaluation(configured(control_chart), values, context={"Values": BoundValue(values, ())})
    scope = Scope()
    copied = evaluator.pipeline("$copy := deepCopy .Values", "composition", 1, scope)
    assert isinstance(copied, NativeValue)
    values["text"] = "changed"
    assert native(evaluator.pipeline('get $copy "text"', "composition", 2, scope)) == '{{ fail "must stay data" }}'


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_helper_prints_native_time_using_go_semantics(control_chart: Chart) -> None:
    """
    Distinguish time.Time's template text from its JSON transport encoding.

    Args:
        control_chart (Chart): Chart with a helper returning a native time value as text.

    Returns:
        None: The helper's compiler result matches a complete independent Helm render.
    """
    (control_chart.path / "templates/_helpers.tpl").write_text('{{ define "native.time" }}{{ toDate "2006-01-02" "2026-01-02" }}{{ end }}')
    (control_chart.path / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: time
        data:
          result: {{ include "native.time" . | quote }}
        """)
    )
    evaluator = Evaluation(configured(control_chart), control_chart.defaults, context={"Values": BoundValue(control_chart.defaults, ())})
    observed = evaluator.evaluate(expression('include "native.time" .'), "composition", 1, Scope())
    expected = mapping(render(control_chart, {})[0]["data"])["result"]
    assert observed == expected


def test_native_nonfinite_and_cyclic_operands_never_launch_a_process(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Bound invalid operand graphs before serialization or process creation.

    Args:
        monkeypatch (pytest.MonkeyPatch): Make an unexpected native process fail the test.

    Returns:
        None: Cycles and nonfinite numbers are explicit unavailable-analysis outcomes.
    """
    monkeypatch.setattr(native_operations, "probe", lambda *args: pytest.fail("invalid operand reached native execution"))
    cycle: list[object] = []
    cycle.append(cycle)
    for value in (cycle, float("nan"), float("inf")):
        with pytest.raises(Unavailable):
            native_operations.evaluate("typeOf", [value], helm="helm", timeout=1, limits=DEFAULT_LIMITS)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_native_date_cache_respects_timezone(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Avoid reusing a local-date result after its renderer timezone changes.

    Args:
        monkeypatch (pytest.MonkeyPatch): Select two explicit Go timezone contexts.

    Returns:
        None: Each evaluation uses its own timezone despite identical function arguments.
    """
    observed = []
    for timezone in ("UTC", "America/New_York"):
        monkeypatch.setitem(env, "TZ", timezone)
        observed.append(native_operations.evaluate("date", ["2006-01-02", 0], helm="helm", timeout=5, limits=DEFAULT_LIMITS))
    assert observed == ["1970-01-01", "1969-12-31"]
