"""
Keep command completion concise while directing detailed evidence to saved artifacts.
"""

from pathlib import Path

from hypothesis_helm.schemas.contracts import mapping

__all__ = ("print_summary",)


def print_summary(report: dict[str, object], artifact: Path, *, reports: tuple[Path, ...] = ()) -> None:
    """
    Print bounded execution statistics without serializing chart inputs or diagnostic inventories.

    Args:
        report (dict[str, object]): Completed, failed or interrupted execution record.
        artifact (Path): JSON evidence already saved by the caller.
        reports (tuple[Path, ...]): Optional published Markdown and PDF paths.

    Returns:
        None: A short summary follows the normal console stream, including manifest-mode redirection.
    """
    scan = "charts_discovered" in report
    status = str(report.get("scan_status" if scan else "status", "completed")).replace("-", " ")
    parts = [f"{'Scan' if scan else 'Test'} {status}"]
    if scan:
        parts.append(f"{report['charts_discovered']} charts")
    if "attempts" in report:
        parts.append(f"{report['attempts']} test attempts")
    errors = mapping(report.get("error_summary", {}))
    if "unique_errors" in errors:
        parts.append(f"{errors['unique_errors']} distinct diagnostics")
    print("; ".join(parts) + ".", flush=True)
    if scan:
        counts = mapping(report.get("counts", {}))
        # Status counts stay small even when a scan contains thousands of charts.
        summary = [f"{name}: {count}" for name, count in sorted(counts.items())[:12]]
        if len(counts) > 12:
            summary.append("additional statuses in saved results")
        if summary:
            print("Charts: " + ", ".join(summary) + ".", flush=True)
    print(f"Results saved: {artifact}", flush=True)
    if reports:
        print("Reports: " + ", ".join(str(path) for path in reports), flush=True)
