"""
Classify CI impact and resolve inherited failure thresholds independently of suppression.
"""

import re
import xml.etree.ElementTree as ET
from contextvars import ContextVar
from pathlib import Path
from typing import cast

from hypothesis_helm.findings.catalog import CATALOG, Severity
from hypothesis_helm.schemas.contracts import mapping, sequence

LEVELS = {"info": 0, "warning": 1, "error": 2}
ACTIVE_POLICY: ContextVar[dict[str, object] | None] = ContextVar("finding_severity", default=None)


def validate(value: object, *, partial: bool = False) -> dict[str, object]:
    """
    Validate a failure threshold and explicit per-code severity overrides.

    Args:
        value (object): Findings configuration containing fail_on and severity.
        partial (bool): Retain only explicitly supplied keys for branch inheritance.

    Returns:
        dict[str, object]: Normalized settings, with no threshold enabled by default.

    Raises:
        ValueError: A setting, severity or finding code is unknown.
    """
    if not isinstance(value, dict) or set(value) - {"fail_on", "severity"}:
        raise ValueError("findings accepts only fail_on and severity")
    threshold = value.get("fail_on")
    if threshold is not None and (not isinstance(threshold, str) or threshold not in LEVELS):
        raise ValueError("findings.fail_on must be null, info, warning or error")
    overrides = value.get("severity", {})
    if not isinstance(overrides, dict) or any(
        code not in CATALOG or not isinstance(level, str) or level not in LEVELS for code, level in overrides.items()
    ):
        raise ValueError("findings.severity must map known HH codes to info, warning or error")
    result: dict[str, object] = {"fail_on": threshold, "severity": dict(overrides)}
    return {key: result[key] for key in value} if partial else result


def global_policy() -> dict[str, object]:
    """
    Read the inherited base policy and whether any configured scope controls fail-fast behavior.

    Returns:
        dict[str, object]: Global findings settings with a flag identifying explicit threshold control.
    """
    from hypothesis_helm.schemas.policy import inherited_policy

    document = inherited_policy()
    result = dict(mapping(document.get("findings", {})))
    if result.get("fail_on") is not None or any(
        "fail_on" in mapping(mapping(rule).get("findings", {})) for rule in sequence(document.get("input_constraints", []))
    ):
        result["threshold_configured"] = True
    return result


def for_paths(
    chart: Path, paths: tuple[tuple[str | int, ...], ...] = (), *, rules: list[dict[str, object]] | None = None
) -> dict[str, object]:
    """
    Merge global, chart and branch settings independently, without weakening a multi-path finding.

    Args:
        chart (Path): Chart source used by the existing source/name selectors.
        paths (tuple[tuple[str | int, ...], ...]): A finding's paths or all changed paths; empty means chart defaults.
        rules (list[dict[str, object]] | None): Already selected chart rules, avoiding repeated chart metadata parsing.

    Returns:
        dict[str, object]: Effective policy, retaining separate decisions for multiple affected paths.

    Raises:
        ValueError: Equally specific rules disagree about the same setting.
    """
    from hypothesis_helm.schemas.policy import path_parts
    from hypothesis_helm.schemas.selectors import matching_rules

    base = global_policy()
    parsed = [
        (path_parts(str(rule["path"])), mapping(rule["findings"]))
        for rule in (matching_rules(chart) if rules is None else rules)
        if "findings" in rule
    ]
    branches = []
    for path in paths or ((),):
        result = {**base, "severity": dict(mapping(base.get("severity", {})))}
        selected: dict[str, tuple[int, object]] = {}
        for prefix, settings in parsed:
            if len(prefix) > len(path) or any(a != "*" and a != b for a, b in zip(prefix, path, strict=False)):
                continue
            entries = {**mapping(settings.get("severity", {})), **({"fail_on": settings["fail_on"]} if "fail_on" in settings else {})}
            for key, value in entries.items():
                previous = selected.get(key)
                if previous is not None and previous[0] == len(prefix) and previous[1] != value:
                    raise ValueError(f"Conflicting input constraints for findings.{key} at {path!r}")
                if previous is None or previous[0] <= len(prefix):
                    selected[key] = (len(prefix), value)
        for key, (_, value) in selected.items():
            if key == "fail_on":
                result[key] = value
            else:
                mapping(result["severity"])[key] = value
        branches.append(result)
    return branches[0] if len(branches) == 1 else {**base, "branches": branches}


def policy() -> dict[str, object]:
    """
    Read the resolved policy shared by the coordinator, workers and shards.

    Returns:
        dict[str, object]: Configured severity overrides and optional failure threshold.
    """
    active = ACTIVE_POLICY.get()
    return global_policy() if active is None else active


def level(code: str, *, settings: dict[str, object] | None = None) -> Severity:
    """
    Resolve a code's configured severity without changing whether its check runs.

    Args:
        code (str): Catalog code, or an uncategorized execution failure.
        settings (dict[str, object] | None): Recorded policy, otherwise the current worker's policy.

    Returns:
        Severity: Configured or catalog severity; uncategorized failures remain errors.
    """
    default = CATALOG[code].severity if code in CATALOG else "error"
    settings = policy() if settings is None else settings
    if "branches" in settings:
        return max((level(code, settings=mapping(branch)) for branch in sequence(settings["branches"])), key=LEVELS.__getitem__)
    return cast(Severity, mapping(settings.get("severity", {})).get(code, default))


def blocks(code: str, *, settings: dict[str, object] | None = None) -> bool:
    """
    Test a finding against the active failure threshold after suppression is resolved.

    Args:
        code (str): Observed code; uncategorized execution failures cannot be downgraded.
        settings (dict[str, object] | None): Recorded policy, otherwise the current worker's policy.

    Returns:
        bool: Whether the finding blocks CI; absent thresholds preserve existing behavior.
    """
    settings = policy() if settings is None else settings
    if "branches" in settings:
        return any(blocks(code, settings=mapping(branch)) for branch in sequence(settings["branches"]))
    threshold = settings.get("fail_on") or "info"
    return LEVELS[level(code, settings=settings)] >= LEVELS[str(threshold)]


def attributes(code: str, *, settings: dict[str, object] | None = None) -> dict[str, object]:
    """
    Freeze the severity decision in evidence so later aggregation need not reload configuration.

    Args:
        code (str): Observed finding code.
        settings (dict[str, object] | None): Recorded policy, otherwise the current worker's policy.

    Returns:
        dict[str, object]: Effective severity and whether this finding meets the threshold.
    """
    settings = policy() if settings is None else settings
    result: dict[str, object] = {"severity": level(code, settings=settings), "blocking": blocks(code, settings=settings)}
    if settings.get("threshold_configured"):
        branches = [mapping(branch) for branch in sequence(settings.get("branches", [settings]))]
        result["fail_fast"] = any(branch.get("fail_on") is not None and blocks(code, settings=branch) for branch in branches)
    return result


def audit_blocks(report: dict[str, object]) -> bool:
    """
    Find threshold-matching observations in an audit that has already applied suppressions.

    Args:
        report (dict[str, object]): Audit findings and unresolved references.

    Returns:
        bool: At least one unsuppressed finding meets the active threshold.
    """
    return any(
        mapping(item).get("fail_fast", mapping(item).get("blocking", blocks(str(mapping(item)["code"]))))
        for key in ("findings", "unresolved")
        for item in sequence(report.get(key, []))
    )


def junit_findings(payload: str) -> list[dict[str, object]]:
    """
    Preserve below-threshold findings reported as incomplete properties by pytest.

    Args:
        payload (str): JUnit XML from the suite's owned workers.

    Returns:
        list[dict[str, object]]: Explicit findings; unrelated skips remain ordinary skips.
    """
    from hypothesis_helm.findings.generator import FindingGenerator

    result = []
    for case in ET.fromstring(payload).iter("testcase"):
        for skipped in case.findall("skipped"):
            diagnostic = skipped.get("message", "") or skipped.text or ""
            match = re.search(r"Finding below failure threshold \[(HH\d{4})\]", diagnostic)
            if match is not None and match[1] in CATALOG:
                code = match[1]
                decision = {**attributes(code), **junit_attributes(case)}
                result.append(
                    {
                        "phase": f"{case.get('classname', '')}.{case.get('name', '')}",
                        "status": "findings",
                        "code": code,
                        "error": diagnostic,
                        "finding": FindingGenerator.create(code, diagnostic).record() | decision,
                        **decision,
                    }
                )
    return result


def junit_attributes(case: ET.Element) -> dict[str, object]:
    """
    Read the policy decision captured while the property's candidate scope was active.

    Args:
        case (ET.Element): Completed JUnit testcase.

    Returns:
        dict[str, object]: Frozen code and severity metadata, or empty for older suites.
    """
    import json

    for entry in case.findall("properties/property"):
        if entry.get("name") == "hypothesis_helm.finding":
            return mapping(json.loads(entry.get("value", "{}")))
    return {}


def junit_stops(path: Path) -> bool:
    """
    Distinguish a scoped non-fail-fast property failure from one that should stop scheduling.

    Args:
        path (Path): Completed worker JUnit report.

    Returns:
        bool: Stop on a blocking threshold, an operational error or unavailable evidence.
    """
    try:
        cases = [
            case for case in ET.parse(path).getroot().iter("testcase") if case.find("failure") is not None or case.find("error") is not None
        ]
    except (OSError, ET.ParseError):
        return True
    return not cases or any(junit_attributes(case).get("fail_fast", True) for case in cases)
