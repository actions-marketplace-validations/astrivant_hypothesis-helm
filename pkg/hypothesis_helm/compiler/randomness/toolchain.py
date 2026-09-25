"""
Build the pinned Helm renderer on demand into a content-addressed local cache.
"""

import fcntl
import hashlib
import logging
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from threading import Event, Lock

from hypothesis_helm.environment import env
from hypothesis_helm.exceptions.rendering import RendererUnavailable
from hypothesis_helm.execution.runtime.processes import Processes

__all__ = ("SOURCE", "build", "ensure", "identity")

SOURCE = Path(__file__).resolve().parents[1] / "assets/renderer"
LOGGER = logging.getLogger(__name__)
_PREPARATION_LOCK = Lock()
_PREPARATION_FAILURES: dict[tuple[str, str | None], str] = {}


def _check_cancelled(stopped: Event | None) -> None:
    """
    Stop preparation when its chart or measurement coordinator is shutting down.

    Args:
        stopped (Event | None): Optional coordinator cancellation signal.

    Returns:
        None: Preparation may continue.

    Raises:
        InterruptedError: The owning coordinator requested cancellation.
    """
    if stopped is not None and stopped.is_set():
        raise InterruptedError("Controlled renderer preparation cancelled")


def ensure(*, stopped: Event | None = None) -> Path:
    """
    Prepare the current renderer automatically without retrying failed builds for every example.

    Args:
        stopped (Event | None): Measurement coordinator's cancellation signal.

    Returns:
        Path: Complete source-addressed executable shared by local workers.

    Raises:
        RendererUnavailable: Go or compilation is unavailable for this process's current toolchain.
    """
    _check_cancelled(stopped)
    binary = Path(".cache/random-renderer").resolve() / identity() / "renderer"
    if binary.is_file():
        return binary
    key = (str(binary), shutil.which("go"))
    # The thread lock shares failed attempts; build's file lock coordinates successful publication across processes.
    while not _PREPARATION_LOCK.acquire(timeout=0.1):
        _check_cancelled(stopped)
    try:
        _check_cancelled(stopped)
        if binary.is_file():
            return binary
        if key not in _PREPARATION_FAILURES:
            try:
                return build(stopped=stopped)
            except InterruptedError:
                raise
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                detail = exc.stderr if isinstance(exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
                _PREPARATION_FAILURES[key] = "Automatic controlled renderer preparation failed: " + str(detail).strip()
        raise RendererUnavailable(_PREPARATION_FAILURES[key])
    finally:
        _PREPARATION_LOCK.release()


def identity() -> str:
    """
    Identify the exact Go source, Helm dependency and transitive dependency lock.

    Returns:
        str: SHA-256 identity used for isolated build outputs and replay provenance.
    """
    digest = hashlib.sha256()
    for path in sorted(SOURCE.iterdir()):
        if path.suffix == ".go" and path.name.endswith("_test.go"):
            continue
        if path.suffix == ".go" or path.name in {"go.mod", "go.sum"}:
            digest.update(path.name.encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def build(*, go: str = "go", cache: Path = Path(".cache/random-renderer"), stopped: Event | None = None) -> Path:
    """
    Compile once and atomically publish a complete executable for concurrent local workers.

    Args:
        go (str): Go executable; Go may acquire the pinned toolchain on the first build.
        cache (Path): User-owned module, object and executable cache.
        stopped (Event | None): Cancellation signal while waiting for a build or owning the compiler process.

    Returns:
        Path: Executable whose filename identifies its complete source.
    """
    _check_cancelled(stopped)
    cache = cache.resolve()
    binary = cache / identity() / "renderer"
    if binary.is_file():
        return binary
    compiler = shutil.which(go)
    if compiler is None:
        raise ValueError("Random input testing requires Go: run hypothesis-helm-renderer --build --go /path/to/go first")
    binary.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 300
    with (binary.parent / "build.lock").open("a") as lock:
        while True:
            _check_cancelled(stopped)
            if time.monotonic() >= deadline:
                raise subprocess.TimeoutExpired([compiler, "build"], 300)
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                time.sleep(0.1)
        # A preceding worker may have published the same build while this one waited.
        if binary.is_file():
            return binary
        LOGGER.info("Preparing controlled Helm renderer; compiling once into %s", binary.parent)
        with tempfile.TemporaryDirectory(dir=binary.parent) as directory:
            output = Path(directory) / "renderer"

            def communicate(child: subprocess.Popen[str]) -> tuple[str, str]:
                """
                Drain compiler output while responding to coordinator cancellation.

                Args:
                    child (subprocess.Popen[str]): Compiler retained by its process owner.

                Returns:
                    tuple[str, str]: Complete standard output and diagnostics.

                Raises:
                    subprocess.TimeoutExpired: Preparation exceeds its build deadline.
                """
                while True:
                    _check_cancelled(stopped)
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise subprocess.TimeoutExpired(child.args, 300)
                    try:
                        return child.communicate(timeout=min(0.1, remaining))
                    except subprocess.TimeoutExpired:
                        continue

            Processes().run(
                [compiler, "build", "-mod=readonly", "-o", str(output), "."],
                cwd=SOURCE,
                env={
                    **env,
                    "GOMODCACHE": str(cache / "go/modules"),
                    "GOCACHE": str(cache / "go/build"),
                    "GOTOOLCHAIN": "auto",
                    "GOWORK": "off",
                },
                capture_output=True,
                check=True,
                timeout=max(0, deadline - time.monotonic()),
                exchange=communicate if stopped is not None else None,
            )
            output.replace(binary)
        LOGGER.info("Controlled Helm renderer ready: %s", binary)
    return binary
