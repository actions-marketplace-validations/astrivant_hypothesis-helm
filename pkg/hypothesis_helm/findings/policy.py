"""
Resolve finding controls for chart paths and isolate each candidate's check policy.
"""

from __future__ import annotations

import json
from contextlib import AbstractContextManager
from contextvars import ContextVar, Token
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING

from deepdiff import DeepDiff

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.reporting.reproductions import leaves
from hypothesis_helm.schemas.contracts import sequence
from hypothesis_helm.schemas.policy import path_parts
from hypothesis_helm.schemas.selectors import matching_rules

if TYPE_CHECKING:
    from hypothesis_helm.charts.model import Chart

ACTIVE_CODES: ContextVar[frozenset[str] | None] = ContextVar("finding_codes", default=None)


def chart_rules(chart: Path) -> list[dict[str, object]]:
    """
    Select finding controls by the exact metadata name, including isolated chart copies.

    Args:
        chart (Path): Chart source directory.

    Returns:
        list[dict[str, object]]: Matching rules; generation-only restrictions are excluded.
    """
    return [rule for rule in matching_rules(chart) if "ignored" in rule or "enabled" in rule]


def resolve_codes(rules: list[dict[str, object]], paths: tuple[tuple[str | int, ...], ...], global_codes: list[str]) -> frozenset[str]:
    """
    Apply branch overrides and require every changed path to permit suppression.

    Args:
        rules (list[dict[str, object]]): Controls for this chart.
        paths (tuple[tuple[str | int, ...], ...]): Finding path or all changed candidate paths.
        global_codes (list[str]): Run-wide disabled checks.

    Returns:
        frozenset[str]: Disabled checks; deeper rules win, with enabling winning equal-depth ties.
    """
    parsed = [(path_parts(str(rule["path"])), rule) for rule in rules]
    decisions: list[set[str]] = []
    for path in paths or ((),):
        disabled = set(global_codes)
        selected: dict[str, tuple[int, bool]] = {}
        for prefix, rule in parsed:
            if len(prefix) > len(path) or any(a != "*" and a != b for a, b in zip(prefix, path, strict=False)):
                continue
            for key, enabled in (("ignored", False), ("enabled", True)):
                for raw_code in sequence(rule.get(key, [])):
                    code = str(raw_code)
                    selected[code] = max(selected.get(code, (-1, False)), (len(prefix), enabled))
        for code, (_, enabled) in selected.items():
            if enabled:
                disabled.discard(code)
            else:
                disabled.add(code)
        decisions.append(disabled)
    return frozenset.intersection(*(frozenset(decision) for decision in decisions))


def candidate_paths(chart: Chart, values: dict[str, object]) -> tuple[tuple[str | int, ...], ...]:
    """
    Identify actual changes after Helm map merging, including dependent fields and deletions.

    Args:
        chart (Chart): Original baseline.
        values (dict[str, object]): Overrides, possibly containing unchanged baseline values.

    Returns:
        tuple[tuple[str | int, ...], ...]: Concrete changed paths; an unchanged baseline has no paths.
    """
    from hypothesis_helm.charts.model import merge_values

    before = json.loads(yamlio.json_for_helm(chart.defaults))
    after = json.loads(yamlio.json_for_helm(merge_values(chart.defaults, values)))
    diff = DeepDiff(before, after, view="tree", threshold_to_diff_deeper=0, zip_ordered_iterables=True)
    paths: set[tuple[str | int, ...]] = set()
    for kind, changes in diff.items():
        for change in changes:
            path = change.path(output_format="list")
            if kind.endswith("_added") or kind.endswith("_removed"):
                subtree = change.t2 if kind.endswith("_added") else change.t1
                paths.update(tuple(leaf) for leaf, _ in leaves(subtree, path))
            else:
                paths.add(tuple(path))
    return tuple(sorted(paths, key=repr))


class RuleScope(AbstractContextManager[None]):
    """
    Bind disabled codes to one candidate without leaking into another worker or render.
    """

    def __init__(self, codes: frozenset[str]) -> None:
        """
        Retain the resolved policy until this scope is entered.

        Args:
            codes (frozenset[str]): Candidate-specific disabled checks.
        """
        self.codes = codes
        self.token: Token[frozenset[str] | None] | None = None

    @classmethod
    def for_values(cls, chart: Chart, values: dict[str, object]) -> RuleScope:
        """
        Compute controls only when the chart has path-specific finding rules.

        Args:
            chart (Chart): Chart and its baseline values.
            values (dict[str, object]): Effective candidate overrides.

        Returns:
            RuleScope: A context that restores the caller's policy even on failure.
        """
        from hypothesis_helm.rules import AUDIT_RULES, ignored_codes

        audit_codes = {*AUDIT_RULES.values(), "HH2005"}
        rules = [
            rule
            for rule in chart_rules(chart.path)
            if any(code not in audit_codes for key in ("ignored", "enabled") for code in sequence(rule.get(key, [])))
        ]
        return cls(resolve_codes(rules, candidate_paths(chart, values) if rules else (), ignored_codes()))

    def __enter__(self) -> None:
        """
        Activate this candidate's policy.

        Returns:
            None: Nested callers see the resolved check set.
        """
        self.token = ACTIVE_CODES.set(self.codes)

    def __exit__(self, kind: type[BaseException] | None, error: BaseException | None, traceback: TracebackType | None) -> None:
        """
        Restore the prior policy without consuming exceptions.

        Args:
            kind (type[BaseException] | None): Exception type, if raised.
            error (BaseException | None): Propagating exception.
            traceback (TracebackType | None): Original traceback.

        Returns:
            None: Candidate failures continue to the owning runner.
        """
        if self.token is not None:
            ACTIVE_CODES.reset(self.token)
