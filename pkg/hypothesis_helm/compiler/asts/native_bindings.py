"""
Reconstruct concrete Go operands while keeping all caller-provided text in data files.
"""

from __future__ import annotations

import json

from hypothesis_helm.compiler.asts.contract_values import (
    BoundValue,
    ContractText,
    DerivedValue,
    NativeValue,
    NilMap,
    NilSlice,
    UnorderedKeys,
    native,
)
from hypothesis_helm.compiler.constants import INTEGER_RESULTS, MAX_INTEGER, MIN_INTEGER, NATIVE_RECORD_FIELDS
from hypothesis_helm.exceptions.compiler import Unavailable

__all__ = ("bind_operands", "contains_native")


def contains_native(arguments: list[object], limits: dict[str, int]) -> bool:
    """
    Detect typed intermediates before a Python handler erases their native identity.

    Args:
        arguments (list[object]): Operands, including nested containers and derived selectors.
        limits (dict[str, int]): Bound the traversal of shared or cyclic structures.

    Returns:
        bool: At least one operand requires native type handling.
    """
    pending = list(arguments)
    seen: set[int] = set()
    while pending:
        value = pending.pop()
        if isinstance(value, NativeValue):
            return True
        if id(value) in seen:
            continue
        seen.add(id(value))
        if len(seen) > limits["max_range_items"]:
            # Admission will diagnose the excessive operand tree before execution.
            return True
        if isinstance(value, DerivedValue):
            pending.extend(value.arguments)
        value = native(value)
        if isinstance(value, dict):
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
    return False


def bind_operands(arguments: list[object], limits: dict[str, int], *, formatting: bool = False) -> tuple[str, tuple[str, ...]]:
    """
    Bind operands as data while reconstructing typed nils that JSON alone cannot preserve.

    Args:
        arguments (list[object]): Already bounded operands with provenance and nil markers.
        limits (dict[str, int]): Compiler data bounds.
        formatting (bool): Preserve numeric Go kinds rather than round-tripping all numbers as chart values.

    Returns:
        tuple[str, tuple[str, ...]]: JSON payload and fixed data-access expressions.
    """
    from hypothesis_helm.compiler.asts.native_operations import plain

    values: list[object] = []

    def bind(value: object, numeric_kind: str = "int") -> str:
        """
        Construct containers from fixed syntax; all caller-provided text stays in the values file.

        Args:
            value (object): Bounded operand or nested element.
            numeric_kind (str): Numeric origin inherited by nested chart values or literal containers.

        Returns:
            str: An adapter expression using only fixed constructors and integer data indexes.
        """
        literal_number = type(value) in {int, float} and numeric_kind == "int"
        if isinstance(value, NativeValue):
            # A replay captures the original operands, not mutable references to
            # inputs. Never replay an obsolete result after a local map write.
            if json.dumps(plain(value, limits), sort_keys=True) != value.snapshot:
                raise Unavailable("native result was mutated; its original Go type recipe is no longer valid")
            position = len(values)
            values.append(json.loads(value.payload)["arguments"])
            return "(" + value.source.replace(".Values.arguments", f"(index .Values.arguments {position})") + ")"
        if isinstance(value, DerivedValue) and value.function in {"_field", "_get", "_index"}:
            receiver, key = value.arguments
            if isinstance(receiver, NativeValue):
                target = bind(receiver)
                if receiver.go_kind in {"struct", "ptr"} and isinstance(key, str) and key in NATIVE_RECORD_FIELDS:
                    return f"({target}.{key})"
                return f"(index {target} {bind(key)})"
        if formatting:
            if isinstance(value, ContractText | UnorderedKeys):
                raise Unavailable("native formatting cannot fix an unordered result to one sampled order")
            if isinstance(value, BoundValue):
                numeric_kind = "values"
            elif isinstance(value, DerivedValue):
                if value.function in INTEGER_RESULTS:
                    numeric_kind = "int" if value.function in {"int", "atoi"} else "int64"
                elif value.function == "fromJson":
                    numeric_kind = "float64"
                else:
                    # Text and Boolean results keep their type; numeric leaves of
                    # other transformations need their own reconstruction contract.
                    numeric_kind = "unknown"
        # Reject symbolic wrappers before native() can select a representative order.
        inspected = value
        while isinstance(inspected, BoundValue | DerivedValue):
            inspected = inspected.value
        if isinstance(inspected, ContractText | UnorderedKeys):
            raise Unavailable("native operands contain unresolved ordering")
        value = native(value)
        if isinstance(value, NilSlice):
            return "(concat)"
        if isinstance(value, NilMap):
            return '(fromJson "null")'
        if isinstance(value, dict):
            entries = " ".join(bind(key, numeric_kind) + " " + bind(item, numeric_kind) for key, item in value.items())
            return "(dict" + (" " + entries if entries else "") + ")"
        if isinstance(value, list):
            entries = " ".join(bind(item, numeric_kind) for item in value)
            return "(list" + (" " + entries if entries else "") + ")"
        index = len(values)
        values.append(plain(value, limits))
        access = f"(index .Values.arguments {index})"
        if formatting and isinstance(value, int | float) and not isinstance(value, bool) and numeric_kind != "values":
            if type(value) is float and numeric_kind == "int":
                numeric_kind = "float64"
            if numeric_kind == "unknown":
                raise Unavailable("native formatting requires a known Go numeric type for transformed operands")
            if numeric_kind in {"int", "int64"} and not MIN_INTEGER <= value <= MAX_INTEGER:
                raise Unavailable("native formatting integer exceeds the supported Go integer range")
            if literal_number:
                # Untyped template constants adapt to the callee's formal type
                # (for example derivePassword's uint32). An int cast does not.
                return repr(value)
            return f"({numeric_kind} {access})"
        return access

    operands = tuple(bind(value) for value in arguments)
    return json.dumps({"arguments": values}, ensure_ascii=False, allow_nan=False), operands
