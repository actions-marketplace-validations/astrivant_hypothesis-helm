"""
Portable Markdown and paginated PDF summaries for repository scans.
"""

from __future__ import annotations

import os
import re
import textwrap
from pathlib import Path
from urllib.parse import quote

from hypothesis_helm.reporting.contents import with_contents
from hypothesis_helm.reporting.errors import deduplicate_errors
from hypothesis_helm.reporting.links import Publication, chart_source_url, publish_links, web_url
from hypothesis_helm.reporting.overview import summarize, write_overview
from hypothesis_helm.reporting.pdf import write_pdf
from hypothesis_helm.reporting.progress import format_path
from hypothesis_helm.reporting.provenance import trace_run
from hypothesis_helm.reporting.references import with_finding_reference
from hypothesis_helm.reporting.reproductions import input_summary
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("HELM_DEBUG_HINT", "artifact_link", "chart_heading", "display_error", "wrap_markdown", "write_reports")


HELM_DEBUG_HINT = re.compile(r"(?m)^[ \t]*Use --debug flag to render out invalid YAML[ \t]*\r?$\n?")


def artifact_link(label: str, destination: object, report: Path, *, prefer: tuple[str, ...] = ()) -> str:
    """
    Link artifacts relative to the report location rather than the working directory.

    Args:
        label (str): Short human-readable link text.
        destination (object): Recorded filesystem artifact path or HTTPS URL.
        report (Path): Markdown report destination.
        prefer (tuple[str, ...]): Existing files to prefer inside a local artifact directory, in order.

    Returns:
        str: Portable Markdown link with an escaped relative target.
    """
    url = web_url(destination)
    if url is not None:
        return f"[{label}](<{url}>)"
    path = Path(str(destination))
    # Finalized scan archives already store paths relative to the human report.
    target = os.path.relpath(path, report.parent) if path.is_absolute() or path.exists() else str(path)
    for filename in prefer:
        if (report.parent / target / filename).is_file():
            target = str(Path(target) / filename)
            break
    return f"[{label}](<{quote(target, safe='/._-')}>)"


def chart_heading(chart: dict[str, object], source: dict[str, object], report: Path, *, artifact_links: bool = True) -> str:
    """
    Make chart names open their source code, falling back to retained run artifacts.

    Args:
        chart (dict[str, object]): Chart identity and available artifact destinations.
        source (dict[str, object]): Stable repository provenance recorded by the scan.
        report (Path): Markdown report location for relative artifact links.
        artifact_links (bool): Whether the report publishes retained run artifacts.

    Returns:
        str: Chart heading with an optional source or artifact link.
    """
    title = str(chart["chart"]).replace("\n", " ")
    destination = chart_source_url(chart, source)
    if destination is None and artifact_links:
        destination = str(chart.get("artifacts") or "") or None
    return "### " + (artifact_link(title, destination, report) if destination else title)


def wrap_markdown(content: str) -> str:
    """
    Wrap report prose to 140 columns without changing code blocks or link targets.

    Headings, tables, indented code, and indivisible tokens may exceed the limit.

    Args:
        content (str): Generated Markdown report.

    Returns:
        str: Wrapped Markdown with a final newline.
    """
    lines: list[str] = []
    fence = ""
    for line in content.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            lines.append(line)
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = ""
            continue
        if marker:
            fence = marker[1]
        if marker or len(line) <= 140 or line.startswith(("#", "|", "    ", "\t")):
            lines.append(line)
            continue
        bullet = re.match(r"^(\s*(?:[-+*]|\d+[.)])\s+)", line)
        prefix = bullet[0] if bullet else ""
        continuation = " " * len(prefix)
        # Keep inline code and complete links together, including paths with spaces.
        tokens = re.findall(r"(?:!?\[[^\]]*\]\((?:<[^>]*>|[^)\s]*)\)|`+[^`]*`+|\S)+", line[len(prefix) :])
        current = prefix
        width = 138 if line.endswith("  ") else 140
        for token in tokens:
            separator = " " if current.strip() and current != prefix else ""
            if len(current) + len(separator) + len(token) > width and current.strip() and current != prefix:
                lines.append(current)
                current = continuation
                separator = ""
            current += separator + token
        lines.append(current + ("  " if line.endswith("  ") else ""))
    return "\n".join(lines) + "\n"


def display_error(error: object) -> str:
    """
    Present useful diagnostics while leaving raw errors in the JSON artifacts.

    Args:
        error (object): Recorded error, including historical tooling failures.

    Returns:
        str: Human-readable diagnostic without Helm's redundant debug suggestion.
    """
    return (
        HELM_DEBUG_HINT.sub("", str(error))
        .rstrip()
        .replace(
            "invalid rendered manifest: Object of type TaggedScalar is not JSON serializable",
            "The test tool could not convert a YAML-tagged value to JSON. "
            "See this chart's reproducing values. "
            "This diagnostic alone does not establish a chart defect.",
        )
    )


def write_reports(
    report: dict[str, object], stem: Path, *, publication: Publication | None = None, artifact_links: bool = True
) -> tuple[Path, Path]:
    """
    Write both report formats, accepting an explicit stem or either extension.

    Args:
        report (dict[str, object]): Scan summary including chart diagnostics.
        stem (Path): Output stem, Markdown filename, or PDF filename.
        publication (Publication | None): Public repository destination for shareable artifact links.
        artifact_links (bool): Link local run evidence; disable for standalone published reports.

    Returns:
        tuple[Path, Path]: Markdown and PDF output paths.
    """
    # Both formats share one grouping and one run identity; formatting must not change the underlying findings.
    deduplicate_errors(report)
    trace_run(report)
    if stem.suffix.lower() in (".md", ".pdf"):
        stem = stem.with_suffix("")
    markdown, pdf = Path(f"{stem}.md"), Path(f"{stem}.pdf")
    markdown.parent.mkdir(parents=True, exist_ok=True)
    overview = summarize(report)
    figure = Path(f"{stem}-overview.png")
    overview_cells = write_overview(overview, figure)
    settings = mapping(report["settings"])
    lines = [
        f"# {report.get('title', 'Helm chart scan')}",
        "",
        f"Directory: {report['directory']}",
        f"Started (Unix epoch): {report['started_epoch']}",
        f"Elapsed (wall clock): {float(str(report['elapsed_seconds'])):.2f} seconds",
        f"Charts discovered: {report['charts_discovered']}",
        f"Scan status: {report.get('scan_status', 'not recorded')}",
        f"Discovery complete: {report.get('discovery_complete', 'not recorded')}",
        f"Unstarted charts: {report.get('unstarted_charts', 'not recorded')}",
        "",
        "Results record outcomes for the tested sample and selected checks.",
        "Baseline-only, skipped, blocked, and incomplete charts retain their respective statuses.",
        "",
        "## Status counts",
        "",
        "; ".join(f"{count} {status}" for status, count in mapping(report["counts"]).items()) + ".",
        "",
        "## Settings",
        "",
        f"Filtering: {settings.get('filter', 'not recorded')} | Seed: {settings.get('seed', 'not recorded')} | "
        f"Traversal: {settings.get('traversal_strategy', 'not recorded')}",
        f"Chart timeout: {settings.get('chart_timeout_seconds', 'not recorded')} seconds | "
        f"Workers: {settings.get('workers', 'not recorded')}",
        "Complete settings are retained in the JSON report.",
        "",
    ]
    if "testing_seconds" in report:
        lines[5:5] = [
            f"Chart testing: {float(str(report['testing_seconds'])):.2f} seconds",
            f"Dependency preparation: {float(str(report['dependency_preparation_seconds'])):.2f} seconds (excluded from testing budgets)",
        ]
    timing_note = " (estimated from recorded timing)" if str(report["finish_time_source"]).startswith("derived") else ""
    lines[4:4] = [
        f"Started (UTC): {report['started_at']}",
        f"Finished (UTC): {report['finished_at']}{timing_note}",
        f"Run fingerprint (SHA-256): `{report['run_hash']}`",
    ]
    summary = report.get("summary", [])
    if isinstance(summary, list):
        lines[2:2] = [str(line) for line in summary] + [""]
    if "input_policy" in report:
        lines.extend(
            [
                "Generated values use the configured input domains and any supported destination constraints. "
                "Coverage excludes inputs outside these domains; supplied defaults are tested unchanged. "
                "The JSON report records constraints and unresolved mappings.",
                "",
            ]
        )
    if report.get("ignored_rules"):
        lines.extend(["Disabled checks: " + ", ".join(str(code) for code in sequence(report["ignored_rules"])), ""])
    errors = sequence(report["error_groups"])
    if errors:
        counts = mapping(report["error_summary"])
        lines.extend(
            [
                "## Errors",
                "",
                f"{counts['unique_errors']} distinct diagnostics across "
                f"{counts['occurrences']} occurrences; {counts['duplicates']} repeats grouped.",
                "Diagnostics and their triggering inputs are grouped under each chart below.",
                "Up to two examples per diagnostic and six fields per example are shown. Long values and diagnostics are shortened.",
                "Full inputs, diagnostics, and remaining cases are retained in local run data.",
                "Selected fields identify the inputs varied by the test. Causal attribution requires further investigation.",
                "",
            ]
        )
    lines.extend(["## Charts", ""])
    charts = report["charts"]
    assert isinstance(charts, list)
    for index, chart in enumerate(charts, 1):
        assert isinstance(chart, dict)
        heading = chart_heading(chart, mapping(report.get("source", {})), markdown, artifact_links=artifact_links)
        lines.extend([heading, "", f"Overview cell: {index:02d}", ""])
        package = chart.get("package")
        if isinstance(package, dict):
            lines.extend(
                [
                    f"Package: {package['reference']} | Version: {package['version']}",
                    f"Package SHA-256: `{package['sha256']}`",
                    "",
                ]
            )
        lines.extend(
            [
                f"Status: {chart['status']} | Attempts: {chart.get('attempts', 'N/A')}",
                "",
            ]
        )
        audit = mapping(chart.get("audit", {}))
        findings = [mapping(item) for item in [*sequence(audit.get("findings", [])), *sequence(audit.get("unresolved", []))]]
        if findings:
            lines.extend([f"Audit findings: {len(findings)}. Full paths and template references are retained in the JSON report.", ""])
            for observed_finding in findings[:6]:
                path = tuple(str(part) for part in sequence(observed_finding.get("path", [])))
                lines.append(
                    f"- `{observed_finding['code']}` at `{format_path(path)}`: "
                    f"{mapping(observed_finding.get('finding', {})).get('title', '')}"
                    f"{(' (' + str(observed_finding['severity']) + ')') if 'severity' in observed_finding else ''}"
                )
            if len(findings) > 6:
                lines.append(f"- {len(findings) - 6} additional audit findings in JSON.")
            lines.append("")
        sampling = chart.get("sampling")
        if isinstance(sampling, dict) and sampling.get("applied"):
            lines.extend(
                [
                    f"Random sample: {sampling['retained']} / {sampling['eligible']} eligible cases retained; "
                    f"{sampling['omitted']} omitted. Minimum: {sampling['minimum']}. Seed: {sampling['seed']}. "
                    "Bug recall depends on the defect-triggering inputs retained.",
                    "",
                ]
            )
        rejections = chart.get("configuration_rejections")
        if isinstance(rejections, dict) and (rejections.get("rejected_candidates") or rejections.get("schema_conflicts")):
            lines.extend(
                [
                    f"Configuration rejections: {rejections['filtered_candidates']} excluded; "
                    f"{rejections['adjusted_candidates']} adjusted and tested; "
                    f"{rejections['verification_renders']} Helm verification renders (separate from manifest-test attempts).",
                    "",
                ]
            )
            requirements = sequence(rejections.get("requirements", []))
            if rejections.get("schema_conflicts"):
                lines.extend(["The template rejected inputs admitted by the declared values schema; these remain reported failures.", ""])
            for requirement in requirements[:3]:
                record = mapping(requirement)
                message = " ".join(str(record["requirement"]).split())
                lines.extend([f"Requirement ({record['source']}:{record['line']}): {message[:500]}", ""])
                for input_path, choices in mapping(record.get("enums", {})).items():
                    values = sequence(choices)
                    shown = ", ".join(f"`{value}`" for value in values[:12])
                    extra = f" (+{len(values) - 12} more in artifacts)" if len(values) > 12 else ""
                    lines.extend([f"Template choices for `{input_path}` on this branch: {shown}{extra}.", ""])
                lines.extend(input_summary({"recorded": True, "paths": record["inputs"]}))
                lines.append("")
            if len(requirements) > 3:
                lines.extend([f"{len(requirements) - 3} more requirements are retained in chart artifacts.", ""])
        dumped = chart.get("minimal_values")
        if isinstance(dumped, dict) and artifact_links:
            destination = str(dumped["yaml"])
            lines.extend([artifact_link("Minimal values", destination, markdown), ""])
            if dumped.get("proof"):
                proof = str(dumped["proof"])
                lines.extend([artifact_link("Verification record", proof, markdown), ""])
        for entry in errors:
            group = mapping(entry)
            occurrences = [mapping(item) for item in sequence(group["occurrences"]) if mapping(item)["chart"] == chart["chart"]]
            if not occurrences:
                continue
            lines.extend([f"#### {group['id']}" + (f" ({group['code']})" if group.get("code") else ""), ""])
            finding = group.get("finding")
            if isinstance(finding, dict):
                lines.extend(
                    [
                        f"**{finding['title']}** ({finding['category']} / {finding['kind']}). "
                        f"{('Severity: **' + str(finding['severity']) + '**. ') if 'severity' in finding else ''}"
                        f"{finding['remediation']}",
                        "",
                    ]
                )
            source = group.get("source")
            if isinstance(source, dict):
                lines.extend([f"Source: {source['name']} {source['version']} / {source['template']}", ""])
            content = display_error(group["error"])
            # Keep the terminal diagnostic, omitting long include stacks and subprocess logs.
            content = " ".join(content.split())
            if len(content) > 500:
                content = "[Diagnostic shortened; full text in artifacts] ... " + content[-450:]
            fence = "`" * max(3, max(map(len, re.findall(r"`+", content)), default=0) + 1)
            lines.extend([fence + "text", *textwrap.wrap(content, width=140, break_long_words=False, break_on_hyphens=False), fence, ""])
            for occurrence in occurrences[:2]:
                lines.extend([f"Phase: {occurrence['phase']} | Status: {occurrence['status']}", ""])
                lines.extend(input_summary(mapping(occurrence["input"])))
                lines.append("")
                occurrence_artifacts = occurrence.get("artifacts")
                if occurrence_artifacts and artifact_links:
                    lines.extend(
                        [
                            artifact_link(
                                "Full input and diagnostic",
                                occurrence_artifacts,
                                markdown,
                                prefer=("report.json", "observed-failure.json"),
                            ),
                            "",
                        ]
                    )
            if len(occurrences) > 2:
                lines.extend([f"{len(occurrences) - 2} additional occurrences are retained in the JSON report and chart artifacts.", ""])
        artifacts = chart.get("artifacts")
        suppressions = chart.get("suppression_export")
        if artifact_links and isinstance(suppressions, dict) and suppressions.get("yaml"):
            lines.extend([artifact_link("Review suggested suppressions (not applied)", suppressions["yaml"], markdown), ""])
        if artifacts and artifact_links:
            lines.extend([artifact_link("Chart artifacts", artifacts, markdown), ""])
    lines[2:2] = [
        "## Overview",
        "",
        "!" + artifact_link("Chart severity and scan-time matrices", figure, markdown),
        "",
        overview.caption,
        "",
        "## Scan summary",
        "",
    ]
    lines = with_finding_reference("\n".join(lines)).splitlines()
    if publication is not None:
        fence = ""
        for index, line in enumerate(lines):
            marker = re.match(r"^(`{3,})", line)
            if marker and not fence:
                fence = marker[1]
            elif fence and re.fullmatch(re.escape(fence) + r"`*\s*", line):
                fence = ""
            elif not fence:
                lines[index] = publish_links(line, markdown, publication)
    markdown.write_text(with_contents(wrap_markdown("\n".join(lines)), max_depth=3))
    write_pdf("\n".join(lines), pdf, title=str(report.get("title", "Helm chart scan")), overview=figure, overview_cells=overview_cells)
    return markdown, pdf
