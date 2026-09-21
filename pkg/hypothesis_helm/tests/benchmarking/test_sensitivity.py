"""
Verify mutation sensitivity, finite differences and bounded Helm diagnostics.
"""

import json
import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.analysis.cli import main
from hypothesis_helm.analysis.sensitivity import Mutation, analyze, distance
from hypothesis_helm.schemas.contracts import mapping, sequence

SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {"a": {"type": "boolean"}, "b": {"type": "boolean"}},
    "required": ["a", "b"],
    "additionalProperties": False,
}


def test_independent_and_interacting_changes() -> None:
    """
    Detect interaction only when one parameter changes another's effect.

    Returns:
        None: Independent leaves have zero mixed difference while a conjunction does not.
    """
    mutations = [Mutation("a-on", ("a",), True), Mutation("b-on", ("b",), True)]
    independent = analyze({"a": False, "b": False}, SCHEMA, mutations, lambda values: values)
    pair = mapping(sequence(independent["interactions"])[0])
    assert pair["mixed_difference_l1"] == 0
    interacting = analyze(
        {"a": False, "b": False},
        SCHEMA,
        mutations,
        lambda values: {"enabled": values["a"] and values["b"]},
    )
    singles = [mapping(row) for row in sequence(interacting["mutations"])]
    assert all(row["distance"] == 0 for row in singles)
    assert mapping(sequence(interacting["interactions"])[0])["mixed_difference_l1"] == 2
    assert interacting["pruning_authorized"] is False


def test_sequence_can_reverse_displacement() -> None:
    """
    Keep accumulated path length distinct from endpoint displacement.

    Returns:
        None: Reversing a change returns to the baseline without erasing traveled distance.
    """
    result = analyze(
        {"a": False, "b": False},
        SCHEMA,
        [Mutation("on", ("a",), True), Mutation("off", ("a",), False)],
        lambda values: values,
    )
    assert mapping(sequence(result["interactions"])[0])["status"] == "order-dependent"
    final = mapping(sequence(result["sequence"])[-1])
    assert final["endpoint_displacement"] == 0
    assert final["cumulative_path_length"] == 4


def test_schema_rejections_and_render_errors_have_no_distance() -> None:
    """
    Record input rejection and rendering failure without converting either to zero distance.

    Returns:
        None: Failed cases are explicit and excluded from interaction arithmetic.
    """
    calls: list[dict[str, object]] = []

    def render(values: dict[str, object]) -> object:
        """
        Reject one valid combination inside the renderer.

        Args:
            values (dict[str, object]): Schema-valid configuration.

        Returns:
            object: Baseline output or a deliberate render exception.
        """
        calls.append(values)
        if values["a"]:
            raise ValueError("deliberate template failure")
        return values

    result = analyze(
        {"a": False, "b": False},
        SCHEMA,
        [Mutation("invalid", ("b",), "wrong-type"), Mutation("fails", ("a",), True)],
        render,
    )
    rows = [mapping(row) for row in sequence(result["mutations"])]
    assert [row["status"] for row in rows] == ["schema-rejected", "render-error"]
    assert all("distance" not in row for row in rows)
    assert len(calls) == 2


def test_limits_and_copy_isolation() -> None:
    """
    Bound pair work and avoid mutating source inputs or aliasing replacement objects.

    Returns:
        None: Explicit selection limits are reported and baseline values remain intact.
    """
    baseline: dict[str, object] = {"a": False, "b": False}
    result = analyze(
        baseline,
        SCHEMA,
        [Mutation("a", ("a",), True), Mutation("b", ("b",), True)],
        lambda values: values,
        max_pairs=0,
    )
    assert result["status"] == "selection-limit"
    assert result["interactions"] == []
    assert baseline == {"a": False, "b": False}
    assert distance({"items": [1, 2]}, {"items": [2, 1]}) == 4
    assert Mutation("index", ("items", 0), 3).apply({"items": [1]}) == {"items": [3]}
    with pytest.raises(ValueError):
        Mutation("negative", ("items", -1), 3).apply({"items": [1]})


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_helm_sensitivity_command(tmp_path: Path) -> None:
    """
    Measure a real Helm interaction and publish numeric evidence plus plots.

    Args:
        tmp_path (Path): Isolated chart and report directory.

    Returns:
        None: A conjunction invisible to single mutations is measured without authorizing pruning.
    """
    chart = tmp_path / "chart"
    (chart / "templates").mkdir(parents=True)
    (chart / "Chart.yaml").write_text("apiVersion: v2\nname: sensitivity\nversion: 0.1.0\n")
    (chart / "values.yaml").write_text("a: false\nb: false\n")
    (chart / "values.schema.json").write_text(json.dumps(SCHEMA))
    (chart / "templates/configmap.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: sensitivity
        data:
          enabled: "{{ if and .Values.a .Values.b }}on{{ else }}off{{ end }}"
    """).lstrip()
    )
    mutations = tmp_path / "mutations.json"
    mutations.write_text(
        json.dumps(
            [
                {"name": "a-on", "path": ["a"], "value": True},
                {"name": "b-on", "path": ["b"], "value": True},
            ]
        )
    )
    output = tmp_path / "report"
    assert main([str(chart), "--mutations", str(mutations), "--output", str(output), "--plot"]) == 0
    document = json.loads((output / "results.json").read_text())
    assert document["interactions"][0]["mixed_difference_l1"] == 2
    assert document["renders"] == 4
    assert document["pruning_authorized"] is False
    assert (output / "sensitivity.png").stat().st_size > 1000
    assert (output / "sensitivity.svg").stat().st_size > 1000
    assert (output / "README.md").is_file()


def test_coupled_values_can_be_valid_only_together() -> None:
    """
    Render joint valid inputs even when individual changes violate an input constraint.

    Returns:
        None: Joint observations survive while their unavailable finite differences are explicit.
    """
    schema = {
        **SCHEMA,
        "oneOf": [
            {"properties": {"a": {"const": False}, "b": {"const": False}}},
            {"properties": {"a": {"const": True}, "b": {"const": True}}},
        ],
    }
    result = analyze(
        {"a": False, "b": False},
        schema,
        [Mutation("a", ("a",), True), Mutation("b", ("b",), True)],
        lambda values: values,
    )
    pair = mapping(sequence(result["interactions"])[0])
    assert pair["status"] == "rendered"
    assert pair["measurement_status"] == "unavailable-reference"
    assert "mixed_difference_l1" not in pair
    assert result["renders"] == 2


def test_deadline_preserves_partial_results() -> None:
    """
    Stop admitting configurations after a slow render exhausts the budget.

    Returns:
        None: Baseline evidence survives without launching another render.
    """
    import time

    def slow(values: dict[str, object]) -> object:
        """
        Consume the small test budget in one render.

        Args:
            values (dict[str, object]): Input snapshot.

        Returns:
            object: Baseline observation.
        """
        time.sleep(0.02)
        return values

    result = analyze({"a": False, "b": False}, SCHEMA, [Mutation("a", ("a",), True)], slow, time_limit=0.01)
    assert result["status"] == "time-limit"
    assert result["renders"] == 1
    assert mapping(result["baseline"])["status"] == "rendered"
    assert result["mutations"] == []


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_dense_sensitivity_study(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Measure all distinct flips and pairs on the shared chart and retain reproducible inputs.

    Args:
        tmp_path (Path): Isolated study directory.
        monkeypatch (pytest.MonkeyPatch): Run automatic publication in an isolated checkout.

    Returns:
        None: Every requested pair has a measurement and no generated chart survives outside the retained sources.
    """
    from hypothesis_helm_benchmarking.studies.sensitivity import main as study

    monkeypatch.chdir(tmp_path)
    output = tmp_path / "studies/sensitivity"
    output.mkdir(parents=True)
    (output / "README.md").write_text("old study")
    assert study(["--inputs", "10", "--components", "4"]) == 0
    cached = next((tmp_path / ".cache/benchmarks/sensitivity").iterdir())
    result = json.loads((cached / "results.json").read_text())
    assert result["status"] == "complete"
    assert len(result["mutations"]) == len(result["sequence"]) == 10
    assert len(result["interactions"]) == result["metadata"]["expected_pairs"] == 45
    assert all(row["status"] == "rendered" and "mixed_difference_l1" in row for row in result["interactions"])
    assert len({tuple(row["mutations"]) for row in result["interactions"]}) == 45
    assert len(json.loads((cached / "mutations.json").read_text())) == 10
    assert "values.yaml" in json.loads((cached / "chart-inputs.json").read_text())
    assert not list(output.rglob("Chart.yaml"))
    report = (output / "README.md").read_text()
    assert report.index("![Sensitivity") < report.index("| ID |")
    assert "every comparable measurement" in report and "hypothesis-helm-benchmark sensitivity" in report
    assert len(list((tmp_path / ".cache/benchmarks/sensitivity").iterdir())) == 1
    assert study(["--inputs", "10", "--components", "4", "--time-limit", "0.000001"]) == 1
    assert (output / "README.md").read_text() == report
    assert len(list((tmp_path / ".cache/benchmarks/sensitivity").iterdir())) == 2
