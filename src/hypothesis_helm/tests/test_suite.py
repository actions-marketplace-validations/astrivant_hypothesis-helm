"""
Verify the Helm-facing generated-suite workflow and failure propagation.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from hypothesis_helm.cli import main
from hypothesis_helm.generate import generate_tests
from hypothesis_helm.suite import run_suite


@pytest.mark.integration
@pytest.mark.skipif(not shutil.which("helm"), reason="Helm is required")
def test_helm_workflow_generates_and_runs(tmp_path: Path) -> None:
    """
    Run per-path properties through the same entry point used by Helm.

    Args:
        tmp_path (Path): Temporary directory receiving generated artifacts.

    Returns:
        None: Generated tests pass and the report records the invocation seed.
    """
    assert (
        main(
            [
                "test",
                "examples/workload",
                "--max-examples",
                "3",
                "--seed",
                "42",
                "--artifact-dir",
                str(tmp_path),
            ]
        )
        == 0
    )
    report = json.loads((tmp_path / "report.json").read_text())
    assert report["status"] == "passed"
    assert report["seed"] == 42
    assert (tmp_path / "test_chart_values.py").is_file()
    assert 'tests="4"' in (tmp_path / "junit.xml").read_text()


@pytest.mark.integration
@pytest.mark.skipif(not shutil.which("helm"), reason="Helm is required")
def test_helm_workflow_returns_chart_failure(tmp_path: Path) -> None:
    """
    Preserve a failing generated property's exit status through the Helm CLI.

    Args:
        tmp_path (Path): Temporary directory receiving failure artifacts.

    Returns:
        None: The broken replica lever fails and its counterexample reaches JUnit.
    """
    assert (
        main(["test", "examples/broken", "--max-examples", "5", "--artifact-dir", str(tmp_path)])
        == 1
    )
    assert "replicas=0" in (tmp_path / "junit.xml").read_text()
    assert json.loads((tmp_path / "report.json").read_text())["exit_code"] == 1


def test_saved_suite_isolated_from_parent_pytest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Collect a saved suite without adopting unrelated pytest flags or plugins.

    Args:
        tmp_path (Path): Temporary directory containing the saved suite.
        monkeypatch (pytest.MonkeyPatch): Fixture restoring caller environment settings.

    Returns:
        None: Selection works and an empty selection remains a nonzero result.
    """
    generate_tests("examples/workload", tmp_path, max_examples=2)
    monkeypatch.setenv("PYTEST_ADDOPTS", "--invalid-parent-option")
    monkeypatch.setenv("PYTEST_PLUGINS", "nonexistent_parent_plugin")
    assert main(["run", str(tmp_path), "--collect-only", "--match", "replicas"]) == 0
    assert main(["run", str(tmp_path), "--collect-only", "--match", "nonexistent_path"]) == 5


def test_render_flags_are_embedded(tmp_path: Path) -> None:
    """
    Preserve Helm rendering flags when generating tests through the CLI.

    Args:
        tmp_path (Path): Temporary directory receiving generated Python tests.

    Returns:
        None: Generated options contain the selected rendering environment.
    """
    assert (
        main(
            [
                "test",
                "examples/workload",
                "--collect-only",
                "--timeout",
                "7",
                "--release",
                "example",
                "--namespace",
                "testing",
                "--kube-version",
                "1.31.0",
                "--helm",
                "/custom/helm",
                "--allow-empty",
                "--artifact-dir",
                str(tmp_path),
            ]
        )
        == 0
    )
    source = (tmp_path / "test_chart_values.py").read_text()
    for expected in (
        "'timeout': 7.0",
        "'helm': '/custom/helm'",
        "'namespace': 'testing'",
        "'release': 'example'",
        "'kube_version': '1.31.0'",
        "'allow_empty': True",
    ):
        assert expected in source


def test_runner_uses_own_interpreter(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Use the plugin interpreter rather than a pytest executable on the caller's PATH.

    Args:
        tmp_path (Path): Temporary directory containing the generated module.
        monkeypatch (pytest.MonkeyPatch): Fixture restoring the subprocess boundary.

    Returns:
        None: The subprocess uses this interpreter and preserves collection failures.
    """
    (tmp_path / "test_chart_values.py").write_text("# saved suite\n")
    calls: list[list[str]] = []

    def execute(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """
        Record the subprocess command and emulate a collection failure.

        Args:
            command (list[str]): Pytest invocation assembled by the runner.
            **kwargs (object): Subprocess execution options.

        Returns:
            subprocess.CompletedProcess[str]: Failed pytest process result.
        """
        calls.append(command)
        return subprocess.CompletedProcess(command, 2)

    monkeypatch.setattr(subprocess, "run", execute)
    assert run_suite(tmp_path) == 2
    assert calls[0][:3] == [sys.executable, "-m", "pytest"]


def test_missing_suite_is_an_error(tmp_path: Path) -> None:
    """
    Reject a nonexistent saved suite before invoking pytest.

    Args:
        tmp_path (Path): Directory with no generated Python module.

    Returns:
        None: The Helm command reports a setup error.
    """
    assert main(["run", str(tmp_path)]) == 2
