"""
Model bounded Go printf output, including diagnostic strings rather than raised formatting errors.
"""

import re

from hypothesis_helm.compiler.asts.contract_values import ContractText, DerivedValue, KeyList, native
from hypothesis_helm.compiler.constants import INTEGER_RESULTS, MAX_INTEGER, MIN_INTEGER
from hypothesis_helm.exceptions.compiler import Unknown

__all__ = ("printf",)


def _integer_kind(operand: object) -> str:
    """
    Identify only Go integer types established by template literals or explicit conversions.

    Args:
        operand (object): Original operand retaining its conversion provenance.

    Returns:
        str: Go's int or int64 type name for format-error diagnostics.

    Raises:
        Unknown: A YAML number does not establish a concrete Go integer type.
    """
    value = native(operand)
    if type(value) is not int or not MIN_INTEGER <= value <= MAX_INTEGER:
        raise Unknown("printf integer lies outside the supported Go integer range")
    if type(operand) is int:
        return "int"
    if isinstance(operand, DerivedValue) and operand.function in INTEGER_RESULTS:
        # Sprig's integer arithmetic returns int64; int and atoi explicitly return int.
        return "int" if operand.function in {"int", "atoi"} else "int64"
    raise Unknown("printf integer formatting requires an explicit integer conversion or known integer result")


def _scalar(operand: object) -> tuple[str, str]:
    """
    Preserve Go type names when constructing a supported scalar formatting diagnostic.

    Args:
        operand (object): Concrete operand and any type provenance.

    Returns:
        tuple[str, str]: Go type and default text, with an empty type name for an untyped nil.

    Raises:
        Unknown: The Go type or output order cannot be established.
    """
    if isinstance(operand, ContractText):
        raise Unknown("printf diagnostic formatting with unordered output requires native evaluation")
    value = native(operand)
    if value is None:
        return "", "<nil>"
    if isinstance(value, str):
        return "string", value
    if type(value) is bool:
        return "bool", str(value).lower()
    if type(value) is int:
        return _integer_kind(operand), str(value)
    raise Unknown("printf diagnostic requires a supported scalar with a known Go type")


def _argument(verb: str, operand: object) -> list[str | KeyList]:
    """
    Format one argument while retaining symbolic ordering only for a string substitution.

    Args:
        verb (str): Supported percent-s, percent-d or percent-v directive.
        operand (object): Evaluated argument with provenance intact.

    Returns:
        list[str | KeyList]: Formatted fragments, including any ordinary Go format-error text.
    """
    if isinstance(operand, ContractText):
        if verb == "%s":
            return list(operand.parts)
        raise Unknown("mixed printf formatting with unordered output requires native evaluation")
    value = native(operand)
    # A raw integral values number has stable default text, but not necessarily Go's int type.
    if verb == "%v" and type(value) is int:
        return [str(value)]
    kind, text = _scalar(operand)
    if verb == "%v" or verb == "%s" and kind == "string" or verb == "%d" and kind in {"int", "int64"}:
        return [text]
    diagnostic = f"{kind}={text}" if kind else text
    return [f"%!{verb[1]}({diagnostic})"]


def printf(format_string: str, arguments: list[object], *, max_chars: int) -> str | ContractText:
    """
    Evaluate the supported printf subset with Go's missing, extra and mismatched operand diagnostics.

    Args:
        format_string (str): Concrete format, supporting percent-s, percent-d, percent-v and escaped percent signs.
        arguments (list[object]): Already evaluated arguments; this function does not change eager evaluation.
        max_chars (int): Configured maximum format and output size, including diagnostic text.

    Returns:
        str | ContractText: Exact output or text retaining proved map-key ordering uncertainty.

    Raises:
        Unknown: Formatting needs unsupported Go semantics or exceeds the configured size bound.
    """
    if len(format_string) > max_chars:
        raise Unknown("printf format exceeds compiler.max_string_chars")
    parts: list[str | KeyList] = []
    size = 0

    def append(part: str | KeyList) -> None:
        """
        Account for output before retaining another literal or unordered-key fragment.

        Args:
            part (str | KeyList): Next fragment emitted in native formatting order.

        Returns:
            None: Output is retained only while within the configured character budget.
        """
        nonlocal size
        size += len(part) if isinstance(part, str) else sum(map(len, part.values)) + len(part.separator) * max(0, len(part.values) - 1)
        if size > max_chars:
            raise Unknown("printf output exceeds compiler.max_string_chars")
        parts.append(part)

    position = 0
    for piece in re.split(r"(%s|%d|%v|%%)", format_string):
        if piece == "%%":
            append("%")
        elif piece in {"%s", "%d", "%v"}:
            if position >= len(arguments):
                append(f"%!{piece[1]}(MISSING)")
            else:
                for fragment in _argument(piece, arguments[position]):
                    append(fragment)
                position += 1
        elif "%" in piece:
            # A trailing bare percent is a Go diagnostic; flags, widths and other verbs stay unresolved.
            if piece.endswith("%") and "%" not in piece[:-1]:
                append(piece[:-1])
                append("%!(NOVERB)")
            else:
                raise Unknown("unsupported printf format")
        else:
            append(piece)
    if position < len(arguments):
        append("%!(EXTRA ")
        for index, operand in enumerate(arguments[position:]):
            if index:
                append(", ")
            kind, text = _scalar(operand)
            append(f"{kind}={text}" if kind else text)
        append(")")
    return ContractText(tuple(parts)) if any(isinstance(part, KeyList) for part in parts) else "".join(str(part) for part in parts)
