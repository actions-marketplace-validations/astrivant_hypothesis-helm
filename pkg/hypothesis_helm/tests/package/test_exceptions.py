"""
Keep exception definitions centralized without changing catches or compiler evidence.
"""

import ast
import builtins

import pytest

from hypothesis_helm.exceptions.compiler import LoopControl, Rejection, Unavailable, Unknown, UnsupportedTransformation
from hypothesis_helm.exceptions.execution import TimeLimitReached
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.exceptions.schemas import NonFiniteSchema
from hypothesis_helm.tests import PACKAGES_ROOT


def test_package_exceptions_have_central_definitions() -> None:
    """
    Require project-defined exceptions, including subclasses, to live in their package's exception directory.

    Returns:
        None: All package exceptions have a single categorized definition.
    """
    packages = PACKAGES_ROOT
    exception_names = {name for name, value in vars(builtins).items() if isinstance(value, type) and issubclass(value, BaseException)}
    classes = [
        (path, node)
        for path in packages.rglob("*.py")
        if "tests" not in path.relative_to(packages).parts
        for node in ast.walk(ast.parse(path.read_text()))
        if isinstance(node, ast.ClassDef)
    ]
    discovered: set[str] = set()
    while True:
        found = {node.name for _, node in classes if any(ast.unparse(base).split(".")[-1] in exception_names for base in node.bases)}
        if found == discovered:
            break
        discovered = found
        exception_names.update(found)
    for path, node in classes:
        if node.name in discovered:
            assert path.relative_to(packages).parts[1] == "exceptions", f"Move {node.name} from {path} into its package's exceptions/"


@pytest.mark.parametrize("exception", [Unknown, Unavailable, UnsupportedTransformation, NonFiniteSchema])
def test_analysis_exceptions_keep_value_error_catches(exception: type[ValueError]) -> None:
    """
    Preserve the unsupported-analysis handlers used by the compiler and schema planner.

    Args:
        exception (type[ValueError]): Canonical analysis exception.

    Returns:
        None: Existing ValueError handlers still receive the original diagnostic.
    """
    with pytest.raises(ValueError, match="unsupported"):
        raise exception("unsupported")


def test_execution_deadline_bypasses_counterexample_handlers() -> None:
    """
    Keep deadline cancellation outside ordinary Exception-based shrinking handlers.

    Returns:
        None: Deadline handling retains its BaseException boundary.
    """
    assert issubclass(TimeLimitReached, BaseException)
    assert not issubclass(TimeLimitReached, Exception)
    with pytest.raises(TimeLimitReached):
        try:
            raise TimeLimitReached()
        except Exception:
            pytest.fail("A deadline was mistaken for a counterexample")


def test_exception_payloads_preserve_finding_and_contract_evidence() -> None:
    """
    Retain classified findings and branch evidence after moving their exception definitions.

    Returns:
        None: Render and compiler exceptions carry their original metadata.
    """
    failure = RenderFailure("malformed YAML", "HH1101")
    assert isinstance(failure, AssertionError)
    assert failure.code == failure.finding.rule.code == "HH1101"
    assert str(failure) == "[HH1101] malformed YAML"
    rejection = Rejection("templates/config.yaml", 7, "choose a mode", {"mode": "invalid"}, ("if mode",), {"mode": ("small", "large")})
    report = rejection.report()
    assert report["inputs"] == {"mode": "invalid"}
    assert report["enums"] == {"mode": ["small", "large"]}
    assert report["id"] == rejection.key
    jump = LoopControl("break", "already rendered")
    assert jump.action == "break"
    assert jump.output == "already rendered"
