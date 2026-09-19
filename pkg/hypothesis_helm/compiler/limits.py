"""
Resolve bounded compiler analysis independently of Helm's rendering limits.
"""

DEFAULT_CALL_DEPTH = 16


def compiler_limits(raw: object, *, max_call_depth: int | None = None) -> dict[str, int]:
    """
    Validate compiler settings and apply an explicit command-line override.

    Args:
        raw (object): Compiler configuration mapping.
        max_call_depth (int | None): Explicit override for nested helper calls.

    Returns:
        dict[str, int]: Complete compiler limits suitable for worker serialization.
    """
    if not isinstance(raw, dict) or set(raw) - {"max_call_depth"}:
        raise ValueError("compiler accepts a mapping containing only max_call_depth")
    configured = raw.get("max_call_depth", DEFAULT_CALL_DEPTH)
    for value in (configured, max_call_depth if max_call_depth is not None else configured):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError("compiler.max_call_depth (--compiler-call-depth) must be a positive integer")
    return {"max_call_depth": max_call_depth if max_call_depth is not None else int(configured)}


def call_depth() -> int:
    """
    Read the coordinator's compiler budget when building a chart analysis.

    Returns:
        int: Maximum nested helper calls, shared by rejection and destination analysis.
    """
    from hypothesis_helm.schemas.policy import inherited_policy

    return compiler_limits(inherited_policy().get("compiler", {}))["max_call_depth"]
