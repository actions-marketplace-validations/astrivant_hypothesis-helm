"""
Exercise a shared chart queue with real interpreters, Helm renders and bounded cleanup.
"""

import json
import os
import shutil
import signal
import sys
import time
from collections.abc import Iterable
from concurrent.futures import Future, wait
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.paths import check_paths
from hypothesis_helm.cli import argument_parser
from hypothesis_helm.exceptions.execution import TimeLimitReached
from hypothesis_helm.schemas.contracts import mapping, sequence


def fixture_chart(tmp_path: Path) -> Chart:
    """
    Write eight independent non-finite paths that all affect one valid ConfigMap.

    Args:
        tmp_path (Path): Chart directory.

    Returns:
        Chart: A chart suitable for real path workers.
    """
    (tmp_path / "Chart.yaml").write_text(
        dedent("""
        apiVersion: v2
        name: workers
        version: 1.0.0
        """)
    )
    (tmp_path / "templates").mkdir()
    # Worker evidence changes while Helm loads this fixture; it is not chart input.
    (tmp_path / ".helmignore").write_text("results/\n")
    (tmp_path / "templates/config.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: workers
        data:
        {{- range $key, $value := .Values }}
          {{ $key }}: {{ $value | quote }}
        {{- end }}
        """)
    )
    defaults = {f"field{index}": index for index in range(8)}
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {key: {"type": "integer", "minimum": 0, "maximum": 100} for key in defaults},
    }
    (tmp_path / "values.yaml").write_text(json.dumps(defaults))
    (tmp_path / "values.schema.json").write_text(json.dumps(schema))
    return Chart.load(tmp_path)


def test_workers_share_one_chart_without_duplicate_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Dispatch every path once, including when more workers than paths are requested.

    Args:
        tmp_path (Path): Real Helm chart and output directory.
        monkeypatch (pytest.MonkeyPatch): Expose installed worker entry points.

    Returns:
        None: Separate processes finish ten examples per path and reconcile coverage.
    """
    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}:{os.environ['PATH']}")
    chart = fixture_chart(tmp_path)
    result = check_paths(
        chart, budget=30, max_examples=10, seed=0, helm="helm", timeout=5, artifacts=tmp_path / "results", jobs=12, filtering=True
    )
    traversal = mapping(result["traversal"])
    phases = [mapping(phase) for phase in sequence(result["phases"])]
    assert result["status"] == "passed"
    assert traversal["completed_paths"] == traversal["selected_paths"] == 8
    assert traversal["remaining_paths"] == traversal["incomplete_paths"] == 0
    assert len({tuple(sequence(phase["path"])) for phase in phases}) == 8
    assert len({phase["worker_pid"] for phase in phases}) > 1
    assert all(phase["attempts"] == 10 for phase in phases)
    assert result["attempts"] == 81
    for phase in phases:
        with pytest.raises(ProcessLookupError):
            os.kill(int(str(phase["worker_pid"])), 0)


@pytest.mark.parametrize("jobs", [1, 3])
def test_missing_chart_stops_queue_without_counterexamples(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int) -> None:
    """
    Stop serial and parallel paths when the prepared source vanishes during a render.

    Args:
        tmp_path (Path): Chart, fake Helm executable and result records.
        monkeypatch (pytest.MonkeyPatch): Supply the verified baseline and worker executable path.
        jobs (int): Serial or shared-queue execution.

    Returns:
        None: Lost input is an execution error, no shrinking occurs, and every owned worker exits.
    """
    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}:{os.environ['PATH']}")
    chart = fixture_chart(tmp_path)
    binary = tmp_path / "disappearing-helm"
    binary.write_text(
        dedent(f"""
        #!{sys.executable}
        import os
        import sys
        from pathlib import Path
        source = Path(sys.argv[3])
        (source / ("invocation-" + str(os.getpid()))).touch()
        (source / "Chart.yaml").unlink(missing_ok=True)
        sys.stderr.write("Error: unable to detect chart: Chart.yaml: no such file or directory")
        sys.exit(1)
        """).lstrip()
    )
    binary.chmod(0o755)
    monkeypatch.setattr("hypothesis_helm.charts.testing.paths.render", lambda *args, **kwargs: [{"kind": "ConfigMap"}])
    started = time.monotonic()
    result = check_paths(
        chart, budget=30, max_examples=10, seed=0, helm=str(binary), timeout=10, artifacts=tmp_path / "results", jobs=jobs, filtering=False
    )
    assert time.monotonic() - started < 20
    assert result["status"] == "error"
    assert result["error_kind"] == "execution"
    assert "Chart source unavailable" in str(result["error"])
    assert 1 <= len(list(tmp_path.glob("invocation-*"))) <= jobs
    assert mapping(result["traversal"])["completed_paths"] == 0
    assert not list((tmp_path / "results").rglob("observed-failure.json"))
    for phase in sequence(result["phases"]):
        item = mapping(phase)
        assert not item.get("code")
        if "worker_pid" in item:
            with pytest.raises(ProcessLookupError):
                os.kill(int(str(item["worker_pid"])), 0)


@pytest.mark.parametrize("stop_signal", [signal.SIGALRM, signal.SIGINT, signal.SIGTERM])
def test_deadline_stops_workers_and_helm_children(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, stop_signal: int) -> None:
    """
    End all active path processes under one budget and preserve their incomplete records.

    Args:
        tmp_path (Path): Shared chart and slow external Helm replacement.
        monkeypatch (pytest.MonkeyPatch): Supply a verified baseline and expire the timer after every child starts.
        stop_signal (int): Deadline, interactive interruption or CI termination signal.

    Returns:
        None: The deadline is shared, queued paths remain unvisited, and descendants are joined.
    """
    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}:{os.environ['PATH']}")
    chart = fixture_chart(tmp_path)
    slow = tmp_path / "slow-helm"
    slow.write_text(
        dedent(f"""
            #!{sys.executable}
            import os
            import time
            from pathlib import Path
            Path(__file__ + '.' + str(os.getpid())).touch()
            time.sleep(60)
            """).lstrip()
    )
    slow.chmod(0o755)
    monkeypatch.setattr("hypothesis_helm.charts.testing.paths.render", lambda *args, **kwargs: [{"kind": "ConfigMap"}])
    expired_at: float | None = None

    def expire_after_children_start(
        futures: Iterable[Future[int]], timeout: float | None = None
    ) -> tuple[set[Future[int]], set[Future[int]]]:
        """
        Deliver the real deadline signal after all three slow Helm children exist.

        Args:
            futures (Iterable[Future[int]]): Workers being awaited by the queue.
            timeout (float | None): Original polling or cleanup wait.

        Returns:
            tuple[set[Future[int]], set[Future[int]]]: Completed and pending futures unless the deadline interrupts polling.
        """
        nonlocal expired_at
        result = wait(futures, timeout=timeout)
        if expired_at is None and len(list(tmp_path.glob("slow-helm.*"))) == 3:
            expired_at = time.monotonic()
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.raise_signal(stop_signal)
        return result

    monkeypatch.setattr("hypothesis_helm.execution.path_queue.wait", expire_after_children_start)
    # Startup can exceed four seconds during parallel suite execution. The budget is
    # a startup watchdog; the handshake above triggers expiry at the state under test.
    result = check_paths(
        chart, budget=60, max_examples=10, seed=0, helm=str(slow), timeout=60, artifacts=tmp_path / "results", jobs=3, filtering=True
    )
    assert expired_at is not None, "Workers never reached the cleanup scenario before the startup watchdog expired"
    assert time.monotonic() - expired_at < 15
    traversal = mapping(result["traversal"])
    assert result["status"] == ("time-limit" if stop_signal == signal.SIGALRM else "interrupted")
    assert traversal["visited_paths"] == traversal["incomplete_paths"] == 3
    assert traversal["remaining_paths"] == 5
    assert traversal["completed_paths"] == 0
    children = list(tmp_path.glob("slow-helm.*"))
    assert len(children) == 3
    for marker in children:
        with pytest.raises(ProcessLookupError):
            os.kill(int(marker.suffix[1:]), 0)
    for phase in sequence(result["phases"]):
        with pytest.raises(ProcessLookupError):
            os.kill(int(str(mapping(phase)["worker_pid"])), 0)


def test_deadline_before_first_path_keeps_all_paths_unvisited(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Report a deadline during startup without inventing visited or incomplete path work.

    Args:
        tmp_path (Path): Discovered chart and report artifacts.
        monkeypatch (pytest.MonkeyPatch): Expire the execution budget at the queue boundary.

    Returns:
        None: All eight paths remain unvisited after a successful baseline and startup timeout.
    """
    chart = fixture_chart(tmp_path)
    monkeypatch.setattr("hypothesis_helm.charts.testing.paths.render", lambda *args, **kwargs: [{"kind": "ConfigMap"}])

    def expire(context: dict[str, object], directory: Path, workers: int) -> list[dict[str, object]]:
        """
        Simulate budget expiry before any path has been claimed.

        Args:
            context (dict[str, object]): Prepared chart and complete path inventory.
            directory (Path): Reserved queue directory.
            workers (int): Requested concurrent workers.

        Returns:
            list[dict[str, object]]: No records are returned because the deadline interrupts startup.
        """
        assert workers == 3
        assert len(sequence(context["paths"])) == 8
        raise TimeLimitReached()

    monkeypatch.setattr("hypothesis_helm.execution.path_queue.execute", expire)
    result = check_paths(
        chart, budget=60, max_examples=10, seed=0, helm="helm", timeout=60, artifacts=tmp_path / "results", jobs=3, filtering=True
    )
    assert result["status"] == "time-limit"
    assert mapping(result["baseline"])["status"] == "passed"
    traversal = mapping(result["traversal"])
    assert traversal["visited_paths"] == traversal["incomplete_paths"] == traversal["completed_paths"] == 0
    assert traversal["selected_paths"] == traversal["remaining_paths"] == 8
    assert not traversal["path_targets_complete"]
    assert result["phases"] == []


def test_repository_options_accept_path_workers() -> None:
    """
    Expose ten examples and a fixed worker count for local and remote repository tests.

    Returns:
        None: Both entry points accept the same per-chart worker configuration.
    """
    assert shutil.which("helm")
    for command, source in [("test", "."), ("scan", "https://example.org/charts.git")]:
        args = argument_parser().parse_args([command, source, "--jobs", "6"])
        assert args.jobs == 6 and args.max_examples == 10


def test_empty_chart_queue_starts_no_workers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Preserve the empty-work base case when a chart has no selected value paths.

    Args:
        tmp_path (Path): Empty values fixture and report directory.
        monkeypatch (pytest.MonkeyPatch): Supply a valid baseline without external rendering.

    Returns:
        None: The chart reports zero workers and no invented path work.
    """
    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}:{os.environ['PATH']}")
    chart = fixture_chart(tmp_path)
    chart.defaults = {}
    chart.schema = {"type": "object", "additionalProperties": False, "properties": {}}
    (chart.path / "templates/config.yaml").write_text("")
    monkeypatch.setattr("hypothesis_helm.charts.testing.paths.render", lambda *args, **kwargs: [{"kind": "ConfigMap"}])
    result = check_paths(
        chart, budget=5, max_examples=10, seed=0, helm="helm", timeout=1, artifacts=tmp_path / "results", jobs=6, filtering=True
    )
    assert result["workers"] == 0 and result["status"] == "passed"
    assert mapping(result["traversal"])["visited_paths"] == 0
    assert result["attempts"] == 1


@pytest.mark.parametrize("jobs", [1, 2])
def test_returned_interrupt_stops_scheduling(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int) -> None:
    """
    Preserve cancellation even when a runner returns it instead of raising an exception.

    Args:
        tmp_path (Path): Chart and partial artifacts.
        monkeypatch (pytest.MonkeyPatch): Return an interrupted path or stop before the first worker claim.
        jobs (int): Serial path iteration or parallel queue boundary.

    Returns:
        None: No later path runs and an empty interrupted queue cannot be reported as passed.
    """
    chart = fixture_chart(tmp_path)
    monkeypatch.setattr("hypothesis_helm.charts.testing.paths.render", lambda *args, **kwargs: [{"kind": "ConfigMap"}])
    calls = []

    def cancelled(*args: object, **kwargs: object) -> dict[str, object]:
        """
        Model a chart runner that records and returns its interruption.

        Args:
            *args (object): Prepared chart.
            **kwargs (object): Path execution options.

        Returns:
            dict[str, object]: Partial chart result.
        """
        calls.append(kwargs)
        return {"status": "interrupted", "attempts": 0}

    def empty_queue(context: dict[str, object], directory: Path, workers: int) -> list[dict[str, object]]:
        """
        Model cancellation after launching workers but before a path is claimed.

        Args:
            context (dict[str, object]): Shared execution settings.
            directory (Path): Queue marker directory.
            workers (int): Requested workers.

        Returns:
            list[dict[str, object]]: Empty partial work list with a separate cancellation marker.
        """
        directory.mkdir()
        (directory / "interrupted").touch()
        return []

    monkeypatch.setattr("hypothesis_helm.charts.testing.paths.check_chart", cancelled)
    monkeypatch.setattr("hypothesis_helm.execution.path_queue.execute", empty_queue)
    result = check_paths(
        chart, budget=30, max_examples=10, seed=0, helm="helm", timeout=5, artifacts=tmp_path / "results", jobs=jobs, filtering=True
    )
    assert result["status"] == "interrupted"
    assert len(calls) == (1 if jobs == 1 else 0)
    assert mapping(result["traversal"])["remaining_paths"] == (7 if jobs == 1 else 8)


def test_fail_fast_stops_claiming_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Stop the shared queue when a worker reports a failure, retaining the failing input.

    Args:
        tmp_path (Path): Chart with a failure hidden by defaults.
        monkeypatch (pytest.MonkeyPatch): Make the installed worker executable discoverable.

    Returns:
        None: The coordinator keeps the failure and leaves the rest of the queue unstarted.
    """
    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}:{os.environ['PATH']}")
    chart = fixture_chart(tmp_path)
    template = chart.path / "templates/config.yaml"
    template.write_text(
        template.read_text()
        + dedent("""
        {{- range $key, $value := .Values }}
        {{- if ne (int $value) (int (trimPrefix "field" $key)) }}
        {{- fail "changed input rejected" }}
        {{- end }}
        {{- end }}
        """)
    )
    result = check_paths(
        chart,
        budget=30,
        max_examples=10,
        seed=0,
        helm="helm",
        timeout=5,
        artifacts=tmp_path / "results",
        jobs=2,
        filtering=True,
        fail_fast=True,
    )
    assert result["status"] == "failed"
    assert mapping(result["traversal"])["remaining_paths"]
    assert any(mapping(phase)["status"] == "failed" for phase in sequence(result["phases"]))
    for phase in sequence(result["phases"]):
        with pytest.raises(ProcessLookupError):
            os.kill(int(str(mapping(phase)["worker_pid"])), 0)
