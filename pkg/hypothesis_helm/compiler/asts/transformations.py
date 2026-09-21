"""
Model a bounded Sprig subset and propose preimage witnesses for transformed allowlists.
"""

from __future__ import annotations

import base64
import hashlib
import math
import re
from functools import lru_cache

from attrs import frozen

from hypothesis_helm.compiler.asts.contract_values import BoundValue, DerivedValue, NilSlice, native
from hypothesis_helm.compiler.constants import (
    COLLECTION_TRANSFORMS,
    FORMAT_TRANSFORMS,
    INTEGER_RESULTS,
    MAX_INTEGER,
    MIN_INTEGER,
    SELECTION_TRANSFORMS,
    TEXT_TRANSFORMS,
)
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.exceptions.compiler import UnsupportedTransformation

__all__ = (
    "TransformedDomain",
    "calculate",
    "describe",
    "inputs",
    "inverse_targets",
    "regular_expression",
    "replay",
)


@lru_cache(maxsize=1024)
def regular_expression(pattern: str, max_pattern_chars: int) -> re.Pattern[str]:
    """
    Translate a small shared Go/Python regex subset without accepting Python-only constructs.

    Args:
        pattern (str): ASCII literals, character classes, anchors and at most one variable repetition.
        max_pattern_chars (int): Configured length bound, included in the cache key.

    Returns:
        re.Pattern[str]: Bounded pattern with Go's strict end-of-text anchor.

    Raises:
        UnsupportedTransformation: Regex syntax, size, or repetition exceeds the supported subset.
    """
    if len(pattern) > max_pattern_chars:
        raise UnsupportedTransformation(f"regex exceeds compiler.max_regex_pattern_chars={max_pattern_chars}")
    if not pattern.isascii():
        raise UnsupportedTransformation("regex requires the supported ASCII subset")
    atom = re.compile(r"\[\^?(?:[A-Za-z0-9 _-]|\\[-\\\]^])+\]|\\[.\\+*?()|\[\]{}^$nrtfvd]|[A-Za-z0-9 _:/,.-]")
    position = 1 if pattern.startswith("^") else 0
    output = ["^"] if position else []
    variable_repetitions = 0
    while position < len(pattern):
        if pattern[position] == "|":
            if position == 0 or position + 1 == len(pattern) or pattern[position - 1] == "|":
                raise UnsupportedTransformation("empty regex alternatives remain unresolved")
            output.append("|")
            variable_repetitions = 0
            position += 1
            if pattern[position] == "^":
                output.append("^")
                position += 1
            continue
        if pattern[position] == "$" and (position + 1 == len(pattern) or pattern[position + 1] == "|"):
            output.append(r"\Z")
            position += 1
            continue
        match = atom.match(pattern, position)
        if match is None:
            raise UnsupportedTransformation("regex syntax is outside the supported Go-compatible subset")
        output.append(match[0])
        position = match.end()
        repeat = re.match(r"[?*+]|\{(0|[1-9][0-9]{0,3})(?:,(0|[1-9][0-9]{0,3})?)?\}", pattern[position:])
        if repeat is not None:
            quantifier = repeat[0]
            if quantifier in {"?", "*", "+"}:
                variable_repetitions += 1
            else:
                low = int(repeat[1])
                high = int(repeat[2]) if repeat[2] else None
                if low > 1000 or high is not None and (high > 1000 or high < low):
                    raise UnsupportedTransformation("regex repetition exceeds Go's supported count")
                if "," in quantifier and high != low:
                    variable_repetitions += 1
            if variable_repetitions > 1:
                raise UnsupportedTransformation("regex has multiple variable repetitions")
            output.append(quantifier)
            position += len(quantifier)
    try:
        return re.compile("".join(output), re.ASCII)
    except re.error as exc:
        raise UnsupportedTransformation("invalid supported regex") from exc


def calculate(function: str, arguments: tuple[object, ...], *, limits: dict[str, int] | None = None) -> object:
    """
    Evaluate supported concrete operands without coercing unknown Go types or Unicode rules.

    Args:
        function (str): Sprig function name.
        arguments (tuple[object, ...]): Evaluated operands in Go-template argument order.
        limits (dict[str, int] | None): Captured compiler budgets, or inherited settings.

    Returns:
        object: Concrete result with Helm-compatible semantics in the supported subset.

    Raises:
        UnsupportedTransformation: The operation cannot be modeled with the required confidence.
    """
    limits = active_limits() if limits is None else limits
    args = tuple(native(value) for value in arguments)
    if any(isinstance(value, str) and len(value) > limits["max_string_chars"] for value in args):
        raise UnsupportedTransformation(f"transformation exceeds compiler.max_string_chars={limits['max_string_chars']}")
    # Shared admission checks run once; each handler owns its operand and arity rules.
    if function in FORMAT_TRANSFORMS:
        return _format(function, args, limits, arguments=arguments)
    if function in SELECTION_TRANSFORMS:
        return _selection(function, args, limits)
    if function in COLLECTION_TRANSFORMS:
        return _collection(function, args, limits)
    if function in TEXT_TRANSFORMS:
        return _text(function, args, limits)
    if function in INTEGER_RESULTS:
        return _integer(function, args, limits)
    raise UnsupportedTransformation(f"unsupported transformation operands: {function}")


def _format(function: str, args: tuple[object, ...], limits: dict[str, int], *, arguments: tuple[object, ...]) -> object:
    """
    Format supported text without guessing Go coercions or allocating unbounded output.

    Args:
        function (str): Canonical operation name.
        args (tuple[object, ...]): Concrete operands after unwrapping provenance.
        limits (dict[str, int]): Captured compiler work and output bounds.
        arguments (tuple[object, ...]): Original operands used to establish explicit integer conversions.

    Returns:
        object: Supported concrete result.

    Raises:
        UnsupportedTransformation: Operand types, semantics or resource bounds cannot be established.
    """
    # Inspect original operand provenance before trusting integer formatting widths.
    if function == "squote" and all(value is None or isinstance(value, str | bool) for value in args):
        texts = [str(value).lower() if isinstance(value, bool) else str(value) for value in args if value is not None]
        if sum(len(value) + 3 for value in texts) - 1 > limits["max_string_chars"]:
            raise UnsupportedTransformation(f"transformation exceeds compiler.max_string_chars={limits['max_string_chars']}")
        # Sprig deliberately wraps single quotes without escaping embedded quotes.
        return " ".join("'" + value + "'" for value in texts)
    if function == "quote" and all(value is None or isinstance(value, str | bool) for value in args):
        escaped = {"\a": r"\a", "\b": r"\b", "\f": r"\f", "\n": r"\n", "\r": r"\r", "\t": r"\t", "\v": r"\v", '"': r"\"", "\\": r"\\"}
        quoted: list[str] = []
        quoted_size = 0
        for value in args:
            if value is None:
                continue
            text = str(value).lower() if isinstance(value, bool) else str(value)
            if not text.isascii():
                raise UnsupportedTransformation("quote requires the supported ASCII subset")
            literal = '"' + "".join(escaped.get(char, char if 32 <= ord(char) < 127 else f"\\x{ord(char):02x}") for char in text) + '"'
            quoted_size += len(literal) + int(bool(quoted))
            if quoted_size > limits["max_string_chars"]:
                raise UnsupportedTransformation(f"quoted output exceeds compiler.max_string_chars={limits['max_string_chars']}")
            quoted.append(literal)
        return " ".join(quoted)
    if function in {"indent", "nindent"} and len(args) == 2 and type(args[0]) is int and isinstance(args[1], str):
        width, text = args[0], args[1]
        if not (type(arguments[0]) is int or isinstance(arguments[0], DerivedValue) and arguments[0].function in INTEGER_RESULTS):
            raise UnsupportedTransformation("indentation width requires a literal or explicitly converted integer")
        size = len(text) + width * (text.count("\n") + 1) + int(function == "nindent")
        if width < 0 or size > limits["max_string_chars"]:
            raise UnsupportedTransformation(f"indentation exceeds compiler.max_string_chars={limits['max_string_chars']}")
        return ("\n" if function == "nindent" else "") + " " * width + text.replace("\n", "\n" + " " * width)
    if function == "print" and all(isinstance(value, str) for value in args):
        if sum(len(str(value)) for value in args) > limits["max_string_chars"]:
            raise UnsupportedTransformation(f"transformation exceeds compiler.max_string_chars={limits['max_string_chars']}")
        return "".join(str(value) for value in args)
    if function == "toString" and len(args) == 1 and type(args[0]) in (str, int, bool):
        return str(args[0]).lower() if type(args[0]) is bool else str(args[0])
    raise UnsupportedTransformation(f"unsupported transformation operands: {function}")


def _selection(function: str, args: tuple[object, ...], limits: dict[str, int]) -> object:
    """
    Apply emptiness and reflection rules separately from general Python truth and types.

    Args:
        function (str): Canonical operation name.
        args (tuple[object, ...]): Concrete operands after unwrapping provenance.
        limits (dict[str, int]): Captured compiler work and output bounds.

    Returns:
        object: Supported concrete result.

    Raises:
        UnsupportedTransformation: Operand types, semantics or resource bounds cannot be established.
    """
    # Nonnumeric reflection kinds survive Helm decoding; numeric kinds may not.
    if function in {"default", "coalesce"}:
        if any(value is not None and not isinstance(value, (str, bool, int, float, list, dict)) for value in args):
            raise UnsupportedTransformation("unknown emptiness semantics")
        if function == "default" and args:
            return args[1] if len(args) > 1 and args[1] else args[0]
        if function == "coalesce":
            return next((value for value in args if value), None)
    if function == "kindIs" and len(args) == 2 and isinstance(args[0], str):
        # Raw YAML numbers do not reliably identify the Go reflection kind.
        # Nonnumeric kinds are stable across Helm's JSON coalescing boundary.
        if args[0] in {"string", "map", "slice", "bool", "invalid"}:
            kinds = {str: "string", dict: "map", list: "slice", bool: "bool", type(None): "invalid"}
            kind = next((name for cls, name in kinds.items() if isinstance(args[1], cls)), None)
            return kind == args[0]
        raise UnsupportedTransformation("numeric and renderer-specific reflection kinds remain unresolved")
    if function == "ternary" and len(args) == 3 and type(args[2]) is bool:
        return args[0] if args[2] else args[1]
    raise UnsupportedTransformation(f"unsupported transformation operands: {function}")


def _collection(function: str, args: tuple[object, ...], limits: dict[str, int]) -> object:
    """
    Transform concrete collections while retaining strict size and index checks.

    Args:
        function (str): Canonical operation name.
        args (tuple[object, ...]): Concrete operands after unwrapping provenance.
        limits (dict[str, int]): Captured compiler work and output bounds.

    Returns:
        object: Supported concrete result.

    Raises:
        UnsupportedTransformation: Operand types, semantics or resource bounds cannot be established.
    """
    # Check cardinality before building the output, including internal replay operations.
    if function in {"splitList", "split"} and len(args) == 2 and all(isinstance(value, str) for value in args):
        separator, text = str(args[0]), str(args[1])
        count = text.count(separator) + 1 if separator else len(text)
        if count > limits["max_range_items"]:
            raise UnsupportedTransformation(f"split exceeds compiler.max_range_items={limits['max_range_items']}")
        if not separator:
            if not text.isascii():
                raise UnsupportedTransformation("empty-separator splitting requires the supported ASCII subset")
            pieces = list(text)
        else:
            pieces = text.split(separator)
        return pieces if function == "splitList" else {f"_{index}": piece for index, piece in enumerate(pieces)}
    if function in {"_field", "_get"} and len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], str):
        return args[0].get(args[1], "" if function == "_get" else None)
    if function == "_index" and len(args) == 2 and isinstance(args[0], list) and type(args[1]) is int:
        if not 0 <= args[1] < len(args[0]):
            raise UnsupportedTransformation("list index is outside the source list")
        return args[0][args[1]]
    if function == "concat" and all(isinstance(value, list) for value in args):
        collections = [value for value in args if isinstance(value, list)]
        if sum(map(len, collections)) > limits["max_range_items"]:
            raise UnsupportedTransformation(f"concat exceeds compiler.max_range_items={limits['max_range_items']}")
        return [item for collection in collections for item in collection] if any(collections) else NilSlice()
    raise UnsupportedTransformation(f"unsupported transformation operands: {function}")


def _text(function: str, args: tuple[object, ...], limits: dict[str, int]) -> object:
    """
    Apply the supported Go-compatible string and regular-expression subset.

    Args:
        function (str): Canonical operation name.
        args (tuple[object, ...]): Concrete operands after unwrapping provenance.
        limits (dict[str, int]): Captured compiler work and output bounds.

    Returns:
        object: Supported concrete result.

    Raises:
        UnsupportedTransformation: Operand types, semantics or resource bounds cannot be established.
    """
    # Unsupported Unicode and regex syntax remain native Helm work.
    if function in {"sha256sum", "b64enc"} and len(args) == 1 and isinstance(args[0], str):
        encoded = args[0].encode("utf-8")
        size = 64 if function == "sha256sum" else 4 * ((len(encoded) + 2) // 3)
        if size > limits["max_string_chars"]:
            raise UnsupportedTransformation("encoded output exceeds compiler.max_string_chars")
        return hashlib.sha256(encoded).hexdigest() if function == "sha256sum" else base64.b64encode(encoded).decode("ascii")
    if function == "trunc" and len(args) == 2 and type(args[0]) is int and isinstance(args[1], str):
        width, text = args[0], args[1]
        if not text.isascii():
            raise UnsupportedTransformation("byte truncation requires the supported ASCII subset")
        return text[:width] if width >= 0 else text[max(0, len(text) + width) :]
    if function in {"lower", "upper", "trim"} and len(args) == 1 and isinstance(args[0], str):
        if not args[0].isascii():
            raise UnsupportedTransformation("Unicode case and whitespace transformations remain unresolved")
        if function == "trim":
            return args[0].strip(" \t\n\r\v\f")
        return args[0].lower() if function == "lower" else args[0].upper()
    if len(args) == 2 and all(isinstance(value, str) for value in args):
        pattern, value = str(args[0]), str(args[1])
        if function in {"regexMatch", "mustRegexMatch", "regexFind"}:
            if len(value) > limits["max_regex_subject_chars"]:
                raise UnsupportedTransformation(
                    f"regex subject exceeds compiler.max_regex_subject_chars={limits['max_regex_subject_chars']}"
                )
            if not value.isascii():
                raise UnsupportedTransformation("regex subject requires the supported ASCII subset")
            match = regular_expression(pattern, limits["max_regex_pattern_chars"]).search(value)
            return (match[0] if match else "") if function == "regexFind" else match is not None
        if function == "trimAll":
            return value.strip(pattern) if pattern else value
        if function == "trimPrefix":
            return value.removeprefix(pattern)
        if function == "trimSuffix":
            return value.removesuffix(pattern)
        if function == "contains":
            return pattern in value
        if function == "hasPrefix":
            return value.startswith(pattern)
        if function == "hasSuffix":
            return value.endswith(pattern)
    if function == "replace" and len(args) == 3 and all(isinstance(value, str) for value in args):
        old, new, value = str(args[0]), str(args[1]), str(args[2])
        if len(value) + value.count(old) * (len(new) - len(old)) > limits["max_string_chars"]:
            raise UnsupportedTransformation(f"replacement exceeds compiler.max_string_chars={limits['max_string_chars']}")
        return value.replace(old, new)
    if function == "regexReplaceAll" and len(args) == 3 and all(isinstance(value, str) for value in args):
        pattern, text, replacement = map(str, args)
        if not text.isascii() or len(text) > limits["max_regex_subject_chars"]:
            raise UnsupportedTransformation("regex replacement subject exceeds the supported ASCII or length bounds")
        compiled = regular_expression(pattern, limits["max_regex_pattern_chars"])
        if "$" in replacement or compiled.search("") is not None:
            raise UnsupportedTransformation("regex capture expansion and empty matches remain unresolved")
        # Literal replacements avoid Python/Go differences in expansion syntax.
        if len(text) * max(1, len(replacement)) > limits["max_string_chars"]:
            raise UnsupportedTransformation(f"regex replacement exceeds compiler.max_string_chars={limits['max_string_chars']}")
        return compiled.sub(lambda _: replacement, text)
    raise UnsupportedTransformation(f"unsupported transformation operands: {function}")


def _integer(function: str, args: tuple[object, ...], limits: dict[str, int]) -> object:
    """
    Perform bounded integer conversions and arithmetic with overflow checks.

    Args:
        function (str): Canonical operation name.
        args (tuple[object, ...]): Concrete operands after unwrapping provenance.
        limits (dict[str, int]): Captured compiler work and output bounds.

    Returns:
        object: Supported concrete result.

    Raises:
        UnsupportedTransformation: Operand types, semantics or resource bounds cannot be established.
    """
    # Intermediate overflow matters even if the final mathematical result would fit.
    if function in {"int", "int64"} and len(args) == 1 and type(args[0]) is int:
        if not MIN_INTEGER <= args[0] <= MAX_INTEGER:
            raise UnsupportedTransformation("integer conversion exceeds the supported signed 64-bit range")
        return args[0]
    if function == "atoi" and len(args) == 1 and isinstance(args[0], str):
        if not re.fullmatch(r"[+-]?[0-9]+", args[0]):
            return 0
        if len(args[0].lstrip("+-0")) > 19:
            raise UnsupportedTransformation("atoi exceeds the supported signed integer range")
        result = int(args[0].lstrip("+-0") or "0") * (-1 if args[0].startswith("-") else 1)
        if MIN_INTEGER <= result <= MAX_INTEGER:
            return result
        raise UnsupportedTransformation("atoi overflow remains unresolved")
    if function in {"add", "add1", "sub", "mul", "min", "max"} and all(type(value) is int for value in args):
        integers = [int(str(value)) for value in args]
        if any(not MIN_INTEGER <= value <= MAX_INTEGER for value in integers):
            raise UnsupportedTransformation("integer operand exceeds the supported signed range")
        if function == "add":
            intermediate = 0
            for integer in integers:
                intermediate += integer
                if not MIN_INTEGER <= intermediate <= MAX_INTEGER:
                    raise UnsupportedTransformation("integer addition overflows")
            return intermediate
        if function == "mul" and integers:
            intermediate = integers[0]
            for integer in integers[1:]:
                intermediate *= integer
                if not MIN_INTEGER <= intermediate <= MAX_INTEGER:
                    raise UnsupportedTransformation("integer multiplication overflows")
            return intermediate
        if function == "add1" and len(integers) == 1:
            result = integers[0] + 1
        elif function == "sub" and len(integers) == 2:
            result = integers[0] - integers[1]
        elif function in {"min", "max"} and integers:
            return min(integers) if function == "min" else max(integers)
        else:
            raise UnsupportedTransformation("unsupported arithmetic arity")
        if MIN_INTEGER <= result <= MAX_INTEGER:
            return result
        raise UnsupportedTransformation("integer result overflows")
    raise UnsupportedTransformation(f"unsupported transformation operands: {function}")


def describe(value: object) -> object:
    """
    Serialize the expression as source paths and operations instead of sampled outputs.

    Args:
        value (object): Derived expression, bound input, or literal operand.

    Returns:
        object: JSON-compatible expression evidence.
    """
    if isinstance(value, BoundValue):
        return {"path": "$." + ".".join(value.path) if value.path else "$"}
    if isinstance(value, DerivedValue):
        return {"function": value.function, "arguments": [describe(argument) for argument in value.arguments]}
    value = native(value)
    if isinstance(value, dict):
        return {str(key): describe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [describe(item) for item in value]
    return value


def inputs(value: object) -> dict[tuple[str, ...], object]:
    """
    Identify source fields used by a composed scalar transformation.

    Args:
        value (object): Expression carrying input provenance.

    Returns:
        dict[tuple[str, ...], object]: Source paths and current candidate values.
    """
    if isinstance(value, BoundValue):
        return {value.path: native(value)}
    if isinstance(value, DerivedValue):
        return {path: item for argument in value.arguments for path, item in inputs(argument).items()}
    return {}


def replay(value: object, path: tuple[str, ...], replacement: object, *, limits: dict[str, int] | None = None) -> object:
    """
    Reevaluate a composed expression with every occurrence of one source input replaced.

    Args:
        value (object): Expression or literal operand.
        path (tuple[str, ...]): Input being changed.
        replacement (object): Proposed source value.
        limits (dict[str, int] | None): Captured chart budgets, or the global configuration.

    Returns:
        object: Concrete transformed output for the proposal.
    """
    if isinstance(value, BoundValue):
        return replacement if value.path == path else native(value)
    if isinstance(value, DerivedValue):
        return calculate(
            value.function, tuple(replay(argument, path, replacement, limits=limits) for argument in value.arguments), limits=limits
        )
    return native(value)


def inverse_targets(value: DerivedValue, target: object) -> list[tuple[object, object]]:
    """
    Propose bounded operand targets without claiming to enumerate the full preimage.

    Args:
        value (DerivedValue): One supported operation with its candidate operands.
        target (object): Desired output of that operation.

    Returns:
        list[tuple[object, object]]: Operand and target pairs that still require forward verification.
    """
    function, arguments = value.function, value.arguments
    args = [native(argument) for argument in arguments]
    if function in {"default", "coalesce", "min", "max"}:
        return [(argument, target) for argument in arguments]
    if function in {"lower", "upper", "trim"}:
        return [(arguments[0], target)]
    if function in {"trimAll", "trimPrefix", "trimSuffix"} and isinstance(target, str):
        return [(arguments[1], target), (arguments[1], str(args[0]) + target), (arguments[1], target + str(args[0]))]
    if function == "replace" and isinstance(target, str):
        proposals: list[tuple[object, object]] = [(arguments[2], target)]
        if args[1]:
            proposals.append((arguments[2], target.replace(str(args[1]), str(args[0]))))
        return proposals
    if function == "toString" and isinstance(target, str):
        if type(args[0]) is str:
            return [(arguments[0], target)]
        if type(args[0]) is int and re.fullmatch(r"-?[0-9]{1,19}", target):
            return [(arguments[0], int(target))]
        if type(args[0]) is bool and target in {"true", "false"}:
            return [(arguments[0], target == "true")]
    if function == "atoi" and type(target) is int:
        return [(arguments[0], str(target))]
    if type(target) is int and all(type(argument) is int for argument in args):
        numbers = [int(str(argument)) for argument in args]
        if function == "add1":
            return [(arguments[0], target - 1)]
        if function == "add":
            return [(argument, target - sum(numbers) + numbers[index]) for index, argument in enumerate(arguments)]
        if function == "sub":
            return [(arguments[0], target + numbers[1]), (arguments[1], numbers[0] - target)]
        if function == "mul":
            result: list[tuple[object, object]] = []
            for index, argument in enumerate(arguments):
                factor = math.prod(numbers[:index] + numbers[index + 1 :])
                if factor and target % factor == 0:
                    result.append((argument, target // factor))
            return result
    return []


@frozen
class TransformedDomain:
    """
    Describe a candidate-local allowlist over an expression, not an enum of raw inputs.

    Attributes:
        expression (DerivedValue): Transformation tree retaining original input paths.
        outputs (tuple[str, ...]): Source-authored allowed results of that expression.
    """

    expression: DerivedValue
    outputs: tuple[str, ...]

    def report(self) -> dict[str, object]:
        """
        Export the predicate defining the accepted transformed values on this branch.

        Returns:
            dict[str, object]: Expression and output choices, without a misleading raw-input enum.
        """
        return {"expression": describe(self.expression), "allowed_outputs": list(self.outputs)}

    def suggestions(self, *, limits: dict[str, int] | None = None) -> dict[str, list[object]]:
        """
        Find a few preimage witnesses and verify them against the entire expression.

        Args:
            limits (dict[str, int] | None): Captured chart budgets, or the global configuration.

        Returns:
            dict[str, list[object]]: Per-path proposals, bounded and awaiting whole-chart checks.
        """
        limits = active_limits() if limits is None else limits
        pending: list[tuple[object, object]] = [(self.expression, target) for target in self.outputs[: limits["max_preimage_choices"]]]
        proposals: dict[str, list[object]] = {}
        for _ in range(limits["max_preimage_steps"]):
            if not pending:
                break
            value, target = pending.pop(0)
            if isinstance(value, DerivedValue):
                pending.extend(inverse_targets(value, target)[: limits["max_preimage_choices"]])
            elif isinstance(value, BoundValue) and value.path and (native(value) is None or type(native(value)) is type(target)):
                try:
                    if replay(self.expression, value.path, target, limits=limits) not in self.outputs:
                        continue
                except UnsupportedTransformation:
                    continue
                path = "$." + ".".join(value.path)
                if target not in proposals.setdefault(path, []):
                    proposals[path].append(target)
        return proposals
