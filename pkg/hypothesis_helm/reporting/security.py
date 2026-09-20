"""
Summarize Kubesec validity and score checks without losing scanner failures.
"""

import hashlib
import html
import json
import os
import shutil
from collections.abc import Iterator
from pathlib import Path
from textwrap import dedent
from xml.etree.ElementTree import Element, SubElement, tostring

from attrs import asdict, define

from hypothesis_helm.schemas.contracts import mapping

__all__ = ("SecurityStatistics", "aggregate", "checksum", "publish", "read_result", "records")


@define
class SecurityStatistics:
    """
    Count resource attempts, independent checks, scanner errors and observed scores.

    Attributes:
        resources (int): Resource attempts, including missing results.
        failed_resources (int): Attempts with any rejected check or execution error.
        checks (int): Completed validity and score checks.
        failed_checks (int): Rejected validity and score checks.
        invalid_resources (int): Explicitly invalid manifests.
        below_minimum (int): Scores below the inclusive threshold.
        report_errors (int): Missing or malformed result records.
        scanner_failures (int): Attempts with nonzero scanner exits or signals.
        critical (int): Critical rule occurrences reported by Kubesec.
        advisories (int): Advisory rule occurrences reported by Kubesec.
        scored (int): Attempts with an integer score.
        score_sum (int): Sum used to calculate the mean observed score.
        score_min (int | None): Lowest observed score, or None without scores.
        score_max (int | None): Highest observed score, or None without scores.
    """

    resources: int = 0
    failed_resources: int = 0
    checks: int = 0
    failed_checks: int = 0
    invalid_resources: int = 0
    below_minimum: int = 0
    report_errors: int = 0
    scanner_failures: int = 0
    critical: int = 0
    advisories: int = 0
    scored: int = 0
    score_sum: int = 0
    score_min: int | None = None
    score_max: int | None = None

    def observe(self, record: dict[str, object], minimum: int) -> None:
        """
        Count completed checks while keeping missing evidence separate from failures.

        Args:
            record (dict[str, object]): Normalized result for one resource attempt.
            minimum (int): Inclusive minimum security score.

        Returns:
            None: Counters include this attempt exactly once.
        """
        self.resources += 1
        valid, score = record.get("valid"), record.get("score")
        invalid = valid is False
        low = type(score) is int and score < minimum
        self.checks += int(type(valid) is bool) + int(type(score) is int)
        self.invalid_resources += int(invalid)
        self.below_minimum += int(low)
        self.failed_checks += int(invalid) + int(low)
        self.report_errors += int(bool(record.get("error")))
        scanner_failure = bool(record.get("exit_code") or record.get("signal"))
        self.scanner_failures += int(scanner_failure)
        self.failed_resources += int(invalid or low or bool(record.get("error")) or scanner_failure)
        self.critical += int(str(record.get("critical", 0)))
        self.advisories += int(str(record.get("advisories", 0)))
        if type(score) is int:
            self.scored += 1
            self.score_sum += score
            self.score_min = score if self.score_min is None else min(score, self.score_min)
            self.score_max = score if self.score_max is None else max(score, self.score_max)


def read_result(path: Path, *, exit_code: int | None, signal: int = 0) -> dict[str, object]:
    """
    Require exactly one JSON result with explicit validity and an integer score.

    Args:
        path (Path): Captured stdout of a single-resource Kubesec invocation.
        exit_code (int | None): Process status, or None when the job did not finish.
        signal (int): Signal recorded by GNU Parallel.

    Returns:
        dict[str, object]: Normalized evidence; invalid or absent output retains an error.
    """
    record: dict[str, object] = {"exit_code": exit_code, "signal": signal, "valid": None, "score": None}
    try:
        raw = json.loads(path.read_text())
        if not isinstance(raw, list) or len(raw) != 1:
            raise ValueError("expected one Kubesec result for one resource")
        result = mapping(raw[0])
        record["object"] = str(result.get("object", path.parent.name))
        record["message"] = str(result.get("message", ""))
        if type(result.get("valid")) is bool:
            record["valid"] = result["valid"]
        if type(result.get("score")) is int:
            record["score"] = result["score"]
        scoring = mapping(result.get("scoring", {}))
        for source, key in (("critical", "critical"), ("advise", "advisories")):
            entries = scoring.get(source, [])
            record[key] = len(entries) if isinstance(entries, list) else 0
        if record["valid"] is None or record["score"] is None:
            raise ValueError("Kubesec result needs boolean valid and integer score fields")
        if exit_code is None:
            raise ValueError("Kubesec job did not complete")
    except (OSError, ValueError, TypeError) as exc:
        record["error"] = str(exc)
    return record


def records(path: Path) -> Iterator[dict[str, object]]:
    """
    Stream normalized resource results from an artifact.

    Args:
        path (Path): JSON Lines result file.

    Yields:
        dict[str, object]: One resource result at a time.
    """
    with path.open() as stream:
        for line in stream:
            yield mapping(json.loads(line))


def checksum(path: Path) -> str:
    """
    Hash transported evidence without loading the manifest stream into memory.

    Args:
        path (Path): Artifact to hash.

    Returns:
        str: SHA-256 digest.
    """
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def publish(output: Path, metadata: dict[str, object], minimum: int) -> int:
    """
    Write compact JSON, Markdown and streaming JUnit reports for completed attempts.

    Args:
        output (Path): Directory containing details.jsonl.
        metadata (dict[str, object]): Run, schema, shard and external validation status.
        minimum (int): Inclusive minimum security score.

    Returns:
        int: One for any rejected resource, missing evidence, or validator failure.
    """
    statistics = SecurityStatistics()
    details = output / "details.jsonl"
    execution_errors = 0
    for record in records(details):
        statistics.observe(record, minimum)
        execution_errors += int(bool(record.get("error") or record.get("exit_code") or record.get("signal")))
    status = int(bool(statistics.failed_resources or metadata.get("schema_exit_code") or metadata.get("parallel_exit_code")))
    report = {
        **metadata,
        "status": "failed" if status else "passed",
        "score_minimum": minimum,
        "statistics": asdict(statistics),
        "details_sha256": checksum(details),
    }
    (output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    observed = (
        "none"
        if not statistics.scored
        else f"{statistics.score_min} / {statistics.score_sum / statistics.scored:.2f} / {statistics.score_max}"
    )
    missing = statistics.resources * 2 - statistics.checks
    summary = dedent(
        f"""
        ## Kubesec: {report["status"]}

        Kubernetes {html.escape(str(metadata["schema_version"]))}; minimum score **{minimum}** (inclusive).
        Counts describe resource attempts across generated configurations, not unique deployed objects.

        | Measure | Count |
        | --- | ---: |
        | Resource attempts | {statistics.resources} |
        | Failed resource attempts | {statistics.failed_resources} |
        | Completed validity and score checks | {statistics.checks} |
        | Failed checks | {statistics.failed_checks} |
        | Invalid manifests | {statistics.invalid_resources} |
        | Scores below minimum | {statistics.below_minimum} |
        | Missing checks | {missing} |
        | Missing or malformed reports | {statistics.report_errors} |
        | Nonzero scanner exits or signals | {statistics.scanner_failures} |
        | Critical rule occurrences | {statistics.critical} |
        | Advisory rule occurrences | {statistics.advisories} |
        | Score minimum / mean / maximum | {observed} |
        | Resources routed to native schema validation | {metadata.get("schema_scanned", 0)} |

        Native schema validation: {"failed" if metadata.get("schema_exit_code") else "passed or not needed"}.
        GNU Parallel: {"failed or interrupted" if metadata.get("parallel_exit_code") else "passed or not needed"}.
        A resource can fail both checks. Advisory counts alone do not fail the gate.
        Raw results and per-resource evidence accompany this summary.
        """
    ).lstrip()
    (output / "summary.md").write_text(summary)
    execution_errors += int(bool(metadata.get("schema_exit_code"))) + int(bool(metadata.get("parallel_exit_code")))
    with (output / "junit.xml").open("w") as junit:
        junit.write(
            f'<testsuites><testsuite name="Kubesec" tests="{statistics.resources * 2 + execution_errors}" '
            f'failures="{statistics.failed_checks}" errors="{missing + execution_errors}">\n'
        )
        for index, record in enumerate(records(details), 1):
            identity = str(record.get("object", f"resource-{index}"))
            for name, value, accepted in (
                ("valid", record.get("valid"), record.get("valid") is True),
                ("score", record.get("score"), type(record.get("score")) is int and int(str(record["score"])) >= minimum),
            ):
                case = Element("testcase", classname=f"kubesec.{metadata['schema_version']}", name=f"{index}: {identity}: {name}")
                if value is None:
                    SubElement(case, "error", message=str(record.get("error", "Missing check result")))
                elif not accepted:
                    SubElement(case, "failure", message=f"{name}={value}; minimum score={minimum}").text = str(record.get("message", ""))
                junit.write(tostring(case, encoding="unicode") + "\n")
            if record.get("error") or record.get("exit_code") or record.get("signal"):
                case = Element("testcase", classname="kubesec.execution", name=f"{index}: {identity}")
                SubElement(
                    case, "error", message=str(record.get("error") or f"Scanner exit={record['exit_code']}, signal={record['signal']}")
                )
                junit.write(tostring(case, encoding="unicode") + "\n")
        for key in ("schema_exit_code", "parallel_exit_code"):
            if metadata.get(key):
                case = Element("testcase", classname="kubesec.execution", name=key)
                SubElement(case, "error", message=f"{key}={metadata[key]}; see validator artifacts")
                junit.write(tostring(case, encoding="unicode") + "\n")
        junit.write("</testsuite></testsuites>\n")
    print(
        f"Kubesec {report['status']}: {statistics.failed_resources}/{statistics.resources} resource attempts failed; "
        f"{statistics.failed_checks}/{statistics.checks} checks failed; {missing} checks missing; minimum score {minimum}. "
        f"Report: {output / 'summary.md'}"
    )
    if destination := os.environ.get("GITHUB_STEP_SUMMARY"):
        with Path(destination).open("a") as stream:
            stream.write(summary + "\n")
    return status


def aggregate(source: Path, output: Path, *, shards: int, run_id: str, version: str, minimum: int) -> int:
    """
    Verify transported shard evidence and recompute totals for one version and run.

    Args:
        source (Path): Root of downloaded security artifacts only.
        output (Path): Separate final security report directory.
        shards (int): Expected number of shards, including idle shards.
        run_id (str): Common pipeline and attempt identity.
        version (str): Expected Kubernetes schema version.
        minimum (int): Expected minimum score used by every shard.

    Returns:
        int: Combined security gate status; inconsistent or missing evidence raises ValueError.
    """
    if shards < 1 or minimum < 0 or not run_id or output.resolve().is_relative_to(source.resolve()):
        raise ValueError("Security aggregation needs a run ID, positive shard count and separate output directory")
    reports: dict[str, tuple[Path, dict[str, object]]] = {}
    identity = None
    for path in source.rglob("summary.json"):
        report = mapping(json.loads(path.read_text()))
        shard = str(report.get("shard"))
        if shard in reports:
            raise ValueError(f"Duplicate security shard: {shard}")
        if version == "latest":
            version = str(report.get("schema_version"))
        if report.get("run_id") != run_id or report.get("schema_version") != version or report.get("score_minimum") != minimum:
            raise ValueError(f"Security run, version or score policy mismatch: {path}")
        if identity is not None and report.get("schema_identity") != identity:
            raise ValueError(f"Security schema snapshot mismatch: {path}")
        identity = report.get("schema_identity")
        if not identity or checksum(path.parent / "details.jsonl") != report.get("details_sha256"):
            raise ValueError(f"Security evidence checksum mismatch: {path}")
        statistics = SecurityStatistics()
        for record in records(path.parent / "details.jsonl"):
            statistics.observe(record, minimum)
        if asdict(statistics) != report.get("statistics") or statistics.resources != report.get("scanned"):
            raise ValueError(f"Security counts disagree with resource evidence: {path}")
        reports[shard] = (path, report)
    if set(reports) != {f"{index}-of-{shards}" for index in range(1, shards + 1)}:
        raise ValueError(f"Expected all {shards} security shards; found {sorted(reports)}")
    output.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, object] = {"run_id": run_id, "schema_version": version, "schema_identity": identity, "shards": sorted(reports)}
    for key in ("schema_scanned", "scanned", "skipped"):
        metadata[key] = sum(int(str(report.get(key, 0))) for _, report in reports.values())
    for key in ("schema_exit_code", "parallel_exit_code"):
        metadata[key] = int(any(report.get(key) for _, report in reports.values()))
    with (output / "details.jsonl").open("w") as stream:
        for path, _ in reports.values():
            with (path.parent / "details.jsonl").open() as incoming:
                shutil.copyfileobj(incoming, stream)
    return publish(output, metadata, minimum)
