"""
Evaluate bounded formatting, regex and serialization with the selected Helm's Go libraries.
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
from hypothesis_helm.compiler.asts.contract_values import NativeValue, NilMap, NilSlice, native
from hypothesis_helm.compiler.asts.native_bindings import bind_operands
from hypothesis_helm.compiler.asts.native_limits import admit
from hypothesis_helm.compiler.constants import NATIVE_EXTENSIONS, NATIVE_OPERATIONS, NATIVE_RECORD_FIELDS, NATIVE_TYPED_OPERATIONS
from hypothesis_helm.environment import env
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
def probe(
    binary: str, stamp: int, timeout: float, operation: str, payload: str, max_chars: int, operands: tuple[str, ...], timezone: str
) -> tuple[object, str, str]:
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
        timezone (str): Captured TZ context, invalidating cached local-date operations when it changes.

    Returns:
        tuple[object, str, str]: Go-evaluated result, reflection kind and concrete type name.
    """
    call = operation + " " + " ".join(operands)
    if operation.startswith("_nativeField:"):
        call = "(" + operands[0] + ")." + operation.split(":", 1)[1]
    # Preserve decoded bytes across JSON transport. Invalid UTF-8 must become
    # unknown rather than silently replacing bytes and changing later checksums.
    transport = " | b64enc" if operation in {"b64dec", "b32dec", "decryptAES", "substr", "trunc"} else ""
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
              type: {{{{ $value | typeOf | quote }}}}
            """)
        )
        result = Processes().run(
            [binary, "template", "function-probe", str(root), "--values", str(root / "values.json")],
            capture_output=True,
            timeout=timeout,
            env={**env, "TZ": timezone} if timezone else dict(env),
        )
        if result.returncode:
            raise Unavailable(f"native Helm {operation} evaluation failed or exceeded compiler.max_string_chars")
        documents = [mapping(item) for item in yamlio.load_all(result.stdout) if item is not None]
        if len(documents) != 1:
            raise Unavailable("native function returned an unexpected document")
        data = mapping(documents[0]["data"])
        decoded = json.loads(str(data["result"]))
        if decoded is None and data["kind"] in {"map", "slice"}:
            decoded = NilMap() if data["kind"] == "map" else NilSlice()
        if transport:
            try:
                decoded = base64.b64decode(str(decoded), validate=True).decode("utf-8")
            except UnicodeError as exc:
                raise Unavailable("Native result contains non-UTF-8 bytes; retain native Helm evaluation") from exc
        return decoded, str(data["kind"]), str(data["type"])


def evaluate(function: str, arguments: list[object], *, helm: str, timeout: float, limits: dict[str, int], typed: bool = False) -> object:
    """
    Admit bounded inputs before invoking deterministic functions in the selected Helm binary.

    Args:
        function (str): Supported deterministic native operation.
        arguments (list[object]): Evaluated operands with their provenance intact.
        helm (str): Renderer executable selected by the executor.
        timeout (float): Same per-invocation deadline as native rendering.
        limits (dict[str, int]): Captured compiler limits for this chart.
        typed (bool): Retain a replay recipe for native Go types that JSON cannot represent.

    Returns:
        object: Concrete native result with no mutable cache objects shared with a candidate.

    Raises:
        Unavailable: Operands or worst-case output exceed a budget, or Helm is unavailable.
    """
    arity = NATIVE_OPERATIONS.get(function)
    field_access = function.startswith("_nativeField:") and function.split(":", 1)[1] in NATIVE_RECORD_FIELDS
    if (
        arity is None
        and function not in NATIVE_EXTENSIONS | NATIVE_TYPED_OPERATIONS
        and not field_access
        or arity is not None
        and arity >= 0
        and len(arguments) != arity
    ):
        raise Unavailable("unsupported native operation or operand count")
    # Bound the combined argument tree, not each argument independently.
    args = plain(arguments, limits)
    assert isinstance(args, list)
    admit(function, arguments, args, limits)
    payload, operands = bind_operands(arguments, limits, formatting=True)
    if len(payload.encode()) + sum(map(len, operands)) > min(limits["max_context_bytes"], limits["max_string_chars"]):
        raise Unavailable("native operand payload exceeds compiler.max_context_bytes or compiler.max_string_chars")
    binary = shutil.which(helm)
    if binary is None:
        raise Unavailable("Helm is unavailable for native function evaluation")
    result, go_kind, go_type = probe(
        binary, Path(binary).stat().st_mtime_ns, timeout, function, payload, limits["max_string_chars"], operands, env.get("TZ", "")
    )
    # Deserialized maps can be mutated locally; never return the cached instance.
    result = type(result)() if isinstance(result, NilMap | NilSlice) else plain(result, limits)
    if not typed:
        return result
    source = function + " " + " ".join(operands)
    if field_access:
        source = "(" + operands[0] + ")." + function.split(":", 1)[1]
    return NativeValue(
        result, function, tuple(arguments), source, payload, json.dumps(plain(result, limits), sort_keys=True), go_kind, go_type
    )
