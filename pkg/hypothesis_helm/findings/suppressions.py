"""
Export reviewable, categorized path suppressions from findings observed during one chart run.
"""

from __future__ import annotations

import json
import logging
import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from collections.abc import Iterator
from glob import escape
from pathlib import Path
from types import TracebackType
from uuid import uuid4

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.findings.policy import candidate_paths, resolve_codes
from hypothesis_helm.reporting.errors import chart_errors
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.policy import path_parts

__all__ = ("ENVIRONMENT", "SuppressionCapture", "constraint_path", "evidence", "observe", "observed_paths")


ENVIRONMENT = "HYPOTHESIS_HELM_SUPPRESSION_OBSERVATIONS"
LOGGER = logging.getLogger(__name__)


def observed_paths(defaults: dict[str, object] | None, values: object) -> tuple[tuple[str | int, ...], ...]:
    """
    Reuse candidate policy semantics or require chart-wide scope when inputs cannot be compared.

    Args:
        defaults (dict[str, object] | None): Actual chart baseline, when recorded.
        values (object): Recorded overrides, potentially unavailable or not JSON-compatible.

    Returns:
        tuple[tuple[str | int, ...], ...]: All changed paths, or the root when no narrower scope is supported.
    """
    if defaults is not None and isinstance(values, dict):
        try:
            return candidate_paths(Chart(Path("."), {}, defaults), values) or ((),)
        except (TypeError, ValueError, OverflowError):
            pass
    return ((),)


def observe(code: str, defaults: dict[str, object], values: dict[str, object]) -> None:
    """
    Journal changed paths for every observed failure, including intermediate shrinking attempts.

    Args:
        code (str): Detected catalog condition, after suppression checks.
        defaults (dict[str, object]): This chart's actual baseline.
        values (dict[str, object]): Actual overrides, including dependent fields.

    Returns:
        None: Only paths and codes are retained; separate process files avoid shared writes.
    """
    directory = os.environ.get(ENVIRONMENT)
    if directory is None or code not in CATALOG:
        return
    try:
        paths = observed_paths(defaults, values)
        with (Path(directory) / f"{os.getpid()}.jsonl").open("a") as stream:
            stream.write(json.dumps({"code": code, "paths": paths or ((),)}) + "\n")
    except (OSError, TypeError, ValueError):
        # A missing journal cannot justify a narrow suppression; final evidence remains available.
        LOGGER.warning("Could not record suppression paths for %s", code)


def constraint_path(path: tuple[str | int, ...]) -> tuple[str, bool]:
    """
    Use the narrowest path expressible by the current input-constraint grammar.

    Args:
        path (tuple[str | int, ...]): Concrete changed or audited path.

    Returns:
        tuple[str, bool]: Dollar-rooted selector and whether it necessarily widens the observed scope.
    """
    result = "$"
    widened = False
    for part in path:
        if isinstance(part, int) or part == "*":
            result += "[*]"
            widened = True
        elif re.fullmatch(r"[A-Za-z_][A-Za-z_0-9-]*", part):
            result += "." + part
        else:
            return result, True
    return result, widened


def evidence(record: dict[str, object], defaults: dict[str, object] | None) -> Iterator[tuple[str, tuple[str | int, ...]]]:
    """
    Extract unsuppressed audit and runtime findings without guessing codes for infrastructure errors.

    Args:
        record (dict[str, object]): Completed or interrupted chart result.
        defaults (dict[str, object] | None): Baseline used in the run, when available.

    Yields:
        tuple[str, tuple[str | int, ...]]: Code and each path that must permit its suppression.
    """
    audit = mapping(record.get("audit", record))
    for item in [*sequence(audit.get("findings", [])), *sequence(audit.get("unresolved", []))]:
        finding = mapping(item)
        path = tuple(part for part in sequence(finding.get("path", [])) if isinstance(part, (str, int)))
        yield str(finding.get("code", "")), path
    # Preserve actual changed paths, including map deletions and all dependent fields.
    sources = [record, *(mapping(item) for item in sequence(record.get("phases", [])))]
    root_diagnostic = any(item.get("phase") == record.get("phase", "chart") for item in chart_errors(record))
    for source in sources:
        expansion = mapping(source.get("failure_expansion", {}))
        candidates = [source, *(mapping(item) for item in sequence(expansion.get("failures", [])))]
        for candidate in candidates:
            if candidate is record and not root_diagnostic:
                continue
            if not candidate.get("error") or candidate.get("status") in {"ignored", "pending", "not-started", "not-needed"}:
                continue
            # Fail-fast audit diagnostics repeat the precise audit finding already handled above.
            if candidate is record and "audit" in record and record.get("coverage") == "audit only":
                continue
            diagnostics = chart_errors({**candidate, "phases": [], "failure_expansion": {}, "status": candidate.get("status", "failed")})
            code = str(diagnostics[0].get("code") or "") if diagnostics else ""
            values = candidate.get("values")
            for path in observed_paths(defaults, values):
                yield code, path


class SuppressionCapture:
    """
    Isolate one chart's worker journals and publish a separate configuration for review.
    """

    def __init__(self, directory: Path, *, enabled: bool) -> None:
        """
        Select an artifact location without creating anything unless requested.

        Args:
            directory (Path): This chart or shard's artifact directory.
            enabled (bool): Whether the user requested a suppression export.
        """
        self.directory = directory
        self.enabled = enabled
        self.journal = directory / "suppression-observations" / uuid4().hex
        self.previous: str | None = None

    def __enter__(self) -> SuppressionCapture:
        """
        Publish this run's journal directory for local workers and subprocesses.

        Returns:
            SuppressionCapture: The active per-chart capture.
        """
        self.previous = os.environ.get(ENVIRONMENT)
        if self.enabled:
            self.journal.mkdir(parents=True, exist_ok=True)
            os.environ[ENVIRONMENT] = str(self.journal.resolve())
        return self

    def __exit__(self, kind: type[BaseException] | None, error: BaseException | None, traceback: TracebackType | None) -> None:
        """
        Restore the caller's journal after workers have joined, without swallowing exceptions.

        Args:
            kind (type[BaseException] | None): Propagating exception type.
            error (BaseException | None): Propagating exception.
            traceback (TracebackType | None): Original traceback.

        Returns:
            None: Journals remain available for review and exporting partial runs.
        """
        if self.enabled:
            if self.previous is None:
                os.environ.pop(ENVIRONMENT, None)
            else:
                os.environ[ENVIRONMENT] = self.previous

    def write(self, record: dict[str, object], *, name: str, source: str, defaults: dict[str, object] | None = None) -> None:
        """
        Write a minimal nonredundant cover of the observed code/path requirements.

        Args:
            record (dict[str, object]): Chart result receiving export metadata.
            name (str): Exact Chart.yaml name.
            source (str): Stable source identity used by chart selectors.
            defaults (dict[str, object] | None): Actual selected values baseline, when available.

        Returns:
            None: Categorized YAML is exported, never installed as the active configuration.
        """
        if not self.enabled:
            return
        scopes: dict[str, set[str]] = defaultdict(set)
        widened: set[tuple[str, str]] = set()
        uncovered = 0

        def add(code: str, path: tuple[str | int, ...]) -> None:
            """
            Retain unique supported requirements and count observations without usable codes.

            Args:
                code (str): Observed catalog code.
                path (tuple[str | int, ...]): Changed or audited path.

            Returns:
                None: Unsupported observations never become invented ignore rules.
            """
            nonlocal uncovered
            if code not in CATALOG:
                uncovered += 1
                return
            selector, broad = constraint_path(path)
            scopes[code].add(selector)
            if broad:
                widened.add((code, selector))

        for code, observed_path in evidence(record, defaults):
            add(code, observed_path)
        for journal in sorted(self.journal.glob("*.jsonl")):
            with journal.open() as stream:
                for line in stream:
                    try:
                        item = json.loads(line)
                        for path in item["paths"]:
                            add(str(item["code"]), tuple(path))
                    except (ValueError, TypeError, KeyError):
                        uncovered += 1
        junit = record.get("junit_xml")
        if isinstance(junit, str):
            try:
                xml = ET.fromstring(junit)
                for item in xml.iter():
                    if item.tag not in {"failure", "error"}:
                        continue
                    junit_codes = set(re.findall(r"\[(HH\d{4})\]", item.text or item.get("message") or "")) & CATALOG.keys()
                    if not junit_codes:
                        uncovered += 1
                    for code in junit_codes - scopes.keys():
                        add(code, ())
            except ET.ParseError:
                uncovered += 1
        # Parent rules already suppress descendants. Never invent a common parent to shorten the file.
        grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
        for code, paths in scopes.items():
            wildcard_rules: list[dict[str, object]] = [{"path": path, "ignored": [code]} for path in paths if "[*]" in path]
            for path in sorted(paths):
                if any(path[:index] in paths for index, char in enumerate(path) if char in ".["):
                    continue
                if wildcard_rules and code in resolve_codes(
                    [rule for rule in wildcard_rules if rule["path"] != path], (path_parts(path),), []
                ):
                    continue
                grouped[(CATALOG[code].category, path)].append(code)
        rows = []
        for (category, path), codes in sorted(grouped.items()):
            rows.append((category, path, sorted(codes)))
        lines = [
            "# Review before use. These rules are NOT applied automatically.",
            "# Copy selected input_constraints entries into your existing configuration.",
            "# Remove a code or rule to keep detecting that condition in its covered paths.",
            "# Rules disable checks for all values at a path, not just the observed counterexample.",
            "# A multi-field failure needs a rule for every changed field, including dependent fields.",
            "# More specific enabled rules in your existing configuration still take precedence.",
            "# Source and chart-name selectors also match same-named charts in the same source.",
            f"# Run status: {record.get('status', 'audit')}; observations without a suppressible code: {uncovered}.",
            "# Uncoded tool/setup errors cannot be silenced using finding rules.",
            "input_constraints:" if rows else "input_constraints: []",
        ]
        for category, path, codes in rows:
            lines.extend(["", f"  # {category.capitalize()}"])
            if path == "$":
                lines.append("  # Chart-wide: defaults failed or no narrower supported path was recorded.")
            if any((code, path) in widened for code in codes):
                lines.append("  # Widened scope: [*] covers matching items/keys; unsupported keys use their nearest supported parent.")
            for code in codes:
                rule = CATALOG[code]
                lines.append(f"  # {code}: {rule.title} ({rule.kind})")
            row = {"charts": [{"sources": [escape(source)], "names": [escape(name)]}], "path": path, "ignored": codes}
            lines.extend("  " + line for line in yamlio.dump([row]).rstrip().splitlines())
        self.directory.mkdir(parents=True, exist_ok=True)
        target = self.directory / "suppressions.yaml"
        temporary = target.with_name(f".suppressions-{uuid4().hex}.tmp")
        try:
            temporary.write_text("\n".join(lines) + "\n")
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
        record["suppression_export"] = {
            "yaml": str(target.resolve()),
            "rules": len(rows),
            "codes": sorted(scopes),
            "uncovered_observations": uncovered,
            "applied": False,
        }
        LOGGER.info("Suppression draft: %s (%d rules; not applied)", target, len(rows))
