"""
Schedule individual pytest tests with fixed or PID-controlled concurrency.
"""

import json
import logging
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path

from .feedback import ThroughputController

LOGGER = logging.getLogger(__name__)


def run_parallel(
    command: list[str],
    directory: Path,
    environment: dict[str, str],
    descriptor: int | None,
    jobs: int,
    adaptive: bool = False,
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

    Returns:
        tuple[int, int]: Aggregate exit status and number of workers used.
    """
    with tempfile.TemporaryDirectory(prefix="workers-", dir=directory) as temporary:
        workspace = Path(temporary)
        collected = workspace / "collected.json"
        collection_environment = dict(environment, HYPOTHESIS_HELM_COLLECT=str(collected))
        collection_environment.pop("HYPOTHESIS_HELM_MANIFEST_FD", None)
        collection = subprocess.run(
            [*command, "--collect-only"],
            cwd=directory,
            env=collection_environment,
            capture_output=True,
            text=True,
            check=False,
        )
        if collection.returncode:
            print(collection.stdout, end="", file=sys.stderr)
            print(collection.stderr, end="", file=sys.stderr)
            return (collection.returncode if collection.returncode > 0 else 130), 0
        nodes: list[str] = json.loads(collected.read_text())
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
            completed = subprocess.run(
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
        with ThreadPoolExecutor(max_workers=maximum, thread_name_prefix="helm-hypothesis") as pool:
            while next_index < len(nodes) or pending:
                while next_index < len(nodes) and len(pending) < controller.limit:
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
                    previous = controller.limit
                    if adaptive:
                        # A batch of simultaneous completions is not underutilization:
                        # all of these tasks ran under the pre-wait occupancy.
                        controller.completed(now, occupied, next_index < len(nodes))
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
        (directory / "concurrency.json").write_text(
            json.dumps(
                {
                    "mode": "auto" if adaptive else "fixed",
                    "maximum": maximum,
                    "peak": peak,
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
        for report in reports:
            if not report.is_file():
                statuses.append(2)
                continue
            for suite in ET.parse(report).getroot().iter("testsuite"):
                for key in totals:
                    totals[key] += int(suite.get(key, "0"))
                elapsed += float(suite.get("time", "0"))
                merged.extend(suite)
        merged.attrib.update({key: str(value) for key, value in totals.items()})
        merged.set("time", str(elapsed))
        ET.ElementTree(root).write(directory / "junit.xml", encoding="utf-8", xml_declaration=True)
        return max(statuses), peak
