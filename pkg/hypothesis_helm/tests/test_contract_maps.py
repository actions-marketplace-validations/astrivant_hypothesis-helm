"""
Check flat-map merge semantics and conservative barriers for shared mutations against Helm.
"""

import json
import shutil
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contract_values import BoundValue, native
from hypothesis_helm.compiler.asts.contracts import Contracts, Evaluation, expression
from hypothesis_helm.compiler.asts.transformations import UnsupportedTransformation, calculate
from hypothesis_helm.schemas.contracts import mapping
from hypothesis_helm.tests.test_contract_control_flow import control_chart as control_chart


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("function", ["mergeOverwrite", "mustMergeOverwrite"])
def test_flat_merge_matches_helm(control_chart: Chart, function: str) -> None:
    """
    Compare scalar overwrite precedence and winning input provenance with native rendering.

    Args:
        control_chart (Chart): Isolated chart directory and values.
        function (str): Supported fresh-map merge alias.

    Returns:
        None: Empty strings, false, zero and null match Helm without modifying either source map.
    """
    values: dict[str, object] = {
        "first": {"text": "old", "empty": "old", "bool": True, "number": 3, "nil": "old", "retained": "yes"},
        "second": {"text": "new", "empty": "", "bool": False, "number": 0, "nil": None, "example.org/name": "new"},
    }
    (control_chart.path / "values.yaml").write_text("{}\n")
    statement = f"{function} (dict) .Values.first .Values.second"
    (control_chart.path / "templates/config.yaml").write_text(
        dedent(f"""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: control
        data:
          merged: {{{{ {statement} | toJson | quote }}}}
        """)
    )
    before = yamlio.dump(values)
    evaluator = Evaluation(Contracts.build(control_chart.path), values, context={"Values": BoundValue(values, ())})
    merged = mapping(evaluator.evaluate(expression(statement), "test", 1, Scope()))
    actual = render(control_chart, values)
    expected = json.loads(str(mapping(actual[0]["data"])["merged"]))
    assert {key: native(value) for key, value in merged.items()} == expected
    assert evaluator.evaluate(expression("$merged.text"), "test", 1, Scope({"$merged": merged})) is merged["text"]
    assert evaluator.inputs["$.second.text"] == "new"
    assert yamlio.dump(values) == before


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    "body",
    [
        '{{ $_ := mergeOverwrite .Values.nested (dict "mode" "good") }}',
        '{{ $alias := .Values.nested }}{{ $_ := mergeOverwrite $alias (dict "mode" "good") }}',
        '{{ $_ := mergeOverwrite (dict) (dict "nested" .Values.nested) (dict "nested" (dict "mode" "good")) }}',
        '{{ $_ := mergeOverwrite (dict) (set .Values.nested "mode" "good") }}',
    ],
)
def test_shared_merges_cannot_authorize_rejection(control_chart: Chart, body: str) -> None:
    """
    Refuse a false prediction when merging changes the input inspected by a later guard.

    Args:
        control_chart (Chart): The initial nested mode is bad.
        body (str): Direct, aliased, nested or argument-level mutation that changes that mode.

    Returns:
        None: Helm succeeds and the compiler retains the candidate with an explicit analysis diagnostic.
    """
    (control_chart.path / "templates/NOTES.txt").write_text(body + '{{ if eq .Values.nested.mode "bad" }}{{ fail "stale value" }}{{ end }}')
    contracts = Contracts.build(control_chart.path)
    before = yamlio.dump(control_chart.defaults)
    assert contracts.predict(control_chart.defaults) is None
    assert contracts.fallbacks
    assert yamlio.dump(control_chart.defaults) == before
    render(control_chart, {})


@pytest.mark.parametrize(
    "function, arguments", [("nindent", (1000000000, "x")), ("indent", (-1, "x")), ("quote", ("x" * 8192, "x" * 8192))]
)
def test_formatting_respects_output_budget(function: str, arguments: tuple[object, ...]) -> None:
    """
    Reject output expansion before allocating oversized indentation or joined quotations.

    Args:
        function (str): Supported formatter.
        arguments (tuple[object, ...]): Operands whose result exceeds its supported budget.

    Returns:
        None: The bounded evaluator retains these operations for Helm.
    """
    with pytest.raises(UnsupportedTransformation, match="compiler.max_string_chars"):
        calculate(function, arguments)
