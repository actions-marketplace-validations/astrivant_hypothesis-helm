"""
Resolve bounded compiler analysis independently of Helm's rendering limits.
"""

import json
import os
from functools import lru_cache

# Resource budgets only. Language semantics, numeric precision and proof requirements
# are not configurable: changing those would change what the analysis can establish.
LIMITS: dict[str, tuple[int, str]] = {
    "max_call_depth": (16, "Nested helper/tpl calls; --compiler-call-depth overrides this."),
    "max_files": (10000, "Members inspected per chart archive, including directories."),
    "max_context_bytes": (64 * 1024 * 1024, "Packed archive bytes and total unpacked member bytes, per archive."),
    "max_template_bytes": (1024 * 1024, "UTF-8 bytes in each dynamically analyzed tpl source."),
    "max_steps": (10000, "Statements and range iterations per root rejection evaluation."),
    "max_discovery_nodes": (10000, "Actions per discovery traversal or nodes per helper projection."),
    "max_tpl_depth": (32, "Nested tpl expansions during value-path discovery."),
    "max_range_items": (4096, "Elements in a collection evaluated by a range."),
    "max_dependency_depth": (16, "Dependency nesting inspected from the root chart."),
    "max_dependencies": (512, "Dependency instances inspected per chart."),
    "max_version_chars": (4096, "Combined characters in a semantic-version constraint and version."),
    "max_string_chars": (16384, "Characters in a transformation operand or replacement result."),
    "max_regex_pattern_chars": (256, "Characters in an analyzed ASCII regex pattern."),
    "max_regex_subject_chars": (4096, "Characters in an analyzed ASCII regex subject."),
    "max_symbolic_variants": (64, "Branch variants per destination projection."),
    "max_indent_width": (128, "Spaces in a projected indent/nindent operation."),
    "max_proof_bytes": (16 * 1024 * 1024, "Chart bytes retained for an exact-pruning proof snapshot."),
    "max_output_nodes": (100000, "Manifest nodes inspected per complexity measurement."),
    "max_complexity_cases": (4096, "Template assignments and witnesses in a complexity search."),
    "max_complexity_seconds": (5, "Whole seconds allowed for a complexity search."),
    "max_sampling_domain_values": (4096, "Values per factor when computing a sampling profile."),
    "max_fallbacks": (128, "Distinct incomplete-analysis diagnostics retained per chart."),
    "max_preimage_steps": (128, "Search steps when proposing inputs for a transformed allowlist."),
    "max_preimage_choices": (16, "Targets and proposals per transformed-allowlist search step."),
    "max_rejections": (64, "Distinct rejection contracts used to guide generation."),
    "max_repair_attempts": (48, "Candidate changes tried for a rejected configuration."),
    "max_repair_branch_attempts": (16, "Candidate changes tried at one repair search node."),
    "max_repair_depth": (3, "Successive changes considered along a repair search branch."),
    "max_repair_length": (16, "Largest proposed list length during rejection repair."),
}
DEFAULT_LIMITS = {name: default for name, (default, _) in LIMITS.items()}
DEFAULT_CALL_DEPTH = DEFAULT_LIMITS["max_call_depth"]


def compiler_limits(raw: object, *, max_call_depth: int | None = None) -> dict[str, int]:
    """
    Validate compiler settings and apply an explicit command-line override.

    Args:
        raw (object): Partial compiler configuration mapping.
        max_call_depth (int | None): Explicit override for nested helper calls.

    Returns:
        dict[str, int]: Complete compiler limits suitable for worker serialization.
    """
    if not isinstance(raw, dict):
        raise ValueError("compiler must be a mapping of analysis budgets")
    unknown = set(raw) - DEFAULT_LIMITS.keys()
    if unknown:
        raise ValueError("Unknown compiler setting(s): " + ", ".join(sorted(str(key) for key in unknown)))
    resolved = dict(DEFAULT_LIMITS)
    for name, value in raw.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"compiler.{name} must be a positive integer")
        resolved[name] = value
    if max_call_depth is not None:
        if isinstance(max_call_depth, bool) or not isinstance(max_call_depth, int) or max_call_depth < 1:
            raise ValueError("compiler.max_call_depth (--compiler-call-depth) must be a positive integer")
        resolved["max_call_depth"] = max_call_depth
    return resolved


@lru_cache(maxsize=32)
def policy_limits(serialized: str) -> tuple[tuple[str, int], ...]:
    """
    Cache validated limits by the complete inherited policy, never by chart or process alone.

    Args:
        serialized (str): Coordinator policy serialized for worker inheritance.

    Returns:
        tuple[tuple[str, int], ...]: Immutable entries safe to reuse across analysis calls.
    """
    from hypothesis_helm.schemas.contracts import mapping

    return tuple(compiler_limits(mapping(json.loads(serialized)).get("compiler", {})).items())


def active_limits() -> dict[str, int]:
    """
    Snapshot the coordinator's compiler budgets when building an analysis.

    Returns:
        dict[str, int]: Detached validated settings, also available in spawned workers.
    """
    from hypothesis_helm.schemas.policy import ENVIRONMENT

    return dict(policy_limits(os.environ.get(ENVIRONMENT, "{}")))


def call_depth() -> int:
    """
    Read the coordinator's nested-call budget when building a chart analysis.

    Returns:
        int: Maximum nested helper calls, shared by rejection and destination analysis.
    """
    return active_limits()["max_call_depth"]
