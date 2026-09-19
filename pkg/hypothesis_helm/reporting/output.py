"""
Stream rendered documents independently of pytest capture and console reports.
"""

import fcntl
import json
import os
from contextlib import ExitStack
from contextvars import ContextVar

from hypothesis_helm.charts import yamlio

MANIFEST_FD: ContextVar[int | None] = ContextVar("manifest_fd", default=None)
MANIFEST_FORMAT: ContextVar[str | None] = ContextVar("manifest_format", default=None)


def manifest_format() -> str:
    """
    Resolve the coordinator's selected serialization in this process or an inherited worker.

    Returns:
        str: JSON lines by default, or YAML documents when explicitly selected.
    """
    return MANIFEST_FORMAT.get() or os.environ.get("HYPOTHESIS_HELM_MANIFEST_FORMAT", "json")


def emit_manifest(resource: object) -> None:
    """
    Write and flush one complete JSON line or YAML document to the manifest descriptor.

    Args:
        resource (object): Parsed Helm document, including structurally invalid resources.

    Returns:
        None: One complete resource is written immediately when output is enabled.
    """
    descriptor = MANIFEST_FD.get()
    if descriptor is None:
        inherited = os.environ.get("HYPOTHESIS_HELM_MANIFEST_FD")
        if inherited is None:
            return
        descriptor = int(inherited)
    text = (
        "---\n" + yamlio.dump(resource) if manifest_format() == "yaml" else json.dumps(resource, ensure_ascii=True, allow_nan=False) + "\n"
    )
    payload = text.encode()
    with ExitStack() as stack:
        lock_path = os.environ.get("HYPOTHESIS_HELM_MANIFEST_LOCK")
        if lock_path is not None:
            lock = stack.enter_context(open(lock_path, "rb"))
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        while payload:
            written = os.write(descriptor, payload)
            payload = payload[written:]
