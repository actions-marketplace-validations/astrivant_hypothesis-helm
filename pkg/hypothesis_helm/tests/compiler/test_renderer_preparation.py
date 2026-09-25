"""
Verify automatic renderer publication, concurrent ownership and cancellation.
"""

import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.compiler.randomness.toolchain import build, ensure, identity
from hypothesis_helm.environment import env
from hypothesis_helm.execution.runtime.processes import Processes


def test_processes_publish_one_renderer(tmp_path: Path) -> None:
    """
    Share one compiler invocation between independent Python processes using a common cache.

    Args:
        tmp_path (Path): Fake compiler and shared publication directory.

    Returns:
        None: Both callers receive the complete executable and only one compiler ran.
    """
    compiler = tmp_path / "go"
    calls = tmp_path / "calls"
    compiler.write_text(
        dedent(f"""
        #!{sys.executable}
        import sys
        import time
        from pathlib import Path
        with Path({str(calls)!r}).open("a") as output:
            output.write("compile\\n")
        time.sleep(0.2)
        Path(sys.argv[sys.argv.index("-o") + 1]).write_text("complete renderer")
        """).lstrip()
    )
    compiler.chmod(0o755)
    command = [
        sys.executable,
        "-c",
        "from pathlib import Path; import sys; from hypothesis_helm.compiler.randomness.toolchain import build; "
        "print(build(go=sys.argv[1], cache=Path(sys.argv[2])))",
        str(compiler),
        str(tmp_path / "cache"),
    ]

    def invoke(worker: int) -> str:
        """
        Run a real Python process with its own locks and interpreter state.

        Args:
            worker (int): Concurrent worker identity.

        Returns:
            str: Published executable path.
        """
        return Processes().run(command, capture_output=True, check=True, timeout=20).stdout.strip()

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(invoke, range(2)))
    assert results[0] == results[1]
    assert Path(results[0]).read_text() == "complete renderer"
    assert calls.read_text().splitlines() == ["compile"]


def test_cancelled_build_joins_compiler_and_does_not_poison_retry(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Cancel a build from its measurement coordinator and leave the cache ready for a later attempt.

    Args:
        tmp_path (Path): Fake toolchain, process evidence and output cache.
        monkeypatch (pytest.MonkeyPatch): Make the fake Go executable discoverable.

    Returns:
        None: Compiler is joined, no partial executable is published, and interruption is not cached as a build failure.
    """
    compiler = tmp_path / "go"
    marker = tmp_path / "compiler-pid"
    compiler.write_text(
        dedent(f"""
        #!{sys.executable}
        import os
        import time
        from pathlib import Path
        Path({str(marker)!r}).write_text(str(os.getpid()))
        time.sleep(30)
        """).lstrip()
    )
    compiler.chmod(0o755)
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{env.get('PATH', '')}")
    monkeypatch.chdir(tmp_path)
    stopped = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(ensure, stopped=stopped)
        second = pool.submit(ensure, stopped=stopped)
        try:
            deadline = time.monotonic() + 10
            while not marker.is_file() and time.monotonic() < deadline:
                time.sleep(0.02)
            assert marker.is_file()
        finally:
            stopped.set()
        for future in (first, second):
            with pytest.raises(InterruptedError, match="cancelled"):
                future.result(timeout=5)
    with pytest.raises(ProcessLookupError):
        os.kill(int(marker.read_text()), 0)
    target = Path(".cache/random-renderer") / identity() / "renderer"
    assert not target.exists()
    compiler.write_text(
        dedent(f"""
        #!{sys.executable}
        import sys
        from pathlib import Path
        Path(sys.argv[sys.argv.index("-o") + 1]).write_text("complete renderer")
        """).lstrip()
    )
    assert ensure().read_text() == "complete renderer"


def test_manual_build_recovers_from_automatic_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Recognize a manually prepared helper even after an automatic build failed earlier in this process.

    Args:
        tmp_path (Path): Empty automatic renderer cache.
        monkeypatch (pytest.MonkeyPatch): Select an unavailable toolchain.

    Returns:
        None: Publishing a complete helper makes it immediately available without restarting Python.
    """
    from hypothesis_helm.exceptions.rendering import RendererUnavailable

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PATH", "")
    with pytest.raises(RendererUnavailable, match="requires Go"):
        ensure()
    target = Path(".cache/random-renderer") / identity() / "renderer"
    target.parent.mkdir(parents=True)
    target.write_text("manually prepared renderer")
    assert ensure() == target.resolve()
    assert build() == target.resolve()
