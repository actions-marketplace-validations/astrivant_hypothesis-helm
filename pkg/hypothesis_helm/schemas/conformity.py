"""
Cache upstream Kubernetes schemas and validate each rendered manifest stream.
"""

import fcntl
import hashlib
import json
import logging
import os
import re
import shutil
import tempfile
import time
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path

from jsonschema import FormatChecker, ValidationError, validators
from jsonschema.protocols import Validator

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.execution.processes import Processes
from hypothesis_helm.rules import ignored
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.policy import check_schema
from hypothesis_helm.schemas.resources import validate_custom

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
    result = Processes().run(["git", "-C", str(directory), *arguments], capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise ValueError(f"schema cache git command failed: {result.stderr.strip()}")
    return result.stdout.strip()


def memory_snapshot(snapshot: Path) -> Path:
    """
    Stage an immutable schema snapshot on an explicitly configured Linux tmpfs.

    Args:
        snapshot (Path): Selected persistent schema snapshot.

    Returns:
        Path: Atomic memory copy, or the original snapshot when staging is disabled.
    """
    setting = os.environ.get("HYPOTHESIS_HELM_SCHEMA_MEMORY_DIR", "")
    if not setting:
        return snapshot
    root = Path(setting).expanduser().resolve()
    ancestor = root
    while not ancestor.exists():
        ancestor = ancestor.parent
    result = Processes().run(
        ["stat", "-f", "-c", "%T", str(ancestor)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode or result.stdout.strip() != "tmpfs":
        raise ValueError("HYPOTHESIS_HELM_SCHEMA_MEMORY_DIR must reside on a Linux tmpfs mount")
    root.mkdir(parents=True, exist_ok=True)
    with (root / "staging.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        target = root / snapshot.parent.name / snapshot.name
        if not target.exists():
            block = os.statvfs(root).f_frsize
            required = sum(((path.stat().st_size + block - 1) // block) * block for path in snapshot.rglob("*") if path.is_file())
            if required > shutil.disk_usage(root).free:
                raise ValueError(f"schema tmpfs needs at least {required} free bytes: {root}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
                staged = Path(temporary) / snapshot.name
                shutil.copytree(snapshot, staged)
                staged.replace(target)
            LOGGER.info("Staged Kubernetes schemas on tmpfs: %s (%s bytes)", target, required)
        return target


def prepare(
    cache: Path,
    version: str,
    offline: bool = False,
    *,
    read_only: bool = False,
    revision: str | None = None,
) -> str:
    """
    Resolve a stable release and materialize strict schemas through sparse checkout.

    Args:
        cache (Path): Persistent schema cache root.
        version (str): Exact Kubernetes version or latest stable published schema version.
        offline (bool): Reuse the cached repository without fetching upstream changes.
        read_only (bool): Inspect existing cache files without creating or changing them.
        revision (str | None): Immutable upstream commit for reproducible catalog rebuilding, or the current schema branch.

    Returns:
        str: Serialized validator configuration inherited by all property workers.
    """
    if version != "latest" and not re.fullmatch(r"v?\d+\.\d+\.\d+", version):
        raise ValueError("--schema-version requires latest or an exact version such as 1.35.0")
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
            git(repository, "fetch", "--depth=1", "--filter=blob:none", "origin", revision or "master")
        revision = git(repository, "rev-parse", revision or "FETCH_HEAD")
        names = git(repository, "ls-tree", "--name-only", revision).splitlines()
        versions = [
            tuple(map(int, match.groups())) for name in names if (match := re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)-standalone-strict", name))
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
        LOGGER.info(
            "%s Kubernetes %s APIs using cached schemas %s",
            "Planning validation for" if read_only else "Validating",
            version,
            identity,
        )
    if not read_only:
        snapshot = memory_snapshot(snapshot)
    catalog = cache / "catalogs" / version / "input-domains.json"
    catalog_identity = None
    if catalog.is_file():
        contents = catalog.read_bytes()
        catalog_identity = hashlib.sha256(contents).hexdigest()
        frozen = catalog.parent / "snapshots" / f"{catalog_identity}.json"
        if not read_only and not frozen.is_file():
            frozen.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=frozen.parent) as temporary:
                staged = Path(temporary) / frozen.name
                staged.write_bytes(contents)
                staged.replace(frozen)
        if frozen.is_file():
            catalog = frozen
    return json.dumps(
        {
            "version": version,
            "identity": identity,
            "schemas": str(snapshot),
            "cache_root": str(cache),
            "validator": "hypothesis-helm-jsonschema-v1",
            "catalog": str(catalog) if catalog.is_file() else None,
            "catalog_digest": catalog_identity,
        }
    )


@lru_cache(maxsize=512)
def schema_validator(file: Path, identity: str) -> Validator:
    """
    Compile a local immutable schema without permitting implicit reference downloads.

    Args:
        file (Path): Standalone schema within the selected snapshot.
        identity (str): Snapshot content identity, also separating cache generations.

    Returns:
        Validator: Reusable validator for the schema's declared JSON Schema dialect.
    """
    schema = mapping(json.loads(file.read_text()))
    check_schema(schema)
    return validators.validator_for(schema)(schema, format_checker=FormatChecker())


def validate(manifests: str | Iterable[object], timeout: float, *, configuration: str | None = None) -> None:
    """
    Validate rendered documents against local API schemas, reusing parsed YAML when available.

    Args:
        manifests (str | Iterable[object]): Complete YAML text or already parsed documents; input objects are not mutated.
        timeout (float): Time budget checked between resources; the owning chart worker enforces its process deadline.
        configuration (str | None): Explicit cache selection, or the configuration inherited by the current worker.

    Returns:
        None: Every resource conforms, or validation raises an assertion failure.
    """
    configuration = configuration or os.environ.get(ENVIRONMENT)
    if not configuration or ignored("HH1108"):
        return
    settings = json.loads(configuration)
    deadline = time.monotonic() + timeout

    def check(document: object) -> None:
        """
        Check one resource, including resources nested in Kubernetes List objects.

        Args:
            document (object): Decoded YAML resource.

        Returns:
            None: Raise an assertion identifying the resource and invalid field on failure.
        """
        if time.monotonic() >= deadline:
            raise AssertionError(f"Kubernetes schema validation exceeded {timeout}s")
        if not isinstance(document, dict):
            raise AssertionError("Kubernetes schema validation requires an object")
        resource = mapping(document)
        if resource.get("apiVersion") == "v1" and resource.get("kind") == "List":
            items = resource.get("items")
            if not isinstance(items, list):
                raise AssertionError("Kubernetes List requires an items array")
            for item in items:
                check(item)
            return
        try:
            if validate_custom(resource):
                return
            api, kind = str(resource.get("apiVersion", "")), str(resource.get("kind", ""))
            if not re.fullmatch(r"(?:[a-z0-9.-]+/)?[a-z0-9]+", api) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", kind):
                raise ValueError("resource needs a valid apiVersion and kind")
            group, version = api.rsplit("/", 1) if "/" in api else ("", api)
            suffix = f"-{group.split('.')[0]}" if group else ""
            file = Path(settings["schemas"]) / f"{kind.lower()}{suffix}-{version.lower()}.json"
            if not file.is_file():
                raise ValueError(f"no cached schema for {api}/{kind}; supply custom resource schemas explicitly")
            validator = schema_validator(file, str(settings.get("identity", "")))
            kinds = sequence(mapping(validator.schema).get("x-kubernetes-group-version-kind", []))
            if kinds and {"group": group, "version": version, "kind": kind} not in kinds:
                raise ValueError(f"cached schema does not describe {api}/{kind}")
            error = next(validator.iter_errors(json_value(resource)), None)
            if error is not None:
                field = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
                raise ValueError(f"{api}/{kind} {field}: {error.message}")
        except (ValueError, OSError, ValidationError) as exc:
            raise AssertionError(f"Kubernetes {settings['version']} API schema validation failed: {exc}") from exc

    for document in yamlio.load_all(manifests) if isinstance(manifests, str) else manifests:
        if document is not None:
            check(document)
