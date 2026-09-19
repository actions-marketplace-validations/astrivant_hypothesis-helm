"""
Guide generation with explicit rejection contracts and retain real Helm witness checks.
"""

from __future__ import annotations

import copy
import hashlib
import re
from collections import deque
from collections.abc import Callable, Iterator

from attrs import define, field

from hypothesis_helm.charts.model import merge_values
from hypothesis_helm.compiler.asts.contracts import Contracts, Rejection
from hypothesis_helm.schemas.contracts import configuration_key


def matches_rejection(error: str, rejection: Rejection) -> bool:
    """
    Confirm an actual Helm execution rejection with the exact chart-authored message.

    Args:
        error (str): Native Helm failure diagnostic.
        rejection (Rejection): Evaluated explicit contract.

    Returns:
        bool: Whether Helm rejected the input with this precise message.
    """
    diagnostic = re.sub(r"(?m)^Use --debug flag to render out invalid YAML\s*$", "", error).strip()
    match = re.search(r"execution error at \([^)]+\):\s*(.*)", diagnostic, re.DOTALL)
    if match is None:
        return False
    if rejection.text is not None:
        return rejection.text.matches(match[1])
    return " ".join(match[1].split()) == " ".join(rejection.message.split())


@define
class RejectionPolicy:
    """
    Track bounded witness checks, exclusions, and dependent-input adjustments per chart.

    Attributes:
        contracts (Contracts): Supported template AST and helper-call relationships.
        defaults (dict[str, object]): Chart defaults available for deterministic repair candidates.
        declared_schema (bool): Preserve failures admitted by an authored values schema.
        verify_every_candidate (bool): Require native confirmation when dependency coalescing is not modeled completely.
        records (dict[str, dict[str, object]]): Rejection evidence and bounded representative cases.
        witnesses (dict[str, set[str]]): Distinct inputs whose rejection Helm verified.
        disabled (set[str]): Contracts contradicted by native execution.
        candidates (int): Generated candidates classified as explicit rejections.
        filtered (int): Rejected candidates excluded without an accepted replacement.
        adjusted (int): Candidates replaced by a nearby schema-valid configuration.
        probes (int): Actual Helm calls made to verify rejection witnesses.
        contradictions (int): Native outcomes disagreeing with the predicted rejection.
        schema_conflicts (int): Observed rejections of inputs admitted by the declared schema.
    """

    contracts: Contracts
    defaults: dict[str, object]
    declared_schema: bool = False
    verify_every_candidate: bool = False
    records: dict[str, dict[str, object]] = field(factory=dict)
    witnesses: dict[str, set[str]] = field(factory=dict)
    disabled: set[str] = field(factory=set)
    candidates: int = 0
    filtered: int = 0
    adjusted: int = 0
    probes: int = 0
    contradictions: int = 0
    schema_conflicts: int = 0

    def preserves(self, rejection: Rejection) -> bool:
        """
        Keep authored-domain failures while allowing guidance for undeclared enum fields.

        Args:
            rejection (Rejection): Contract prediction with field-specific schema provenance.

        Returns:
            bool: The rejection must remain a finding rather than an inferred-domain exclusion.
        """
        return rejection.declared_schema or (self.declared_schema and not (rejection.enums or rejection.transformed_domains))

    def predict(self, values: dict[str, object]) -> Rejection | None:
        """
        Return an enabled contract prediction without classifying unknown branches.

        Args:
            values (dict[str, object]): Coalesced candidate configuration.

        Returns:
            Rejection | None: Supported enabled rejection or no filtering decision.
        """
        rejection = self.contracts.predict(values)
        if (
            rejection is None
            or rejection.key in self.disabled
            or (rejection.key not in self.records and len(self.records) >= self.contracts.limits["max_rejections"])
        ):
            return None
        return rejection

    def needs_probe(self, rejection: Rejection, values: dict[str, object]) -> bool:
        """
        Request native verification for initial witnesses or every candidate when required.

        Args:
            rejection (Rejection): Predicted explicit rejection.
            values (dict[str, object]): Effective input being classified.

        Returns:
            bool: Whether native verification is still needed for this witness.
        """
        seen = self.witnesses.get(rejection.key, set())
        return (
            bool(rejection.enums)
            or rejection.transformed
            or rejection.contextual
            or self.verify_every_candidate
            or (len(seen) < 2 and configuration_key(values) not in seen)
        )

    def verified(self, rejection: Rejection, values: dict[str, object]) -> None:
        """
        Retain a verified witness without ever storing it as a successful chart test.

        Args:
            rejection (Rejection): Contract that Helm also rejected.
            values (dict[str, object]): Effective rejected input.

        Returns:
            None: Witness identities and bounded explanatory examples are recorded.
        """
        seen = self.witnesses.setdefault(rejection.key, set())
        identity = configuration_key(values)
        fresh = identity not in seen
        if len(seen) < 2:
            seen.add(identity)
        record = self.records.setdefault(rejection.key, {**rejection.report(), "occurrences": 0, "examples": []})
        examples = record["examples"]
        assert isinstance(examples, list)
        if len(examples) < 2 and fresh:
            examples.append(rejection.report())

    def repair(
        self,
        values: dict[str, object],
        rejection: Rejection,
        protected: tuple[tuple[str | int, ...], ...],
        accept: Callable[[dict[str, object]], bool],
        *,
        allow_enum_changes: bool = False,
    ) -> dict[str, object] | None:
        """
        Try bounded joint changes while preserving the selected paths and complete chart schema.

        Args:
            values (dict[str, object]): Original overrides.
            rejection (Rejection): Evaluated contract and dependent paths.
            protected (tuple[tuple[str | int, ...], ...]): Selected fields that must remain unchanged.
            accept (Callable[[dict[str, object]], bool]): Schema and rejection checks on a replacement.
            allow_enum_changes (bool): Allow a sampled scalar target to select a verified allowlist member; finite cases remain fixed.

        Returns:
            dict[str, object] | None: Nearby candidate requiring real testing, or no supported repair.
        """
        if self.preserves(rejection):
            return None
        limits = self.contracts.limits

        def options(state: dict[str, object], current_rejection: Rejection) -> Iterator[tuple[tuple[str, ...], list[object]]]:
            """
            Propose small changes only to fields read by the current rejection.

            Args:
                state (dict[str, object]): Overrides at this search node.
                current_rejection (Rejection): Guard evaluated for this intermediate candidate.

            Yields:
                tuple[tuple[str, ...], list[object]]: Editable input path and deterministic alternatives.
            """
            lengths = sorted(
                {value for value in current_rejection.inputs.values() if type(value) is int and 0 <= value <= limits["max_repair_length"]}
            )
            suggestions: dict[str, list[object]] = {}
            for domain in current_rejection.transformed_domains:
                for name, choices in domain.suggestions().items():
                    suggestions.setdefault(name, []).extend(choices)
            for name in sorted(current_rejection.inputs, key=lambda name: name not in current_rejection.enums):
                value = current_rejection.inputs[name]
                path = tuple(name.removeprefix("$.").split("."))
                enums = current_rejection.enums.get(name, ())
                protected_input = any(
                    all(left == right or right == "*" for left, right in zip(path, item, strict=False)) for item in protected
                )
                if protected_input and not (allow_enum_changes and (enums or suggestions.get(name)) and path in protected):
                    continue
                default: object = self.defaults
                for key in path:
                    default = default.get(key) if isinstance(default, dict) else None
                alternatives: list[object] = list(suggestions.get(name, []))
                if enums:
                    offset = int(hashlib.sha256(f"{configuration_key(state)}:{name}".encode()).hexdigest(), 16) % len(enums)
                    alternatives.extend((*enums[offset:], *enums[:offset]))
                if default is not None:
                    alternatives.append(default)
                if type(value) is bool:
                    alternatives.append(not value)
                elif type(value) is int:
                    alternatives.extend([0, 1, value - 1, value + 1])
                elif isinstance(value, str) and not value:
                    alternatives.append("example")
                elif isinstance(value, list):
                    source = value or (default if isinstance(default, list) else [])
                    if source:
                        alternatives.extend([source[0]] * length for length in lengths)
                unique: list[object] = []
                for alternative in alternatives:
                    if not (type(alternative) is type(value) and alternative == value) and alternative not in unique:
                        unique.append(alternative)
                if unique:
                    yield path, unique

        pending = deque([(values, rejection, 0)])
        seen = {configuration_key(values)}
        attempts = 0
        while pending and attempts < limits["max_repair_attempts"]:
            state, current_rejection, depth = pending.popleft()
            local_attempts = 0
            for path, alternatives in options(state, current_rejection):
                for alternative in alternatives:
                    if local_attempts >= limits["max_repair_branch_attempts"] or attempts >= limits["max_repair_attempts"]:
                        break
                    candidate = copy.deepcopy(state)
                    current = candidate
                    for key in path[:-1]:
                        child = current.setdefault(key, {})
                        if not isinstance(child, dict):
                            break
                        current = child
                    else:
                        current[path[-1]] = copy.deepcopy(alternative)
                        identity = configuration_key(candidate)
                        if identity in seen:
                            continue
                        seen.add(identity)
                        attempts += 1
                        local_attempts += 1
                        if accept(candidate):
                            return candidate
                        if depth + 1 < limits["max_repair_depth"]:
                            following = self.predict(merge_values(self.defaults, candidate))
                            if following is not None and not self.preserves(following):
                                pending.append((candidate, following, depth + 1))
                if local_attempts >= limits["max_repair_branch_attempts"] or attempts >= limits["max_repair_attempts"]:
                    break
        return None

    def snapshot(self) -> dict[str, object]:
        """
        Report configuration exclusions independently from passes, failures, and render attempts.

        Returns:
            dict[str, object]: Counters, source requirements, bounded witnesses, and unsupported-source diagnostics.
        """
        return {
            "enabled": True,
            "max_call_depth": self.contracts.max_call_depth,
            "rejected_candidates": self.candidates,
            "filtered_candidates": self.filtered,
            "adjusted_candidates": self.adjusted,
            "verification_renders": self.probes,
            "verify_every_candidate": self.verify_every_candidate,
            "classifier_disagreements": self.contradictions,
            "declared_schema": self.declared_schema,
            "schema_conflicts": self.schema_conflicts,
            "requirements": copy.deepcopy(list(self.records.values())),
            "unsupported_sources": self.contracts.diagnostics,
            "compiler_limits": {**self.contracts.limits, "max_call_depth": self.contracts.max_call_depth},
            "analysis_fallbacks": copy.deepcopy(self.contracts.fallbacks),
            "incomplete_evaluations": self.contracts.incomplete_evaluations,
            "scope": "Explicit chart rejection contracts; unknown branches are tested normally. Not a proof of valid chart semantics.",
        }
