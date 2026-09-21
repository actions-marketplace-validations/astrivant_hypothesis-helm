"""
Record execution timestamps and stable run fingerprints independently of report publication.
"""

from datetime import UTC, datetime

from hypothesis_helm.reporting.evidence.changes import digest

__all__ = ("IDENTITY_FIELDS", "finish_epoch", "trace_run")


# Report titles and layout are excluded so republishing the same run preserves its identity.
IDENTITY_FIELDS = (
    "run_id",
    "directory",
    "source",
    "suite",
    "suite_fingerprint",
    "input_digest",
    "started_epoch",
    "finished_epoch",
    "settings",
    "input_policy",
    "finding_policy",
    "seed",
    "sampling",
    "traversal_strategy",
    "jobs",
)


def finish_epoch(report: dict[str, object]) -> float:
    """
    Read the execution finish time, estimating it from duration for historical records.

    Args:
        report (dict[str, object]): Scan, suite, or aggregate result with recorded timing.

    Returns:
        float: Unix finish timestamp, never the time at which a report is republished.
    """
    if "finished_epoch" in report:
        return float(str(report["finished_epoch"]))
    return float(str(report["started_epoch"])) + float(str(report["elapsed_seconds"]))


def trace_run(report: dict[str, object], *, finished_epoch: float | None = None) -> None:
    """
    Retain UTC timestamps and hash run metadata without including mutable publication details.

    Args:
        report (dict[str, object]): Result updated before saving JSON or producing human-readable reports.
        finished_epoch (float | None): Actual execution finish time; omitted when formatting previously saved results.

    Returns:
        None: Add finish provenance, ISO timestamps, and a versioned SHA-256 run identifier to the result.
    """
    if finished_epoch is not None:
        report.update(finished_epoch=float(finished_epoch), finish_time_source="recorded")
    else:
        report.setdefault("finish_time_source", "recorded" if "finished_epoch" in report else "derived-start-plus-elapsed")
        report["finished_epoch"] = finish_epoch(report)
    report["started_at"] = datetime.fromtimestamp(float(str(report["started_epoch"])), UTC).isoformat(timespec="milliseconds")
    report["finished_at"] = datetime.fromtimestamp(float(str(report["finished_epoch"])), UTC).isoformat(timespec="milliseconds")
    report["run_hash_algorithm"] = "sha256-run-metadata-v1"
    report["run_hash"] = digest(
        {"algorithm": report["run_hash_algorithm"], "metadata": {key: report[key] for key in IDENTITY_FIELDS if key in report}}
    )
