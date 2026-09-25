"""
Admit deterministic native calls only after bounding allocation and excluding implicit effects.
"""

import json
import re

from hypothesis_helm.compiler.asts.contract_values import DerivedValue, NativeValue
from hypothesis_helm.compiler.constants import INTEGER_RESULTS
from hypothesis_helm.exceptions.compiler import Unavailable

__all__ = ("admit",)


def _sequence(function: str, args: list[object], limits: dict[str, int]) -> None:
    """
    Bound loops before Go allocates their output, including descending and empty sequences.

    Args:
        function (str): Sequence constructor.
        args (list[object]): Concrete operands.
        limits (dict[str, int]): Configured collection and string budgets.

    Returns:
        None: Excessive or unproved sequence sizes raise Unavailable.
    """
    if any(type(value) is not int for value in args):
        raise Unavailable("native sequence bounds require explicit integers")
    numbers = [int(str(value)) for value in args]
    # Bounding endpoints also prevents integer wraparound making a finite loop endless.
    if any(abs(value) > limits["max_range_items"] for value in numbers):
        raise Unavailable("sequence bounds exceed compiler.max_range_items")
    if function == "until" and len(numbers) == 1:
        count = abs(numbers[0])
    elif function == "untilStep" and len(numbers) == 3:
        start, stop, step = numbers
        count = len(range(start, stop, step)) if step else 0
    elif function == "seq" and 1 <= len(numbers) <= 3:
        if len(numbers) == 1:
            start, step, stop = 1, 1, numbers[0]
        elif len(numbers) == 2:
            start, step, stop = numbers[0], 1, numbers[1]
        else:
            start, step, stop = numbers
        if len(numbers) != 3 and stop < start:
            step = -1
        count = len(range(start, stop + (1 if stop >= start else -1), step)) if step else 0
    else:
        return  # Native arity validation handles this without allocating a sequence.
    if count > limits["max_range_items"] or function == "seq" and count * 24 > limits["max_string_chars"]:
        raise Unavailable("sequence output exceeds compiler.max_range_items or compiler.max_string_chars")


def _dates(function: str, arguments: list[object]) -> None:
    """
    Reject Sprig date operands whose type would silently select the current clock.

    Args:
        function (str): Native function name.
        arguments (list[object]): Typed operands before JSON transport.

    Returns:
        None: Fixed dates proceed; implicit current-time fallback remains unknown.
    """
    position = 1 if function in {"date", "dateInZone", "date_in_zone"} else 0
    if function in {"date", "dateInZone", "date_in_zone", "htmlDate", "htmlDateInZone"} and len(arguments) > position:
        value = arguments[position]
        fixed = type(value) is int or isinstance(value, DerivedValue) and value.function in INTEGER_RESULTS
        if isinstance(value, NativeValue):
            fixed = value.go_type in {"time.Time", "*time.Time", "int", "int32", "int64"}
        if not fixed:
            raise Unavailable("date operand may fall back to the current clock; use a fixed time or explicit integer conversion")
    if function == "durationRound" and arguments and isinstance(arguments[0], NativeValue):
        if arguments[0].go_type == "time.Time":
            raise Unavailable("durationRound of a time value reads the current clock")


def _regex(function: str, args: list[object], limits: dict[str, int]) -> None:
    """
    Bound regex compilation and replacement expansion independently of the subprocess timeout.

    Args:
        function (str): Go regex operation.
        args (list[object]): Concrete operands.
        limits (dict[str, int]): Pattern, subject, collection and string bounds.

    Returns:
        None: Native evaluation may run only after the worst-case expansion is bounded.
    """
    if function == "regexQuoteMeta":
        return
    if len(args) < 2 or not all(isinstance(value, str) for value in args[:2]):
        raise Unavailable("native regex requires string pattern and subject")
    pattern, subject = str(args[0]), str(args[1])
    if len(pattern) > limits["max_regex_pattern_chars"] or len(subject) > limits["max_regex_subject_chars"]:
        raise Unavailable("regex exceeds compiler.max_regex_pattern_chars or compiler.max_regex_subject_chars")
    if "Replace" in function and len(args) == 3 and isinstance(args[2], str):
        replacement = args[2]
        expansion = len(replacement) * (max(1, len(subject)) if "$" in replacement and "Literal" not in function else 1)
        if len(subject) + (len(subject) + 1) * expansion > limits["max_string_chars"]:
            raise Unavailable("regex replacement may exceed compiler.max_string_chars")
    if "FindAll" in function or "Split" in function:
        count = min(len(subject) + 1, args[2]) if len(args) == 3 and type(args[2]) is int and args[2] >= 0 else len(subject) + 1
        if count > limits["max_range_items"]:
            raise Unavailable("regex output may exceed compiler.max_range_items")


def admit(function: str, arguments: list[object], args: list[object], limits: dict[str, int]) -> None:
    """
    Check function-specific effects and allocations before starting the native process.

    Args:
        function (str): Reviewed deterministic operation.
        arguments (list[object]): Original typed operands.
        args (list[object]): Bounded JSON-compatible operand copies.
        limits (dict[str, int]): Per-chart compiler budgets.

    Returns:
        None: Invalid native operand types still defer through Helm's own error handling.

    Raises:
        Unavailable: A result is nondeterministic or its allocation exceeds the analysis budget.
    """
    _dates(function, arguments)
    if "Regex" in function or function.startswith("regex"):
        _regex(function, args, limits)
    if function in {"until", "untilStep", "seq"}:
        _sequence(function, args, limits)
    if function == "repeat" and len(args) == 2 and type(args[0]) is int and isinstance(args[1], str):
        if max(0, args[0]) * len(args[1].encode()) > limits["max_string_chars"]:
            raise Unavailable("repeat output exceeds compiler.max_string_chars")
    if function in {"indent", "nindent"} and len(args) == 2 and type(args[0]) is int and isinstance(args[1], str):
        if (
            args[0] < 0
            or args[0] > limits["max_indent_width"]
            or args[0] * (args[1].count("\n") + 1) + len(args[1]) + 1 > limits["max_string_chars"]
        ):
            raise Unavailable("indentation exceeds compiler.max_indent_width or compiler.max_string_chars")
    if function == "values" and args and isinstance(args[0], dict) and len(args[0]) > 1:
        raise Unavailable("values has unspecified map iteration order; retain native rendering")
    if function in {"chunk", "mustChunk"} and args and type(args[0]) is int and args[0] > limits["max_range_items"]:
        raise Unavailable("chunk allocation exceeds compiler.max_range_items")
    if function in {"print", "println", "printf", "cat", "wrap", "wrapWith", "toPrettyJson", "toYamlPretty"}:
        # Includes JSON escaping and formatting diagnostics, not just successful output.
        expansion = 8 * len(json.dumps(args, ensure_ascii=False)) + len(args) + 1
        if function == "printf" and args and isinstance(args[0], str):
            # Widths and precision can allocate even when the input string is tiny.
            dimensions = [int(token) for token in re.findall(r"\d+", args[0])]
            if "*" in args[0]:
                dimensions.extend(abs(value) for value in args[1:] if type(value) is int)
            expansion += args[0].count("%") * max(dimensions, default=0)
        if function == "wrapWith" and len(args) == 3 and isinstance(args[1], str) and isinstance(args[2], str):
            expansion += (len(args[2]) + 1) * len(args[1])
        if expansion > limits["max_string_chars"]:
            raise Unavailable("native formatting may exceed compiler.max_string_chars")
    if function in {"fromYaml", "fromJson", "b64dec", "b32dec"} and args and not isinstance(args[0], str):
        raise Unavailable("native deserialization requires a string")
