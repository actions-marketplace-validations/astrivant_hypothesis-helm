"""
Retain JSON Schema dialects at schema boundaries without interpreting literal data as schema code.
"""

import copy
from collections.abc import Callable, Iterator
from urllib.parse import unquote

from hypothesis_helm.schemas.contracts import mapping

__all__ = (
    "DRAFT4",
    "DRAFT6",
    "DRAFT7",
    "DRAFT2019",
    "DRAFT2020",
    "active",
    "canonical",
    "dialect",
    "fragment",
    "map_children",
    "numeric_bounds",
    "pointer_target",
    "resolve",
    "walk",
)

DRAFT4 = "http://json-schema.org/draft-04/schema#"
DRAFT6 = "http://json-schema.org/draft-06/schema#"
DRAFT7 = "http://json-schema.org/draft-07/schema#"
DRAFT2019 = "https://json-schema.org/draft/2019-09/schema"
DRAFT2020 = "https://json-schema.org/draft/2020-12/schema"
_DIALECTS = (DRAFT4, DRAFT6, DRAFT7, DRAFT2019, DRAFT2020)
_MODERN = {"dependentRequired", "dependentSchemas", "unevaluatedItems", "unevaluatedProperties", "minContains", "maxContains"}
_SINGLE = {
    "additionalItems",
    "additionalProperties",
    "propertyNames",
    "contains",
    "not",
    "if",
    "then",
    "else",
    "unevaluatedItems",
    "unevaluatedProperties",
}
_LIST = {"allOf", "anyOf", "oneOf", "prefixItems"}
_MAP = {"properties", "patternProperties", "$defs", "definitions", "dependentSchemas"}


def dialect(schema: dict[str, object], inherited: str = DRAFT2020) -> str:
    """
    Resolve supported declarations, including the unversioned alias used by Helm charts.

    Args:
        schema (dict[str, object]): Current schema node.
        inherited (str): Dialect of its enclosing schema resource.

    Returns:
        str: Canonical supported metaschema URI.

    Raises:
        ValueError: An explicit dialect is unknown rather than silently assumed current.
    """
    declaration = schema.get("$schema", inherited)
    if not isinstance(declaration, str):
        raise ValueError("JSON Schema $schema must be a URI string")
    normalized = declaration.removeprefix("https://").removeprefix("http://").rstrip("#")
    if normalized == "json-schema.org/schema":
        return DRAFT2020
    for version in _DIALECTS:
        if normalized == version.split("://", 1)[1].rstrip("#"):
            return version
    raise ValueError(f"Unsupported JSON Schema dialect: {declaration}")


def active(schema: dict[str, object], inherited: str = DRAFT2020) -> dict[str, object]:
    """
    Ignore keywords that are annotations rather than constraints in the declared draft.

    Args:
        schema (dict[str, object]): Current schema, without changing its children or data literals.
        inherited (str): Enclosing dialect for nodes without their own declaration.

    Returns:
        dict[str, object]: Shallow copy of the keywords meaningful in this dialect.
    """
    version = dialect(schema, inherited)
    if "$ref" in schema and version in (DRAFT4, DRAFT6, DRAFT7):
        return {key: value for key, value in schema.items() if key in {"$ref", "$schema"}}
    ignored = {"prefixItems"} if version != DRAFT2020 else {"additionalItems"}
    if version in (DRAFT4, DRAFT6, DRAFT7):
        ignored |= _MODERN | {"$dynamicRef", "$recursiveRef"}
    else:
        ignored |= {"dependencies"}
        ignored |= {"$dynamicRef", "$dynamicAnchor"} if version == DRAFT2019 else {"$recursiveRef", "$recursiveAnchor"}
    if version in (DRAFT4, DRAFT6):
        ignored |= {"if", "then", "else"}
    if version == DRAFT4:
        ignored |= {"const", "contains", "propertyNames"}
    return {key: value for key, value in schema.items() if key not in ignored}


def fragment(schema: dict[str, object], parent: dict[str, object]) -> dict[str, object]:
    """
    Preserve inherited semantics when a child becomes an independent schema.

    Args:
        schema (dict[str, object]): Extracted subschema.
        parent (dict[str, object]): Schema supplying the inherited dialect.

    Returns:
        dict[str, object]: Detached fragment with an explicit dialect when needed.
    """
    version = dialect(schema, dialect(parent))
    result = dict(schema)
    if version != DRAFT2020 or "$schema" in result:
        result["$schema"] = version
    return result


def numeric_bounds(schema: dict[str, object], version: str) -> dict[str, object]:
    """
    Convert Draft 4 Boolean exclusivity to numeric bounds accepted by later drafts.

    Args:
        schema (dict[str, object]): Scalar or larger schema containing direct bounds.
        version (str): Dialect giving those bounds their meaning.

    Returns:
        dict[str, object]: Copy using numeric exclusive bounds without changing accepted values.
    """
    result = dict(schema)
    if version == DRAFT4:
        for inclusive, exclusive in (("minimum", "exclusiveMinimum"), ("maximum", "exclusiveMaximum")):
            enabled = result.pop(exclusive, False)
            if enabled is True and inclusive in result:
                result[exclusive] = result.pop(inclusive)
    return result


def canonical(schema: dict[str, object]) -> dict[str, object]:
    """
    Normalize metaschema aliases at schema positions while preserving authored constraints and literal data.

    Args:
        schema (dict[str, object]): Root document or standalone fragment.

    Returns:
        dict[str, object]: Independent schema copy with recognized canonical dialect declarations.
    """

    def visit(raw: object, inherited: str) -> object:
        """
        Retain each declaration's meaning as nested resources change dialect.

        Args:
            raw (object): Current child schema.
            inherited (str): Parent dialect.

        Returns:
            object: Schema with canonical declarations and unchanged assertions.
        """
        if not isinstance(raw, dict):
            return raw
        version = dialect(raw, inherited)
        result = {**raw, **map_children(active(raw, inherited), lambda child: visit(child, version))}
        if "$schema" in result:
            result["$schema"] = version
        return result

    return copy.deepcopy(mapping(visit(schema, dialect(schema))))


def map_children(schema: dict[str, object], transform: Callable[[object], object], *, definitions: bool = True) -> dict[str, object]:
    """
    Transform schema positions while preserving objects inside const, enum, default and examples.

    Args:
        schema (dict[str, object]): Schema whose immediate children are visited.
        transform (Callable[[object], object]): Transformation for each child schema.
        definitions (bool): Also visit definition containers when requested.

    Returns:
        dict[str, object]: Copy with transformed schema children and untouched literal data.
    """
    result = dict(schema)
    for key, value in schema.items():
        if key in _SINGLE or key == "items" and not isinstance(value, list):
            result[key] = transform(value)
        elif key in _LIST or key == "items" and isinstance(value, list):
            result[key] = [transform(child) for child in value] if isinstance(value, list) else value
        elif key in _MAP and (definitions or key not in {"$defs", "definitions"}):
            result[key] = {name: transform(child) for name, child in mapping(value).items()}
        elif key == "dependencies":
            result[key] = {
                name: copy.deepcopy(child) if isinstance(child, list) else transform(child) for name, child in mapping(value).items()
            }
    return result


def pointer_target(root: dict[str, object], reference: object) -> tuple[object, str]:
    """
    Locate an original schema node without copying it, decoding URI fragments and JSON Pointer escapes.

    Args:
        root (dict[str, object]): Document owning the local pointer.
        reference (object): Local JSON Pointer string.

    Returns:
        tuple[object, str]: Target and inherited dialect; mutable targets retain their original identity.

    Raises:
        ValueError: The pointer is nonlocal, malformed, or names an unsupported anchor.
    """
    if not isinstance(reference, str) or reference != "#" and not reference.startswith("#/"):
        raise ValueError("only local JSON Pointer schema references are supported")
    target: object = root
    target_version = dialect(root)
    for segment in unquote(reference[2:]).split("/") if reference != "#" else []:
        key = segment.replace("~1", "/").replace("~0", "~")
        try:
            target = target[int(key)] if isinstance(target, list) and key.isdecimal() else mapping(target)[key]
        except (KeyError, IndexError, ValueError) as error:
            raise ValueError(f"invalid local schema reference: {reference}") from error
        if isinstance(target, dict) and isinstance(target.get("$schema"), str):
            target_version = dialect(target, target_version)
    return target, target_version


def resolve(schema: dict[str, object], root: dict[str, object], seen: tuple[str, ...] = ()) -> dict[str, object]:
    """
    Resolve local JSON Pointers, retaining modern reference siblings and ignoring legacy siblings.

    Args:
        schema (dict[str, object]): Reference or inline schema.
        root (dict[str, object]): Original document supplying definitions and pointer targets.
        seen (tuple[str, ...]): References already followed along this expansion.

    Returns:
        dict[str, object]: Equivalent dereferenced schema with its inherited dialect.

    Raises:
        ValueError: A reference is recursive, nonlocal, an anchor, or not a schema.
    """
    selected = fragment(schema, root)
    version = dialect(selected)
    node = active(selected)
    if "$ref" not in node:
        return node
    reference = node["$ref"]
    if not isinstance(reference, str) or reference != "#" and not reference.startswith("#/"):
        raise ValueError("only local JSON Pointer schema references are supported")
    if reference in seen:
        raise ValueError(f"recursive schema reference cannot be expanded: {reference}")
    target, target_version = pointer_target(root, reference)
    if isinstance(target, bool):
        resolved: dict[str, object] = {} if target else {"not": {}}
    elif isinstance(target, dict):
        resolved = resolve(fragment(target, {"$schema": target_version}), root, (*seen, reference))
    else:
        raise ValueError(f"schema reference does not target a schema: {reference}")
    siblings = {key: value for key, value in node.items() if key not in {"$ref", "$schema"}}
    return {"$schema": version, "allOf": [resolved, siblings]} if siblings else resolved


def walk(schema: dict[str, object]) -> Iterator[dict[str, object]]:
    """
    Visit actual schema nodes without descending into literal JSON payloads.

    Args:
        schema (dict[str, object]): Root schema carrying the default dialect.

    Yields:
        dict[str, object]: Original schema nodes, suitable for read-only validation checks.
    """
    pending: list[tuple[object, str]] = [(schema, dialect(schema))]
    while pending:
        raw, inherited = pending.pop()
        if not isinstance(raw, dict):
            continue
        version = dialect(raw, inherited)
        yield raw

        def queue(child: object, parent_version: str = version) -> object:
            """
            Queue one schema child with its inherited dialect.

            Args:
                child (object): Boolean or object subschema.
                parent_version (str): Dialect at the parent boundary.

            Returns:
                object: Original child, left unmodified.
            """
            pending.append((child, parent_version))
            return child

        map_children(active(raw, inherited), queue)
