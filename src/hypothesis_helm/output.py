"""
Stream rendered documents independently of pytest capture and console reports.
"""

import fcntl
import json
import os
from contextlib import ExitStack
from contextvars import ContextVar

MANIFEST_FD: ContextVar[int | None] = ContextVar("manifest_fd", default=None)


def emit_manifest(resource: object) -> None:
    """
    Write and flush one compact JSON document to the selected manifest descriptor.

    Args:
        resource (object): Parsed Helm document, including structurally invalid resources.

    Returns:
        None: A complete JSON line is written immediately when output is enabled.
    """
    descriptor = MANIFEST_FD.get()
    if descriptor is None:
        inherited = os.environ.get("HYPOTHESIS_HELM_MANIFEST_FD")
        if inherited is None:
            return
        descriptor = int(inherited)
    payload = (json.dumps(resource, ensure_ascii=True, allow_nan=False) + "\n").encode()
    with ExitStack() as stack:
        lock_path = os.environ.get("HYPOTHESIS_HELM_MANIFEST_LOCK")
        if lock_path is not None:
            lock = stack.enter_context(open(lock_path, "rb"))
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        while payload:
            written = os.write(descriptor, payload)
            payload = payload[written:]
