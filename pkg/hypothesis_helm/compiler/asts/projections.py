"""
Represent symbolic input origins and output choices without executing Helm templates.
"""

from __future__ import annotations

from attrs import define, field, frozen

__all__ = ("Input", "LocalMap", "Operation", "Piece", "output")


@frozen
class Input:
    """
    Identify a values field in the calling chart's namespace.

    Attributes:
        path (tuple[str, ...]): Absolute values path.
    """

    path: tuple[str, ...]


@frozen
class Operation:
    """
    Retain a transformation or condition whose result is symbolic.

    Attributes:
        name (str): Function name, or an internal output operation.
        arguments (tuple[object, ...]): Operands retaining their source origins.
    """

    name: str
    arguments: tuple[object, ...] = ()


@frozen
class Piece:
    """
    Associate one symbolic output segment with its source location.

    Attributes:
        value (object): Literal text, symbolic expression, or conditional output.
        file (str): Source template, including helper definitions.
        line (int): Original source line.
    """

    value: object
    file: str
    line: int


@define
class LocalMap:
    """
    Track a fresh helper-local map and its merged sources, including local aliases.

    Attributes:
        entries (dict[str, object]): Statically named entries.
        sources (list[object]): Symbolic maps merged into this fresh destination.
    """

    entries: dict[str, object] = field(factory=dict)
    sources: list[object] = field(factory=list)


def output(pieces: list[Piece]) -> object:
    """
    Collapse empty literal fragments without losing conditional or source information.

    Args:
        pieces (list[Piece]): Helper output in execution order.

    Returns:
        object: Single value or a structured sequence of output fragments.
    """
    selected = [piece for piece in pieces if piece.value != ""]
    if len(selected) == 1:
        return selected[0].value
    if all(isinstance(piece.value, str) for piece in selected):
        return "".join(str(piece.value) for piece in selected)
    return Operation("text", tuple(selected))
