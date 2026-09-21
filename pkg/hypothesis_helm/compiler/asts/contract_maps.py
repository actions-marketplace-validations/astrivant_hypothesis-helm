"""
Evaluate fresh flat-map merges without modeling mutations of shared chart inputs.
"""

import re

from hypothesis_helm.compiler.asts.contract_values import BoundValue, DerivedValue, native
from hypothesis_helm.exceptions.compiler import UnsupportedTransformation

__all__ = ("dictionary", "fresh_merge", "merge_flat_sources")


def dictionary(arguments: tuple[object, ...]) -> dict[str, object]:
    """
    Construct a Sprig dictionary without guessing coercion of non-string keys.

    Args:
        arguments (tuple[object, ...]): Alternating keys and values, retaining input provenance.

    Returns:
        dict[str, object]: Entries, including Sprig's empty-string value for a trailing key.

    Raises:
        UnsupportedTransformation: A key requires Go-specific conversion to a string.
    """
    entries: dict[str, object] = {}
    for index in range(0, len(arguments), 2):
        key = native(arguments[index])
        if not isinstance(key, str):
            raise UnsupportedTransformation(
                f"dict key at argument {index + 1} is {type(key).__name__}; "
                "Go key coercion is unresolved; check alternating key/value arguments"
            )
        # Sprig accepts an unmatched final key and supplies an empty string for it.
        entries[key] = arguments[index + 1] if index + 1 < len(arguments) else ""
    return entries


def fresh_merge(expression: object) -> bool:
    """
    Recognize overwrite calls whose destination is a newly allocated empty dictionary.

    Args:
        expression (object): Parsed contract expression, before operand evaluation.

    Returns:
        bool: The destination cannot alias an existing input or lexical variable.
    """
    return (
        isinstance(expression, tuple)
        and len(expression) >= 2
        and expression[0] in {"mergeOverwrite", "mustMergeOverwrite"}
        and expression[1] == "dict"
    )


def merge_flat_sources(sources: list[object], max_items: int) -> dict[str, object]:
    """
    Merge scalar-valued maps in source order while preserving each winning input's origin.

    Args:
        sources (list[object]): Evaluated source maps; the fresh empty destination is excluded.
        max_items (int): Maximum inspected entries across all source maps.

    Returns:
        dict[str, object]: Last-source-wins mapping that shares no mutable nested containers.

    Raises:
        UnsupportedTransformation: A source is not a bounded flat map or could introduce shared mutable aliases.
    """
    result: dict[str, object] = {}
    inspected = 0
    for source in sources:
        entries = native(source)
        if not isinstance(entries, dict):
            raise UnsupportedTransformation("fresh merge requires map sources")
        inspected += len(entries)
        if inspected > max_items:
            raise UnsupportedTransformation(f"fresh merge exceeds compiler.max_range_items={max_items}")
        for key, value in entries.items():
            # Nested containers could alias the inputs; the flat-map proof deliberately excludes them.
            concrete = native(value)
            if not isinstance(key, str) or concrete is not None and not isinstance(concrete, str | bool | int | float):
                raise UnsupportedTransformation("fresh merge requires scalar map entries; nested aliases remain unresolved")
            result[key] = (
                BoundValue(value, (*source.path, key))
                if isinstance(source, BoundValue) and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9-]*", key)
                else DerivedValue(value, "get", (source, key))
                if isinstance(source, BoundValue)
                else value
            )
    return result
