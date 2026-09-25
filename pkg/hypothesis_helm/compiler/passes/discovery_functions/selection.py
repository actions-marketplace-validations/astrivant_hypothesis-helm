"""
Resolve choices and predicates while preserving every possible selected origin.
"""

from hypothesis_helm.compiler.asts.origins import Dictionary, Literal, Origin, Projection, join
from hypothesis_helm.compiler.passes.discovery_flow import truth
from hypothesis_helm.compiler.passes.discovery_functions.scalars import declared, derived

__all__ = ("result",)


def _fallback(function: str, arguments: list[Origin]) -> Origin:
    """
    Follow Helm emptiness without treating false or zero fallbacks as absent.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    if function == "ternary" and len(arguments) == 3:
        if isinstance(arguments[2], Literal) and isinstance(arguments[2].value, bool):
            return arguments[0] if arguments[2].value else arguments[1]
        return join(*arguments[:2])
    if function == "default" and arguments:
        if len(arguments) == 1:
            return arguments[0]
        known = truth(arguments[1])
        return arguments[1] if known is True else arguments[0] if known is False else join(*arguments[:2])
    if function == "coalesce":
        # A known nonempty operand ends the search; unknown earlier operands remain possible.
        possible: list[Origin] = []
        for argument in arguments:
            known = truth(argument)
            if known is not False:
                possible.append(argument)
            if known is True:
                return join(*possible)
        return join(*possible, Literal(None))
    return declared(function, arguments)


def _boolean(function: str, arguments: list[Origin]) -> Origin:
    """
    Track short-circuit selections and supported literal comparisons.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    scalar = derived(arguments)
    if function in {"not", "empty"} and len(arguments) == 1:
        known = truth(arguments[0])
        return scalar if known is None else Literal(not known)
    if function in {"and", "or"} and arguments:
        # Go template Boolean functions return the selected operand, not a coerced bool.
        possible = []
        for argument in arguments:
            known = truth(argument)
            if known is None:
                possible.append(argument)
            elif known == (function == "or"):
                return join(*possible, argument)
        return join(*possible, arguments[-1])
    if function in {"eq", "ne"} and len(arguments) == 2:
        left, right = arguments
        if isinstance(left, Literal) and isinstance(right, Literal) and type(left.value) is type(right.value):
            return Literal((left.value == right.value) == (function == "eq"))
        return scalar
    return declared(function, arguments)


def _membership(function: str, arguments: list[Origin]) -> Origin:
    """
    Use only exact dictionary keys or known projections to decide membership.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    scalar = derived(arguments)
    if function == "hasKey" and len(arguments) == 2:
        source, key = arguments
        if isinstance(key, Literal) and isinstance(key.value, str):
            if isinstance(source, Dictionary) and not source.uncertain:
                return Literal(key.value in source.fields)
            if isinstance(source, Projection) and not source.uncertain and (key.value in source.keys) != source.include:
                return Literal(False)
        return scalar
    return declared(function, arguments)


def result(function: str, arguments: list[Origin]) -> Origin:
    """
    Route choice and predicate calls to their individual proof rules.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Literal predicate, possible selected origins, or unknown result.
    """
    if function in {"default", "coalesce", "ternary"}:
        return _fallback(function, arguments)
    if function == "hasKey":
        return _membership(function, arguments)
    return _boolean(function, arguments)
