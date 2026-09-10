"""
Run generated Python properties inside the Helm plugin's bundled environment.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from .output import MANIFEST_FD


def run_suite(
    directory: Path,
    *,
    seed: int = 0,
    match: str | None = None,
    collect_only: bool = False,
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

    Returns:
        int: Pytest exit status, or 130 when the child is interrupted.
    """
    directory = directory.resolve()
    module = directory / "test_chart_values.py"
    if not module.is_file():
        raise ValueError(f"no generated test suite found at {module}")
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
    descriptor = MANIFEST_FD.get()
    environment.pop("HYPOTHESIS_HELM_MANIFEST_FD", None)
    if descriptor is not None:
        environment["HYPOTHESIS_HELM_MANIFEST_FD"] = str(descriptor)
    completed = subprocess.run(
        command,
        cwd=directory,
        env=environment,
        check=False,
        pass_fds=() if descriptor is None else (descriptor,),
        stdout=None if descriptor is None else sys.stderr,
    )
    status = completed.returncode if completed.returncode >= 0 else 130
    report = {
        "status": "collected"
        if status == 0 and collect_only
        else "passed"
        if status == 0
        else "failed",
        "exit_code": status,
        "suite": str(directory),
        "seed": seed,
        "match": match,
        "collect_only": collect_only,
        "junit": str(directory / "junit.xml"),
    }
    (directory / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return status
