"""
Keep README error-discovery comparisons paired and complete.
"""

from pathlib import Path

import pytest

from hypothesis_helm.benchmarking.reporting.error_highlight import plot


@pytest.mark.parametrize("damage", [None, "missing", "timeout", "duplicate", "population"])
def test_error_highlight(tmp_path: Path, damage: str | None) -> None:
    """
    Generate a matched comparison or reject incomplete and mismatched observations.

    Args:
        tmp_path (Path): Plot destination.
        damage (str | None): Missing, incomplete, duplicate or mismatched measurement.

    Returns:
        None: Only complete paired observations produce a figure.
    """
    rows: list[dict[str, object]] = [
        {
            "axis": "clustering",
            "axis_value": 0,
            "repeat": 0,
            "error_percent": 5,
            "strategy": method,
            "status": "passed",
            "population_sha256": "same-population",
            "chart_sha256": "same-chart",
            "error_count": 12,
            "valid_domain": 256,
            "errors_detected": 12,
            "render_invocations": renders,
            "total_seconds": seconds,
        }
        for method, renders, seconds in [("default", 256, 13), ("exact-equivalence", 4, 1)]
    ]
    if damage == "missing":
        rows.pop()
    elif damage == "timeout":
        rows[0]["status"] = "time-limit"
    elif damage == "duplicate":
        rows.append(dict(rows[0]))
    elif damage == "population":
        rows[0]["population_sha256"] = "different"
    document: dict[str, object] = {"metadata": {"axes": {"clustering": [0]}, "repeats": 1}, "rows": rows}
    if damage in {"duplicate", "population"}:
        with pytest.raises(ValueError):
            plot(tmp_path, document)
    else:
        assert plot(tmp_path, document) == (damage is None)
    assert (tmp_path / "errors-found-fast.png").exists() == (damage is None)
