"""
Evaluate fresh flat-map merges without modeling mutations of shared chart inputs.
"""

import re

from attrs import define, field

from hypothesis_helm.compiler.asts.contract_values import BoundValue, DerivedValue, NilMap, native
from hypothesis_helm.exceptions.compiler import UnsupportedTransformation

__all__ = ("LocalMaps", "dictionary", "fresh_merge", "merge_flat_sources")


@define
class LocalMaps:
    """
    Prove mutation ownership separately from whether a dictionary's keys form an allowlist.

    Attributes:
        owned (dict[int, dict[str, object]]): Strong references prevent identity reuse within an evaluation.
        changed (set[int]): Maps whose keys can no longer establish a literal allowlist.
    """

    owned: dict[int, dict[str, object]] = field(factory=dict)
    changed: set[int] = field(factory=set)

    def register(self, value: object) -> object:
        """
        Mark a newly allocated map as safe to mutate through any local alias.

        Args:
            value (object): New map, possibly wrapped as a constant-key map.

        Returns:
            object: Original wrapper without marking shared nested values as owned.
        """
        contents = native(value)
        if isinstance(contents, dict):
            self.owned[id(contents)] = contents
        return value

    def apply(self, function: str, arguments: list[object], max_items: int) -> object:
        """
        Apply bounded writes only to proved local destinations.

        Args:
            function (str): Set, unset, or a merge variant.
            arguments (list[object]): Evaluated operands retaining provenance.
            max_items (int): Maximum entries inspected or retained.

        Returns:
            object: Original destination, preserving alias identity.

        Raises:
            UnsupportedTransformation: Ownership, shape, arity or bounds cannot be established.
        """
        args = [native(value) for value in arguments]
        if not args or not isinstance(args[0], dict) or id(args[0]) not in self.owned:
            raise UnsupportedTransformation("map mutation requires a proven-local destination; shared context remains unresolved")
        target = args[0]
        if isinstance(target, NilMap):
            raise UnsupportedTransformation("mutation of a nil map requires native allocation or raises a template error")
        if function in {"set", "unset"}:
            if len(args) != (3 if function == "set" else 2) or not isinstance(args[1], str):
                raise UnsupportedTransformation("local map mutation has unsupported operands")
            if function == "set":
                self._set(target, args[1], arguments[2], max_items)
            else:
                target.pop(args[1], None)
        else:
            self._merge(function, target, arguments, max_items)
        # A candidate-dependent write cannot create a new constant enum proof.
        self.changed.add(id(target))
        return arguments[0]

    def _set(self, target: dict[str, object], key: str, value: object, max_items: int) -> None:
        """
        Check size and cycle safety before changing one local dictionary entry.

        Args:
            target (dict[str, object]): Owned destination map.
            key (str): Entry being assigned.
            value (object): Source value, retaining provenance and aliases.
            max_items (int): Maximum nodes inspected and entries retained.

        Returns:
            None: Assignment succeeds without creating a cyclic analysis object.
        """
        if len(target) + (key not in target) > max_items:
            raise UnsupportedTransformation("local map exceeds compiler.max_range_items")
        pending = [value]
        seen: set[int] = set()
        inspected = 0
        while pending:
            item = native(pending.pop())
            inspected += 1
            if inspected > max_items:
                raise UnsupportedTransformation("local map assignment exceeds compiler.max_range_items")
            if item is target:
                raise UnsupportedTransformation("local map assignment would create a cyclic value")
            if isinstance(item, dict | list) and id(item) not in seen:
                if inspected + len(item) > max_items:
                    raise UnsupportedTransformation("local map assignment exceeds compiler.max_range_items")
                seen.add(id(item))
                pending.extend(item.values() if isinstance(item, dict) else item)
        target[key] = value

    def _merge(self, function: str, target: dict[str, object], arguments: list[object], max_items: int) -> None:
        """
        Apply Mergo's flat-map precedence after inspecting every source for shared aliases.

        Args:
            function (str): Ordinary or overwrite merge variant.
            target (dict[str, object]): Owned destination, changed only after validation.
            arguments (list[object]): Destination and sources with provenance intact.
            max_items (int): Maximum total entries inspected.

        Returns:
            None: Winning source values replace destination entries in place.
        """
        if len(arguments) < 2:
            raise UnsupportedTransformation("local merge needs at least one source")
        # Mergo can mutate nested destination aliases. Restrict this adapter to
        # flat maps until recursive alias ownership and precedence are modeled.
        snapshots = [merge_flat_sources([item], max_items) for item in arguments]
        if sum(len(item) for item in snapshots) > max_items:
            raise UnsupportedTransformation("local merge exceeds compiler.max_range_items")
        for source in snapshots[1:]:
            for key, value in source.items():
                # Ordinary merge ignores nil sources when a key already exists,
                # even when the existing scalar is false, zero or an empty string.
                if "Overwrite" in function or key not in target or (not native(target[key]) and native(value) is not None):
                    target[key] = value


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
