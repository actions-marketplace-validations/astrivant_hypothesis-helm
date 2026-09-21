"""
Evaluate bounded regex and serialization operations with the selected Helm's Go libraries.
"""

from __future__ import annotations

import base64
import json
import math
import shutil
import tempfile
from functools import lru_cache
from pathlib import Path
from textwrap import dedent

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.contract_values import NilMap, NilSlice, native
from hypothesis_helm.compiler.constants import NATIVE_OPERATIONS
from hypothesis_helm.exceptions.compiler import Unavailable
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("evaluate", "plain", "probe")


def plain(value: object, limits: dict[str, int]) -> object:
    """
    Copy concrete data for a native probe without discarding provenance in the evaluator.

    Args:
        value (object): Value containing optional compiler wrappers.
        limits (dict[str, int]): Bounds on inspected nodes, nesting and text.

    Returns:
        object: An acyclic JSON-compatible copy.

    Raises:
        Unavailable: A value is not concrete, exceeds a budget or contains a cycle.
    """
    remaining = limits["max_range_items"]
    ancestors: set[int] = set()

    def visit(item: object, depth: int) -> object:
        """
        Unwrap one value while accounting for the entire probe payload.

        Args:
            item (object): Current node.
            depth (int): Container nesting from the argument root.

        Returns:
            object: Concrete node copied without shared mutable state.
        """
        nonlocal remaining
        remaining -= 1
        if remaining < 0 or depth > limits["max_call_depth"]:
            raise Unavailable("native operands exceed compiler.max_range_items or compiler.max_call_depth")
        item = native(item)
        if isinstance(item, NilMap | NilSlice):
            return None
        if isinstance(item, str) and len(item) > limits["max_string_chars"]:
            raise Unavailable("native operand exceeds compiler.max_string_chars")
        if item is None or isinstance(item, str | bool | int):
            return item
        if isinstance(item, float) and math.isfinite(item):
            return item
        if not isinstance(item, dict | list) or id(item) in ancestors:
            raise Unavailable("native operands require acyclic concrete JSON values")
        ancestors.add(id(item))
        try:
            if isinstance(item, list):
                return [visit(child, depth + 1) for child in item]
            if not all(isinstance(key, str) for key in item):
                raise Unavailable("native operand maps require string keys")
            if any(len(key) > limits["max_string_chars"] for key in item):
                raise Unavailable("native map key exceeds compiler.max_string_chars")
            return {str(key): visit(child, depth + 1) for key, child in item.items()}
        finally:
            ancestors.remove(id(item))

    return visit(value, 0)


@lru_cache(maxsize=128)
def probe(binary: str, stamp: int, timeout: float, operation: str, payload: str, max_chars: int, operands: tuple[str, ...]) -> object:
    """
    Run a fixed function call in Helm, keyed by executable identity, operands and budget.

    Args:
        binary (str): Resolved Helm executable used for the real render.
        stamp (int): Executable modification timestamp, invalidating old cached results.
        timeout (float): Invocation deadline including native regex execution.
        operation (str): Explicitly admitted function name.
        payload (str): Arguments encoded as JSON data, never template source.
        max_chars (int): Maximum serialized result before returning it through stdout.
        operands (tuple[str, ...]): Fixed adapter expressions preserving typed nil containers.

    Returns:
        object: Go-evaluated result, or an explicit unavailable-analysis error.
    """
    call = operation + " " + " ".join(operands)
    # Preserve decoded bytes across JSON transport. Invalid UTF-8 must become
    # unknown rather than silently replacing bytes and changing later checksums.
    transport = " | b64enc" if operation == "b64dec" else ""
    with tempfile.TemporaryDirectory(prefix="helm-function-") as temporary:
        root = Path(temporary)
        (root / "templates").mkdir()
        (root / "Chart.yaml").write_text(
            dedent("""
            apiVersion: v2
            name: function-probe
            version: 0.1.0
            """)
        )
        (root / "values.json").write_text(payload)
        (root / "templates/result.yaml").write_text(
            dedent(f"""
            {{{{- $value := {call}{transport} -}}}}
            {{{{- $result := $value | toJson -}}}}
            {{{{- if gt (len $result) {max_chars} -}}}}
            {{{{- fail "native result exceeds compiler.max_string_chars" -}}}}
            {{{{- end }}}}
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: function-probe
            data:
              result: {{{{ $result | quote }}}}
              kind: {{{{ $value | kindOf | quote }}}}
            """)
        )
        result = Processes().run(
            [binary, "template", "function-probe", str(root), "--values", str(root / "values.json")],
            capture_output=True,
            timeout=timeout,
        )
        if result.returncode:
            raise Unavailable(f"native Helm {operation} evaluation failed or exceeded compiler.max_string_chars")
        documents = [mapping(item) for item in yamlio.load_all(result.stdout) if item is not None]
        if len(documents) != 1:
            raise Unavailable("native function returned an unexpected document")
        data = mapping(documents[0]["data"])
        decoded = json.loads(str(data["result"]))
        if decoded is None and data["kind"] in {"map", "slice"}:
            return NilMap() if data["kind"] == "map" else NilSlice()
        if operation == "b64dec":
            try:
                return base64.b64decode(str(decoded), validate=True).decode("utf-8")
            except UnicodeError as exc:
                raise Unavailable("Base64 result contains non-UTF-8 bytes; retain native Helm evaluation") from exc
        return decoded


def _bind(arguments: list[object], limits: dict[str, int]) -> tuple[str, tuple[str, ...]]:
    """
    Bind operands as data while reconstructing typed nils that JSON alone cannot preserve.

    Args:
        arguments (list[object]): Already bounded operands with provenance and nil markers.
        limits (dict[str, int]): Compiler data bounds.

    Returns:
        tuple[str, tuple[str, ...]]: JSON payload and fixed data-access expressions.
    """
    values: list[object] = []

    def bind(value: object) -> str:
        """
        Construct containers from fixed syntax; all caller-provided text stays in the values file.

        Args:
            value (object): Bounded operand or nested element.

        Returns:
            str: An adapter expression using only fixed constructors and integer data indexes.
        """
        value = native(value)
        if isinstance(value, NilSlice):
            return "(concat)"
        if isinstance(value, NilMap):
            return '(fromJson "null")'
        if isinstance(value, dict):
            entries = " ".join(bind(key) + " " + bind(item) for key, item in value.items())
            return "(dict" + (" " + entries if entries else "") + ")"
        if isinstance(value, list):
            entries = " ".join(bind(item) for item in value)
            return "(list" + (" " + entries if entries else "") + ")"
        index = len(values)
        values.append(plain(value, limits))
        return f"(index .Values.arguments {index})"

    operands = tuple(bind(value) for value in arguments)
    return json.dumps({"arguments": values}, ensure_ascii=False, allow_nan=False), operands


def evaluate(function: str, arguments: list[object], *, helm: str, timeout: float, limits: dict[str, int]) -> object:
    """
    Admit bounded inputs before invoking Go's regex engine or Helm's serializers.

    Args:
        function (str): Supported deterministic native operation.
        arguments (list[object]): Evaluated operands with their provenance intact.
        helm (str): Renderer executable selected by the executor.
        timeout (float): Same per-invocation deadline as native rendering.
        limits (dict[str, int]): Captured compiler limits for this chart.

    Returns:
        object: Concrete native result with no mutable cache objects shared with a candidate.

    Raises:
        Unavailable: Operands or worst-case output exceed a budget, or Helm is unavailable.
    """
    if function not in NATIVE_OPERATIONS or len(arguments) != NATIVE_OPERATIONS[function]:
        raise Unavailable("unsupported native operation or operand count")
    args = [plain(value, limits) for value in arguments]
    if "Regex" in function or function.startswith("regex"):
        if not all(isinstance(value, str) for value in args):
            raise Unavailable("native regex requires string operands")
        pattern, subject = str(args[0]), str(args[1])
        if len(pattern) > limits["max_regex_pattern_chars"] or len(subject) > limits["max_regex_subject_chars"]:
            raise Unavailable("regex exceeds compiler.max_regex_pattern_chars or compiler.max_regex_subject_chars")
        if len(args) == 3:
            replacement = str(args[2])
            # Empty matches can insert once at every boundary; a capture expansion
            # can repeat the entire subject. Bound allocation before calling Go.
            expansion = len(replacement) * (max(1, len(subject)) if "$" in replacement and "Literal" not in function else 1)
            if len(subject) + (len(subject) + 1) * expansion > limits["max_string_chars"]:
                raise Unavailable("regex replacement may exceed compiler.max_string_chars")
    if function in {"fromYaml", "fromJson", "b64dec"} and not isinstance(args[0], str):
        raise Unavailable("native deserialization requires a string")
    payload, operands = _bind(arguments, limits)
    if len(payload.encode()) + sum(map(len, operands)) > min(limits["max_context_bytes"], limits["max_string_chars"]):
        raise Unavailable("native operand payload exceeds compiler.max_context_bytes or compiler.max_string_chars")
    binary = shutil.which(helm)
    if binary is None:
        raise Unavailable("Helm is unavailable for native function evaluation")
    result = probe(binary, Path(binary).stat().st_mtime_ns, timeout, function, payload, limits["max_string_chars"], operands)
    # Deserialized maps can be mutated locally; never return the cached instance.
    if isinstance(result, NilMap | NilSlice):
        return type(result)()
    return plain(result, limits)
