"""
Run generated Python properties inside the Helm plugin's bundled environment.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Literal

from rich.console import Console

from .output import MANIFEST_FD
from .parallel import run_parallel
from .processes import Processes


def run_suite(
    directory: Path,
    *,
    seed: int = 0,
    match: str | None = None,
    collect_only: bool = False,
    jobs: int | Literal["auto"] = "auto",
) -> int:
    """
    Execute a saved generated suite with the plugin's Python and pytest.

    Pytest output streams to Helm's console. Its exit status is preserved, including
    failures, collection errors, and empty selections. Parent pytest configuration
    and unrelated auto-loaded plugins cannot change the generated test invocation.

    Args:
        directory (Path): Directory containing the generated test module.
        seed (int): Hypothesis seed applied to every property in this invocation.
        match (str | None): Optional pytest keyword expression selecting value paths.
        collect_only (bool): Whether to list tests without invoking Helm rendering.
        jobs (int | Literal["auto"]): Fixed worker count or automatic PID throughput tuning.

    Returns:
        int: Pytest exit status, or 130 when the child is interrupted.
    """
    if isinstance(jobs, int) and jobs < 1:
        raise ValueError("jobs must be positive")
    workers = jobs if isinstance(jobs, int) else 4 * (os.process_cpu_count() or 1)
    directory = directory.resolve()
    module = directory / "test_chart_values.py"
    if not module.is_file():
        raise ValueError(f"no generated test suite found at {module}")
    (directory / "concurrency.json").unlink(missing_ok=True)
    (directory / "junit.xml").unlink(missing_ok=True)
    # A dedicated config file prevents accidental adoption of the caller's pytest
    # settings; the generated module and any suite-local conftest remain editable.
    config = directory / "hypothesis-helm.pytest.ini"
    config.write_text("[pytest]\n")
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-c",
        str(config),
        "--confcutdir",
        str(directory),
        "-p",
        "hypothesis.extra.pytestplugin",
        "-p",
        "hypothesis_helm.progress",
        "--log-cli-level=INFO",
        "--log-cli-format=[%(levelname)s] %(message)s",
        f"--hypothesis-seed={seed}",
        "--junitxml",
        str(directory / "junit.xml"),
        "-ra",
    ]
    if match is not None:
        command += ["-k", match]
    if collect_only:
        command.append("--collect-only")
    command.append(str(module))
    environment = dict(os.environ)
    environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    environment.pop("PYTEST_ADDOPTS", None)
    environment.pop("PYTEST_PLUGINS", None)
    environment.pop("HYPOTHESIS_HELM_COLLECT", None)
    environment.pop("HYPOTHESIS_HELM_PROGRESS", None)
    environment.pop("HYPOTHESIS_HELM_MANIFEST_LOCK", None)
    descriptor = MANIFEST_FD.get()
    environment.pop("HYPOTHESIS_HELM_MANIFEST_FD", None)
    if descriptor is not None:
        environment["HYPOTHESIS_HELM_MANIFEST_FD"] = str(descriptor)
    try:
        if workers > 1 and not collect_only:
            status, workers = run_parallel(
                command, directory, environment, descriptor, workers, adaptive=jobs == "auto"
            )
        else:
            workers = 1
            environment["HYPOTHESIS_HELM_PROGRESS"] = "1"
            completed = Processes().run(
                command,
                cwd=directory,
                env=environment,
                check=False,
                pass_fds=() if descriptor is None else (descriptor,),
                stdout=None if descriptor is None else sys.stderr,
            )
            status = completed.returncode if completed.returncode >= 0 else 130
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Testing interrupted")
        status = 130
    if status == 130:
        Console(stderr=True).show_cursor()
    if status == 130 and not (directory / "junit.xml").exists():
        (directory / "junit.xml").write_text(
            '<testsuites><testsuite name="hypothesis-helm" tests="0" '
            'failures="0" errors="0" skipped="0"/></testsuites>'
        )
    report = {
        "status": "interrupted"
        if status == 130
        else "collected"
        if status == 0 and collect_only
        else "passed"
        if status == 0
        else "failed",
        "exit_code": status,
        "suite": str(directory),
        "seed": seed,
        "workers": workers,
        "jobs": jobs,
        "match": match,
        "collect_only": collect_only,
        "junit": str(directory / "junit.xml"),
        "concurrency": str(directory / "concurrency.json")
        if (directory / "concurrency.json").is_file()
        else None,
    }
    (directory / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return status
