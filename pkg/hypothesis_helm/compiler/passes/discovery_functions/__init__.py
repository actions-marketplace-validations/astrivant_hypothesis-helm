"""
Dispatch discovery calls to literal, selection, collection and scalar handlers.
"""

from hypothesis_helm.compiler.asts.origins import Origin
from hypothesis_helm.compiler.constants import COLLECTIONS, FUNCTION_ALIASES, SELECTIONS
from hypothesis_helm.compiler.passes.discovery_functions import collections, scalars, selection

__all__ = ("result",)


def result(function: str, arguments: list[Origin], *, offline: bool = False, limits: dict[str, int] | None = None) -> Origin:
    """
    Propagate supported literal results and origins without inferring global input constraints.

    Args:
        function (str): Statically named template function.
        arguments (list[Origin]): Symbolic input arguments in Helm call order.
        offline (bool): Executor guarantees plain helm template, without cluster or DNS access.
        limits (dict[str, int] | None): Compiler budgets captured by the chart's discovery pass.

    Returns:
        Origin: Supported shape and source dependencies, or explicit uncertainty.
    """
    # Folding has priority, but a known collection must retain its member origins.
    folded = scalars.literal(function, arguments, limits)
    if folded is not None:
        return folded
    function = FUNCTION_ALIASES.get(function, function)
    if function in SELECTIONS:
        return selection.result(function, arguments)
    if function in COLLECTIONS:
        return collections.result(function, arguments)
    # Unknown functions use the upstream effect inventory rather than guessed semantics.
    return scalars.result(function, arguments, offline=offline)
