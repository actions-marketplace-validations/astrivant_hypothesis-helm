"""
Track input origins through lexical aliases and literal helper dictionaries.
"""

from __future__ import annotations

from attrs import define, frozen

__all__ = (
    "Choice",
    "Derived",
    "Dictionary",
    "Literal",
    "Origin",
    "Projection",
    "Record",
    "Sequence",
    "Text",
    "identity",
    "join",
    "paths",
    "select",
    "unresolved",
)


@frozen
class Literal:
    """
    Distinguish a known literal from an unresolved context and an input path.

    Attributes:
        value (object): Literal value; discovery never evaluates it as template code.
    """

    value: object


@frozen
class Derived:
    """
    Retain dependencies of a computed scalar or an externally supplied result.

    Attributes:
        inputs (tuple[tuple[str, ...], ...]): Original input paths; output fields never extend these paths.
        external (bool): An opaque external object permits field selection without inventing chart inputs.
    """

    inputs: tuple[tuple[str, ...], ...]
    external: bool = False


@frozen
class Record:
    """
    Describe known fields of a function result without computing their contents.

    Attributes:
        fields (dict[str, Origin]): Supported fields, such as semver components or certificate material.
    """

    fields: dict[str, Origin]


@frozen
class Sequence:
    """
    Preserve possible collection members for symbolic range traversal.

    Attributes:
        items (tuple[Origin, ...]): Literal members or one symbolic representative of generated members.
        exact (bool): Whether items enumerate the complete collection in iteration order.
    """

    items: tuple[Origin, ...]
    exact: bool = True


@define
class Dictionary:
    """
    Retain literal map entries and invalidate facts shared by aliases after mutation.

    Attributes:
        fields (dict[str, Origin]): Statically constructed entries.
        uncertain (bool): Whether an unsupported mutation may have changed any entry.
    """

    fields: dict[str, Origin]
    uncertain: bool = False


@define
class Projection:
    """
    Describe a shallow map copy made by selecting or omitting known keys.

    Attributes:
        source (Origin): Original map whose remaining entries retain their origins.
        keys (frozenset[str]): Selected or omitted keys.
        include (bool): True for pick, false for omit.
        uncertain (bool): Whether the copied map was subsequently mutated.
    """

    source: Origin
    keys: frozenset[str]
    include: bool
    uncertain: bool = False


@frozen
class Text:
    """
    Retain a supported serialization operation for concrete tpl source discovery.

    Attributes:
        source (Origin): Original value, including aliases and alternative sources.
        operation (str): Supported conversion whose output is textual.
    """

    source: Origin
    operation: str


@frozen
class Choice:
    """
    Retain all possible origins after branches or repeated assignments.

    Attributes:
        alternatives (tuple[Origin, ...]): Distinct possible origins, including an explicit unknown when needed.
    """

    alternatives: tuple[Origin, ...]


type Origin = tuple[str, ...] | Dictionary | Projection | Text | Literal | Derived | Record | Sequence | Choice | None


def identity(origin: Origin) -> tuple[object, ...]:
    """
    Identify a symbolic calling context for reuse within one discovery run.

    Args:
        origin (Origin): A path, literal dictionary, literal, or unknown origin.

    Returns:
        tuple[object, ...]: Hashable context identity, independent of dictionary insertion order.
    """
    if isinstance(origin, Dictionary):
        return ("dict", tuple((key, identity(value)) for key, value in sorted(origin.fields.items())), origin.uncertain)
    if isinstance(origin, Projection):
        return ("projection", identity(origin.source), tuple(sorted(origin.keys)), origin.include, origin.uncertain)
    if isinstance(origin, Text):
        return ("text", identity(origin.source), origin.operation)
    if isinstance(origin, Literal):
        return ("literal", repr(origin.value))
    if isinstance(origin, Derived):
        return ("derived", origin.inputs, origin.external)
    if isinstance(origin, Record):
        return ("record", tuple((key, identity(value)) for key, value in sorted(origin.fields.items())))
    if isinstance(origin, Sequence):
        return ("sequence", tuple(identity(item) for item in origin.items), origin.exact)
    if isinstance(origin, Choice):
        return ("choice", tuple(identity(item) for item in origin.alternatives))
    return ("path", origin) if isinstance(origin, tuple) else ("unknown",)


def join(*origins: Origin) -> Origin:
    """
    Merge branch possibilities without discarding unknown or earlier loop iterations.

    Args:
        *origins (Origin): Origins visible on different paths through a template.

    Returns:
        Origin: Deterministic union, or its sole member when every path agrees.
    """
    unique: dict[tuple[object, ...], Origin] = {}
    for origin in origins:
        for item in origin.alternatives if isinstance(origin, Choice) else (origin,):
            unique[identity(item)] = item
    alternatives = tuple(unique[key] for key in sorted(unique, key=repr))
    return alternatives[0] if len(alternatives) == 1 else Choice(alternatives)


def paths(origin: Origin) -> tuple[tuple[str, ...], ...]:
    """
    Collect source paths without interpreting generated fields as new values keys.

    Args:
        origin (Origin): Direct, derived, structured or joined origin.

    Returns:
        tuple[tuple[str, ...], ...]: Distinct original paths in deterministic order.
    """
    if isinstance(origin, tuple):
        return (origin,)
    if isinstance(origin, Derived):
        return origin.inputs
    if isinstance(origin, (Projection, Text)):
        return paths(origin.source)
    items = (
        origin.fields.values()
        if isinstance(origin, Dictionary)
        else origin.fields.values()
        if isinstance(origin, Record)
        else origin.items
        if isinstance(origin, Sequence)
        else origin.alternatives
        if isinstance(origin, Choice)
        else ()
    )
    return tuple(sorted({path for item in items for path in paths(item)}))


def unresolved(origin: Origin) -> bool:
    """
    Detect uncertainty in an otherwise partially resolved branch union.

    Args:
        origin (Origin): Selected value whose context may differ between branches.

    Returns:
        bool: At least one possible selected origin is unknown.
    """
    return origin is None or isinstance(origin, Choice) and any(unresolved(item) for item in origin.alternatives)


def select(origin: Origin, parts: tuple[str, ...]) -> Origin:
    """
    Follow fields through a known path or dictionary without assuming unknown values are roots.

    Args:
        origin (Origin): Lexically resolved base context.
        parts (tuple[str, ...]): Fields selected from that context.

    Returns:
        Origin: Input origin, literal, mapped context, or unresolved result.
    """
    for part in parts:
        if isinstance(origin, tuple):
            origin = (*origin, part)
        elif isinstance(origin, Dictionary):
            selected = join(*origin.fields.values()) if part == "*" else origin.fields.get(part, Literal(None))
            origin = join(selected, None) if origin.uncertain else selected
        elif isinstance(origin, Projection):
            selected = (
                join(*(select(origin.source, (key,)) for key in sorted(origin.keys)))
                if part == "*" and origin.include
                else select(origin.source, (part,))
                if part == "*" or (part in origin.keys) == origin.include
                else Literal(None)
            )
            origin = join(selected, None) if origin.uncertain else selected
        elif isinstance(origin, Choice):
            origin = join(*(select(item, (part,)) for item in origin.alternatives))
        elif isinstance(origin, Sequence) and part == "*":
            origin = join(*origin.items)
        elif isinstance(origin, Record):
            origin = origin.fields.get(part)
        elif isinstance(origin, Derived) and origin.external:
            continue
        else:
            return None
    return origin
