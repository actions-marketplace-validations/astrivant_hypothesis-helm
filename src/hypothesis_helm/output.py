"""
Stream rendered documents independently of pytest capture and console reports.
"""

import json
import os
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
    while payload:
        written = os.write(descriptor, payload)
        payload = payload[written:]
