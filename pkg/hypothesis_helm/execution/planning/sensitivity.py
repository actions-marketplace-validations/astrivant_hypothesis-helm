"""
Rank retained finite tests using interactions measured by their own manifest checks.
"""

from collections import Counter
from collections.abc import Callable, Iterator, Sequence
from itertools import combinations

from hypothesis_helm.analysis.sensitivity import features
from hypothesis_helm.charts.model import merge_values
from hypothesis_helm.schemas.contracts import configuration_key
from hypothesis_helm.schemas.generation.replay import select

__all__ = ("SensitivityOrder", "mutations", "validate_order")


def validate_order(strategy: str, order: int | None, permutations: int | None) -> int | None:
    """
    Keep sensitivity analysis inside the requested interaction coverage.

    Args:
        strategy (str): Requested traversal.
        order (int | None): User's maximum measurement order, or the pairwise default.
        permutations (int | None): Requested bug-testing interaction strength.

    Returns:
        int | None: Resolved sensitivity order, or None for another traversal.
    """
    if strategy != "sensitivity-first":
        if order is not None:
            raise ValueError("--sensitivity-order requires --traversal-strategy sensitivity-first")
        return None
    if permutations is None:
        raise ValueError("sensitivity-first requires finite --permutations testing")
    resolved = min(2, permutations) if order is None else order
    if type(resolved) is not int or not 1 <= resolved <= permutations:
        raise ValueError("--sensitivity-order must be between 1 and --permutations")
    return resolved


def mutations(before: object, after: object, path: tuple[str | int, ...] = ()) -> dict[str, tuple[str | int, ...]]:
    """
    Describe disjoint changes from a fixed baseline with exact values and typed paths.

    Args:
        before (object): Baseline subtree.
        after (object): Candidate subtree.
        path (tuple[str | int, ...]): Current values path.

    Returns:
        dict[str, tuple[str | int, ...]]: Canonical mutation identities mapped to paths.
    """
    if isinstance(before, dict) and isinstance(after, dict):
        result = {}
        for key in sorted(before.keys() | after.keys()):
            child = (*path, key)
            if key in before and key in after:
                result.update(mutations(before[key], after[key], child))
            else:
                identity = configuration_key({"path": child, "present": key in after, "value": after.get(key)})
                result[identity] = child
        return result
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return {
            key: value for i, (a, b) in enumerate(zip(before, after, strict=True)) for key, value in mutations(a, b, (*path, i)).items()
        }
    if configuration_key({"value": before}) == configuration_key({"value": after}):
        return {}
    return {configuration_key({"path": path, "present": True, "value": after}): path}


class SensitivityOrder:
    """
    Profile complete baseline-relative interaction groups already present in the retained plan.

    Profiling cases are ordinary bug tests. Their proper subsets must also be retained;
    missing references remain unknown. No additional configuration is generated.
    """

    def __init__(self, values: Sequence[dict[str, object]], defaults: dict[str, object], order: int, tick: Callable[[], float]) -> None:
        """
        Find complete measurement groups without rendering or copying candidate documents.

        Args:
            values (Sequence[dict[str, object]]): Retained candidates in seeded tie order.
            defaults (dict[str, object]): Fixed chart baseline.
            order (int): Maximum interaction order, already bounded by permutations.
            tick (Callable[[], float]): Shared execution deadline check.
        """
        self.values, self.defaults, self.order, self.tick = values, defaults, order, tick
        self.signatures: list[frozenset[str]] = []
        self.paths: dict[str, tuple[str | int, ...]] = {}
        positions: dict[frozenset[str], int] = {}
        for index, value in enumerate(values):
            tick()
            changed = mutations(defaults, merge_values(defaults, value))
            self.paths.update(changed)
            signature = frozenset(changed)
            self.signatures.append(signature)
            positions.setdefault(signature, index)
        available: set[frozenset[str]] = set(positions) | {frozenset()}
        self.groups: set[frozenset[str]] = set()
        self.incomplete_groups = 0
        for signature in positions:
            tick()
            if not 1 <= len(signature) <= order:
                continue
            if all(subset in available for subset in self.subsets(signature)):
                self.groups.add(signature)
            else:
                self.incomplete_groups += 1
        probes = {subset for group in self.groups for subset in self.subsets(group) if subset}
        self.prefix = sorted((positions[signature] for signature in probes), key=lambda index: (len(self.signatures[index]), index))
        profiled = set(self.prefix)
        self.tail = [index for index in range(len(values)) if index not in profiled]
        self.references: set[frozenset[str]] = probes | {frozenset()}
        self.observations: dict[frozenset[str], Counter[str]] = {}
        self.measured: set[frozenset[str]] = set()
        self.interactions: dict[frozenset[tuple[str | int, ...]], int] = {}
        self.effects: dict[tuple[str | int, ...], int] = {}

    def subsets(self, signature: frozenset[str]) -> Iterator[frozenset[str]]:
        """
        Visit the vertices needed for an exact mixed finite difference.

        Args:
            signature (frozenset[str]): Independent baseline-relative mutations.

        Yields:
            frozenset[str]: One subset, including the baseline and full group.
        """
        ordered = sorted(signature)
        for size in range(len(ordered) + 1):
            for subset in combinations(ordered, size):
                self.tick()
                yield frozenset(subset)

    def observe(self, effective: dict[str, object], resources: list[dict[str, object]]) -> None:
        """
        Retain output features only for successful profiling tests.

        Args:
            effective (dict[str, object]): Fully merged input that passed the configured checks.
            resources (list[dict[str, object]]): Validated manifests before custom-property mutation.

        Returns:
            None: Evidence is reused without another Helm invocation.
        """
        signature = frozenset(mutations(self.defaults, effective))
        if signature in self.references:
            self.observations[signature] = features(resources)

    def score_groups(self) -> None:
        """
        Measure complete groups; multiple values for the same paths count as one interaction.

        Returns:
            None: Missing or rejected references stay unmeasured, never zero-valued.
        """
        for group in self.groups - self.measured:
            vertices = list(self.subsets(group))
            if any(vertex not in self.observations for vertex in vertices):
                continue
            difference: Counter[str] = Counter()
            for vertex in vertices:
                sign = (-1) ** (len(group) - len(vertex))
                for feature, value in self.observations[vertex].items():
                    difference[feature] += sign * value
            magnitude = sum(abs(value) for value in difference.values())
            paths = frozenset(self.paths[key] for key in group)
            self.measured.add(group)
            if len(group) == 1:
                path = next(iter(paths))
                self.effects[path] = max(self.effects.get(path, 0), magnitude)
            elif magnitude:
                self.interactions[paths] = max(self.interactions.get(paths, 0), magnitude)

    def rank(self, values: Sequence[dict[str, object]]) -> Sequence[dict[str, object]]:
        """
        Prioritize group order, interaction count, magnitude and then individual effect.

        Args:
            values (Sequence[dict[str, object]]): Untested configurations in seeded tie order.

        Returns:
            Sequence[dict[str, object]]: The same candidates, with no additional exclusions.
        """
        self.score_groups()

        def priority(index: int) -> tuple[int, int, int, int]:
            """
            Rank one candidate using measured groups and effects of its changed paths.

            Args:
                index (int): Candidate position in the supplied sequence.

            Returns:
                tuple[int, int, int, int]: Descending priorities encoded for ascending sorting.
            """
            self.tick()
            paths = set(mutations(self.defaults, merge_values(self.defaults, values[index])).values())
            groups = [(group, size) for group, size in self.interactions.items() if group <= paths]
            return (
                -max((len(group) for group, _ in groups), default=0),
                -len(groups),
                -sum(size for _, size in groups),
                -sum(self.effects.get(path, 0) for path in paths),
            )

        return select(values, sorted(range(len(values)), key=priority))

    def initial(self) -> Sequence[dict[str, object]]:
        """
        Place reference tests first without claiming that unmeasured priorities are known.

        Returns:
            Sequence[dict[str, object]]: Profiling prefix followed by the seeded remainder.
        """
        return select(self.values, [*self.prefix, *self.tail])

    def traverse(self) -> Iterator[dict[str, object]]:
        """
        Test references once, then rank the remaining tests using their measured interactions.

        Yields:
            dict[str, object]: One retained configuration, without repeating profiling inputs.
        """
        for index in self.prefix:
            yield self.values[index]
        yield from self.rank(select(self.values, self.tail))

    def report(self) -> dict[str, object]:
        """
        Report measured evidence and unresolved groups without doing more deadline-bound work.

        Returns:
            dict[str, object]: Search size, observed references and ranking semantics.
        """
        return {
            "order": self.order,
            "profile_cases": len(self.prefix),
            "observed_references": len(self.observations),
            "eligible_groups": len(self.groups),
            "measured_groups": len(self.measured),
            "unmeasured_groups": len(self.groups - self.measured),
            "groups_missing_retained_references": self.incomplete_groups,
            "interacting_path_groups": len(self.interactions),
            "path_scores": [
                {
                    "path": list(path),
                    "largest_interaction": max((len(group) for group in self.interactions if path in group), default=0),
                    "interactions": sum(path in group for group in self.interactions),
                    "individual_effect": self.effects.get(path),
                }
                for path in sorted(set(self.paths.values()), key=lambda path: configuration_key({"path": path}))
            ],
            "priority": "group order, distinct interactions, mixed-difference magnitude, individual effect, seeded tie",
            "extra_test_cases": 0,
            "scope": "Complete baseline-relative groups in the retained finite plan; unmeasured effects are unknown",
        }
