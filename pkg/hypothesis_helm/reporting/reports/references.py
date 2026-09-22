"""
Link report finding codes to a compact, local appendix derived from the finding catalog.
"""

import re

from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.reporting.documentation.contents import heading_inventory

__all__ = ("APPENDIX_TITLE", "CODE", "TOKENS", "linked_codes", "with_finding_reference")


APPENDIX_TITLE = "Appendix: finding codes"
CODE = re.compile(r"HH\d{4}\Z")
TOKENS = re.compile(r"\[[^\]\n]+\]\((?:<[^>]+>|[^\s)]+)\)|(`+)(.*?)\1(?!`)|\[?\b(HH\d{4})\b\]?")


def linked_codes(line: str, destinations: dict[str, str], observed: set[str]) -> str:
    """
    Link code references without rewriting URLs or literal reproducing input values.

    Args:
        line (str): One prose line outside a fenced block.
        destinations (dict[str, str]): Appendix destinations, empty when collecting references.
        observed (set[str]): Codes referenced by report prose.

    Returns:
        str: Prose with clickable codes; existing links and non-code inline literals are unchanged.
    """

    def replace(match: re.Match[str]) -> str:
        """
        Recognize bare codes and code-only inline literals.

        Args:
            match (re.Match[str]): Link, inline literal, or finding reference.

        Returns:
            str: Original token or the matching appendix link.
        """
        code = match[3] or (match[2] if match[2] and CODE.fullmatch(match[2]) else None)
        if code is None:
            return match[0]
        observed.add(code)
        return f"[{code}](#{destinations[code]})" if code in destinations else match[0]

    return TOKENS.sub(replace, line)


def with_finding_reference(content: str) -> str:
    """
    Append definitions for referenced codes and link prose to collision-safe destinations.

    Args:
        content (str): Generated report, optionally containing an older contents block and appendix.

    Returns:
        str: Report with a single final appendix; fenced diagnostics and reproducing values remain literal.
    """
    content = re.sub(r"<!-- toc:start -->.*?<!-- toc:end -->\n*", "", content, flags=re.DOTALL)
    inventory = heading_inventory(content)
    lines = content.splitlines()
    for index, level, label, _ in inventory:
        if level == 2 and label == APPENDIX_TITLE:
            lines = lines[:index]
            break
    while lines and not lines[-1].strip():
        lines.pop()
    observed: set[str] = set()
    prose: list[int] = []
    fence = ""
    for index, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = ""
            continue
        if marker:
            fence = marker[1]
            continue
        # Existing appendix links are regenerated, which also makes repeated publication idempotent.
        line = re.sub(r"\[(HH\d{4})\]\((?:<#hh\d{4}[^>]*>|#hh\d{4}[^)]*)\)", r"\1", line)
        lines[index] = linked_codes(line, {}, observed)
        prose.append(index)
    appendix_start = len(lines)
    lines.extend(["", f"## {APPENDIX_TITLE}", ""])
    if observed:
        lines.extend(
            [
                "HH codes identify finding categories. Numbered E entries, when present, identify recorded diagnostics.",
                "Severities below are defaults; configured overrides are shown with the findings above.",
                "",
            ]
        )
    else:
        lines.extend(["No finding codes are referenced in this report.", ""])
    for code in sorted(observed):
        rule = CATALOG.get(code)
        lines.extend([f"### {code} - {rule.title if rule else 'Unknown finding code'}", ""])
        if rule is None:
            lines.extend(
                ["This tool version has no definition for this code. Consult the recorded diagnostic and its producing version.", ""]
            )
            continue
        lines.extend(
            [
                f"Default severity: **{rule.severity}** | Category: {rule.category} | Evidence type: {rule.kind}",
                "",
                rule.detection,
                "",
                f"Suggested action: {rule.remediation}",
                "",
            ]
        )
    destinations = {
        label.split(" ", 1)[0]: anchor
        for index, level, label, anchor in heading_inventory("\n".join(lines))
        if index >= appendix_start and level == 3
    }
    for index in prose:
        lines[index] = linked_codes(lines[index], destinations, observed)
    for index in range(appendix_start, len(lines)):
        if not lines[index].startswith("#"):
            lines[index] = linked_codes(lines[index], destinations, observed)
    return "\n".join(lines).rstrip() + "\n"
