"""
Compare fallback semantics across compiler passes and native Helm.
"""

import itertools
import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contracts import Contracts, expression
from hypothesis_helm.compiler.asts.origins import Literal
from hypothesis_helm.compiler.asts.transformations import calculate
from hypothesis_helm.compiler.passes.discovery_functions import result
from hypothesis_helm.compiler.passes.domain_constraints import normalize
from hypothesis_helm.compiler.passes.domain_interpreter import Interpreter
from hypothesis_helm.compiler.passes.rejections import matches_rejection
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.tests.generation.test_input_domains import fixture_chart


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_fallback_matrix_matches_native_helm(tmp_path: Path) -> None:
    """
    Compare scalar and collection emptiness, fallback arities and result types with Helm in one render.

    Args:
        tmp_path (Path): Isolated chart holding each comparison as a ConfigMap entry.

    Returns:
        None: Concrete evaluation, discovery and symbolic projection agree with Helm, including all-empty calls.
    """
    samples: list[object] = [None, False, 0, "", [], {}, True, "0", [None], {"enabled": False}]
    cases = [
        (function, args)
        for function in ("coalesce", "default")
        for args in [*((value,) for value in samples), *itertools.product(samples, repeat=2)]
    ]
    cases.extend([("coalesce", ()), ("default", ("fallback", "", "ignored")), ("coalesce", (False, 0, "", [], {}))])
    values: dict[str, object] = {}
    calls = []
    for index, (function, arguments) in enumerate(cases):
        names = [f"v{index}_{position}" for position in range(len(arguments))]
        values.update(zip(names, arguments, strict=True))
        calls.append(" ".join([function, *(f".Values.{name}" for name in names)]))
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "fallbacks", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump(values))
    (tmp_path / "templates/result.yaml").write_text(
        dedent("""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: fallbacks
            data:
            """)
        + "".join(f"  c{index}: {{{{ {call} | toJson | quote }}}}\n" for index, call in enumerate(calls))
    )
    chart = Chart(tmp_path, {"type": "object"}, values)
    observed = mapping(render(chart, {})[0]["data"])
    interpreter = Interpreter(Contracts.build(tmp_path), chart.schema)
    context = {"Values": values}
    disagreements = []
    for index, ((function, arguments), call) in enumerate(zip(cases, calls, strict=True)):
        expected = json.loads(str(observed[f"c{index}"]))
        projected = normalize(interpreter.evaluate(expression(call), context, Scope({"$": context})))
        discovered = result(function, [Literal(value) for value in arguments])
        for pass_name, actual in (
            ("projection", projected),
            ("discovery", discovered.value if isinstance(discovered, Literal) else discovered),
            ("evaluation", calculate(function, arguments)),
        ):
            if type(actual) is not type(expected) or actual != expected:
                disagreements.append((function, arguments, pass_name, actual, expected))
    assert not disagreements, disagreements


@pytest.mark.parametrize(
    "selection",
    [
        'coalesce (dict) (dict "active" true "limit" .Values.port)',
        'default (dict "active" true "limit" .Values.port) (dict)',
        'coalesce (dict "active" true "limit" .Values.port) (dict "active" false)',
    ],
)
def test_literal_map_fallbacks_preserve_destination_origins(tmp_path: Path, selection: str) -> None:
    """
    Recover a destination through empty and nonempty helper argument maps.

    Args:
        tmp_path (Path): Isolated chart whose port is passed inside a local map.
        selection (str): Map selection independent of any chart-specific field names.

    Returns:
        None: The active source receives the port bounds rather than losing its origin at a fallback call.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        "{{ $selected := "
        + selection
        + " }}\n{{ if $selected.active }}\n"
        + template.read_text().replace(".Values.port", "$selected.limit")
        + "{{ end }}\n"
    )
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    for port in (0, 1, 80, 65535, 65536):
        assert validator.is_valid(json_value({**chart.defaults, "port": port})) == (1 <= port <= 65535)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_coalesce_evaluates_unused_failure_arguments(tmp_path: Path) -> None:
    """
    Preserve Helm's eager argument evaluation even when the first operand is nonempty.

    Args:
        tmp_path (Path): Chart containing a failing fallback expression.

    Returns:
        None: Rejection prediction and Helm both observe the otherwise unselected failure.
    """
    chart = fixture_chart(tmp_path)
    (tmp_path / "templates/NOTES.txt").write_text('{{ coalesce "selected" (fail "fallback was evaluated") }}')
    rejection = Contracts.build(tmp_path).predict(chart.defaults)
    assert rejection is not None
    with pytest.raises(RenderFailure) as failure:
        render(chart, {})
    assert matches_rejection(str(failure.value), rejection)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_coalesce_evaluates_unused_mutation_arguments(tmp_path: Path) -> None:
    """
    Evaluate a fallback mutation before deciding which alias supplies the output field.

    Args:
        tmp_path (Path): Chart whose unused fallback changes the selected helper-local map.

    Returns:
        None: The overwritten input stays unconstrained and Helm emits the replacement port.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        dedent("""
            {{ $map := dict "limit" .Values.port }}
            {{ $selected := coalesce $map (set $map "limit" 8080) }}
            """)
        + template.read_text().replace(".Values.port", "$selected.limit")
    )
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert validator.is_valid(json_value({**chart.defaults, "port": 0}))
    resources = render(chart, {"port": 0})
    container = mapping(sequence(mapping(resources[0]["spec"])["containers"])[0])
    assert mapping(sequence(container["ports"])[0])["containerPort"] == 8080


def test_partly_known_selection_constrains_only_the_established_region(tmp_path: Path) -> None:
    """
    Retain a proven selection region without treating an unresolved capability check as false.

    Args:
        tmp_path (Path): Chart choosing an input port or a literal fallback.

    Returns:
        None: The known true region is constrained and the ambiguous region remains available for rendering.
    """
    chart = fixture_chart(tmp_path)
    template = tmp_path / "templates/pod.yaml"
    template.write_text(
        template.read_text().replace(
            ".Values.port", 'ternary .Values.port 8080 (or .Values.enabled (.Capabilities.APIVersions.Has "example/v1"))'
        )
    )
    schema = chart.generation_schema()
    validator = validators.validator_for(schema)(schema)
    assert not validator.is_valid(json_value({**chart.defaults, "enabled": True, "port": 0}))
    assert validator.is_valid(json_value({**chart.defaults, "enabled": False, "port": 0}))
    assert validator.is_valid(json_value({**chart.defaults, "enabled": True, "port": 8080}))
