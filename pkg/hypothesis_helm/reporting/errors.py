"""
Group repeated scan diagnostics while retaining every chart and reproducer.
"""

from __future__ import annotations

import hashlib
import json
import re
import tarfile
from pathlib import Path, PurePosixPath

from ruamel.yaml.error import YAMLError

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.findings.generator import FindingGenerator
from hypothesis_helm.findings.severity import attributes
from hypothesis_helm.reporting.reproductions import failing_input
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("TEMPLATE_FRAME", "chart_errors", "deduplicate_errors", "template_source")


TEMPLATE_FRAME = re.compile(r"(?:template: |execution error at \()(?P<path>[^\s\"():]+/templates/[^\s\"():]+):\d+(?::\d+)?")


def template_source(chart: Path, location: str) -> dict[str, object] | None:
    """
    Resolve a diagnostic's template against built directories or a packaged dependency.

    Args:
        chart (Path): Isolated chart after dependency preparation.
        location (str): Helm template path including its chart prefix.

    Returns:
        dict[str, object] | None: Source identity, or no evidence when resolution is ambiguous.
    """
    parts = PurePosixPath(location).parts
    if ".." in parts or location.startswith("/") or "templates" not in parts:
        return None
    index = parts.index("templates")
    directory = chart.joinpath(*parts[1:index])
    relative = PurePosixPath(*parts[index:]).as_posix()
    try:
        if directory.is_dir():
            metadata = yamlio.load((directory / "Chart.yaml").read_text())
            content = (directory / relative).read_bytes()
        else:
            # Helm presents aliases as chart names even when the archive uses
            # the dependency's original name. Resolve that declaration first.
            parent = directory.parent.parent
            declaration = mapping(yamlio.load((parent / "Chart.yaml").read_text()))
            name = directory.name
            for dependency in sequence(declaration.get("dependencies", [])):
                entry = mapping(dependency)
                if entry.get("alias", entry.get("name")) == name:
                    name = str(entry["name"])
                    break
            matches: list[tuple[object, bytes]] = []
            for archive in sorted(directory.parent.glob("*.tgz")):
                with tarfile.open(archive, "r:gz") as bundle:
                    headers = [member for member in bundle if member.name == f"{name}/Chart.yaml"]
                    if len(headers) != 1:
                        continue
                    header = bundle.extractfile(headers[0])
                    template = bundle.extractfile(f"{name}/{relative}")
                    if header is not None and template is not None:
                        matches.append((yamlio.load(header.read().decode()), template.read()))
            if len(matches) != 1:
                return None
            metadata, content = matches[0]
        identity = mapping(metadata)
        if not identity.get("name") or not identity.get("version"):
            return None
        return {
            "name": identity["name"],
            "version": identity["version"],
            "template": relative,
            "sha256": hashlib.sha256(content).hexdigest(),
        }
    except (OSError, ValueError, KeyError, tarfile.TarError, YAMLError):
        return None


def chart_errors(record: dict[str, object], chart: Path | None = None) -> list[dict[str, object]]:
    """
    Extract distinct phase diagnostics without repeating their aggregate error text.

    Args:
        record (dict[str, object]): One chart's results, kept unchanged.
        chart (Path | None): Built source available for dependency provenance.

    Returns:
        list[dict[str, object]]: Diagnostic signatures and optional verified template identities.
    """
    phases = [
        mapping(phase)
        for phase in sequence(record.get("phases", []))
        if isinstance(phase, dict) and (phase.get("error") or phase.get("failure_expansion") or phase.get("findings"))
    ]
    aggregate = "\n\n".join(
        f"{phase.get('phase')}: {phase['error']}" for phase in phases if phase.get("status") == "failed" and phase.get("error")
    )
    sources = list(phases)
    for source in [record, *phases]:
        observed = source.get("observed_failure")
        if isinstance(observed, dict) and observed.get("error"):
            sources.append({**{key: source[key] for key in ("phase", "artifacts") if key in source}, **observed})
        sources.extend(
            {**{key: source[key] for key in ("phase", "artifacts") if key in source}, **item}
            for item in sequence(source.get("findings", []))
            if isinstance(item, dict) and item.get("error")
        )
    baseline = record.get("baseline")
    if isinstance(baseline, dict) and baseline.get("status") == "findings" and baseline.get("error"):
        sources.append(baseline)
    baseline_error = baseline.get("error") if isinstance(baseline, dict) and baseline.get("status") == "findings" else None
    if (record.get("error") and record["error"] not in (aggregate, baseline_error)) or record.get("failure_expansion"):
        sources.append(record)
    expanded_sources = []
    for source in sources:
        expansion = source.get("failure_expansion")
        failures = sequence(expansion.get("failures", [])) if isinstance(expansion, dict) else []
        matching_primary = False
        for index, failure in enumerate(failures, 1):
            case = mapping(failure)
            if not case.get("error"):
                continue
            expanded_sources.append(
                {
                    **source,
                    **case,
                    "phase": f"{source.get('phase', 'chart')} / case {index}",
                    "status": "failed",
                    "failure_type": case.get("failure_type"),
                }
            )
            matching_primary |= case.get("values") == source.get("values") and case["error"] == source.get("error")
        # A later execution error cannot erase defects already seen during
        # expansion, but the execution error itself is not a chart defect.
        if source.get("error") and not matching_primary and source.get("error_kind") != "execution":
            expanded_sources.append(source)
    errors: list[dict[str, object]] = []
    for source in expanded_sources:
        if source.get("status") in {"pending", "not-started", "not-needed", "ignored"}:
            continue
        diagnostic = str(source["error"]).strip()
        identity = None
        frames = list(TEMPLATE_FRAME.finditer(diagnostic))
        if chart is not None and frames:
            leaf = frames[-1]
            location = leaf.group("path")
            identity = template_source(chart, location)
            if identity is not None:
                diagnostic = diagnostic[leaf.start() :].replace(location, f"{identity['name']}/{identity['template']}", 1)
        code = source.get("code") or (match.group(1) if (match := re.search(r"\[(HH\d{4})\]", str(source["error"]))) else None)
        finding = source.get("finding") or (FindingGenerator.create(str(code), diagnostic).record() if code in CATALOG else None)
        if isinstance(finding, dict):
            if not source.get("finding") and "finding_policy" in record:
                finding = {**finding, **attributes(str(code), settings=mapping(record["finding_policy"]))}
            finding = {**finding, **{key: source[key] for key in ("severity", "blocking", "fail_fast") if key in source}}
        errors.append(
            {
                "phase": source.get("phase", "chart"),
                "status": source["status"],
                "failure_type": source.get("failure_type"),
                "code": code,
                "finding": finding,
                **(
                    {key: finding[key] for key in ("severity", "blocking", "fail_fast") if key in finding}
                    if isinstance(finding, dict)
                    else {}
                ),
                "error": diagnostic,
                "source": identity,
                "input": failing_input(source),
                "artifacts": source.get("artifacts", record.get("artifacts")),
            }
        )
    return errors


def deduplicate_errors(report: dict[str, object]) -> None:
    """
    Add shared error groups and chart references without changing raw results or exit status.

    Args:
        report (dict[str, object]): Mutable aggregate scan report, including all chart records.

    Returns:
        None: Error groups, references, and occurrence counts are added in place.
    """
    charts = [mapping(chart) for chart in sequence(report["charts"])]
    groups: dict[str, dict[str, object]] = {}
    for chart in charts:
        references: list[str] = []
        diagnostics = chart.get("error_diagnostics")
        if diagnostics is None:
            diagnostics = chart_errors(chart)
        for diagnostic in sequence(diagnostics):
            error = mapping(diagnostic)
            signature = {key: value for key, value in error.items() if key not in {"phase", "input", "artifacts"}}
            key = json.dumps(signature, sort_keys=True)
            if key not in groups:
                groups[key] = {**signature, "occurrences": []}
            source = chart
            for phase in sequence(chart.get("phases", [])):
                if isinstance(phase, dict) and phase.get("phase") == error["phase"]:
                    source = phase
                    break
            occurrence = {
                "chart": chart["chart"],
                "phase": error["phase"],
                "status": error["status"],
                "artifacts": error.get("artifacts") or source.get("artifacts") or chart.get("artifacts"),
                "input": error.get("input", failing_input(source)),
            }
            sequence(groups[key]["occurrences"]).append(occurrence)
            if key not in references:
                references.append(key)
        chart["error_refs"] = references
    identifiers = {key: f"E{index:03d}" for index, key in enumerate(sorted(groups), 1)}
    for chart in charts:
        chart["error_refs"] = [identifiers[str(key)] for key in sequence(chart["error_refs"])]
    result: list[dict[str, object]] = []
    for key in sorted(groups):
        group = groups[key]
        occurrences = sequence(group["occurrences"])
        affected = sorted({str(mapping(item)["chart"]) for item in occurrences})
        result.append(
            {
                **group,
                "id": identifiers[key],
                "occurrence_count": len(occurrences),
                "affected_charts": affected,
            }
        )
    total = sum(int(str(group["occurrence_count"])) for group in result)
    report["error_groups"] = result
    report["error_summary"] = {
        "unique_errors": len(result),
        "occurrences": total,
        "duplicates": total - len(result),
    }
