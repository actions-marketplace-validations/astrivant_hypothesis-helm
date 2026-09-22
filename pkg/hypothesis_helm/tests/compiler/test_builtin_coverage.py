"""
Enforce an executed support decision or a documented deferral for every Helm builtin.
"""

import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler import builtin_coverage
from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contract_values import BoundValue, UnorderedKeys
from hypothesis_helm.compiler.asts.contracts import Contracts, Evaluation, expression
from hypothesis_helm.compiler.asts.native_operations import plain
from hypothesis_helm.compiler.builtins import BUILTINS
from hypothesis_helm.compiler.limits import DEFAULT_LIMITS
from hypothesis_helm.exceptions.compiler import Rejection, Unknown
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.schemas.contracts import mapping


def test_every_upstream_function_requires_a_reviewed_semantic_case(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Reject an inventory upgrade without a matching executable case and explanation.

    Args:
        monkeypatch (pytest.MonkeyPatch): Simulate a newly registered upstream function.

    Returns:
        None: New functions cannot inherit an unsupported or pure classification silently.
    """
    assert {case.name for case in builtin_coverage.cases()} == BUILTINS.keys()
    monkeypatch.setattr(builtin_coverage, "BUILTINS", {**BUILTINS, "futureBuiltin": BUILTINS["print"]})
    with pytest.raises(ValueError, match="futureBuiltin"):
        builtin_coverage.cases()


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("case", builtin_coverage.cases(), ids=lambda case: case.name)
def test_builtin_support_contract(tmp_path: Path, case: builtin_coverage.CoverageCase) -> None:
    """
    Exercise each claimed support level and compare concrete results with native Helm.

    Args:
        tmp_path (Path): Isolated chart for the compiler and independent Helm render.
        case (builtin_coverage.CoverageCase): Required function-specific probe and documented limitation.

    Returns:
        None: Supported output agrees with Helm; deferred code stays unresolved and cannot prune its input.
    """
    fixture = builtin_coverage.fixture()
    values = mapping(fixture["values"])
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(
        dedent("""
        apiVersion: v2
        name: coverage
        version: 0.1.0
        """)
    )
    (tmp_path / "values.yaml").write_text(yamlio.dump(values))
    (tmp_path / "templates/_helpers.tpl").write_text(str(fixture["helpers"]))
    contracts = Contracts.build(tmp_path)
    contracts.configure(helm="helm", kube_version=None, timeout=5, release="hypothesis", namespace="default", fail_fast=False)
    evaluator = Evaluation(contracts, values, context={"Values": BoundValue(values, ())})
    original = json.dumps(values, sort_keys=True)
    if case.outcome == "deferred":
        with pytest.raises(Unknown):
            evaluator.evaluate(expression(case.expression), "coverage", 1, Scope())
        # An unavailable guard cannot be turned into an unconditional fail.
        (tmp_path / "templates/NOTES.txt").write_text("{{ if " + case.expression + ' }}{{ fail "must remain unknown" }}{{ end }}')
        guarded = Contracts.build(tmp_path)
        guarded.renderer = contracts.renderer
        assert guarded.predict(values) is None
        assert guarded.fallbacks
        assert json.dumps(values, sort_keys=True) == original
        return
    if case.outcome == "rejection":
        with pytest.raises(Rejection):
            evaluator.evaluate(expression(case.expression), "coverage", 1, Scope())
        observed: object = None
    else:
        observed = evaluator.evaluate(expression(case.expression), "coverage", 1, Scope())
    assert json.dumps(values, sort_keys=True) == original
    (tmp_path / "templates/result.yaml").write_text(
        dedent(f"""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: coverage
        data:
          result: {{{{ {case.expression} | toJson | quote }}}}
        """)
    )
    rendered = Processes().run(["helm", "template", "hypothesis", str(tmp_path)], capture_output=True, timeout=5)
    if case.outcome == "rejection":
        assert rendered.returncode != 0 and "coverage rejection" in rendered.stderr
        return
    assert rendered.returncode == 0, rendered.stderr
    document = next(item for item in yamlio.load_all(rendered.stdout) if item is not None)
    expected = json.loads(str(mapping(mapping(document)["data"])["result"]))
    if case.outcome == "symbolic":
        assert isinstance(observed, UnorderedKeys)
        assert set(observed.values) == set(expected)
    else:
        actual = plain(observed, DEFAULT_LIMITS)
        assert actual == expected and isinstance(actual, bool) == isinstance(expected, bool)
