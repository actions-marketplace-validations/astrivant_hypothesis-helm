"""
Audit original chart values, declared schemas, and template references.
"""

from __future__ import annotations

import logging

from hypothesis_helm.charts.inspection.templates import discover
from hypothesis_helm.charts.model import Chart, _default_paths, _schema_nodes
from hypothesis_helm.charts.values.presence import has_path
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.compiler.passes.complexity import measure
from hypothesis_helm.compiler.passes.inputs import InputInventory
from hypothesis_helm.compiler.passes.sampling import profile as sampling_profile
from hypothesis_helm.findings.generator import FindingGenerator
from hypothesis_helm.findings.policy import chart_rules, resolve_codes
from hypothesis_helm.findings.severity import attributes, for_paths
from hypothesis_helm.findings.severity import policy as finding_policy
from hypothesis_helm.reporting.progress import format_path
from hypothesis_helm.rules import AUDIT_RULES, ignored_codes
from hypothesis_helm.schemas.contracts import sequence
from hypothesis_helm.schemas.opaque import MESSAGE, opaque_paths, warn_opaque

LOGGER = logging.getLogger(__name__)


def audit_findings(chart: Chart) -> dict[str, object]:
    """
    Inventory schema, template, and default paths against the original values document.

    Args:
        chart (Chart): Loaded chart and its schema and defaults.

    Returns:
        dict[str, object]: Resulting schema, values mapping, or structured report.
    """
    from attrs import asdict

    from hypothesis_helm.schemas.paths import enumerate_paths

    references, diagnostics = discover(chart.path, prune_literals=True, offline=True)
    defaults = set(_default_paths(chart.defaults))
    declared = {entry.path: entry.schema for entry in enumerate_paths(chart.schema)}
    # A wildcard reference records an access pattern, not a required concrete field.
    # Keep explicit schema/default paths, including their collection item contracts.
    paths = defaults | {r.path for r in references if r.path and "*" not in r.path} | declared.keys()
    findings: list[dict[str, object]] = []
    for path in sorted(paths, key=repr):
        LOGGER.info("Auditing path %s", format_path(path))
        nodes = _schema_nodes(chart.schema, tuple(str(segment) for segment in path), chart.schema)
        if not nodes and path in declared:
            nodes = [declared[path]]
        locations = [asdict(r) for r in references if r.path == path]
        if not nodes:
            findings.append({"path": list(path), "issue": "undocumented", "references": locations})
        elif not any("type" in n or "enum" in n or "const" in n for n in nodes):
            findings.append({"path": list(path), "issue": "untyped", "references": locations})
        elif not any(n.get("description") for n in nodes):
            findings.append({"path": list(path), "issue": "missing-description", "references": locations})
        if not has_path(chart.defaults, path):
            findings.append(
                {
                    "path": list(path),
                    "issue": "no-default",
                    "references": locations,
                    "message": "Configurable field is absent from the original values.yaml",
                }
            )
    for path in opaque_paths(chart.schema):
        findings.append(
            {
                "path": list(path),
                "issue": "opaque-object",
                "message": MESSAGE,
                "references": [asdict(r) for r in references if r.path == path],
            }
        )
    warn_opaque(chart.schema, str(chart.path))
    for finding in findings:
        finding["code"] = AUDIT_RULES[str(finding["issue"])]
    unresolved: list[dict[str, object]] = [{**asdict(d), "code": "HH2005"} for d in diagnostics]
    controls = chart_rules(chart.path)
    for finding in [*findings, *unresolved]:
        path = tuple(str(part) if not isinstance(part, int) else part for part in sequence(finding.get("path", [])))
        decision = attributes(str(finding["code"]), settings=for_paths(chart.path, (path,), rules=controls))
        finding.update(decision)
        finding["finding"] = (
            FindingGenerator.create(
                str(finding["code"]), str(finding.get("message", finding.get("issue", "Unresolved value access")))
            ).record()
            | decision
        )
    global_codes = ignored_codes()
    suppressed: list[dict[str, object]] = []
    visible: list[dict[str, object]] = []
    for finding in [*findings, *unresolved]:
        path = tuple(str(part) if not isinstance(part, int) else part for part in sequence(finding.get("path", [])))
        disabled = resolve_codes(controls, (path,), global_codes)
        (suppressed if finding["code"] in disabled else visible).append(finding)
    return {
        "chart": str(chart.path),
        "compiler_limits": active_limits(chart.path),
        "references": [asdict(r) for r in references],
        "dynamic_references": [asdict(r) for r in references if not r.path or "*" in r.path],
        "findings": [finding for finding in visible if finding["code"] != "HH2005"],
        "unresolved": [finding for finding in visible if finding["code"] == "HH2005"],
        "ignored_findings": suppressed,
        "ignored_rules": global_codes,
        "finding_controls": controls,
        "finding_policy": finding_policy(),
    }


def audit(chart: Chart) -> dict[str, object]:
    """
    Combine finding evidence with compiler inventories and complexity analysis.

    Args:
        chart (Chart): Original chart and its declared contract.

    Returns:
        dict[str, object]: Complete audit with suppressed findings retained separately.
    """
    findings = audit_findings(chart)
    complexity = measure(chart)
    return {
        **findings,
        "complexity": complexity,
        "sampling_profile": sampling_profile(chart, complexity),
        "input_inventory": InputInventory.build(chart).report(),
        "input_domains": chart.input_domains().report(),
    }
