"""
Track input origins through lexical aliases and literal helper dictionaries.
"""

from __future__ import annotations

from attrs import frozen


@frozen
class Literal:
    """
    Distinguish a known literal from an unresolved context and an input path.

    Attributes:
        value (object): Literal value; discovery never evaluates it as template code.
    """

    value: object


type Origin = tuple[str, ...] | dict[str, Origin] | Literal | None


def identity(origin: Origin) -> tuple[object, ...]:
    """
    Identify a symbolic calling context for reuse within one discovery run.

    Args:
        origin (Origin): A path, literal dictionary, literal, or unknown origin.

    Returns:
        tuple[object, ...]: Hashable context identity, independent of dictionary insertion order.
    """
    if isinstance(origin, dict):
        return ("dict", tuple((key, identity(value)) for key, value in sorted(origin.items())))
    if isinstance(origin, Literal):
        return ("literal", repr(origin.value))
    return ("path", origin) if isinstance(origin, tuple) else ("unknown",)


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
        elif isinstance(origin, dict):
            origin = origin.get(part)
        else:
            return None
    return origin
