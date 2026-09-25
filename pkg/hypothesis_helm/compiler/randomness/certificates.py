"""
Retain native certificate observations for stable retries and exact failure replay.
"""

import copy
import hashlib
import json
import threading

from hypothesis_helm.compiler.constants import CERTIFICATES
from hypothesis_helm.exceptions.rendering import RandomInputUnavailable

__all__ = ("CERTIFICATE_FUNCTIONS", "CertificateInputs", "CertificateStore")

CERTIFICATE_FUNCTIONS = CERTIFICATES | {"genPrivateKey"}
_STORE_LOCK = threading.Lock()


def _encoded(value: object) -> bytes:
    """
    Serialize observation identities consistently across JSON transports.

    Args:
        value (object): Native arguments, result or context.

    Returns:
        bytes: Canonical UTF-8 JSON with integer precision preserved.
    """
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode()


class CertificateStore:
    """
    Own a bounded chart-run cache without evicting observations needed by shrinking.

    Attributes:
        records (dict[str, dict[str, object]]): Call identities and their frozen native outcomes.
        size (int): Encoded bytes retained by this chart instance.
    """

    records: dict[str, dict[str, object]]
    size: int

    def __init__(self) -> None:
        """
        Start an empty, pickleable cache for one prepared chart and its worker copies.
        """
        self.records: dict[str, dict[str, object]] = {}
        self.size = 0

    def get(self, key: str) -> dict[str, object] | None:
        """
        Read a detached observation without exposing mutable cache entries.

        Args:
            key (str): Context and native-call digest.

        Returns:
            dict[str, object] | None: Previously observed result, when present.
        """
        with _STORE_LOCK:
            return copy.deepcopy(self.records.get(key))

    def retain(self, key: str, record: dict[str, object], max_bytes: int, max_calls: int) -> dict[str, object]:
        """
        Publish one stable result even when concurrent renders first reach the same call.

        Args:
            key (str): Context and native-call digest.
            record (dict[str, object]): Newly observed result and its integrity digest.
            max_bytes (int): Chart-scoped compiler byte budget.
            max_calls (int): Chart-scoped compiler invocation budget.

        Returns:
            dict[str, object]: Winning observation, shared by every retry in this chart run.

        Raises:
            RandomInputUnavailable: Retention would exceed configured limits.
        """
        with _STORE_LOCK:
            if key not in self.records:
                size = len(_encoded(record))
                if self.size + size > max_bytes or len(self.records) >= max_calls:
                    # Eviction would silently change a retry's key material and make shrinking flaky.
                    raise RandomInputUnavailable("Certificate recording exceeds compiler.max_context_bytes or compiler.max_steps")
                self.records[key] = copy.deepcopy(record)
                self.size += size
            return copy.deepcopy(self.records[key])


class CertificateInputs:
    """
    Coordinate native generation, acknowledgment and replay for one render.
    """

    def __init__(self, store: CertificateStore, context: dict[str, object], max_bytes: int, max_calls: int) -> None:
        """
        Scope observations to renderer identity, chart source and release context.

        Args:
            store (CertificateStore): Prepared chart's retained observations.
            context (dict[str, object]): Verified renderer context, including source hashes.
            max_bytes (int): Maximum retained native argument/result bytes.
            max_calls (int): Maximum retained distinct calls.
        """
        self.store = store
        # Unrelated values changes must not regenerate the same native call during shrinking.
        self.context = {key: value for key, value in context.items() if key != "values_digest"}
        self.max_bytes = max_bytes
        self.max_calls = max_calls
        self.pending: dict[str, object] | None = None

    def exchange(self, request: dict[str, object], replay: dict[str, object] | None) -> dict[str, object]:
        """
        Request native generation once or return a verified recorded result.

        Args:
            request (dict[str, object]): Typed call identity, optionally followed by its native result.
            replay (dict[str, object] | None): Next record from an explicit replay tape.

        Returns:
            dict[str, object]: Generation instruction or acknowledged native observation.

        Raises:
            RandomInputUnavailable: Protocol, identity, integrity or size checks fail.
        """
        identity = {key: request.get(key) for key in ("path", "function", "arguments")}
        if identity["function"] not in CERTIFICATE_FUNCTIONS or not isinstance(identity["arguments"], list):
            raise RandomInputUnavailable("Unknown certificate generator or invalid native arguments")
        key = hashlib.sha256(_encoded([self.context, identity])).hexdigest()
        if "result" in request:
            if replay is not None or self.pending != identity:
                raise RandomInputUnavailable("Unexpected native certificate observation")
            self.pending = None
            observed = {**identity, "result": request["result"], "error": request.get("error", "")}
            observed["checksum"] = hashlib.sha256(_encoded(observed)).hexdigest()
            self._verify(observed, identity)
            return self.store.retain(key, observed, self.max_bytes, self.max_calls)
        if self.pending is not None:
            raise RandomInputUnavailable("Certificate generator did not finish its preceding observation")
        record = replay if replay is not None else self.store.get(key)
        if record is not None:
            self._verify(record, identity)
            return copy.deepcopy(record)
        if len(_encoded(identity)) > self.max_bytes:
            raise RandomInputUnavailable("Certificate arguments exceed compiler.max_context_bytes")
        self.pending = identity
        return {**identity, "generate": True}

    def _verify(self, record: dict[str, object], identity: dict[str, object]) -> None:
        """
        Reject mismatched arguments or damaged tapes before returning material to Helm.

        Args:
            record (dict[str, object]): Claimed native observation.
            identity (dict[str, object]): Currently executing typed call.

        Returns:
            None: Record identity, native shape and integrity are consistent.

        Raises:
            RandomInputUnavailable: A record cannot reproduce this call.
        """
        content = {key: value for key, value in record.items() if key != "checksum"}
        if any(record.get(key) != value for key, value in identity.items()):
            raise RandomInputUnavailable(f"Certificate replay diverged at {identity['path']}")
        if record.get("checksum") != hashlib.sha256(_encoded(content)).hexdigest():
            raise RandomInputUnavailable("Certificate replay checksum mismatch")
        result = record.get("result")
        valid = (
            isinstance(result, str)
            if identity["function"] == "genPrivateKey"
            else isinstance(result, dict) and set(result) == {"Cert", "Key"} and all(isinstance(value, str) for value in result.values())
        )
        if not valid or not isinstance(record.get("error"), str) or len(_encoded(record)) > self.max_bytes:
            raise RandomInputUnavailable("Certificate replay has an invalid result or exceeds compiler.max_context_bytes")
