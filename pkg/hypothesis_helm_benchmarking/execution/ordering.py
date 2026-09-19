"""
Replay observed Helm outputs through production traversal algorithms without future evidence.
"""

import math
from collections.abc import Callable

from attrs import frozen
from hypothesis_helm.charts.model import merge_values
from hypothesis_helm.execution.sensitivity import SensitivityOrder, mutations
from hypothesis_helm.execution.traversal import order_configurations
from hypothesis_helm.schemas.contracts import configuration_key


@frozen
class Observation:
    """
    Keep one actual render and its independently verified defect identities.

    Attributes:
        values (dict[str, object]): Complete schema-valid values.
        resources (list[dict[str, object]]): Parsed Helm output.
        bugs (tuple[str, ...]): Incorrect injected fields in this output.
        render_seconds (float): Time measured for this single render.
    """

    values: dict[str, object]
    resources: list[dict[str, object]]
    bugs: tuple[str, ...]
    render_seconds: float = 0


def methods(permutations: int) -> list[str]:
    """
    Include a no-profiling baseline and every permitted sensitivity order.

    Args:
        permutations (int): Maximum bug-test interaction strength.

    Returns:
        list[str]: Stable ordering labels for the matrix columns.
    """
    return ["random", "linear", "root-first", "leaf-first", *(f"sensitivity-{order}" for order in range(1, permutations + 1))]


def replay(
    observations: list[Observation],
    bug_orders: dict[str, int],
    method: str,
    seed: int,
    tick: Callable[[], float] = lambda: math.inf,
) -> dict[str, object]:
    """
    Reveal each result only when its configuration reaches the scheduler.

    Args:
        observations (list[Observation]): Retained population, with the baseline first.
        bug_orders (dict[str, int]): Fixed defect denominator and trigger orders.
        method (str): Random, structural traversal, or sensitivity-N.
        seed (int): Shared tie-breaking seed for this trial.
        tick (Callable[[], float]): Cooperative measurement deadline check.

    Returns:
        dict[str, object]: Complete iteration trace, profiling costs and discovery scores.
    """
    defaults = observations[0].values
    lookup = {configuration_key(item.values): index for index, item in enumerate(observations)}
    if len(lookup) != len(observations) or observations[0].bugs or not bug_orders:
        raise ValueError("ordering observations require unique configurations and a passing baseline")
    order = int(method.split("-")[-1]) if method.startswith("sensitivity-") else 0
    strategy = "sensitivity-first" if order else method
    values = order_configurations(
        [item.values for item in observations[1:]], lambda value: merge_values(defaults, value), defaults, strategy=strategy, seed=seed
    )
    scheduler = SensitivityOrder(values, defaults, order, tick) if order else None
    found: set[str] = set()
    paths: set[tuple[str | int, ...]] = set()
    trace: list[dict[str, object]] = []
    measured_seconds = 0.0

    def visit(value: dict[str, object], profiling: bool) -> None:
        """
        Check the scheduled input and make only its successful output available to ranking.

        Args:
            value (dict[str, object]): Next scheduled configuration.
            profiling (bool): Whether this is a nonbaseline profiling reference.

        Returns:
            None: Counters, the trace and scheduler evidence advance once.
        """
        nonlocal measured_seconds
        tick()
        case_id = lookup[configuration_key(value)]
        item = observations[case_id]
        new = set(item.bugs) - found
        found.update(item.bugs)
        changed = set(mutations(defaults, value).values())
        paths.update(changed)
        measured_seconds += item.render_seconds
        if scheduler is not None and not item.bugs:
            scheduler.observe(value, item.resources)
        trace.append(
            {
                "iteration": len(trace) + 1,
                "case_id": case_id,
                "changed_paths": [list(path) for path in sorted(changed, key=str)],
                "distinct_paths": len(paths),
                "found": len(found),
                "new_bugs": sorted(new),
                "found_by_order": {str(k): sum(bug_orders[bug] == k for bug in found) for k in sorted(set(bug_orders.values()))},
                "profiling": profiling,
                "summed_render_seconds": measured_seconds,
            }
        )

    visit(defaults, False)
    candidates = scheduler.traverse() if scheduler else iter(values)
    for index, value in enumerate(candidates):
        visit(value, scheduler is not None and index < len(scheduler.prefix))
    count = len(observations)
    early = max(1, math.ceil(count / 4))
    denominator = len(bug_orders)
    return {
        "method": method,
        "order": order,
        "seed": seed,
        "status": "complete",
        "completed": len(trace),
        "planned": count,
        "total_bugs": denominator,
        "found": len(found),
        "early_iteration": early,
        "early_recall_percent": 100 * int(str(trace[early - 1]["found"])) / denominator,
        "discovery_area_percent": 100 * sum(int(str(row["found"])) for row in trace) / (count * denominator),
        "sensitivity": scheduler.report() if scheduler else None,
        "trace": trace,
    }
