"""
Compare bounded printf diagnostics and eager helper evaluation with native Helm.
"""

import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contract_values import BoundValue, ContractText, DerivedValue, KeyList
from hypothesis_helm.compiler.asts.contracts import Contracts, Evaluation, expression
from hypothesis_helm.compiler.asts.formatting import printf
from hypothesis_helm.compiler.passes.rejections import matches_rejection
from hypothesis_helm.exceptions.compiler import Unknown
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import mapping


@pytest.fixture
def printf_chart(tmp_path: Path) -> Chart:
    """
    Create a small chart with a valid manifest and replaceable formatting expressions.

    Args:
        tmp_path (Path): Fixture directory.

    Returns:
        Chart: Chart independent of Bitnami's names and installed dependencies.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(
        dedent("""
        apiVersion: v2
        name: formatting
        version: 1.0.0
        """)
    )
    defaults: dict[str, object] = {"reject": False, "count": 2}
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    return Chart(tmp_path, {"type": "object"}, defaults)


def manifest(chart: Chart, output: str) -> None:
    """
    Render an arbitrary expression safely inside a ConfigMap string field.

    Args:
        chart (Chart): Prepared fixture.
        output (str): Trusted test template expression.

    Returns:
        None: The fixture can be rendered directly with Helm.
    """
    (chart.path / "templates/config.yaml").write_text(
        dedent(f"""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: formatting
        data:
          result: {{{{ {output} | quote }}}}
        """)
    )


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    ("call", "expected"),
    [
        ('printf "%s." nil', "%!s(<nil>)."),
        ('printf "%s" true', "%!s(bool=true)"),
        ('printf "%d" false', "%!d(bool=false)"),
        ('printf "%d" "two"', "%!d(string=two)"),
        ('printf "%d" "a\\nb%"', "%!d(string=a\nb%)"),
        ('printf "%d" nil', "%!d(<nil>)"),
        ('printf "%s" 2', "%!s(int=2)"),
        ('printf "%s" (int64 2)', "%!s(int64=2)"),
        ('printf "%s" (int 2)', "%!s(int=2)"),
        ('printf "%s" (atoi "2")', "%!s(int=2)"),
        ('printf "%s" (add 1 1)', "%!s(int64=2)"),
        ('printf "%d" (int64 2)', "2"),
        ('printf "%v:%v:%v" nil false 2', "<nil>:false:2"),
        ('printf "%s"', "%!s(MISSING)"),
        ('printf "%s/%d/%v"', "%!s(MISSING)/%!d(MISSING)/%!v(MISSING)"),
        ('printf "%s/%d" "present"', "present/%!d(MISSING)"),
        ('printf "plain" "extra"', "plain%!(EXTRA string=extra)"),
        ('printf "" nil false 2 (int64 3)', "%!(EXTRA <nil>, bool=false, int=2, int64=3)"),
        ('printf "%%%s" "x" "y"', "%x%!(EXTRA string=y)"),
        ('printf "100%%"', "100%"),
        ('printf "trailing%"', "trailing%!(NOVERB)"),
        ('printf "%" true', "%!(NOVERB)%!(EXTRA bool=true)"),
        ('printf "%s%" nil', "%!s(<nil>)%!(NOVERB)"),
    ],
)
def test_printf_diagnostics_match_native_helm(printf_chart: Chart, call: str, expected: str) -> None:
    """
    Check valid and malformed scalar formatting against Go rather than Python's interpolation rules.

    Args:
        printf_chart (Chart): Native comparison fixture.
        call (str): Template printf expression.
        expected (str): Go's exact resulting text, including format-error markers.

    Returns:
        None: Compiler output and native Helm agree on all observed characters.
    """
    manifest(printf_chart, call)
    evaluator = Evaluation(Contracts.build(printf_chart.path), printf_chart.defaults)
    assert evaluator.evaluate(expression(call), "comparison", 1, Scope()) == expected
    assert mapping(render(printf_chart, {}, stream=False)[0]["data"])["result"] == expected


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    ("argument", "prefix"), [("", ""), ('"subchart" nil', ""), ('"subchart" ""', ""), ('"subchart" false', ""), ('"subchart" "db"', "db.")]
)
@pytest.mark.parametrize("reject", [False, True])
def test_optional_helper_argument_does_not_block_rejection_analysis(printf_chart: Chart, argument: str, prefix: str, reject: bool) -> None:
    """
    Model the optional subchart prefix without abandoning later explicit validation.

    Args:
        printf_chart (Chart): Chart with an optional helper argument.
        argument (str): Dictionary entry, or omitted entry.
        prefix (str): Selected text after eager formatting and ternary selection.
        reject (bool): Whether the helper should reject this candidate.

    Returns:
        None: Rejection predictions match native Helm and no incomplete-analysis warning remains.
    """
    (printf_chart.path / "templates/_helpers.tpl").write_text(
        dedent("""
        {{- define "validate" -}}
        {{- $prefix := ternary "" (printf "%s." .subchart) (empty .subchart) -}}
        {{- if .reject -}}{{- fail (printf "%spassword required" $prefix) -}}{{- end -}}
        {{- $prefix -}}
        {{- end -}}
        """)
    )
    manifest(printf_chart, 'include "validate" (dict "reject" .Values.reject ' + argument + ")")
    contracts = Contracts.build(printf_chart.path)
    prediction = contracts.predict({**printf_chart.defaults, "reject": reject})
    assert not contracts.fallbacks
    if reject:
        assert prediction is not None
        assert prediction.message == prefix + "password required"
        with pytest.raises(RenderFailure) as failure:
            render(printf_chart, {"reject": True}, stream=False)
        assert matches_rejection(str(failure.value), prediction)
    else:
        assert prediction is None
        assert mapping(render(printf_chart, {}, stream=False)[0]["data"])["result"] == prefix


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize(
    "source",
    [
        '{{ $_ := ternary "selected" (fail "eager argument") true }}',
        dedent("""
        {{ $state := dict "changed" false }}
        {{ $_ := ternary "selected" (set $state "changed" true) true }}
        {{ if $state.changed }}{{ fail "eager argument" }}{{ end }}
        """),
    ],
)
def test_ternary_arguments_still_execute(printf_chart: Chart, source: str) -> None:
    """
    Preserve failures and mutations in the argument whose value ternary does not select.

    Args:
        printf_chart (Chart): Native comparison fixture.
        source (str): An eagerly evaluated failing or mutating argument.

    Returns:
        None: Compiler and Helm both execute the otherwise unused argument.
    """
    manifest(printf_chart, '"valid"')
    (printf_chart.path / "templates/NOTES.txt").write_text(source)
    contracts = Contracts.build(printf_chart.path)
    prediction = contracts.predict(printf_chart.defaults)
    assert prediction is not None
    assert not contracts.fallbacks
    with pytest.raises(RenderFailure) as failure:
        render(printf_chart, {}, stream=False)
    assert matches_rejection(str(failure.value), prediction)


@pytest.mark.parametrize(
    ("format_string", "arguments"),
    [("%s", [None]), ("%d", ["wrong"]), ("%s", []), ("", [None]), ("%s", ["abcdef"]), ("abcdef", []), ("%", [])],
)
def test_printf_diagnostics_respect_output_budget(format_string: str, arguments: list[object]) -> None:
    """
    Count diagnostic text and ordinary string substitutions against the same compiler budget.

    Args:
        format_string (str): Supported format.
        arguments (list[object]): Concrete evaluated operands.

    Returns:
        None: Oversized diagnostic or formatted output remains unresolved.
    """
    with pytest.raises(Unknown, match="max_string_chars"):
        printf(format_string, arguments, max_chars=5)


@pytest.mark.parametrize("format_string", ["%s", "%d", ""])
def test_printf_diagnostics_do_not_guess_raw_numeric_types(format_string: str) -> None:
    """
    Avoid labeling a decoded values number as int merely because Python uses that type.

    Args:
        format_string (str): An operation whose output reveals the concrete Go type.

    Returns:
        None: Ambiguous types still defer to Helm rather than publishing a guessed diagnostic.
    """
    with pytest.raises(Unknown, match="explicit integer conversion"):
        printf(format_string, [BoundValue(2, ("count",))], max_chars=100)


def test_printf_preserves_unordered_message_evidence() -> None:
    """
    Retain unordered map keys while formatting messages and new missing-argument diagnostics.

    Returns:
        None: All key orders match, but repeated or missing keys do not.
    """
    keys = ContractText((KeyList(",", ("a", "b")),))
    result = printf("keys=%s; missing=%d", [keys], max_chars=100)
    assert isinstance(result, ContractText)
    assert result.matches("keys=a,b; missing=%!d(MISSING)")
    assert result.matches("keys=b,a; missing=%!d(MISSING)")
    assert not result.matches("keys=a,a; missing=%!d(MISSING)")
    with pytest.raises(Unknown, match="unordered"):
        printf("", [keys], max_chars=100)
    with pytest.raises(Unknown, match="max_string_chars"):
        printf("%s", [keys], max_chars=2)


@pytest.mark.parametrize("operand", [{}, [], 1.5, DerivedValue(2, "unsupported", ())])
def test_printf_keeps_unmodeled_types_unknown(operand: object) -> None:
    """
    Retain explicit uncertainty for composite, floating-point and unknown derived numeric operands.

    Args:
        operand (object): Value outside the formatter's established scalar type domain.

    Returns:
        None: Broader Go formatting semantics are not silently fabricated.
    """
    with pytest.raises(Unknown):
        printf("%s", [operand], max_chars=100)
