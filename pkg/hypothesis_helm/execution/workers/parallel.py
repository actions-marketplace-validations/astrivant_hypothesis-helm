"""
Schedule individual pytest tests with fixed or PID-controlled concurrency.
"""

import json
import logging
import os
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Literal

from hypothesis_helm.exceptions.execution import TimeLimitReached
from hypothesis_helm.execution.planning.traversal import validate_strategy
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.execution.runtime.signals import DeferredSignals, Termination
from hypothesis_helm.execution.workers.feedback import ThroughputController
from hypothesis_helm.findings.severity import junit_stops
from hypothesis_helm.reporting.console.display import start_progress

__all__ = ("run_parallel", "worker_limit")


LOGGER = logging.getLogger(__name__)


def worker_limit(jobs: int | Literal["auto"]) -> int:
    """
    Resolve the same suite concurrency ceiling for execution and dry-run estimates.

    Args:
        jobs (int | Literal["auto"]): Fixed worker count or automatic throughput tuning.

    Returns:
        int: Positive fixed count or four times the available process CPUs.

    Raises:
        ValueError: The fixed worker count is not positive.
    """
    if isinstance(jobs, int):
        if jobs < 1:
            raise ValueError("jobs must be positive")
        return jobs
    return 4 * (os.process_cpu_count() or 1)


def run_parallel(
    command: list[str],
    directory: Path,
    environment: dict[str, str],
    descriptor: int | None,
    jobs: int,
    adaptive: bool = False,
    artifact_dir: Path | None = None,
    *,
    force_progress: bool = False,
    fail_fast: bool = False,
) -> tuple[int, int]:
    """
    Collect selected tests, schedule them individually, and combine JUnit results.

    Args:
        command (list[str]): Base pytest invocation including the suite module.
        directory (Path): Artifact directory and subprocess working directory.
        environment (dict[str, str]): Isolated child environment.
        descriptor (int | None): Inherited manifest output descriptor.
        jobs (int): Maximum number of concurrent worker threads.
        adaptive (bool): Whether throughput feedback adjusts the active worker count.
        artifact_dir (Path | None): Destination for reports, separate from the suite root.
        force_progress (bool): Force a live bar even when stderr is redirected.
        fail_fast (bool): Stop scheduling and join active children after the first failed property.

    Returns:
        tuple[int, int]: Aggregate exit status and number of workers used.
    """
    results = artifact_dir or directory
    with Termination(), tempfile.TemporaryDirectory(prefix="workers-", dir=results) as temporary:
        workspace = Path(temporary)
        collected = workspace / "collected.json"
        depths_file = workspace / "path-depths.json"
        collection_environment = dict(environment, HYPOTHESIS_HELM_COLLECT=str(collected), HYPOTHESIS_HELM_COLLECT_DEPTHS=str(depths_file))
        collection_environment.pop("HYPOTHESIS_HELM_MANIFEST_FD", None)
        # Allow pytest to clean up its own bounded external-command groups first.
        processes = Processes(interrupt_grace=5.0)
        collection = processes.run(
            [*command, "--collect-only"],
            cwd=directory,
            env=collection_environment,
            capture_output=True,
            text=True,
            check=False,
        )
        if collection.returncode == 5:
            destination = environment.get("HYPOTHESIS_HELM_SHARD_REPORT")
            if destination is not None and Path(destination).is_file():
                assignment = json.loads(Path(destination).read_text())
                if assignment["matched"] > 0 and assignment["selected"] == 0:
                    LOGGER.info("Shard has no assigned tests")
                    return 0, 0
        if collection.returncode:
            print(collection.stdout, end="", file=sys.stderr)
            print(collection.stderr, end="", file=sys.stderr)
            return (collection.returncode if collection.returncode > 0 else 130), 0
        nodes: list[str] = json.loads(collected.read_text())
        depths: dict[str, int] = json.loads(depths_file.read_text()) if depths_file.exists() else {}
        layered = validate_strategy(environment.get("HYPOTHESIS_HELM_TRAVERSAL_STRATEGY", "linear")) in {"root-first", "leaf-first"}
        if not nodes:
            return 5, 0
        maximum = min(jobs, len(nodes))
        workers = min(os.process_cpu_count() or 1, maximum) if adaptive else maximum
        started = time.monotonic()
        controller = ThroughputController(workers, maximum, started)
        LOGGER.info(
            "Running %s value-path tests with %s worker threads (%s; maximum %s)",
            len(nodes),
            workers,
            "PID auto" if adaptive else "fixed",
            maximum,
        )
        # Each process opens the same lock independently before writing a JSON line.
        # This covers manifests larger than PIPE_BUF and partial pipe writes.
        lock = workspace / "manifests.lock"
        lock.touch()
        worker_environment = dict(environment, HYPOTHESIS_HELM_MANIFEST_LOCK=str(lock))
        worker_environment.pop("HYPOTHESIS_HELM_SHARD_REPORT", None)
        worker_environment.pop("HYPOTHESIS_HELM_SAMPLING", None)
        worker_environment.pop("HYPOTHESIS_HELM_SAMPLING_REPORT", None)
        report_index = command.index("--junitxml") + 1
        reports = [workspace / f"junit-{index}.xml" for index in range(len(nodes))]

        def execute(index: int) -> tuple[int, float]:
            """
            Run one property in its own interpreter with isolated pytest state.

            Args:
                index (int): Zero-based property index.

            Returns:
                tuple[int, float]: Normalized exit status and monotonic completion time.
            """
            shard = command.copy()
            shard[report_index] = str(reports[index])
            shard[-1:] = [str(directory / nodes[index])]
            completed = processes.run(
                shard,
                cwd=directory,
                env=worker_environment,
                check=False,
                pass_fds=() if descriptor is None else (descriptor,),
                stdout=None if descriptor is None else sys.stderr,
            )
            return (completed.returncode if completed.returncode >= 0 else 130), time.monotonic()

        statuses: list[int] = []
        history: list[dict[str, object]] = []
        pending: dict[Future[tuple[int, float]], int] = {}
        next_index = 0
        peak = 0
        interrupted = False
        failed_early = False
        stop_status = 130
        progress, task = start_progress(len(nodes), workers, force=force_progress)
        pool = ThreadPoolExecutor(max_workers=maximum, thread_name_prefix="helm-hypothesis")
        try:
            while (next_index < len(nodes) or pending) and not failed_early:
                while next_index < len(nodes) and len(pending) < controller.limit:
                    if layered and pending and depths.get(nodes[next_index], 0) != depths.get(nodes[next(iter(pending.values()))], 0):
                        break
                    pending[pool.submit(execute, next_index)] = next_index
                    next_index += 1
                    peak = max(peak, len(pending))
                occupied = len(pending)
                finished, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in sorted(finished, key=lambda item: item.result()[1]):
                    active = len(pending)
                    index = pending.pop(future)
                    status, now = future.result()
                    statuses.append(status)
                    progress.update(task, advance=1, workers=controller.limit, refresh=True)
                    previous = controller.limit
                    if adaptive:
                        # A batch of simultaneous completions is not underutilization:
                        # all of these tasks ran under the pre-wait occupancy.
                        controller.completed(now, occupied, next_index < len(nodes))
                        progress.update(task, workers=controller.limit, refresh=True)
                    if controller.limit != previous:
                        LOGGER.info(
                            "PID throughput %.3f tests/s: worker target %s -> %s",
                            controller.throughput,
                            previous,
                            controller.limit,
                        )
                    history.append(
                        {
                            "test": nodes[index],
                            "exit_code": status,
                            "elapsed": now - started,
                            "active": active,
                            "target": controller.limit,
                            "throughput": controller.throughput,
                        }
                    )
                    if fail_fast and status != 0 and (status != 1 or junit_stops(reports[index])):
                        failed_early = True
                        LOGGER.info("Stopping after the first failed property (--fail)")
                        break
        except (KeyboardInterrupt, TimeLimitReached) as cancellation:
            stop_status = 124 if isinstance(cancellation, TimeLimitReached) else 130
            interrupted = True
            LOGGER.info("Interrupted; stopping active tests and preserving partial results")
        finally:
            try:
                with DeferredSignals():
                    try:
                        for future in pending:
                            future.cancel()
                        processes.stop()
                    finally:
                        try:
                            pool.shutdown(wait=True, cancel_futures=True)
                        finally:
                            if interrupted:
                                progress.update(task, description="Interrupted", workers=0)
                            progress.stop()
            except (KeyboardInterrupt, TimeLimitReached) as cancellation:
                interrupted = True
                stop_status = 124 if isinstance(cancellation, TimeLimitReached) else 130
        if interrupted or failed_early:
            for future, index in pending.items():
                if future.cancelled():
                    continue
                status, now = future.result()
                history.append(
                    {
                        "test": nodes[index],
                        "exit_code": status,
                        "elapsed": now - started,
                        "active": 0,
                        "target": 0,
                        "throughput": controller.throughput,
                    }
                )
        (results / "concurrency.json").write_text(
            json.dumps(
                {
                    "mode": "auto" if adaptive else "fixed",
                    "maximum": maximum,
                    "peak": peak,
                    "interrupted": interrupted,
                    "failed_early": failed_early,
                    "not_started": nodes[next_index:],
                    "completions": history,
                },
                indent=2,
            )
            + "\n"
        )
        root = ET.Element("testsuites")
        merged = ET.SubElement(root, "testsuite", name="hypothesis-helm")
        totals = dict.fromkeys(("tests", "failures", "errors", "skipped"), 0)
        elapsed = 0.0
        for index, report in enumerate(reports):
            try:
                document = ET.parse(report).getroot()
            except (FileNotFoundError, ET.ParseError):
                if interrupted or failed_early:
                    case = ET.SubElement(merged, "testcase", name=nodes[index])
                    ET.SubElement(
                        case, "skipped", message="Stopped after first finding" if failed_early else "Interrupted before completion"
                    )
                    totals["tests"] += 1
                    totals["skipped"] += 1
                else:
                    statuses.append(2)
                continue
            for suite in document.iter("testsuite"):
                for key in totals:
                    totals[key] += int(suite.get(key, "0"))
                elapsed += float(suite.get("time", "0"))
                merged.extend(suite)
        merged.attrib.update({key: str(value) for key, value in totals.items()})
        merged.set("time", str(elapsed))
        ET.ElementTree(root).write(results / "junit.xml", encoding="utf-8", xml_declaration=True)
        return (stop_status if interrupted else 1 if failed_early else max(statuses)), peak
