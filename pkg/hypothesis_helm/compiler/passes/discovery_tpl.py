"""
Recover available tpl source strings through aliases and supported serializations.
"""

import json

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.origins import Choice, Literal, Origin, Text

__all__ = ("sources", "values")


def values(origin: Origin, defaults: object) -> tuple[tuple[object, ...], bool]:
    """
    Read available concrete source alternatives without using defaults for branch proofs.

    Args:
        origin (Origin): Symbolic source expression.
        defaults (object): Supplied values document used only to inspect available template text.

    Returns:
        tuple[tuple[object, ...], bool]: Available values and whether any alternative remains unresolved.
    """
    if isinstance(origin, Literal):
        return (origin.value,), False
    if isinstance(origin, Choice):
        results = [values(item, defaults) for item in origin.alternatives]
        return tuple(value for result, _ in results for value in result), any(unknown for _, unknown in results)
    if isinstance(origin, tuple) and origin[:1] == ("Values",):
        # Defaults supply code to inspect, not evidence that other input values choose the same branch.
        value = defaults
        for key in origin[1:]:
            if not isinstance(value, dict) or key not in value:
                return (), True
            value = value[key]
        return (value,), False
    if isinstance(origin, Text):
        sources, unknown = values(origin.source, defaults)
        outputs: list[object] = []
        for source in sources:
            if origin.operation == "toYaml":
                outputs.append(yamlio.dump(source))
            elif origin.operation == "toJson":
                outputs.append(json.dumps(source))
            elif isinstance(source, str):
                outputs.append(source)
            elif isinstance(source, bool):
                outputs.append("true" if source else "false")
            elif isinstance(source, int):
                outputs.append(str(source))
            else:
                unknown = True
        return tuple(outputs), unknown
    return (), True


def sources(origin: Origin, defaults: object) -> tuple[tuple[str, ...], bool]:
    """
    Extract distinct known strings while retaining uncertainty from other possible sources.

    Args:
        origin (Origin): Possibly aliased or converted template string.
        defaults (object): Supplied chart values.

    Returns:
        tuple[tuple[str, ...], bool]: Known template strings and an incompleteness indicator.
    """
    alternatives, unknown = values(origin, defaults)
    strings = tuple(dict.fromkeys(value for value in alternatives if isinstance(value, str)))
    return strings, unknown or any(not isinstance(value, str) for value in alternatives)
