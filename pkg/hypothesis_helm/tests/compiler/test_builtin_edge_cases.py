"""
Exercise every pinned builtin at argument boundaries and compare modeled outcomes with Helm.
"""

import json
import shutil
from collections.abc import Iterator
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contract_values import BoundValue, UnorderedKeys, native
from hypothesis_helm.compiler.asts.contracts import Contracts, Evaluation, expression
from hypothesis_helm.compiler.asts.native_operations import plain
from hypothesis_helm.compiler.builtins import BUILTINS
from hypothesis_helm.compiler.limits import DEFAULT_LIMITS
from hypothesis_helm.exceptions.compiler import Rejection, Unavailable, Unknown
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.schemas.contracts import mapping


def boundary_arguments() -> Iterator[tuple[str, ...]]:
    """
    Generate replayable argument boundaries without allocating a Cartesian values space.

    Yields:
        tuple[str, ...]: Missing, nil, empty, mixed-type, collection and arity cases.
    """
    yield ()
    for atom in ("nil", '""', "false", "0", "-1", '"x"', "(list)", "(dict)", ".Values.scalar", ".Values.collection"):
        yield (atom,)
    yield ("nil", "nil")
    yield ('""', '""')
    yield ('"x"', '"x"')
    yield ("0", '"x"')
    yield ('"x"', "0")
    yield ('""', '(list "")')
    yield ('(list "x")', '"x"')
    yield ('(dict "x" "value")', '"x"')
    yield ('(dict "x" "value")', '"x"', '"updated"')
    yield ('"a*"', '"aaa"', '"x"')
    yield ("0", "1", "1")
    yield ('"x"', '"x"', '"x"', '"x"')


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("function", sorted(BUILTINS))
def test_every_builtin_handles_argument_boundaries(tmp_path: Path, function: str) -> None:
    """
    Check traversal safety for every builtin and native equivalence for concrete results.

    Args:
        tmp_path (Path): Private probe chart and renderer output.
        function (str): A function from the complete source-derived registry.

    Returns:
        None: Unsupported cases remain explicit; concrete results agree with native Helm.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(
        dedent("""
        apiVersion: v2
        name: boundaries
        version: 0.1.0
        """)
    )
    values: dict[str, object] = {"scalar": "x", "collection": ["x"]}
    (tmp_path / "values.yaml").write_text(yamlio.dump(values))
    contracts = Contracts.build(tmp_path)
    contracts.configure(helm="helm", kube_version=None, timeout=5, release="hypothesis", namespace="default", fail_fast=False)
    original = json.dumps(values, sort_keys=True)
    for arguments in boundary_arguments():
        statement = " ".join((function, *arguments))
        evaluator = Evaluation(contracts, values, context={"Values": BoundValue(values, ())})
        try:
            result = evaluator.evaluate(expression(statement), "boundaries", 1, Scope())
        except (Unknown, Rejection):
            # Unknown is a supported analysis outcome, not evidence to exclude an
            # input. Never hide ordinary Python errors behind a blanket catch.
            assert json.dumps(values, sort_keys=True) == original
            continue
        if isinstance(result, UnorderedKeys):
            continue
        try:
            observed = plain(native(result), DEFAULT_LIMITS)
        except Unavailable:
            continue
        assert json.dumps(values, sort_keys=True) == original
        (tmp_path / "templates/result.yaml").write_text(
            dedent(f"""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: boundaries
            data:
              result: {{{{ {statement} | toJson | quote }}}}
            """)
        )
        rendered = Processes().run(["helm", "template", "hypothesis", str(tmp_path)], capture_output=True, timeout=5)
        assert rendered.returncode == 0, (statement, rendered.stderr)
        document = next(item for item in yamlio.load_all(rendered.stdout) if item is not None)
        expected = json.loads(str(mapping(mapping(document)["data"])["result"]))
        assert observed == expected and isinstance(observed, bool) == isinstance(expected, bool), (statement, observed, expected)
