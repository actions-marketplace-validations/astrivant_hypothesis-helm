"""
Publish complete worker evidence before shrinking or cancellation can interrupt it.
"""

import os
from pathlib import Path

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.execution.runtime.signals import DeferredSignals

__all__ = ("save",)


def save(path: Path, value: dict[str, object]) -> None:
    """
    Replace one owned JSON record atomically while deferring cancellation.

    Args:
        path (Path): Destination owned by this worker or coordinator.
        value (dict[str, object]): Complete JSON-compatible evidence.

    Returns:
        None: Readers observe either the previous complete record or the new record.
    """
    with DeferredSignals():
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(f".{os.getpid()}.tmp")
        try:
            temporary.write_text(yamlio.json_for_helm(value, indent=2) + "\n", encoding="utf-8")
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
