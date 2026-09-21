"""
Verify bounded sensitivity ranking and reuse of profiling cases as real bug tests.
"""

import itertools
import json
from collections.abc import Sequence
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart, merge_values
from hypothesis_helm.charts.testing.runner import check_chart
from hypothesis_helm.exceptions.execution import TimeLimitReached
from hypothesis_helm.execution.planning.sensitivity import SensitivityOrder, mutations, validate_order
from hypothesis_helm.schemas.contracts import configuration_key, mapping


def test_larger_groups_then_more_interactions() -> None:
    """
    Rank triples before pairs and multiple pair interactions before one pair.

    Returns:
        None: Ordering uses measured structure, not configuration size alone.
    """
    defaults: dict[str, object] = dict.fromkeys("abcdxyz", False)
    probes: list[dict[str, object]] = [dict.fromkeys(group, True) for n in (1, 2, 3) for group in itertools.combinations("abcd", n)]
    weak: dict[str, object] = dict.fromkeys("abx", True)
    strong: dict[str, object] = dict.fromkeys("abdy", True)
    triple: dict[str, object] = dict.fromkeys("abcz", True)
    scheduler = SensitivityOrder([*probes, weak, strong, triple], defaults, 3, lambda: 100)

    def output(value: dict[str, object]) -> list[dict[str, object]]:
        """
        Provide independent pair and triple response fields with known nonlinearity.

        Args:
            value (dict[str, object]): Fully specified Boolean inputs.

        Returns:
            list[dict[str, object]]: Fixed manifest coordinates for each response.
        """
        return [{"ab": value["a"] and value["b"], "bd": value["b"] and value["d"], "abc": value["a"] and value["b"] and value["c"]}]

    scheduler.observe(defaults, output(defaults))
    for index in scheduler.prefix:
        value = merge_values(defaults, scheduler.values[index])
        scheduler.observe(value, output(value))
    assert list(scheduler.rank([weak, strong, triple])) == [triple, strong, weak]
    assert scheduler.report()["interacting_path_groups"] == 3
    assert scheduler.rank([strong, weak]) == [strong, weak]


def test_missing_references_are_unknown() -> None:
    """
    Leave a pair unmeasured when filtering removed one of its reference cases.

    Returns:
        None: No omitted configuration is generated or treated as a zero effect.
    """
    defaults: dict[str, object] = {"a": False, "b": False}
    values: list[dict[str, object]] = [{"a": True}, {"a": True, "b": True}]
    scheduler = SensitivityOrder(values, defaults, 2, lambda: 100)
    assert scheduler.prefix == [0]
    assert list(scheduler.traverse()) == values
    assert scheduler.report()["interacting_path_groups"] == 0
    assert scheduler.report()["unmeasured_groups"] == 1
    assert scheduler.report()["extra_test_cases"] == 0
    assert scheduler.report()["groups_missing_retained_references"] == 1


@pytest.mark.parametrize(
    ("strategy", "order", "permutations"),
    [("random", 2, 2), ("sensitivity-first", 3, 2), ("sensitivity-first", 0, 2), ("sensitivity-first", 2, None)],
)
def test_invalid_sensitivity_bound(strategy: str, order: int, permutations: int | None) -> None:
    """
    Reject analysis outside the declared bug-test interaction space.

    Args:
        strategy (str): Requested traversal.
        order (int): Invalid measurement bound.
        permutations (int | None): Bug-test interaction strength.

    Returns:
        None: Invalid combinations cannot silently change test coverage.
    """
    with pytest.raises(ValueError):
        validate_order(strategy, order, permutations)


def chart_fixture(tmp_path: Path) -> Chart:
    """
    Create a small closed Boolean chart for scheduler integration tests.

    Args:
        tmp_path (Path): Isolated chart directory.

    Returns:
        Chart: Eight configurations with a pair interaction and an unrelated path.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(
        dedent("""
        apiVersion: v2
        name: sensitivity
        version: 1.0.0
        """).lstrip()
    )
    (tmp_path / "values.yaml").write_text(
        dedent("""
        a: false
        b: false
        c: false
        """).lstrip()
    )
    (tmp_path / "templates/test.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: test
        data:
          pair: '{{ and .Values.a .Values.b }}'
          independent: '{{ .Values.c }}'
        """).lstrip()
    )
    schema = {
        "type": "object",
        "properties": {name: {"type": "boolean"} for name in "abc"},
        "required": list("abc"),
        "additionalProperties": False,
    }
    (tmp_path / "values.schema.json").write_text(json.dumps(schema))
    return Chart.load(tmp_path)


@pytest.mark.parametrize("expansion", [False, True])
def test_profile_cases_are_checked_once(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, expansion: bool) -> None:
    """
    Reuse successful checked renders in ranking, including the failure-expansion executor.

    Args:
        tmp_path (Path): Temporary chart.
        monkeypatch (pytest.MonkeyPatch): Deterministic renderer and application property.
        expansion (bool): Whether failure-region expansion is enabled.

    Returns:
        None: Every finite input is rendered and checked exactly once, with measured pair evidence.
    """
    chart = chart_fixture(tmp_path)
    rendered: list[str] = []
    tested: list[object] = []

    def render(*args: object, **kwargs: object) -> list[dict[str, object]]:
        """
        Observe inputs without requiring Helm for the scheduler accounting test.

        Args:
            *args (object): Chart and overrides.
            **kwargs (object): Renderer options.

        Returns:
            list[dict[str, object]]: A response containing one nonlinear pair.
        """
        values = merge_values(chart.defaults, mapping(args[1]))
        rendered.append(configuration_key(values))
        return [{"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": "test"}, "data": {"pair": str(values["a"] and values["b"])}}]

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", render)
    result = check_chart(
        chart,
        permutations=2,
        traversal_strategy="sensitivity-first",
        sensitivity_order=2,
        properties=(tested.append,),
        expand_failures=expansion,
    )
    assert result["status"] == "passed", result
    assert len(rendered) == len(set(rendered)) == len(tested) == 8
    evidence = mapping(result["sensitivity"])
    assert evidence["profile_cases"] == 6
    assert evidence["interacting_path_groups"] == 1
    assert evidence["measured_groups"] == 6


def test_profiling_consumes_execution_budget(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Preserve time-limit reporting when a profiling render exhausts the execution budget.

    Args:
        tmp_path (Path): Temporary chart.
        monkeypatch (pytest.MonkeyPatch): Renderer deadline injection.

    Returns:
        None: Profiling cannot run outside the chart deadline or report complete coverage.
    """
    chart = chart_fixture(tmp_path)

    def stop(*args: object, **kwargs: object) -> list[dict[str, object]]:
        """
        Stop at the same boundary as a timed-out Helm invocation.

        Args:
            *args (object): Renderer inputs.
            **kwargs (object): Renderer options.

        Returns:
            list[dict[str, object]]: No result because the shared deadline expired.
        """
        raise TimeLimitReached()

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", stop)
    result = check_chart(chart, permutations=2, traversal_strategy="sensitivity-first")
    assert result["status"] == "time-limit"
    assert mapping(result["sensitivity"])["observed_references"] == 0


def test_mutations_keep_json_types_distinct() -> None:
    """
    Preserve Boolean-versus-integer changes through nested values.

    Returns:
        None: Equality coercions cannot hide a changed input coordinate.
    """
    assert set(mutations({"nested": {"v": False}}, {"nested": {"v": 0}}).values()) == {("nested", "v")}
    assert not mutations({"a": [1]}, {"a": [1]})


@pytest.mark.parametrize("expansion", [False, True])
def test_profile_failure_is_a_bug_test(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, expansion: bool) -> None:
    """
    Keep failures discovered during profiling in the normal test report.

    Args:
        tmp_path (Path): Temporary chart.
        monkeypatch (pytest.MonkeyPatch): Deterministic response function.
        expansion (bool): Whether to continue testing after the first failed region.

    Returns:
        None: Profiling failures are reported and unsuccessful references are not scored.
    """
    chart = chart_fixture(tmp_path)
    rendered: list[str] = []

    def render(*args: object, **kwargs: object) -> list[dict[str, object]]:
        """
        Produce a known failing joint configuration.

        Args:
            *args (object): Chart and overrides.
            **kwargs (object): Renderer context.

        Returns:
            list[dict[str, object]]: Manifest with an application-specific defect marker.
        """
        values = merge_values(chart.defaults, mapping(args[1]))
        rendered.append(configuration_key(values))
        return [{"broken": bool(values["a"] and values["b"])}]

    def property_check(resources: list[dict[str, object]]) -> None:
        """
        Detect the known joint-input defect.

        Args:
            resources (list[dict[str, object]]): Rendered response.

        Returns:
            None: Valid output passes; the deliberate defect fails.
        """
        assert not resources[0]["broken"], "pair defect"

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", render)
    result = check_chart(
        chart, permutations=2, traversal_strategy="sensitivity-first", properties=(property_check,), expand_failures=expansion
    )
    assert result["status"] == "failed" and "pair defect" in str(result["error"])
    assert len(rendered) == len(set(rendered))
    assert mapping(result["sensitivity"])["interacting_path_groups"] == 0


def test_cli_rejects_analysis_above_permutations(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Reject the invalid bound before chart discovery or any rendering.

    Args:
        capsys (pytest.CaptureFixture[str]): Parser diagnostics.

    Returns:
        None: The user sees the relationship between the two independent options.
    """
    from hypothesis_helm.cli import main

    with pytest.raises(SystemExit, match="2"):
        main(["test", "missing", "--permutations", "2", "--traversal-strategy", "sensitivity-first", "--sensitivity-order", "3"])
    assert "between 1 and --permutations" in capsys.readouterr().err


def test_expansion_ranking_timeout_retains_failed_iteration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Account for the completed failure when ranking expanded work hits the deadline.

    Args:
        tmp_path (Path): Temporary finite chart.
        monkeypatch (pytest.MonkeyPatch): Failure and post-failure deadline injection.

    Returns:
        None: Every attempted bug test remains counted in the time-limit report.
    """
    chart = chart_fixture(tmp_path)
    failed = False
    rank = SensitivityOrder.rank

    def render(*args: object, **kwargs: object) -> list[dict[str, object]]:
        """
        Render a deterministic failure marker.

        Args:
            *args (object): Chart and overrides.
            **kwargs (object): Render settings.

        Returns:
            list[dict[str, object]]: Response for the current configuration.
        """
        values = merge_values(chart.defaults, mapping(args[1]))
        return [{"broken": bool(values["a"] and values["b"])}]

    def assertion(resources: list[dict[str, object]]) -> None:
        """
        Record the deliberate pair failure.

        Args:
            resources (list[dict[str, object]]): Renderer output.

        Returns:
            None: Passed checks leave the deadline enabled.
        """
        nonlocal failed
        if resources[0]["broken"]:
            failed = True
            raise AssertionError("pair defect")

    def deadline(self: SensitivityOrder, values: Sequence[dict[str, object]]) -> Sequence[dict[str, object]]:
        """
        Expire only during post-failure expansion ranking.

        Args:
            self (SensitivityOrder): Current scheduler.
            values (Sequence[dict[str, object]]): Proposed expanded candidates.

        Returns:
            Sequence[dict[str, object]]: Original ranking if no test has failed yet.
        """
        if failed:
            raise TimeLimitReached()
        return rank(self, values)

    monkeypatch.setattr("hypothesis_helm.charts.testing.runner.render", render)
    monkeypatch.setattr(SensitivityOrder, "rank", deadline)
    result = check_chart(chart, permutations=2, traversal_strategy="sensitivity-first", properties=(assertion,), expand_failures=True)
    assert result["status"] == "failed"
    assert result["stop_reason"] == "time-limit"
    assert result["minimization_complete"] is False
    assert result["completed_iterations"] == result["attempts"]
    assert result["failed_iterations"] == 1
