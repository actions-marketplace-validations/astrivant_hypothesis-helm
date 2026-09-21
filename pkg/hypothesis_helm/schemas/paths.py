"""
Enumerate schema paths independently of chart generation and execution.
"""

from __future__ import annotations

import copy
import json
import logging

from attrs import define

from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.dialects import fragment, map_children, resolve

__all__ = ("ValuePath", "dereference", "enumerate_paths")


LOGGER = logging.getLogger(__name__)


@define
class ValuePath:
    """
    Describe a schema path and the provenance of its strategy.

    Attributes:
        path (tuple[str | int, ...]): Resolved value path or chart location.
        schema (dict[str, object]): Schema describing accepted values.
        origin (str): Source of the inferred or documented contract.
    """

    path: tuple[str | int, ...]
    schema: dict[str, object]
    origin: str = "schema"


def dereference(schema: dict[str, object], root: dict[str, object], seen: tuple[str, ...] = ()) -> dict[str, object]:
    """
    Expand local references without discarding sibling constraints.

    Args:
        schema (dict[str, object]): JSON Schema defining the accepted value domain.
        root (dict[str, object]): Root schema used to resolve local references.
        seen (tuple[str, ...]): References already visited while resolving this schema.

    Returns:
        dict[str, object]: Resulting schema, values mapping, or structured report.
    """
    return resolve(schema, root, seen)


def enumerate_paths(schema: dict[str, object]) -> list[ValuePath]:
    """
    Enumerate containers, leaves, array items and schema-defined map entries.

    `*` denotes array items or arbitrary map keys, and integer segments denote
    positional array schemas. Branch constraints are retained as a union of candidate
    subschemas; the complete schema is checked again when running each generated test.

    Args:
        schema (dict[str, object]): JSON Schema defining the accepted value domain.

    Returns:
        list[ValuePath]: Result of the documented operation.
    """
    collected: dict[tuple[str | int, ...], list[dict[str, object]]] = {}
    primary: dict[tuple[str | int, ...], list[dict[str, object]]] = {}
    root = schema

    def walk(
        node: object,
        path: tuple[str | int, ...],
        ancestors: tuple[int, ...] = (),
        unconditional: bool = True,
        parent: dict[str, object] | None = None,
        references: tuple[str, ...] = (),
    ) -> None:
        """
        Collect schema paths and their unconditional declarations.

        Args:
            node (object): Current schema or template node.
            path (tuple[str | int, ...]): Value path or chart location to inspect.
            ancestors (tuple[int, ...]): Node identities already visited along this traversal.
            unconditional (bool): Whether the schema declaration applies outside conditional
                branches.
            parent (dict[str, object] | None): Enclosing schema carrying the effective dialect.
            references (tuple[str, ...]): References already expanded along this path.

        Returns:
            None: None. The operation completes through its documented side effects.
        """
        if not isinstance(node, dict):
            if node is True and path:
                collected.setdefault(path, []).append({})
            return
        if id(node) in ancestors:
            raise ValueError(f"recursive schema at {path}")
        ancestors = (*ancestors, id(node))
        if "$ref" in node:
            reference = str(node["$ref"])
            if reference in references:
                raise ValueError(f"recursive schema path cannot be enumerated: {reference}")
            references = (*references, reference)
        node = dereference(fragment(node, parent if parent is not None else root), root)
        if path:
            collected.setdefault(path, []).append(copy.deepcopy(node))
            if unconditional:
                primary.setdefault(path, []).append(copy.deepcopy(node))
        for key, child in mapping(node.get("properties", {})).items():
            walk(child, (*path, key), ancestors, unconditional, node, references)
        items = node.get("items")
        if isinstance(items, dict):
            walk(items, (*path, "*"), ancestors, unconditional, node, references)
        elif isinstance(items, list):
            for index, child in enumerate(items):
                walk(child, (*path, index), ancestors, unconditional, node, references)
            if isinstance(node.get("additionalItems"), dict):
                walk(node["additionalItems"], (*path, "*"), ancestors, unconditional, node, references)
        for index, child in enumerate(sequence(node.get("prefixItems", []))):
            walk(child, (*path, index), ancestors, unconditional, node, references)
        if isinstance(node.get("additionalProperties"), dict):
            walk(node["additionalProperties"], (*path, "*"), ancestors, unconditional, node, references)
        for child in mapping(node.get("patternProperties", {})).values():
            walk(child, (*path, "*"), ancestors, unconditional, node, references)
        for keyword in ("allOf", "anyOf", "oneOf"):
            for branch in sequence(node.get(keyword, [])):
                walk(branch, path, ancestors, False, node, references)
        for keyword in ("then", "else"):
            if keyword in node:
                walk(node[keyword], path, ancestors, False, node, references)

    walk(schema, ())
    result = []
    for path, branches in collected.items():
        # Repeated branch paths generate one test whose complete input must still
        # satisfy the original full contract, including conjunctions/conditionals.
        # Outer declarations constrain all branches. A conditional minItems
        # fragment must not broaden a declared array into arbitrary JSON.
        branches = primary.get(path, branches)
        unique = {json.dumps(b, sort_keys=True): b for b in branches}
        node: dict[str, object] = next(iter(unique.values())) if len(unique) == 1 else {"anyOf": list(unique.values())}

        def expand(value: object, refs: tuple[str, ...] = (), parent: dict[str, object] = node) -> object:
            """
            Inline local schema references for standalone path strategies.

            Args:
                value (object): Candidate value supplied by the property strategy.
                refs (tuple[str, ...]): Reference pointers already expanded on this path.
                parent (dict[str, object]): Parent carrying inherited dialect semantics.

            Returns:
                object: Parsed or generated value at the requested boundary.
            """
            if not isinstance(value, dict):
                return value
            value = fragment(value, parent)
            if "$ref" in value:
                ref = str(value["$ref"])
                if ref in refs:
                    raise ValueError(f"recursive schema path cannot be generated: {ref}")
                return expand(dereference(value, root), (*refs, ref))
            expanded = map_children(value, lambda child: expand(child, refs, value), definitions=False)
            return {k: v for k, v in expanded.items() if k not in ("$defs", "definitions")}

        result.append(ValuePath(path, mapping(expand(node))))
    return result
