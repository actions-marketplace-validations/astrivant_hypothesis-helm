"""
Measure output sensitivity and interactions of explicit chart-value mutations.
"""

import copy
import itertools
import json
import time
from collections import Counter
from collections.abc import Callable, Sequence
from typing import cast

from attrs import define
from jsonschema import validators

from hypothesis_helm.schemas.contracts import Json, configuration_key


@define(frozen=True)
class Mutation:
    """
    Replace one value at an explicit object or array path.

    Attributes:
        name (str): Unique mutation label.
        path (tuple[str | int, ...]): Object keys and array indices.
        value (object): JSON-compatible replacement value.
    """

    name: str
    path: tuple[str | int, ...]
    value: object

    def apply(self, values: dict[str, object]) -> dict[str, object]:
        """
        Apply a replacement without modifying the original configuration.

        Args:
            values (dict[str, object]): Source configuration.

        Returns:
            dict[str, object]: Independently owned mutated configuration.
        """
        if not self.name or not self.path:
            raise ValueError("mutations need a name and a nonempty path")
        result = copy.deepcopy(values)
        node: object = result
        for part in self.path[:-1]:
            if isinstance(node, dict) and isinstance(part, str):
                node = node[part]
            elif isinstance(node, list) and type(part) is int and 0 <= part < len(node):
                node = node[part]
            else:
                raise ValueError("mutation path does not address an existing container")
        part = self.path[-1]
        if isinstance(node, dict) and isinstance(part, str):
            node[part] = copy.deepcopy(self.value)
        elif isinstance(node, list) and type(part) is int and 0 <= part < len(node):
            node[part] = copy.deepcopy(self.value)
        else:
            raise ValueError("mutation path does not address a replaceable value")
        configuration_key(result)
        return result


def features(value: object, path: tuple[str | int, ...] = ()) -> Counter[str]:
    """
    Encode manifest leaves as exact path-and-value indicators.

    Args:
        value (object): JSON manifest bundle or subtree.
        path (tuple[str | int, ...]): Current structural position.

    Returns:
        Counter[str]: One-hot leaf features, including empty containers.
    """
    result: Counter[str] = Counter()
    if isinstance(value, dict) and value:
        for key, item in value.items():
            result.update(features(item, (*path, str(key))))
    elif isinstance(value, list) and value:
        for index, item in enumerate(value):
            result.update(features(item, (*path, index)))
    else:
        result[json.dumps([path, value], sort_keys=True, allow_nan=False)] += 1
    return result


def distance(left: object, right: object) -> int:
    """
    Compute L1 displacement between leaf-indicator representations.

    Args:
        left (object): First parsed manifest bundle.
        right (object): Second parsed manifest bundle.

    Returns:
        int: Added plus removed path/value indicators; a replacement counts twice.
    """
    a, b = features(left), features(right)
    return sum(abs(a[key] - b[key]) for key in a.keys() | b.keys())


def analyze(
    baseline: dict[str, object],
    schema: dict[str, object],
    mutations: Sequence[Mutation],
    render: Callable[[dict[str, object]], object],
    *,
    max_pairs: int = 100,
    max_mutations: int = 100,
    time_limit: float = 180,
) -> dict[str, object]:
    """
    Measure single mutations, pairwise interactions and a cumulative mutation sequence.

    Args:
        baseline (dict[str, object]): Starting values configuration.
        schema (dict[str, object]): JSON Schema restricting all measured configurations.
        mutations (Sequence[Mutation]): Explicit replacement operations in sequence order.
        render (Callable[[dict[str, object]], object]): Renderer with fixed chart and invocation context.
        max_pairs (int): Maximum unordered pairs of selected mutations to examine.
        max_mutations (int): Maximum supplied mutations to examine.
        time_limit (float): Admission deadline; callers must also bound individual render invocations.

    Returns:
        dict[str, object]: Sensitivity rankings, interactions, sequence distances and explicit failures.
    """
    if max_pairs < 0 or max_mutations < 1 or not 0 < time_limit < float("inf"):
        raise ValueError("analysis limits must be nonnegative pairs, positive mutations and finite positive time")
    if not mutations or len({mutation.name for mutation in mutations}) != len(mutations):
        raise ValueError("provide at least one mutation with unique names")
    validator = validators.validator_for(schema)(schema)
    validator.validate(cast(Json, baseline))
    deadline = time.monotonic() + time_limit
    selected = list(mutations[:max_mutations])
    observations: dict[str, dict[str, object]] = {}
    singles: list[dict[str, object]] = []
    interactions: list[dict[str, object]] = []
    sequence_rows: list[dict[str, object]] = []
    input_values: dict[str, dict[str, object]] = {}
    renders = 0

    def observe(values: dict[str, object]) -> dict[str, object]:
        """
        Render a schema-valid configuration once within this analysis.

        Args:
            values (dict[str, object]): Candidate chart input.

        Returns:
            dict[str, object]: Output evidence or a schema/render failure.
        """
        nonlocal renders
        if time.monotonic() >= deadline:
            raise TimeoutError("analysis admission deadline reached")
        key = configuration_key(values)
        if key in observations:
            return observations[key]
        from jsonschema.exceptions import ValidationError

        try:
            validator.validate(cast(Json, values))
        except ValidationError as error:
            return {"status": "schema-rejected", "error": error.message}
        renders += 1
        try:
            output = render(copy.deepcopy(values))
            json.dumps(output, sort_keys=True, allow_nan=False)
            observation: dict[str, object] = {"status": "rendered", "output": output}
        except Exception as error:
            observation = {"status": "render-error", "error": str(error), "error_type": type(error).__name__}
        observations[key] = observation
        return observation

    origin: dict[str, object] = {"status": "unobserved"}
    status = "complete"
    try:
        origin = observe(baseline)
        for mutation in selected:
            row: dict[str, object] = {"name": mutation.name, "path": list(mutation.path), "value": mutation.value}
            try:
                values = mutation.apply(baseline)
            except (ValueError, KeyError, IndexError, TypeError) as error:
                singles.append({**row, "status": "invalid-mutation", "error": str(error)})
                continue
            observation = observe(values)
            row.update(observation)
            if observation["status"] == "rendered" and origin["status"] == "rendered":
                row["distance"] = distance(origin["output"], observation["output"])
            input_values[mutation.name] = values
            singles.append(row)
        for first, second in itertools.islice(itertools.combinations(selected, 2), max_pairs):
            row = {"mutations": [first.name, second.name]}
            if first.name not in input_values or second.name not in input_values:
                interactions.append({**row, "status": "unavailable-single"})
                continue
            a, b = input_values[first.name], input_values[second.name]
            try:
                ab, ba = second.apply(a), first.apply(b)
            except (ValueError, KeyError, IndexError, TypeError) as error:
                interactions.append({**row, "status": "invalid-mutation", "error": str(error)})
                continue
            if configuration_key(ab) != configuration_key(ba):
                interactions.append({**row, "status": "order-dependent"})
                continue
            joint = observe(ab)
            row.update(joint)
            observation_a, observation_b = observe(a), observe(b)
            comparable = all(item["status"] == "rendered" for item in (origin, observation_a, observation_b, joint))
            if comparable:
                fa, fb, fab, f0 = (
                    features(observation_a["output"]),
                    features(observation_b["output"]),
                    features(joint["output"]),
                    features(origin["output"]),
                )
                keys = fa.keys() | fb.keys() | fab.keys() | f0.keys()
                row["mixed_difference_l1"] = sum(abs(fab[key] - fa[key] - fb[key] + f0[key]) for key in keys)
                row["joint_distance"] = distance(origin["output"], joint["output"])
            else:
                row["measurement_status"] = "unavailable-reference"
            interactions.append(row)
        current, previous = copy.deepcopy(baseline), origin
        cumulative = 0
        for mutation in selected:
            try:
                next_values = mutation.apply(current)
            except (ValueError, KeyError, IndexError, TypeError) as error:
                sequence_rows.append({"name": mutation.name, "status": "invalid-mutation", "error": str(error)})
                break
            next_observation = observe(next_values)
            row = {"name": mutation.name, "status": next_observation["status"]}
            if next_observation["status"] != "rendered" or previous["status"] != "rendered":
                if previous["status"] != "rendered":
                    row["status"] = "preceding-output-unavailable"
                row["error"] = next_observation.get("error", "preceding output unavailable")
                sequence_rows.append(row)
                break
            step_distance = distance(previous["output"], next_observation["output"])
            cumulative += step_distance
            row.update(
                step_distance=step_distance,
                cumulative_path_length=cumulative,
                endpoint_displacement=distance(origin["output"], next_observation["output"]),
            )
            sequence_rows.append(row)
            current, previous = next_values, next_observation
    except TimeoutError:
        status = "time-limit"
    if time.monotonic() >= deadline:
        status = "time-limit"
    if status == "complete" and (len(selected) < len(mutations) or len(selected) * (len(selected) - 1) // 2 > max_pairs):
        status = "selection-limit"
    return {
        "version": 1,
        "status": status,
        "metric": "L1 of JSON path/value leaf indicators; arrays and documents remain ordered",
        "baseline": origin,
        "mutations": singles,
        "interactions": interactions,
        "sequence": sequence_rows,
        "selected_mutations": len(selected),
        "provided_mutations": len(mutations),
        "renders": renders,
        "pruning_authorized": False,
        "assumption": "The renderer is deterministic under a fixed chart, dependency and invocation context.",
    }
