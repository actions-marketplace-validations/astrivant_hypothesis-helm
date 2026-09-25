"""
Describe bounded input regions where tpl cannot change serialized YAML structure.
"""

import copy
from functools import lru_cache

from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("contribution", "literal_region")


def contribution(schema: dict[str, object]) -> dict[str, object]:
    """
    Retain constraints on contributed fields and items without requiring the fragment to be the whole container.

    Args:
        schema (dict[str, object]): Contract for the assembled destination container.

    Returns:
        dict[str, object]: Necessary fragment constraints, leaving collection-wide assertions to the completed manifest.
    """
    aggregate = {
        "required",
        "minProperties",
        "maxProperties",
        "minItems",
        "maxItems",
        "uniqueItems",
        "contains",
        "minContains",
        "maxContains",
        "const",
        "enum",
        "if",
        "then",
        "else",
        "not",
        "dependentRequired",
        "dependentSchemas",
        "dependencies",
        "unevaluatedProperties",
        "unevaluatedItems",
        "prefixItems",
        "additionalItems",
        "allOf",
        "anyOf",
        "oneOf",
    }
    # The surrounding template determines the fragment's array offset. Tuple
    # positions and tail-only schemas cannot be assigned to its first item.
    if isinstance(schema.get("items"), list) or "prefixItems" in schema:
        aggregate.add("items")
    result = copy.deepcopy({key: value for key, value in schema.items() if key not in aggregate})
    for key in ("allOf", "anyOf", "oneOf"):
        if isinstance(schema.get(key), list):
            # Two exclusive whole-object alternatives can describe the same
            # partial fragment; exclusivity must be checked after assembly.
            clause = {"anyOf" if key == "oneOf" else key: [contribution(mapping(child)) for child in sequence(schema[key])]}
            sequence(result.setdefault("allOf", [])).append(clause)
    return result


@lru_cache(maxsize=32)
def literal_region(max_depth: int, max_nodes: int) -> dict[str, object]:
    """
    Prove the absence of template delimiters in keys and values within a bounded JSON tree.

    Args:
        max_depth (int): Maximum nested containers whose literal contents can be established.
        max_nodes (int): Maximum schema expansion work, counting repeated child expressions.

    Returns:
        dict[str, object]: A sufficient literal-input region; deeper or templated values remain outside it.
    """
    no_template: dict[str, object] = {"not": {"type": "string", "pattern": r"\{\{"}}
    region: dict[str, object] = {"type": ["null", "boolean", "number", "string"], **no_template}
    nodes = 4
    for _ in range(max_depth):
        nodes = 2 * nodes + 8
        if nodes > max_nodes:
            break
        # Type-specific keywords already ignore other JSON types. An explicit
        # anyOf at every level would multiply alternatives during generation.
        region = {**no_template, "items": region, "propertyNames": no_template, "additionalProperties": region}
    return region
