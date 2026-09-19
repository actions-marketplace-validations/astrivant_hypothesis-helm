"""
Keep ordering comparisons reproducible, evidence-limited and faithful to chart constraints.
"""

import copy
import itertools
from pathlib import Path

import pytest
from hypothesis_helm_benchmarking.charts.fixture import FixtureWorkspace, case_path
from hypothesis_helm_benchmarking.charts.generator import generate, reproduce
from hypothesis_helm_benchmarking.charts.ordering import nest_inputs
from hypothesis_helm_benchmarking.charts.structures import STRUCTURES
from hypothesis_helm_benchmarking.execution.ordering import Observation, methods, replay
from hypothesis_helm_benchmarking.studies.ordering import verify

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.reporting.budget import TimeLimitReached
from hypothesis_helm.schemas.combinations import plan_interactions
from hypothesis_helm.schemas.contracts import configuration_key, mapping, sequence


def measurements() -> list[Observation]:
    """
    Supply independent pair effects and one known two-path bug over eight cases.

    Returns:
        list[Observation]: Unique Boolean inputs with a passing all-false baseline.
    """
    return [
        Observation(dict(zip("abc", bits, strict=True)), [{"pair": bits[0] and bits[1]}], ("bug",) if bits[1] and bits[2] else ())
        for bits in itertools.product((False, True), repeat=3)
    ]


def document() -> dict[str, object]:
    """
    Build a small complete matrix for publication invariants.

    Returns:
        dict[str, object]: All traversal strategies at r=0..2 and two paired seeds.
    """
    return {
        "metadata": {"status": "complete", "structures": ["interactions"], "permutations": 2, "seeds": [10, 11]},
        "fixtures": {"interactions": {"cases": 8, "bug_orders": {"bug": 2}, "paths": {key: [key] for key in "abc"}}},
        "rows": [
            {"structure": "interactions", **replay(measurements(), {"bug": 2}, method, seed)} for method in methods(2) for seed in (10, 11)
        ],
    }


def test_replay_counts_profiles_without_repeated_tests() -> None:
    """
    Include failed probes in discovery while withholding their outputs from sensitivity evidence.

    Returns:
        None: Each candidate is checked once and profiling failures remain unknown measurements.
    """
    row = replay(measurements(), {"bug": 2}, "sensitivity-2", 10)
    assert row == replay(measurements(), {"bug": 2}, "sensitivity-2", 10)
    assert row["completed"] == 8 and row["found"] == 1
    trace = [mapping(point) for point in sequence(row["trace"])]
    assert len({point["case_id"] for point in trace}) == 8
    assert any(point["profiling"] and point["new_bugs"] for point in trace)
    sensitivity = mapping(row["sensitivity"])
    assert sensitivity["profile_cases"] == 6
    assert sensitivity["observed_references"] == 6
    assert sensitivity["extra_test_cases"] == 0
    assert sensitivity["unmeasured_groups"] == 1
    assert mapping(trace[-1])["distinct_paths"] == 3


@pytest.mark.parametrize("damage", ["none", "missing-run", "duplicate-case", "false-count", "missing-bug", "timeout"])
def test_publication_requires_consistent_matrix(damage: str) -> None:
    """
    Refuse incomplete or fabricated evidence rather than plotting it as complete.

    Args:
        damage (str): One intentional defect in the retained ledger.

    Returns:
        None: Only the intact population and trace pass publication.
    """
    result = document()
    rows = sequence(result["rows"])
    trace = sequence(mapping(rows[0])["trace"])
    if damage == "missing-run":
        rows.pop()
    elif damage == "duplicate-case":
        mapping(trace[-1])["case_id"] = 0
    elif damage == "false-count":
        mapping(trace[0])["found"] = 1
    elif damage == "missing-bug":
        mapping(rows[0])["found"] = 0
    elif damage == "timeout":
        mapping(result["metadata"])["status"] = "time-limit"
    if damage == "none":
        verify(result)
    else:
        with pytest.raises(AssertionError):
            verify(result)


def test_replay_honors_deadline() -> None:
    """
    Stop profiling before an expired budget can be reported as a completed trial.

    Returns:
        None: Deadline termination propagates to the study's partial-result handler.
    """

    def expired() -> float:
        """
        Raise the same deadline signal as the real executor.

        Returns:
            float: No value is returned after expiry.
        """
        raise TimeLimitReached()

    with pytest.raises(TimeLimitReached):
        replay(measurements(), {"bug": 2}, "sensitivity-2", 10, expired)


@pytest.mark.parametrize("structure", STRUCTURES)
def test_nesting_preserves_domain_and_reproduces(tmp_path: Path, structure: str) -> None:
    """
    Keep cross-field constraints and integer boundary domains intact when varying path depth.

    Args:
        tmp_path (Path): Isolated retained fixture recipes.
        structure (str): Shared generator structural family.

    Returns:
        None: Nested schemas accept the same assignments and retained recipes reproduce templates.
    """
    with FixtureWorkspace() as workspace:
        logical = tmp_path / "cases" / structure
        generate(logical, input_complexity=6, output_bins=4, structure=structure, workspace=workspace)
        original = Chart.load(workspace.chart)
        flat = {configuration_key(value) for value in plan_interactions(original.schema, 2).values}
        paths = nest_inputs(logical, workspace=workspace)
        nested = Chart.load(workspace.chart)
        received = set()
        for value in plan_interactions(nested.schema, 2).values:
            extracted: dict[str, object] = {}
            for name, path in paths.items():
                node: object = value
                for part in path:
                    node = mapping(node)[part]
                extracted[name] = node
            received.add(configuration_key(extracted))
        assert received == flat
        assert {len(path) for path in paths.values()} == {1, 2, 3}
        templates = {path.name: path.read_text() for path in (workspace.chart / "templates").iterdir()}
        defaults = copy.deepcopy(nested.defaults)
        reproduce(case_path(logical), tmp_path / "restored", workspace=workspace)
        assert Chart.load(workspace.chart).defaults == defaults
        assert {path.name: path.read_text() for path in (workspace.chart / "templates").iterdir()} == templates
