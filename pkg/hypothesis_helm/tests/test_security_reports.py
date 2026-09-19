"""
Verify score gates, missing evidence and shard aggregation independently of scanner exits.
"""

import json
from pathlib import Path
from xml.etree.ElementTree import parse

import pytest

from hypothesis_helm.reporting.security import SecurityStatistics, aggregate, publish, read_result


@pytest.mark.parametrize(
    ("valid", "score", "failed_checks", "failed_resources"),
    [(True, 5, 0, 0), (True, 4, 1, 1), (False, 5, 1, 1), (False, -10, 2, 1)],
)
def test_independent_checks(tmp_path: Path, valid: bool, score: int, failed_checks: int, failed_resources: int) -> None:
    """
    Count two independent checks without double-counting failed resources.

    Args:
        tmp_path (Path): Scanner output directory.
        valid (bool): Simulated schema validity.
        score (int): Simulated security score.
        failed_checks (int): Expected invalidity and score failures.
        failed_resources (int): Expected failed resource attempts.

    Returns:
        None: Equality passes and simultaneous failures retain distinct counts.
    """
    raw = tmp_path / "stdout"
    raw.write_text(json.dumps([{"object": "Deployment/demo.default", "valid": valid, "score": score}]))
    statistics = SecurityStatistics()
    statistics.observe(read_result(raw, exit_code=0), 5)
    assert statistics.checks == 2
    assert statistics.failed_checks == failed_checks
    assert statistics.failed_resources == failed_resources


@pytest.mark.parametrize("raw", ["not json", "[]", "{}", "[{}, {}]", '[{"valid": true}]', '[{"valid": true, "score": true}]'])
def test_bad_reports_fail_closed(tmp_path: Path, raw: str) -> None:
    """
    Reject incomplete reports even when the scanner exits successfully.

    Args:
        tmp_path (Path): Captured output directory.
        raw (str): Invalid or incomplete scanner result.

    Returns:
        None: Incomplete output cannot count as successful security validation.
    """
    path = tmp_path / "stdout"
    path.write_text(raw)
    statistics = SecurityStatistics()
    statistics.observe(read_result(path, exit_code=0), 0)
    assert statistics.failed_resources == statistics.report_errors == 1


def shard_report(root: Path, index: int, *, failed: bool = False) -> Path:
    """
    Publish a small security shard, with shard three deliberately idle.

    Args:
        root (Path): Artifact root.
        index (int): One-based shard index.
        failed (bool): Whether to include a resource failing both checks.

    Returns:
        Path: Published summary path.
    """
    destination = root / str(index)
    destination.mkdir(parents=True)
    record = {"object": "Pod/demo.default", "valid": not failed, "score": -1 if failed else 5, "exit_code": 0, "signal": 0}
    (destination / "details.jsonl").write_text("" if index == 3 else json.dumps(record) + "\n")
    publish(
        destination,
        {
            "scanned": int(index != 3),
            "shard": f"{index}-of-3",
            "run_id": "pipeline-123-attempt-1",
            "schema_version": "1.35.0",
            "schema_identity": "same-snapshot",
        },
        5,
    )
    return destination / "summary.json"


@pytest.mark.parametrize("failed", [False, True])
def test_aggregate_security(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failed: bool) -> None:
    """
    Recompute totals and publish JUnit and Markdown, including an idle shard.

    Args:
        tmp_path (Path): Transported and final reports.
        monkeypatch (pytest.MonkeyPatch): Redirect the GitHub step summary.
        failed (bool): Whether shard one includes a resource with two failures.

    Returns:
        None: Each resource is counted once and all report formats agree on failure.
    """
    for index in range(1, 4):
        shard_report(tmp_path / "source", index, failed=failed and index == 1)
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(tmp_path / "step.md"))
    output = tmp_path / "final"
    assert aggregate(tmp_path / "source", output, shards=3, run_id="pipeline-123-attempt-1", version="latest", minimum=5) == int(failed)
    summary = json.loads((output / "summary.json").read_text())
    assert summary["statistics"]["resources"] == 2
    assert summary["statistics"]["checks"] == 4
    assert summary["statistics"]["failed_checks"] == 2 * int(failed)
    assert summary["statistics"]["failed_resources"] == int(failed)
    assert len(parse(output / "junit.xml").findall(".//failure")) == 2 * int(failed)
    assert (tmp_path / "step.md").read_text() == (output / "summary.md").read_text() + "\n"


@pytest.mark.parametrize(
    "mismatch", ["missing", "duplicate", "run_id", "schema_version", "score_minimum", "schema_identity", "data", "statistics"]
)
def test_aggregate_rejects_mismatches(tmp_path: Path, mismatch: str) -> None:
    """
    Refuse stale, duplicate or missing shard evidence before publishing a final report.

    Args:
        tmp_path (Path): Shard report workspace.
        mismatch (str): Evidence component deliberately corrupted.

    Returns:
        None: Missing idle shards and inconsistent policies never produce a passing report.
    """
    for index in range(1, 4):
        path = shard_report(tmp_path / "source", index)
    report = json.loads(path.read_text())
    if mismatch == "missing":
        path.unlink()
    elif mismatch == "data":
        (path.parent / "details.jsonl").write_text("corrupted\n")
    else:
        report["shard" if mismatch == "duplicate" else mismatch] = "1-of-3" if mismatch == "duplicate" else "different"
        path.write_text(json.dumps(report))
    with pytest.raises(ValueError):
        aggregate(tmp_path / "source", tmp_path / "final", shards=3, run_id="pipeline-123-attempt-1", version="1.35.0", minimum=5)
    assert not (tmp_path / "final/summary.json").exists()


def test_missing_and_unsuccessful_scans(tmp_path: Path) -> None:
    """
    Preserve missing jobs and nonzero process exits despite successful JSON checks.

    Args:
        tmp_path (Path): Captured resource output.

    Returns:
        None: Operational failures cannot be overridden by an acceptable score.
    """
    missing = read_result(tmp_path / "absent", exit_code=None)
    assert missing["error"]
    raw = tmp_path / "stdout"
    raw.write_text('[{"valid":true,"score":5}]')
    statistics = SecurityStatistics()
    statistics.observe(read_result(raw, exit_code=2), 0)
    assert statistics.failed_resources == statistics.scanner_failures == 1
    assert statistics.failed_checks == 0
    assert read_result(raw, exit_code=None)["error"]
