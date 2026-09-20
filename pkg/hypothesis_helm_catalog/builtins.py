"""
Rebuild compiler function facts from checksum-locked Helm, Sprig and Go sources.
"""

import argparse
import hashlib
import io
import json
import tempfile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

from hypothesis_helm.environment import refresh_env
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.schemas.contracts import mapping, sequence

from hypothesis_helm_catalog import toolchain

__all__ = ("LIBRARY", "LOCK", "acquire", "main", "rebuild", "unpack")


LOCK = Path(__file__).with_name("data") / "builtin-sources.json"
LIBRARY = Path(__file__).parents[1] / "hypothesis_helm/compiler/builtin_inventory.json"


def acquire(record: dict[str, object], cache: Path, *, offline: bool) -> bytes:
    """
    Read or fetch a source artifact and verify its locked checksum before use.

    Args:
        record (dict[str, object]): URL and expected SHA-256 from the reviewed source lock.
        cache (Path): Download cache; each artifact is named by its content hash.
        offline (bool): Prohibit network requests.

    Returns:
        bytes: Verified source artifact.

    Raises:
        ValueError: The artifact is unavailable offline or fails checksum verification.
    """
    expected = str(record["sha256"])
    path = cache / expected
    if path.is_file():
        content = path.read_bytes()
    elif offline:
        raise ValueError(f"Builtin source is not cached: {record['name']} {record['version']}")
    else:
        with urllib.request.urlopen(str(record["url"]), timeout=60) as response:
            content = response.read()
    if hashlib.sha256(content).hexdigest() != expected:
        raise ValueError(f"Builtin source checksum mismatch: {record['name']} {record['version']}")
    if not path.is_file():
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as temporary:
            staged = Path(temporary) / expected
            staged.write_bytes(content)
            staged.replace(path)
    return content


def unpack(record: dict[str, object], content: bytes, destination: Path) -> None:
    """
    Copy only a provider's package-level Go source into a private build directory.

    Args:
        record (dict[str, object]): Locked archive prefix and relevant source directory.
        content (bytes): Verified archive or individual source file.
        destination (Path): Private extraction destination.

    Returns:
        None: Source files are written without executing upstream code or extracting archive paths.
    """
    destination.mkdir(parents=True)
    if record["prefix"] is None:
        (destination / "funcs.go").write_bytes(content)
        return
    prefix = str(record["prefix"]) + str(record["subdirectory"])
    with ZipFile(io.BytesIO(content)) as archive:
        for member in archive.namelist():
            if not member.startswith(prefix):
                continue
            relative = member.removeprefix(prefix)
            if "/" not in relative and relative.endswith(".go") and not relative.endswith("_test.go"):
                (destination / relative).write_bytes(archive.read(member))


def rebuild(cache: Path, go: str, *, offline: bool = False, lock: Path = LOCK) -> dict[str, object]:
    """
    Compile the Go extractor and generate deterministic function facts from locked sources.

    Args:
        cache (Path): User-owned download and Go build cache.
        go (str): Go executable, required only for rebuilding.
        offline (bool): Require previously downloaded sources.
        lock (Path): Explicitly reviewed source lock, including for an upstream upgrade.

    Returns:
        dict[str, object]: Generated signatures, shapes, effects, unresolved boundaries and source provenance.

    Raises:
        ValueError: A provider name is unsupported or the source inventory is inconsistent.
    """
    records = [mapping(raw) for raw in sequence(mapping(json.loads(lock.read_text()))["sources"])]
    if [record["name"] for record in records] != ["Go", "Sprig", "Helm"]:
        raise ValueError("Builtin sources must be ordered Go, Sprig, Helm to preserve overrides")
    cache = cache.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        root = Path(temporary)
        inputs = []
        sources = []
        for record in records:
            provider = str(record["name"]) + " " + str(record["version"])
            destination = root / str(record["name"])
            unpack(record, acquire(record, cache / "downloads", offline=offline), destination)
            inputs.append(
                {
                    "provider": provider,
                    "directory": str(destination),
                    "map": {"Go": "builtins", "Sprig": "genericMap", "Helm": "extra"}[str(record["name"])],
                }
            )
            sources.append(
                {
                    "version": provider,
                    "url": record["url"],
                    "sha256": record["sha256"],
                    "files": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(destination.glob("*.go"))},
                }
            )
        config = root / "sources.json"
        config.write_text(json.dumps(inputs))
        executable = root / "extract"
        owner = Processes()
        try:
            toolchain.build(executable, cache, go, owner, offline=offline)
            process = owner.run([str(executable), "--config", str(config)], capture_output=True, check=True, timeout=60)
        finally:
            owner.stop()
        extracted = mapping(json.loads(process.stdout))
        return {
            "format": 2,
            "analysis": "Go AST facts; unresolved calls are not purity proofs",
            "extractor_sha256": toolchain.fingerprint(),
            "sources": sources,
            **extracted,
        }


def main(argv: list[str] | None = None) -> int:
    """
    Regenerate or check the compiler inventory as a repeatable release step.

    Args:
        argv (list[str] | None): CLI arguments, defaulting to process arguments.

    Returns:
        int: Zero on success, one for a stale inventory or invalid source.
    """
    refresh_env()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache/compiler-builtins"))
    parser.add_argument("--source-lock", type=Path, default=LOCK, help="reviewed upstream artifact URLs and checksums")
    parser.add_argument("--go", default="go", help="Go 1.25+ executable; no upstream Go code is executed")
    parser.add_argument("--offline", action="store_true", help="require cached sources; prohibit downloads")
    parser.add_argument("--output", type=Path, default=LIBRARY)
    parser.add_argument("--check", action="store_true", help="compare generated facts with the inventory without writing")
    args = parser.parse_args(argv)
    result = rebuild(args.cache_dir, args.go, offline=args.offline, lock=args.source_lock)
    content = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.check:
        matches = args.output.is_file() and args.output.read_text() == content
        print("Builtin inventory is current" if matches else "Builtin inventory is stale; rebuild and review the diff")
        return 0 if matches else 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.output.parent) as temporary:
        staged = Path(temporary) / "inventory.json"
        staged.write_text(content)
        staged.replace(args.output)
    print(f"Wrote {len(mapping(result['functions']))} builtin definitions to {args.output}")
    return 0
