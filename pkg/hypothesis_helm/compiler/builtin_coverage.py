"""
Keep executable support claims separate from the upstream function inventory.
"""

import json
from collections import Counter
from importlib.resources import files

from attrs import frozen

from hypothesis_helm.compiler.builtins import BUILTINS
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("CoverageCase", "cases", "fixture", "reference")


@frozen
class CoverageCase:
    """
    Describe one required semantic probe and the limits behind its support claim.

    Attributes:
        name (str): Exact upstream function identifier.
        expression (str): Representative expression evaluated by the compiler regression suite.
        outcome (str): Expected evaluated, symbolic, rejection or deferred result.
        scope (str): Supported domain or specific semantics still missing from analysis.
        limitation (str): Distinguish missing implementations from runtime effects and dynamic calls.
    """

    name: str
    expression: str
    outcome: str
    scope: str
    limitation: str


def fixture() -> dict[str, object]:
    """
    Load the shared chart data for the checked function-support contract.

    Returns:
        dict[str, object]: Test values, helper definitions and per-function coverage records.

    Raises:
        ValueError: The installed coverage artifact has an incompatible format.
    """
    document = mapping(json.loads(files("hypothesis_helm.compiler.assets").joinpath("builtin_coverage.json").read_text(encoding="utf-8")))
    if document.get("format") != 1:
        raise ValueError("Unsupported compiler builtin coverage format")
    return document


def cases() -> tuple[CoverageCase, ...]:
    """
    Require an explicit, executable support decision for every upstream registration.

    Returns:
        tuple[CoverageCase, ...]: Stable function-ordered regression cases and documentation.

    Raises:
        ValueError: Upstream names changed or a case lacks an outcome, matching call or explanation.
    """
    records = mapping(fixture()["functions"])
    missing, obsolete = BUILTINS.keys() - records.keys(), records.keys() - BUILTINS.keys()
    if missing or obsolete:
        raise ValueError(f"Review compiler builtin coverage: missing={sorted(missing)}, obsolete={sorted(obsolete)}")
    result = []
    for name, raw in sorted(records.items()):
        record = mapping(raw)
        expression, outcome, scope, limitation = (str(record.get(key, "")) for key in ("expression", "outcome", "scope", "limitation"))
        if expression.split(" ", 1)[0] != name or outcome not in {"evaluated", "symbolic", "rejection", "deferred"} or not scope.strip():
            raise ValueError(f"Incomplete compiler builtin coverage for {name}")
        if limitation not in {"runtime effect", "dynamic call", "implementation gap", "bounded support"}:
            raise ValueError(f"Missing analysis limitation for {name}")
        result.append(CoverageCase(name, expression, outcome, scope, limitation))
    return tuple(result)


def reference() -> str:
    """
    Publish the same per-function contract enforced by semantic regression tests.

    Returns:
        str: Coverage counts and a complete Markdown table of probes and analysis boundaries.
    """
    entries = cases()
    counts = Counter(case.outcome for case in entries)
    lines = [
        f"All **{len(entries)} registered functions** have a checked support decision. The representative probes produce "
        f"**{counts['evaluated']} concrete results**, **{counts['symbolic']} symbolic result**, "
        f"**{counts['rejection']} explicit rejections**, and **{counts['deferred']} deferred results**.",
        "",
        "| Function | Probe outcome | Representative expression | Supported scope or reason for deferral |",
        "| --- | --- | --- | --- |",
    ]
    for case in entries:
        expression = case.expression.replace("|", "&#124;")
        scope = case.scope.replace("|", "&#124;")
        outcome = case.outcome + (f" ({case.limitation})" if case.outcome == "deferred" else "")
        lines.append(f"| `{case.name}` | {outcome} | `{expression}` | {scope} |")
    return "\n".join(lines)
