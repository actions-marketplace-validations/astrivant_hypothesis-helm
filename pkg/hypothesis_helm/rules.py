"""
Stable built-in check identifiers and an inherited, explicit ignore policy.
"""

import json
import logging
from pathlib import Path

from hypothesis_helm.environment import env
from hypothesis_helm.exceptions.rendering import RenderFailure
from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.findings.policy import ACTIVE_CODES, chart_rules, resolve_codes
from hypothesis_helm.schemas.configuration.policy import configuration, inherited_policy
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = (
    "AUDIT_RULES",
    "ENVIRONMENT",
    "RULES",
    "check",
    "effective_ignored_codes",
    "ignored",
    "ignored_codes",
    "load_codes",
    "load_ignored",
    "may_check",
    "record_ignored",
)


ENVIRONMENT = "HYPOTHESIS_HELM_IGNORED_RULES"
LOGGER = logging.getLogger(__name__)
RULES = {code: rule.title for code, rule in CATALOG.items()}
AUDIT_RULES = {
    "undocumented": "HH2001",
    "untyped": "HH2002",
    "missing-description": "HH2003",
    "no-default": "HH2004",
    "opaque-object": "HH2006",
}


def load_ignored(config: Path | None, codes: list[str]) -> list[str]:
    """
    Combine an explicit or working-directory YAML policy with command-line codes.

    Args:
        config (Path | None): Explicit file, or discover .hypothesis-helm.yaml in the working directory.
        codes (list[str]): Additional stable identifiers, checked for spelling mistakes.

    Returns:
        list[str]: Sorted unique identifiers; invalid policies raise ValueError.
    """
    path = config or Path(".hypothesis-helm.yaml")
    configured = configuration(config).get("ignored", []) or []
    if not isinstance(configured, list) or any(not isinstance(code, str) for code in configured):
        raise ValueError(f"{path}: 'ignored' must be a list of rule codes")
    result = sorted(set([*configured, *codes]))
    unknown = [code for code in result if code not in RULES]
    if unknown:
        raise ValueError(f"Unknown rule codes: {', '.join(unknown)}; run 'helm hypothesis rules'")
    return result


def ignored_codes() -> list[str]:
    """
    Read the CLI-resolved policy inherited unchanged by subprocess workers.

    Returns:
        list[str]: Active ignored rule identifiers.
    """
    return load_codes(env.get(ENVIRONMENT, "[]"))


def load_codes(value: str) -> list[str]:
    """
    Validate serialized policy before it can disable a check.

    Args:
        value (str): JSON-encoded identifiers supplied by the coordinator.

    Returns:
        list[str]: Valid identifiers, or a ValueError for malformed policy.
    """
    codes = json.loads(value)
    if not isinstance(codes, list) or any(not isinstance(code, str) or code not in RULES for code in codes):
        raise ValueError("Invalid inherited ignored-rule policy")
    return sorted(set(codes))


def ignored(code: str, *, chart: Path | None = None, paths: tuple[tuple[str | int, ...], ...] = ()) -> bool:
    """
    Check whether an explicitly identified built-in rule is disabled.

    Args:
        code (str): Stable built-in rule identifier.
        chart (Path | None): Explicit chart for a path-level audit finding.
        paths (tuple[tuple[str | int, ...], ...]): Finding paths; omitted for chart-wide observations.

    Returns:
        bool: Whether the current policy disables this check.
    """
    if chart is not None:
        return code in resolve_codes(chart_rules(chart), paths, ignored_codes())
    return code in effective_ignored_codes()


def effective_ignored_codes() -> list[str]:
    """
    Include candidate overrides in validation and exact-equivalence cache identities.

    Returns:
        list[str]: Resolved disabled checks, or the global policy outside candidate evaluation.
    """
    active = ACTIVE_CODES.get()
    return sorted(active) if active is not None else ignored_codes()


def may_check(code: str) -> bool:
    """
    Prepare optional validators when any branch can enable their checks.

    Args:
        code (str): Check whose external tooling may be needed.

    Returns:
        bool: Whether the global or a branch policy allows this check to execute.
    """
    return code not in ignored_codes() or any(
        code in sequence(mapping(rule).get("enabled", [])) for rule in sequence(inherited_policy().get("input_constraints", []))
    )


def record_ignored(code: str, message: str) -> None:
    """
    Expose skipped checks in diagnostics without emitting manifest output.

    Args:
        code (str): Disabled rule identifier.
        message (str): Reason the check could not pass.

    Returns:
        None: Emit an informational diagnostic.
    """
    LOGGER.info("[%s] Ignored: %s", code, message)


def check(condition: bool, code: str, message: str) -> None:
    """
    Enforce one independent check without skipping subsequent enabled checks.

    Args:
        condition (bool): Whether the checked requirement holds.
        code (str): Stable identifier.
        message (str): Failure diagnostic.

    Returns:
        None: Continue on success or explicit opt-out; otherwise raise RenderFailure.
    """
    if condition:
        return
    if ignored(code):
        record_ignored(code, message)
        return
    raise RenderFailure(message, code)
