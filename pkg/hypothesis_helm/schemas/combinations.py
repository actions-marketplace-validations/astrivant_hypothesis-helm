"""
Construct bounded suites covering finite schema interactions.
"""

from __future__ import annotations

import copy
import itertools
from collections.abc import Callable

from attrs import define
from jsonschema import validators

from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.finite import NonFiniteSchema, enumerate_values


@define
class InteractionPlan:
    """
    Store configurations and the finite factors whose interactions they cover.

    Attributes:
        values (list[dict[str, object]]): Complete schema-valid configurations.
        factors (list[tuple[str, ...]]): Paths treated as independent factors.
        domains (list[list[dict[str, object]]]): Per-factor assignments, including omission.
        strength (int): Effective interaction strength, capped at the factor count.
        interactions (int): Number of valid interactions covered by the suite.
        candidates (int): Complete configurations examined during planning.
    """

    values: list[dict[str, object]]
    factors: list[tuple[str, ...]]
    domains: list[list[dict[str, object]]]
    strength: int
    interactions: int
    candidates: int


def plan_interactions(
    schema: dict[str, object],
    strength: int,
    *,
    max_cases: int = 1000,
    max_candidates: int = 100000,
    accept: Callable[[dict[str, object]], bool] | None = None,
) -> InteractionPlan:
    """
    Cover every feasible t-way assignment without materializing the Cartesian product.

    Required closed objects are flattened into leaf factors. Optional objects and
    arrays are atomic finite factors. Constraints are checked on complete inputs;
    an interaction is infeasible only after all its completions have been rejected.
    Planning limits refuse incomplete coverage before any configuration is rendered.

    Args:
        schema (dict[str, object]): Schema defining finite configurable domains.
        strength (int): Number of factors in each interaction to cover.
        max_cases (int): Maximum configurations and values per factor.
        max_candidates (int): Maximum complete assignments examined during planning.
        accept (Callable[[dict[str, object]], bool] | None): Additional context validation.

    Returns:
        InteractionPlan: Complete coverage plan for the declared finite factors.
    """
    if strength < 1 or max_cases < 1 or max_candidates < 1:
        raise ValueError("permutations, max_cases and max_candidates must be positive")
    factors: list[tuple[str, ...]] = []
    domains: list[list[dict[str, object]]] = []
    skeleton: dict[str, object] = {}

    def discover(node: dict[str, object], path: tuple[str, ...], base: dict[str, object]) -> None:
        """
        Extract finite domains from required closed object properties.

        Args:
            node (dict[str, object]): Object schema at the current path.
            path (tuple[str, ...]): Path to the current object.
            base (dict[str, object]): Skeleton retaining required empty objects.

        Returns:
            None: Populates factors, domains and the object skeleton.
        """
        if node.get("additionalProperties") is not False or node.get("patternProperties"):
            raise NonFiniteSchema(
                f"permutations need closed objects at {path!r}; set additionalProperties: false"
            )
        required = sequence(node.get("required", []))
        for name, child in mapping(node.get("properties", {})).items():
            child_schema = mapping(child)
            child_path = (*path, name)
            if (
                name in required
                and child_schema.get("type") == "object"
                and "enum" not in child_schema
                and "const" not in child_schema
            ):
                nested: dict[str, object] = {}
                base[name] = nested
                discover(child_schema, child_path, nested)
            else:
                wrapper: dict[str, object] = {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {name: child_schema},
                    "required": [name] if name in required else [],
                }
                try:
                    choices = enumerate_values(wrapper, max_cases)
                except NonFiniteSchema as exc:
                    raise NonFiniteSchema(
                        f"cannot cover permutations at {child_path!r}: {exc}"
                    ) from exc
                factors.append(child_path)
                domains.append(choices)

    if schema.get("type") != "object":
        raise NonFiniteSchema("permutations require an object schema")
    if "enum" in schema or "const" in schema:
        raise NonFiniteSchema("root enum/const schemas should use --exhaustive")
    discover(schema, (), skeleton)
    validator = validators.validator_for(schema)(schema)
    width = min(strength, len(factors))
    # Bound the interaction inventory independently of the full Cartesian domain.
    groups = []
    inventory_size = 0
    for group in itertools.combinations(range(len(factors)), width):
        size = 1
        for index in group:
            size *= len(domains[index])
        inventory_size += size
        if inventory_size > max_candidates:
            raise NonFiniteSchema("interaction inventory exceeds --max-candidates")
        groups.append(group)
    uncovered = {
        tuple(zip(group, choices, strict=True))
        for group in groups
        for choices in itertools.product(*(range(len(domains[index])) for index in group))
    }
    values: list[dict[str, object]] = []
    covered = 0
    candidates = 0
    while uncovered:
        target = min(uncovered)
        fixed = dict(target)
        choices = [
            [fixed[index]] if index in fixed else range(len(domain))
            for index, domain in enumerate(domains)
        ]
        for row in itertools.product(*choices):
            candidates += 1
            if candidates > max_candidates:
                raise NonFiniteSchema("interaction completion search exceeds --max-candidates")
            candidate = copy.deepcopy(skeleton)
            for path, domain, choice in zip(factors, domains, row, strict=True):
                parent = candidate
                for part in path[:-1]:
                    parent = mapping(parent[part])
                parent.update(copy.deepcopy(domain[choice]))
            if not validator.is_valid(json_value(candidate)) or (
                accept is not None and not accept(candidate)
            ):
                continue
            if len(values) >= max_cases:
                raise NonFiniteSchema("interaction suite exceeds --max-cases")
            values.append(candidate)
            for group in groups:
                interaction = tuple((index, row[index]) for index in group)
                if interaction in uncovered:
                    uncovered.remove(interaction)
                    covered += 1
            break
        else:
            uncovered.remove(target)
    if not values:
        raise NonFiniteSchema("schema has no feasible configurations for permutations")
    return InteractionPlan(values, factors, domains, width, covered, candidates)
