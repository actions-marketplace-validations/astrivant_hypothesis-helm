"""
Verify shared CI detection and concurrency defaults across their caller policies.
"""

import ast
import os
import sys
from pathlib import Path

import pytest

from hypothesis_helm import env, set_env
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.execution.runtime.environment import CI_PROVIDERS, in_ci
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.execution.workers.parallel import worker_limit


@pytest.mark.parametrize("marker", ["CI", *CI_PROVIDERS])
@pytest.mark.parametrize("value", ["", "0", " false ", "NO", " off ", "true", "1", " yes ", "https://ci.example"])
def test_ci_markers(marker: str, value: str) -> None:
    """
    Apply identical whitespace and boolean handling to every recognized marker.

    Args:
        marker (str): Generic CI flag or provider marker.
        value (str): Enabled or disabled marker value.

    Returns:
        None: Both policies agree when no explicit override conflicts with a provider.
    """
    expected = value.strip().lower() in {"true", "1", "yes", "https://ci.example"}
    assert in_ci({marker: value}) is expected
    assert in_ci({marker: value}, honor_override=False) is expected


def test_ci_reads_refreshed_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep explicit empty environments isolated and observe explicitly refreshed process settings.

    Args:
        monkeypatch (pytest.MonkeyPatch): Change process markers between calls.

    Returns:
        None: CI detection uses the shared snapshot unless an explicit mapping is supplied.
    """
    monkeypatch.setenv("CI", "true")
    refresh_env()
    assert in_ci()
    assert not in_ci({})
    monkeypatch.setenv("CI", "false")
    refresh_env()
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    refresh_env()
    assert not in_ci()
    assert in_ci(honor_override=False)


def test_refresh_preserves_imported_dictionary(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Apply additions, replacements and deletions only when the shared snapshot is refreshed.

    Args:
        monkeypatch (pytest.MonkeyPatch): Restore real process values when the test ends.

    Returns:
        None: Modules holding imported references see the same updated object.
    """
    from hypothesis_helm.execution.state import cache

    cache_env = vars(cache)["env"]

    name = "HYPOTHESIS_HELM_ENV_SNAPSHOT_TEST"
    monkeypatch.delenv(name, raising=False)
    refresh_env()
    monkeypatch.setenv(name, "first")
    assert name not in env
    assert refresh_env() is env is cache_env
    assert cache_env[name] == "first"
    monkeypatch.setenv(name, "second")
    assert env[name] == "first"
    refresh_env()
    assert cache_env[name] == "second"
    monkeypatch.delenv(name)
    assert env[name] == "second"
    refresh_env()
    assert name not in cache_env


def test_published_settings_and_child_environments(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep deliberate writes synchronized and pass cached defaults or explicit overrides to children.

    Args:
        monkeypatch (pytest.MonkeyPatch): Isolate one environment variable and its inherited state.

    Returns:
        None: Child processes use the selected snapshot and removal affects both stores.
    """
    name = "HYPOTHESIS_HELM_ENV_CHILD_TEST"
    monkeypatch.setenv(name, "")
    refresh_env()
    assert set_env(name, "published") == ""
    assert env[name] == os.environ[name] == "published"
    monkeypatch.setenv(name, "outside-change")
    command = [sys.executable, "-c", f"import os; print(os.environ.get({name!r}, 'absent'))"]
    owner = Processes()
    assert owner.run(command, capture_output=True, check=True).stdout.strip() == "published"
    assert owner.run(command, env={name: "explicit"}, capture_output=True, check=True).stdout.strip() == "explicit"
    assert owner.run(command, env={}, capture_output=True, check=True).stdout.strip() == "absent"
    assert set_env(name, None) == "published"
    assert name not in env and name not in os.environ


def test_temporary_scope_restores_both_environments(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Restore chart source identity in both stores when a scoped operation fails.

    Args:
        monkeypatch (pytest.MonkeyPatch): Restore the original source variable after the test.

    Returns:
        None: Exceptional scope exit leaves neither readers nor child processes with stale chart identity.
    """
    from hypothesis_helm.schemas.selectors import SOURCE_ENVIRONMENT, SourceScope

    monkeypatch.setenv(SOURCE_ENVIRONMENT, "original")
    refresh_env()
    with pytest.raises(RuntimeError, match="interrupted"), SourceScope("temporary"):
        assert env[SOURCE_ENVIRONMENT] == os.environ[SOURCE_ENVIRONMENT] == "temporary"
        raise RuntimeError("interrupted")
    assert env[SOURCE_ENVIRONMENT] == os.environ[SOURCE_ENVIRONMENT] == "original"


def test_application_environment_access_is_centralized() -> None:
    """
    Prevent new application readers or writers from bypassing the environment snapshot.

    Returns:
        None: Only the central environment module accesses os.environ or os.getenv directly.
    """
    packages = Path(__file__).resolve().parents[2]
    for name in ("hypothesis_helm", "hypothesis_helm_catalog", "hypothesis_helm_benchmarking"):
        for path in (packages / name).rglob("*.py"):
            if "tests" in path.parts or path == packages / "hypothesis_helm/environment.py":
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "os":
                    assert node.attr not in {"environ", "getenv", "putenv", "unsetenv"}, (path, node.lineno)
                if isinstance(node, ast.ImportFrom) and node.module == "os":
                    assert not {alias.name for alias in node.names} & {"environ", "getenv", "putenv", "unsetenv"}, path


@pytest.mark.parametrize("cpus, expected", [(None, 4), (1, 4), (8, 32)])
def test_automatic_worker_limit(cpus: int | None, expected: int, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Use available process CPUs for automatic ceilings while retaining explicit limits.

    Args:
        cpus (int | None): Available CPU count or unavailable platform result.
        expected (int): Expected automatic worker ceiling.
        monkeypatch (pytest.MonkeyPatch): Replace the process CPU probe.

    Returns:
        None: Fixed and automatic modes share a validated concurrency rule.
    """
    monkeypatch.setattr("hypothesis_helm.execution.workers.parallel.os.process_cpu_count", lambda: cpus)
    assert worker_limit("auto") == expected
    assert worker_limit(3) == 3
    with pytest.raises(ValueError, match="jobs must be positive"):
        worker_limit(0)
