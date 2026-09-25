"""
Track literal and scalar results without treating their shape as a value proof.
"""

from hypothesis_helm.compiler.asts.origins import Derived, Dictionary, Literal, Origin, Record, Sequence, Text, paths
from hypothesis_helm.compiler.asts.transformations import calculate
from hypothesis_helm.compiler.builtins import BUILTINS
from hypothesis_helm.compiler.constants import (
    CERTIFICATE_FIELDS,
    CERTIFICATES,
    CONTEXT_EFFECTS,
    SCALARS,
    SEMVER_FIELDS,
    TEMPLATE_CALLS,
    TEXT_CONVERSIONS,
    TRANSFORMATIONS,
)
from hypothesis_helm.exceptions.compiler import UnsupportedTransformation

__all__ = ("declared", "derived", "literal", "result")


def derived(arguments: list[Origin]) -> Derived:
    """
    Collect all input dependencies even when the output value is unknown.

    Args:
        arguments (list[Origin]): Symbolic operands.

    Returns:
        Derived: Scalar result depending on every referenced input.
    """
    inputs = tuple(sorted({path for argument in arguments for path in paths(argument)}))
    return Derived(inputs)


def literal(function: str, arguments: list[Origin], limits: dict[str, int] | None) -> Origin:
    """
    Fold only supported concrete scalars; keep collections available for element tracking.

    Args:
        function (str): Original Helm function name.
        arguments (list[Origin]): Symbolic operands.
        limits (dict[str, int] | None): Captured chart inspection budgets.

    Returns:
        Origin: Literal result or None when folding cannot establish one.
    """
    if function in TRANSFORMATIONS and all(isinstance(argument, Literal) for argument in arguments):
        try:
            value = calculate(function, tuple(argument.value for argument in arguments if isinstance(argument, Literal)), limits=limits)
            if not isinstance(value, (dict, list)):
                return Literal(value)
            # Collection-producing functions need the structured origins below;
            # folding their result into a scalar loses exact loop/key traversal.
        except UnsupportedTransformation:
            pass  # Share the reviewed Go-compatible subset; never fall back to Python coercion.
    return None


def result(function: str, arguments: list[Origin], *, offline: bool) -> Origin:
    """
    Describe text conversions, fixed records and renderer-dependent results.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.
        offline (bool): Whether Helm executes without cluster or DNS access.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    scalar = derived(arguments)
    inputs = scalar.inputs
    if function in TEXT_CONVERSIONS and len(arguments) == 1:
        return Text(arguments[0], function)
    if function in SCALARS and len(arguments) == 1:
        return scalar
    if function in TEMPLATE_CALLS:
        return scalar  # Template output is text, never another Values context.
    if function == "semver" and len(arguments) == 1:
        return Record({name: scalar for name in SEMVER_FIELDS})
    if function in CERTIFICATES or function == "buildCustomCert":
        return Record({field: scalar for field in CERTIFICATE_FIELDS})
    if function == "lookup" and len(arguments) == 4:
        return Dictionary({}) if offline else Derived(inputs, external=True)
    if function == "getHostByName" and len(arguments) == 1 and offline:
        return Literal("")
    if function == "print" and all(isinstance(arg, Literal) and isinstance(arg.value, str) for arg in arguments):
        return Literal("".join(str(arg.value) for arg in arguments if isinstance(arg, Literal)))
    if function in {"print", "printf"}:
        return scalar
    return declared(function, arguments)


def declared(function: str, arguments: list[Origin]) -> Origin:
    """
    Retain source-declared shapes without inferring concrete values or purity.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    scalar = derived(arguments)
    inputs = scalar.inputs
    specification = BUILTINS.get(function)
    if specification is not None and specification.shape == "scalar" and not specification.effects & CONTEXT_EFFECTS:
        # A known result type does not establish a value, truthiness, enum, or equality proof.
        return scalar
    if specification is not None and not specification.effects & CONTEXT_EFFECTS:
        if specification.shape == "record" and specification.fields:
            return Record({name: Derived(inputs, external=True) for name in specification.fields})
        if specification.shape == "sequence":
            return Sequence((Derived(inputs, external=True),), exact=False)
    return None
