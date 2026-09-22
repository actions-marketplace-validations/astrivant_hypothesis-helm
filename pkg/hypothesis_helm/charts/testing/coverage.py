"""
Distinguish executed chart tests from incomplete or intentionally skipped work.
"""

__all__ = ("require_attempts",)


def require_attempts(result: dict[str, object]) -> None:
    """
    Reject a successful fresh execution result that did not attempt any manifest tests.

    Args:
        result (dict[str, object]): Fresh chart-run result, updated in place if execution was empty.

    Returns:
        None: Existing failures, deadlines, dry runs, and explicit cache/shard skips retain their status.
    """
    if result.get("status") not in {"passed", "findings", "ignored"} or result.get("attempts", 0):
        return
    diagnostic = "No manifest tests were attempted; this chart was not tested. Inspect the chart's preparation and generation diagnostics."
    if result.get("error"):
        diagnostic += " " + str(result["error"])
    result.update(status="error", error=diagnostic, error_kind="execution", attempts=0, coverage_complete=False)
