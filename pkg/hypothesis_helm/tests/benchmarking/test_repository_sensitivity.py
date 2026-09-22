"""
Verify bounded per-chart sensitivity measurements and their publication evidence.
"""

import json
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest
from matplotlib.figure import Figure
from numpy.ma import getmaskarray

from hypothesis_helm.analysis.repository import measure_chart, mutations, plot_panel, prepare_figures
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.reporting.reports.figures import SENSITIVITY_FIELDS_KEY
from hypothesis_helm.schemas.contracts import mapping, sequence


def test_interaction_ticks_identify_actual_fields(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Preserve field identity and pair alignment when mutation names differ from paths.

    Args:
        tmp_path (Path): Unused figure destination under the intercepted save boundary.
        monkeypatch (pytest.MonkeyPatch): Inspect the plotted axes before rasterization.

    Returns:
        None: Numbered axes and their caption key preserve arrays, quoted keys, and an unmeasured row.
    """
    captured: list[Figure] = []
    metadata: list[dict[str, object]] = []

    def capture(figure: Figure, *args: object, **kwargs: object) -> None:
        """
        Retain the plotted axes and their embedded path key for inspection.

        Args:
            figure (Figure): Figure that would be written to disk.
            *args (object): Destination supplied to savefig.
            **kwargs (object): Save settings including PNG metadata.

        Returns:
            None: Captured data replaces image serialization in this test.
        """
        captured.append(figure)
        metadata.append(mapping(kwargs["metadata"]))

    monkeypatch.setattr(Figure, "savefig", capture)
    document: dict[str, object] = {
        "status": "complete",
        "mutations": [
            {"name": "enable", "path": ["first", "enabled"], "distance": 2},
            {"name": "resize", "path": ["pods", 2, "replicas"], "distance": 4},
            {"name": "fails", "path": ["nested.configuration", "cost$  center", "enabled"], "status": "render-error"},
        ],
        "interactions": [{"mutations": ["resize", "enable"], "mixed_difference_l1": 7}],
    }
    plot_panel(document, tmp_path / "plot.png", "chart")
    heatmap, _ = captured[0].axes  # The only other axis is the heatmap's color scale.
    assert heatmap.get_box_aspect() == heatmap.get_aspect() == 1
    expected = ["$.first.enabled", "$.pods[2].replicas", '$["nested.configuration"]["cost$  center"].enabled']
    assert [tick.get_text() for tick in heatmap.get_xticklabels()] == ["1", "2", "3"]
    assert [tick.get_text() for tick in heatmap.get_yticklabels()] == ["1", "2", "3"]
    assert json.loads(str(metadata[0][SENSITIVITY_FIELDS_KEY])) == expected
    matrix = heatmap.images[0].get_array()
    assert matrix is not None
    assert matrix[0, 1] == matrix[1, 0] == 7
    assert getmaskarray(matrix)[2].all()


def test_mutations_are_unique_reproducible_and_schema_valid() -> None:
    """
    Respect authored bounds while selecting existing Boolean and integer fields.

    Returns:
        None: A fixed seed yields nested unique-path samples without inventing strings.
    """
    values: dict[str, object] = {"enabled": False, "replicas": 1, "name": "valid-name", "items": [True]}
    schema: dict[str, object] = {
        "type": "object",
        "properties": {"replicas": {"type": "integer", "minimum": 1, "maximum": 2}},
    }
    selected = mutations(values, schema, 10, 12)
    assert len(selected) == len({item.path for item in selected}) == 3
    assert next(item.value for item in selected if item.path == ("replicas",)) == 2
    assert mutations(values, schema, 2, 12) == selected[:2]
    assert all(item.path != ("name",) for item in selected)
    assert values == {"enabled": False, "replicas": 1, "name": "valid-name", "items": [True]}


def test_renderer_preparation_precedes_measurement_budget(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Exclude first-use compilation from the per-chart sensitivity deadline.

    Args:
        tmp_path (Path): Small source chart.
        monkeypatch (pytest.MonkeyPatch): Simulate a long build without sleeping.

    Returns:
        None: Measurements retain their full time allowance after automatic preparation.
    """
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "test", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump({"a": False, "b": False}))
    clock = [0.0]
    stopped = threading.Event()

    def prepare(*args: object, **kwargs: object) -> None:
        """
        Advance the setup clock beyond the requested testing budget.

        Args:
            *args (object): Prepared chart and configured Helm executable.
            **kwargs (object): Forced preparation and cancellation signal.

        Returns:
            None: The fake renderer is ready after a lengthy setup.
        """
        assert kwargs == {"force": True, "stopped": stopped}
        clock[0] += 1000

    def render(*args: object, **kwargs: object) -> object:
        """
        Assert that the render starts with the complete measurement budget.

        Args:
            *args (object): Prepared chart and mutated values.
            **kwargs (object): Renderer options and remaining deadline.

        Returns:
            object: Stable input-shaped output.
        """
        assert clock[0] == 1000
        assert kwargs["timeout"] == 1
        return args[1]

    monkeypatch.setattr("hypothesis_helm.analysis.repository.prepare_renderer", prepare)
    monkeypatch.setattr("hypothesis_helm.analysis.repository.time", SimpleNamespace(monotonic=lambda: clock[0]))
    monkeypatch.setattr("hypothesis_helm.analysis.repository.render", render)
    result = measure_chart(tmp_path, helm="helm", limit=2, seed=0, seconds=1, stopped=stopped)
    assert result["status"] == "complete", result


@pytest.mark.parametrize("unstable", [False, True])
def test_measurements_preserve_baseline_repeatability(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, unstable: bool) -> None:
    """
    Measure an interacting pair or reject a changing baseline without fabricating sensitivity.

    Args:
        tmp_path (Path): Private source chart.
        monkeypatch (pytest.MonkeyPatch): Controlled render boundary.
        unstable (bool): Simulate nondeterministic baseline output.

    Returns:
        None: Only comparable outputs receive distances and the source chart stays unchanged.
    """
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "test", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump({"a": False, "b": False}))
    calls = 0

    def render(*args: object, **kwargs: object) -> object:
        """
        Model a conjunction whose single-input changes leave the output unchanged.

        Args:
            *args (object): Chart and candidate values.
            **kwargs (object): Rendering options.

        Returns:
            object: Stable conjunction or deliberately unstable baseline.
        """
        nonlocal calls
        calls += 1
        values = mapping(args[1])
        return {"enabled": calls if unstable else values["a"] and values["b"]}

    monkeypatch.setattr("hypothesis_helm.analysis.repository.render", render)
    result = measure_chart(tmp_path, helm="helm", limit=2, seed=0, seconds=10, stopped=threading.Event())
    if unstable:
        assert result["status"] == "unavailable"
        assert "baseline renders differed" in str(result["reason"])
        assert result["mutations"] == []
    else:
        assert result["status"] == "complete"
        assert all(mapping(item)["distance"] == 0 for item in sequence(result["mutations"]))
        assert mapping(sequence(result["interactions"])[0])["mixed_difference_l1"] == 2
    assert yamlio.load((tmp_path / "values.yaml").read_text()) == {"a": False, "b": False}


@pytest.mark.parametrize("name", ["charts/example", "charts/parent/charts/example", "."])
def test_publication_preserves_identity_and_raw_measurements(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    """
    Route a chart's measured panel to its study namespace while keeping raw data in cache.

    Args:
        tmp_path (Path): Local evidence and publication roots.
        monkeypatch (pytest.MonkeyPatch): Isolate rendering from this publication check.
        name (str): Root, nested, or repository-relative chart identity.

    Returns:
        None: Report metadata points to its own PNG and preserves the measured reason and configuration.
    """
    monkeypatch.setattr(
        "hypothesis_helm.analysis.repository.measure_chart",
        lambda *args, **kwargs: {"status": "unavailable", "reason": "No repeatable baseline", "renders": 2},
    )
    chart: dict[str, object] = {"chart": name, "status": "passed"}
    report: dict[str, object] = {"charts": [chart]}
    prepare_figures(report, output=tmp_path / "studies", cache=tmp_path / ".cache", source_root=tmp_path, repository="prometheus", jobs=2)
    published = Path(str(mapping(chart["report_figures"])["sensitivity"]))
    assert published == tmp_path / "studies/prometheus" / name.removeprefix("charts/") / "sensitivity.png"
    assert published.read_bytes().startswith(b"\x89PNG")
    saved = json.loads((tmp_path / ".cache" / name / "sensitivity.json").read_text())
    assert saved["reason"] == "No repeatable baseline"
    assert saved["context"]["chart"] == name
    assert saved["context"]["maximum_mutations"] == 8
    assert chart["status"] == "passed"  # Measurements do not rewrite scan outcomes.


def test_coordinator_joins_running_jobs_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Cancel queued work and wait for in-flight measurements after a coordinator failure.

    Args:
        tmp_path (Path): Disposable evidence destination.
        monkeypatch (pytest.MonkeyPatch): Controlled concurrent measurements.

    Returns:
        None: The running job observes cancellation and exits before the failure escapes.
    """
    started = threading.Event()
    joined = threading.Event()

    def measure(source: Path, *, stopped: threading.Event, **kwargs: object) -> dict[str, object]:
        """
        Fail one job only after another has started waiting for cancellation.

        Args:
            source (Path): Job identity.
            stopped (threading.Event): Coordinator cancellation signal.
            **kwargs (object): Measurement options.

        Returns:
            dict[str, object]: Explicit cancellation for the remaining job.
        """
        if source.name == "fails":
            assert started.wait(5)
            raise RuntimeError("publication failure")
        started.set()
        assert stopped.wait(5)
        joined.set()
        return {"status": "unavailable"}

    monkeypatch.setattr("hypothesis_helm.analysis.repository.measure_chart", measure)
    with pytest.raises(RuntimeError, match="publication failure"):
        prepare_figures(
            {"charts": [{"chart": "fails"}, {"chart": "waits"}]},
            output=tmp_path / "studies",
            cache=tmp_path / ".cache",
            source_root=tmp_path,
            jobs=2,
        )
    assert joined.is_set()
