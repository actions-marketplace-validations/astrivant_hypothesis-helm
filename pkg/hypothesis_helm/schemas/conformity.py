"""Cache upstream Kubernetes schemas and validate each rendered manifest stream."""

import fcntl
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ENVIRONMENT = "HYPOTHESIS_HELM_CONFORMITY"
REPOSITORY = "https://github.com/yannh/kubernetes-json-schema.git"
LOGGER = logging.getLogger(__name__)


def git(directory: Path, *arguments: str) -> str:
    """
    Execute a bounded Git command without writing progress to manifest stdout.

    Args:
        directory (Path): Git working directory.
        *arguments (str): Git arguments.

    Returns:
        str: Git standard output.
    """
    result = subprocess.run(
        ["git", "-C", str(directory), *arguments], capture_output=True, text=True, timeout=180
    )
    if result.returncode:
        raise ValueError(f"schema cache git command failed: {result.stderr.strip()}")
    return result.stdout.strip()


def prepare(
    cache: Path,
    version: str,
    executable: str,
    offline: bool = False,
    *,
    read_only: bool = False,
) -> str:
    """
    Resolve a stable release and materialize strict schemas through sparse checkout.

    Args:
        cache (Path): Persistent schema cache root.
        version (str): Exact Kubernetes version or latest stable published schema version.
        executable (str): Kubeconform executable name or path.
        offline (bool): Reuse the cached repository without fetching upstream changes.
        read_only (bool): Inspect existing cache files without creating or changing them.

    Returns:
        str: Serialized validator configuration inherited by all property workers.
    """
    if version != "latest" and not re.fullmatch(r"v?\d+\.\d+\.\d+", version):
        raise ValueError("--schema-version requires latest or an exact version such as 1.35.0")
    binary = shutil.which(executable)
    if binary is None:
        raise ValueError(
            f"kubeconform executable not found: {executable}; install kubeconform first"
        )
    cache = cache.expanduser().resolve()
    if read_only:
        offline = True
    else:
        cache.mkdir(parents=True, exist_ok=True)
    with (cache / "checkout.lock").open("r" if read_only else "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_SH if read_only else fcntl.LOCK_EX)
        repository = cache / "repository"
        if not (repository / ".git").exists():
            if offline:
                raise ValueError("schema cache is empty; omit --schema-offline to populate it")
            repository.mkdir(exist_ok=True)
            git(repository, "init")
            git(repository, "remote", "add", "origin", REPOSITORY)
            git(repository, "config", "remote.origin.promisor", "true")
            git(repository, "config", "remote.origin.partialclonefilter", "blob:none")
        if not offline:
            LOGGER.info("Refreshing Kubernetes schema catalog")
            git(repository, "fetch", "--depth=1", "--filter=blob:none", "origin", "master")
        revision = git(repository, "rev-parse", "FETCH_HEAD")
        names = git(repository, "ls-tree", "--name-only", revision).splitlines()
        versions = [
            tuple(map(int, match.groups()))
            for name in names
            if (match := re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)-standalone-strict", name))
        ]
        if version == "latest":
            if not versions:
                raise ValueError("schema repository contains no stable Kubernetes releases")
            version = ".".join(map(str, max(versions)))
        version = version.removeprefix("v")
        folder = f"v{version}-standalone-strict"
        if folder not in names:
            raise ValueError(f"Kubernetes {version} has no published strict schemas")
        identity = git(repository, "rev-parse", f"{revision}:{folder}")
        snapshot = cache / "snapshots" / identity / folder
        if not snapshot.exists():
            if offline:
                raise ValueError(f"Kubernetes {version} schemas are not cached; run once online")
            LOGGER.info("Caching Kubernetes %s strict schemas with sparse checkout", version)
            git(repository, "sparse-checkout", "set", "--no-cone", f"/{folder}/")
            git(repository, "checkout", "--force", "--detach", revision)
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=snapshot.parent) as temporary:
                staged = Path(temporary) / folder
                shutil.copytree(repository / folder, staged)
                staged.replace(snapshot)
        LOGGER.info("Validating Kubernetes %s APIs using cached schemas %s", version, identity)
    return json.dumps(
        {
            "version": version,
            "identity": identity,
            "schemas": str(snapshot),
            "cache_root": str(cache),
            "executable": str(Path(binary).resolve()),
            "binary_digest": hashlib.sha256(Path(binary).read_bytes()).hexdigest(),
        }
    )


def validate(manifests: str, timeout: float) -> None:
    """
    Validate rendered YAML strictly against the selected local API schemas.

    Args:
        manifests (str): Complete rendered YAML stream.
        timeout (float): Maximum validator runtime in seconds.

    Returns:
        None: Every resource conforms, or validation raises an assertion failure.
    """
    configuration = os.environ.get(ENVIRONMENT)
    if not configuration:
        return
    settings = json.loads(configuration)
    location = settings["schemas"] + "/{{ .ResourceKind }}{{ .KindSuffix }}.json"
    try:
        result = subprocess.run(
            [
                settings["executable"],
                "-strict",
                "-n",
                "1",
                "-kubernetes-version",
                settings["version"],
                "-schema-location",
                location,
                "-output",
                "json",
            ],
            input=manifests,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError(f"kubeconform exceeded {timeout}s") from exc
    if result.returncode:
        raise AssertionError(
            f"Kubernetes {settings['version']} API schema validation failed: "
            f"{result.stdout.strip()} {result.stderr.strip()}"
        )
