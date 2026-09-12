"""Verify reproducible finite-plan thinning without false coverage claims."""

from pathlib import Path

import pytest

from hypothesis_helm.charts.runner import check_chart
from hypothesis_helm.cli import main
from hypothesis_helm.schemas.combinations import trim_values
from hypothesis_helm.schemas.contracts import mapping


def test_nested_trim() -> None:
    """
    Keep deterministic nested subsets and preserve execution order and zero defaults.

    Returns:
        None: Levels reduce counts without replacement and reject negative depths.
    """
    values: list[dict[str, object]] = [{"value": index} for index in range(64)]
    stages = [trim_values(values, level, 2026) for level in range(5)]
    assert [len(stage) for stage in stages] == [64, 16, 4, 1, 1]
    assert stages[0] is values
    for previous, current in zip(stages, stages[1:], strict=False):
        assert all(item in previous for item in current)
        assert [item["value"] for item in current] == sorted(
            int(str(item["value"])) for item in current
        )
    assert stages[1] == trim_values(values, 1, 2026)
    assert stages[1] != trim_values(values, 1, 2027)
    assert trim_values([], 100, 0) == []
    with pytest.raises(ValueError, match="nonnegative"):
        trim_values(values, -1, 0)


def test_trim_reports(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Align execution, dry-run forecasts, history deltas and coverage after thinning.

    Args:
        tmp_path (Path): Isolated report history.
        monkeypatch (pytest.MonkeyPatch): Replace rendering while retaining real planning.

    Returns:
        None: Defaults run first, omitted cases remain explicit, and coverage is incomplete.
    """
    rendered: list[dict[str, object]] = []

    def render(
        chart: object, values: dict[str, object], **kwargs: object
    ) -> list[dict[str, object]]:
        """
        Record planned cases without invoking Helm.

        Args:
            chart (object): Loaded chart.
            values (dict[str, object]): Override configuration.
            **kwargs (object): Rendering options.

        Returns:
            list[dict[str, object]]: Accepted synthetic resource.
        """
        rendered.append(values)
        return [{}]

    monkeypatch.setattr("hypothesis_helm.charts.runner.render", render)
    baseline = check_chart("examples/workload", permutations=2, artifact_dir=tmp_path)
    assert baseline["coverage_complete"] is True
    rendered.clear()
    forecast = check_chart("examples/workload", permutations=2, trim=1, dry_run=True)
    assert not rendered
    result = check_chart("examples/workload", permutations=2, trim=1, artifact_dir=tmp_path)
    assert rendered[0] == {}
    assert result["status"] == "passed"
    assert result["coverage_complete"] is False
    assert result["coverage_strategy"] == "trimmed"
    assert result["coverage_guaranteed_by_plan"] is False
    assert result["untrimmed_iterations"] == baseline["planned_iterations"]
    assert result["trimmed_iterations"] == -int(str(result["iteration_delta"]))
    assert result["completed_iterations"] == result["planned_iterations"] == len(rendered)
    assert result["remaining_iterations"] == 0
    assert forecast["planned_iterations"] == len(rendered)
    progressive = mapping(forecast["progressive_estimate"])
    assert mapping(progressive["configured_run"])["candidate_inputs"] == len(rendered)
    assert progressive["trim"] == 1


@pytest.mark.parametrize("arguments", [["--trim", "-1"], ["--trim", "1", "--paths"]])
def test_invalid_trim_cli(arguments: list[str]) -> None:
    """
    Reject invalid depths and incompatible testing modes before execution.

    Args:
        arguments (list[str]): Invalid test options.

    Returns:
        None: The CLI fails rather than silently ignoring requested thinning.
    """
    assert main(["test", "examples/workload", *arguments]) == 2
