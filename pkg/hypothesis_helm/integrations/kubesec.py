"""
Scan manifest streams with core-sized GNU Parallel pools and local Kubernetes schemas.
"""

import argparse
import csv
import json
import os
import shutil
import tempfile
import time
from pathlib import Path

from hypothesis_helm.execution.processes import Processes
from hypothesis_helm.integrations.sharding import Shard, parse_shard_option, resolve_shard
from hypothesis_helm.reporting.security import aggregate, publish, read_result
from hypothesis_helm.schemas.conformity import prepare, validate
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("SUPPORTED", "main", "scan", "worker_count")


SUPPORTED = {"Pod", "Deployment", "StatefulSet", "DaemonSet"}


def worker_count(value: str) -> int:
    """
    Resolve automatic concurrency from the logical CPUs available to this process.

    Args:
        value (str): Auto or a positive worker count.

    Returns:
        int: Number of concurrent Kubesec processes on this runner.
    """
    if value == "auto":
        return os.process_cpu_count() or 1
    try:
        count = int(value)
        if count > 0:
            return count
    except ValueError:
        pass
    raise ValueError("Kubesec jobs must be auto or a positive integer")


def scan(
    manifests: Path,
    output: Path,
    configuration: str,
    *,
    jobs: str = "auto",
    executable: str = "kubesec",
    shard: Shard | None = None,
    pre_sharded: bool = False,
    validate_rest: bool = False,
    score_minimum: int = 0,
    run_id: str = "",
) -> int:
    """
    Run each supported resource through GNU Parallel and retain every scan result.

    Args:
        manifests (Path): JSON Lines resource stream, possibly already owned by a shard.
        output (Path): Artifact root; shard coordinates select an isolated subdirectory.
        configuration (str): Prepared local conformity configuration serialized as JSON.
        jobs (str): Auto CPU count or explicit positive concurrency limit.
        executable (str): Installed Kubesec binary.
        shard (Shard | None): Partition coordinates for a shared input stream.
        pre_sharded (bool): Input is already selected; do not partition its records again.
        validate_rest (bool): Route unsupported resources to native schema validation.
        score_minimum (int): Inclusive minimum acceptable score for each resource.
        run_id (str): Common identity used to verify transported shard reports.

    Returns:
        int: Zero if all scans succeed, one if any scan fails.
    """
    if type(score_minimum) is not int or score_minimum < 0:
        raise ValueError("Kubesec score minimum must be a nonnegative integer")
    started = time.monotonic()
    workers = worker_count(jobs)
    settings = mapping(json.loads(configuration))
    binary, parallel = shutil.which(executable), shutil.which("parallel")
    if not binary or not parallel:
        raise ValueError("Kubesec scanning requires kubesec and GNU Parallel")
    version = Processes().run([parallel, "--version"], capture_output=True, text=True, timeout=10)
    if version.returncode or not version.stdout.startswith("GNU parallel"):
        raise ValueError("parallel must be GNU Parallel")
    output = output.resolve()
    if shard:
        output = output / "shards" / shard.name
    output.mkdir(parents=True, exist_ok=True)
    records = output / "manifests"
    records.mkdir(exist_ok=True)
    tasks = output / "tasks.bin"
    results = Path(tempfile.mkdtemp(prefix="results-", dir=output))
    selected, skipped = 0, 0
    remaining = output / "schema-validation.yaml"
    with (
        manifests.open() as source,
        tasks.open("wb") as destinations,
        remaining.open("w") as fallback,
    ):
        for index, line in enumerate(source):
            if not line.strip():
                continue
            if shard and not pre_sharded and index % shard.total != shard.index - 1:
                continue
            resource = mapping(json.loads(line))
            if resource.get("kind") not in SUPPORTED:
                skipped += 1
                if validate_rest:
                    fallback.write("---\n" + json.dumps(resource) + "\n")
                continue
            path = records / f"{index + 1:08d}.json"
            path.write_text(json.dumps(resource) + "\n")
            destinations.write(os.fsencode(path) + b"\0")
            selected += 1
    command = [
        parallel,
        "--plain",
        "--term-seq",
        "TERM,10000,KILL,1000",
        "--jobs",
        str(workers),
        "--halt",
        "never",
        "--null",
        "--arg-file",
        str(tasks),
        "--joblog",
        str(output / "joblog.tsv"),
        "--results",
        str(results / "{#}") + "/",
        "--quote",
        "--replace",
        "__HH_MANIFEST__",
        binary,
        "scan",
        # Kubesec 2.14.2 rejects score zero even though its JSON labels it passed.
        # Let our explicit validity and score checks own policy failures. Native
        # command errors still return nonzero, and malformed reports fail closed.
        "--exit-code",
        "0",
        "--format",
        "json",
        "--kubernetes-version",
        str(settings["version"]),
        "--schema-location",
        str(settings["schemas"]) + "/{{ .ResourceKind }}{{ .KindSuffix }}.json",
        "__HH_MANIFEST__",
    ]
    if any("__HH_MANIFEST__" in str(path) for path in (output, settings["schemas"], binary)):
        raise ValueError("reserved GNU Parallel replacement token in path")
    disposition = "routed to native schema validation" if validate_rest else "skipped"
    print(f"Kubesec: {selected} resources, {workers} workers, {skipped} {disposition}")
    status = 0
    interrupted = False
    if selected:
        try:
            with (output / "parallel.stdout").open("w") as stdout:
                result = Processes(interrupt_grace=12).run(command, cwd=Path.cwd(), env={**os.environ, "GOMAXPROCS": "1"}, stdout=stdout)
            status = result.returncode
        except KeyboardInterrupt:
            status, interrupted = 130, True
    completed = {}
    if selected and (output / "joblog.tsv").exists():
        with (output / "joblog.tsv").open() as joblog:
            for row in csv.DictReader(joblog, delimiter="\t"):
                try:
                    completed[int(row["Seq"])] = (int(row["Exitval"]), int(row["Signal"]))
                except (KeyError, TypeError, ValueError):
                    # A cancelled writer can leave a partial row. Its absent
                    # completion status becomes missing evidence below.
                    continue
    with (output / "details.jsonl").open("w") as details:
        for index in range(1, selected + 1):
            exit_code, signal = completed.get(index, (None, 0))
            path = results / str(index) / "stdout"
            record = read_result(path, exit_code=exit_code, signal=signal)
            record["result_path"] = str(path.relative_to(output))
            details.write(json.dumps(record) + "\n")
    conformity_status = 0
    if validate_rest and skipped and not interrupted:
        error = None
        try:
            validate(remaining.read_text(), max(30, skipped * 30), configuration=configuration)
        except (AssertionError, ValueError) as exc:
            conformity_status, error = 1, str(exc)
        except KeyboardInterrupt:
            conformity_status, error, interrupted = 130, "Schema validation interrupted", True
        (output / "schema-validation.json").write_text(json.dumps({"status": "failed" if error else "passed", "error": error}) + "\n")
    report = {
        "run_id": run_id,
        "parallel_exit_code": status,
        "elapsed_seconds": time.monotonic() - started,
        "scanned": selected,
        "skipped": 0 if validate_rest else skipped,
        "schema_scanned": skipped if validate_rest else 0,
        "schema_exit_code": conformity_status,
        "jobs": workers,
        "shard": shard.name if shard else None,
        "pre_sharded": pre_sharded,
        "schema_version": settings["version"],
        "schema_identity": settings["identity"],
    }
    outcome = publish(output, report, score_minimum)
    return 130 if interrupted else outcome


def main() -> int:
    """
    Scan saved CI manifests against restored schemas with optional shard selection.

    Returns:
        int: Scan status or two for an invalid setup.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", type=Path, help="Manifest JSONL stream, or downloaded security artifact directory with --aggregate")
    parser.add_argument("--output", type=Path, default=Path(".cache/hypothesis-helm/kubesec"))
    parser.add_argument("--jobs", default="auto")
    parser.add_argument("--shard", type=parse_shard_option, default="auto")
    parser.add_argument("--pre-sharded", action="store_true")
    parser.add_argument("--validate-rest", action="store_true", help="Validate other kinds with native schema validation")
    parser.add_argument("--schema-version", default="latest")
    parser.add_argument("--schema-cache-dir", type=Path, default=Path("schemas"))
    parser.add_argument("--schema-offline", action="store_true")
    parser.add_argument("--kubesec-binary", default="kubesec")
    parser.add_argument(
        "--score-minimum", type=int, default=0, help="Minimum acceptable score per resource, a nonnegative integer (default: 0)"
    )
    parser.add_argument("--run-id", default="", help="Common pipeline and attempt identity for all shards")
    parser.add_argument(
        "--aggregate", action="store_true", help="Verify security shard evidence and publish combined statistics without scanning"
    )
    parser.add_argument("--shards", type=int, help="Expected security shard count, required with --aggregate")
    args = parser.parse_args()
    try:
        if args.score_minimum < 0:
            raise ValueError("Kubesec score minimum must be a nonnegative integer")
        if args.aggregate:
            return aggregate(
                args.manifests,
                args.output,
                shards=args.shards or 0,
                run_id=args.run_id,
                version=args.schema_version,
                minimum=args.score_minimum,
            )
        if args.shards is not None:
            raise ValueError("--shards requires --aggregate; use --shard INDEX/TOTAL to scan")
        worker_count(args.jobs)
        shard, _ = resolve_shard(args.shard, os.environ)
        configuration = prepare(args.schema_cache_dir, args.schema_version, args.schema_offline)
        return scan(
            args.manifests,
            args.output,
            configuration,
            jobs=args.jobs,
            executable=args.kubesec_binary,
            shard=shard,
            pre_sharded=args.pre_sharded,
            validate_rest=args.validate_rest,
            score_minimum=args.score_minimum,
            run_id=args.run_id,
        )
    except KeyboardInterrupt:
        return 130
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Kubesec setup failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
