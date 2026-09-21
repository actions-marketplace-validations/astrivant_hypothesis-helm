"""
Build the pinned Helm renderer on demand into a content-addressed local cache.
"""

import fcntl
import hashlib
import shutil
import tempfile
from pathlib import Path

from hypothesis_helm.environment import env
from hypothesis_helm.execution.runtime.processes import Processes

__all__ = ("SOURCE", "build", "identity")

SOURCE = Path(__file__).resolve().parents[1] / "assets/renderer"


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


def build(*, go: str = "go", cache: Path = Path(".cache/random-renderer")) -> Path:
    """
    Compile once and atomically publish a complete executable for concurrent local workers.

    Args:
        go (str): Go executable; Go may acquire the pinned toolchain on the first build.
        cache (Path): User-owned module, object and executable cache.

    Returns:
        Path: Executable whose filename identifies its complete source.
    """
    cache = cache.resolve()
    binary = cache / identity() / "renderer"
    if binary.is_file():
        return binary
    compiler = shutil.which(go)
    if compiler is None:
        raise ValueError("Random input testing requires Go: run hypothesis-helm-renderer --build --go /path/to/go first")
    binary.parent.mkdir(parents=True, exist_ok=True)
    with (binary.parent / "build.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        # A preceding worker may have published the same build while this one waited.
        if binary.is_file():
            return binary
        with tempfile.TemporaryDirectory(dir=binary.parent) as directory:
            output = Path(directory) / "renderer"
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
                timeout=300,
            )
            output.replace(binary)
    return binary
