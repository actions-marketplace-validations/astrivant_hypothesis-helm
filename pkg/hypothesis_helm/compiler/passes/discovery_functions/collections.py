"""
Preserve collection members, key projections and exact traversal order when known.
"""

from hypothesis_helm.compiler.asts.origins import Choice, Dictionary, Literal, Origin, Projection, Sequence, join, select
from hypothesis_helm.compiler.passes.discovery_functions.scalars import declared, derived

__all__ = ("result",)


def _split(function: str, arguments: list[Origin]) -> Origin:
    """
    Model literal separators while retaining uncertain collection sizes.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    scalar = derived(arguments)
    if function in {"splitList", "split"} and len(arguments) == 2:
        separator, value = arguments
        if (
            isinstance(separator, Literal)
            and isinstance(separator.value, str)
            and isinstance(value, Literal)
            and isinstance(value.value, str)
        ):
            pieces = value.value.split(separator.value) if separator.value else list(value.value)
            if function == "split":
                return Dictionary({f"_{index}": Literal(piece) for index, piece in enumerate(pieces)})
            return Sequence(tuple(Literal(piece) for piece in pieces))
        if function == "split":
            # Unknown number of numbered keys; their string values still depend on the input.
            return Dictionary({"*": scalar}, uncertain=True)
        return Sequence((scalar,), exact=False)
    if function == "splitn" and len(arguments) == 3:
        separator, count, value = arguments
        if (
            isinstance(separator, Literal)
            and isinstance(separator.value, str)
            and isinstance(count, Literal)
            and type(count.value) is int
            and isinstance(value, Literal)
            and isinstance(value.value, str)
        ):
            if count.value == 0:
                pieces = []
            elif not separator.value:
                pieces = list(value.value)
                if count.value > 0 and len(pieces) > count.value:
                    pieces = [*pieces[: count.value - 1], "".join(pieces[count.value - 1 :])]
            else:
                pieces = value.value.split(separator.value, maxsplit=count.value - 1 if count.value > 0 else -1)
            return Dictionary({f"_{index}": Literal(piece) for index, piece in enumerate(pieces)})
        return None
    return declared(function, arguments)


def _project(function: str, arguments: list[Origin]) -> Origin:
    """
    Select known map keys without copying unrelated values origins.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    source = arguments[0]
    if function in {"omit", "pick"}:
        keys = frozenset(arg.value for arg in arguments[1:] if isinstance(arg, Literal) and isinstance(arg.value, str))
        if len([arg for arg in arguments[1:] if isinstance(arg, Literal) and isinstance(arg.value, str)]) != len(arguments) - 1:
            return None
        if isinstance(source, Dictionary) and not source.uncertain:
            return Dictionary({key: value for key, value in source.fields.items() if (key in keys) == (function == "pick")})
        return Projection(source, keys, include=function == "pick")
    return None


def _extend(function: str, arguments: list[Origin]) -> Origin:
    """
    Track the added member while preserving uncertainty about the existing list.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    source = arguments[0]
    if function in {"append", "prepend"} and len(arguments) == 2:
        members = source.items if isinstance(source, Sequence) else (select(source, ("*",)),)
        members = (*members, arguments[1]) if function == "append" else (arguments[1], *members)
        return Sequence(members, exact=isinstance(source, Sequence) and source.exact)
    # Partial calls retain possible member origins; Helm still checks their arity.
    return _reorder(function, arguments)


def _reorder(function: str, arguments: list[Origin]) -> Origin:
    """
    Preserve exact positions only when the source sequence is known.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    source = arguments[0]
    if len(arguments) == 1:
        if function in {"first", "last"}:
            if isinstance(source, Sequence) and source.exact:
                return source.items[0 if function == "first" else -1] if source.items else Literal(None)
            return join(select(source, ("*",)), Literal(None))
        if function == "reverse":
            return (
                Sequence(tuple(reversed(source.items)), source.exact)
                if isinstance(source, Sequence)
                else Sequence((select(source, ("*",)),), False)
            )
        if (
            isinstance(source, Sequence)
            and source.exact
            and all(isinstance(item, Literal) and isinstance(item.value, str) for item in source.items)
        ):
            strings = [item.value for item in source.items if isinstance(item, Literal) and isinstance(item.value, str)]
            strings = sorted(strings) if function == "sortAlpha" else list(dict.fromkeys(strings))
            return Sequence(tuple(Literal(item) for item in strings))
        return Sequence((select(source, ("*",)),), exact=False)
    return declared(function, arguments)


def result(function: str, arguments: list[Origin]) -> Origin:
    """
    Dispatch collection operations without flattening their element origins.

    Args:
        function (str): Canonical Helm function name.
        arguments (list[Origin]): Operands with their input origins retained.

    Returns:
        Origin: Established result shape or explicit uncertainty.
    """
    if function == "list":
        return Sequence(tuple(arguments))
    if function == "concat":
        members = tuple(item for arg in arguments for item in (arg.items if isinstance(arg, Sequence) else (select(arg, ("*",)),)))
        return Sequence(members, exact=all(isinstance(arg, Sequence) and arg.exact for arg in arguments))

    if function in {"splitList", "split", "splitn"}:
        return _split(function, arguments)
    if arguments:
        source = arguments[0]
        # Distribute the operation over alternatives before projecting members.
        if isinstance(source, Choice):
            return join(*(result(function, [item, *arguments[1:]]) for item in source.alternatives))
        if function in {"omit", "pick"}:
            return _project(function, arguments)
        if function in {"append", "prepend"}:
            return _extend(function, arguments)
        return _reorder(function, arguments)
    return declared(function, arguments)
