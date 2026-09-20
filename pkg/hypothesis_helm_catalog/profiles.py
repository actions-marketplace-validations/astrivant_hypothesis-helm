"""
Expose primitive domains generated from the pinned Kubernetes validators.
"""

import copy
import json
from functools import lru_cache
from pathlib import Path

__all__ = ("schema",)


@lru_cache(maxsize=1)
def _profiles() -> dict[str, dict[str, object]]:
    """
    Read the generated primitive domains without importing the compiler or builder.

    Returns:
        dict[str, dict[str, object]]: Immutable-by-convention source records.
    """
    document = json.loads((Path(__file__).with_name("data") / "input-domains.json").read_text())
    profiles: dict[str, dict[str, object]] = document["upstream"]["profiles"]
    return profiles


def schema(name: str) -> dict[str, object]:
    """
    Return a detached generated schema for an explicitly named input role.

    Args:
        name (str): Primitive profile exported by the upstream Go extractor.

    Returns:
        dict[str, object]: Portable generation contract.
    """
    value = _profiles()[name]["schema"]
    if not isinstance(value, dict):
        raise ValueError(f"Invalid bundled profile: {name}")
    return copy.deepcopy(value)
