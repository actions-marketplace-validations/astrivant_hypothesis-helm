"""
Build and fingerprint the shared Go catalog extractor.
"""

import hashlib
import json
import shutil
from pathlib import Path

from hypothesis_helm.environment import env
from hypothesis_helm.execution.runtime.processes import Processes

__all__ = ("TOOL", "build", "fingerprint")


TOOL = Path(__file__).with_name("upstream")


def fingerprint(directory: Path = TOOL) -> str:
    """
    Identify every compiled Go source and the pinned dependency manifests.

    Args:
        directory (Path): Catalog Go module directory.

    Returns:
        str: Stable SHA-256 digest; test-only edits do not change the extractor identity.
    """
    files = [path for path in directory.glob("*.go") if not path.name.endswith("_test.go")]
    files.extend(directory / name for name in ("go.mod", "go.sum"))
    records = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(files)}
    return hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()


def build(output: Path, cache: Path, go: str, owner: Processes, *, offline: bool) -> None:
    """
    Compile the catalog module with pinned dependencies and user-owned build caches.

    Args:
        output (Path): Destination for the private executable.
        cache (Path): Go module and build cache root.
        go (str): Go 1.25 or newer executable.
        owner (Processes): Owner responsible for subprocess cancellation and joining.
        offline (bool): Require cached dependencies and prohibit dependency downloads.

    Returns:
        None: The executable is built or the subprocess failure propagates.

    Raises:
        ValueError: The Go executable is unavailable.
    """
    binary = shutil.which(go)
    if binary is None:
        raise ValueError("Catalog rebuilds require Go 1.25 or newer; run scripts/setup-dev.sh")
    cache = cache.resolve()
    environment = {
        **env,
        "GOMODCACHE": str(cache / "go/modules"),
        "GOCACHE": str(cache / "go/build"),
        "GOTOOLCHAIN": "local",
        "GOWORK": "off",
    }
    if offline:
        environment.update(GOPROXY="off", GOSUMDB="off")
    owner.run(
        [binary, "build", "-mod=readonly", "-o", str(output.resolve()), "."],
        cwd=TOOL,
        env=environment,
        capture_output=True,
        check=True,
        timeout=300,
    )
