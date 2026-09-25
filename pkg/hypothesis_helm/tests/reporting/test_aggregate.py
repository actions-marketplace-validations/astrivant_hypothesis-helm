"""
Verify aggregation of self-contained reports transported from independent CI runners.
"""

import hashlib
import io
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from hypothesis_helm.cli import main
from hypothesis_helm.integrations.sharding import Shard


def records() -> list[dict[str, object]]:
    """
    Construct complete, disjoint reports whose original filesystem paths do not exist.

    Returns:
        list[dict[str, object]]: Two verified shard records covering six properties.
    """
    nodes = [f"test_chart_values.py::test_example[{index}]" for index in range(6)]
    digest = hashlib.sha256(json.dumps(sorted(nodes)).encode()).hexdigest()
    result = []
    for index in (1, 2):
        selected = [node for node in nodes if Shard(index, 2).includes(node)]
        junit = "<testsuites><testsuite>" + "".join(f'<testcase name="{node}"/>' for node in selected) + "</testsuite></testsuites>"
        result.append(
            {
                "run_id": "pipeline-42-attempt-1",
                "suite_fingerprint": "same-content",
                "suite": "/nonexistent/other-runner/generated",
                "status": "passed",
                "exit_code": 0,
                "jobs": 2,
                "started_epoch": 1000,
                "elapsed_seconds": 2,
                "junit": "/nonexistent/other-runner/junit.xml",
                "junit_xml": junit,
                "junit_sha256": hashlib.sha256(junit.encode()).hexdigest(),
                "shard": {
                    "index": index,
                    "total": 2,
                    "matched": len(nodes),
                    "matched_digest": digest,
                    "selected": len(selected),
                    "tests": selected,
                },
            }
        )
    return result


@pytest.mark.parametrize("encoding", ["array", "concatenated", "ndjson"])
def test_piped_reports(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, encoding: str) -> None:
    """
    Merge all supported pipe encodings without reading original JUnit or source files.

    Args:
        tmp_path (Path): Final report destination.
        monkeypatch (pytest.MonkeyPatch): Replace standard input.
        encoding (str): Transport representation.

    Returns:
        None: All report artifacts appear together with correct executed and selected counts.
    """
    reports = records()
    payload = (
        json.dumps(reports)
        if encoding == "array"
        else "\n".join(json.dumps(record, indent=2 if encoding == "concatenated" else None) for record in reports)
    )
    monkeypatch.setattr("sys.stdin", io.StringIO(payload))
    output = tmp_path / "final"
    assert (
        main(
            [
                "aggregate",
                "--shards",
                "2",
                "--run-id",
                "pipeline-42-attempt-1",
                "--output-dir",
                str(output),
            ]
        )
        == 0
    )
    assert {path.name for path in output.iterdir()} == {
        "report.json",
        "report.md",
        "report.pdf",
        "report-overview.png",
        "junit.xml",
    }
    report = json.loads((output / "report.json").read_text())
    assert report["properties"]["selected"] == report["properties"]["tests"] == 6
    assert report["charts"][0]["elapsed_seconds"] == 2
    assert report["finished_epoch"] == 1002
    assert report["finish_time_source"] == "derived-shard-timings"
    assert report["run_hash"] in (output / "report.md").read_text()
    assert report["artifact_checksums"]["report-overview.png"] == hashlib.sha256((output / "report-overview.png").read_bytes()).hexdigest()


def test_aggregate_uses_latest_recorded_shard_finish(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Preserve actual shard finish timestamps when aggregation runs later.

    Args:
        tmp_path (Path): Final report destination.
        monkeypatch (pytest.MonkeyPatch): Supply independent shard records through standard input.

    Returns:
        None: Aggregate timing spans the earliest start through the latest recorded finish.
    """
    reports = records()
    reports[0]["finished_epoch"] = 1003.5
    reports[1]["finished_epoch"] = 1004.5
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(reports)))
    output = tmp_path / "final"
    assert main(["aggregate", "--shards", "2", "--run-id", "pipeline-42-attempt-1", "--output-dir", str(output)]) == 0
    report = json.loads((output / "report.json").read_text())
    assert report["finished_epoch"] == 1004.5
    assert report["finish_time_source"] == "recorded-shards"
    assert report["elapsed_seconds"] == 4.5
    assert report["finished_at"] == "1970-01-01T00:16:44.500+00:00"


def test_aggregate_counts_distinct_junit_diagnostics(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep individual diagnostics available to report plots instead of one concatenated failure.

    Args:
        tmp_path (Path): Final report destination.
        monkeypatch (pytest.MonkeyPatch): Supply independently transported shard reports.

    Returns:
        None: Repeated property failures count once, while different diagnostics remain distinct.
    """
    reports = records()
    for record in reports:
        xml = ET.fromstring(str(record["junit_xml"]))
        for index, case in enumerate(xml.iter("testcase")):
            ET.SubElement(case, "failure").text = "same failure" if index == 0 else "another failure"
        junit = ET.tostring(xml, encoding="unicode")
        record.update(junit_xml=junit, junit_sha256=hashlib.sha256(junit.encode()).hexdigest(), exit_code=1, status="failed")
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(reports)))
    output = tmp_path / "final"
    assert main(["aggregate", "--shards", "2", "--run-id", "pipeline-42-attempt-1", "--output-dir", str(output)]) == 1
    report = json.loads((output / "report.json").read_text())
    assert report["properties"]["failures"] == 6
    assert len(report["charts"][0]["error_refs"]) == 2
    assert report["error_summary"]["unique_errors"] == 2


def test_directory_aggregation_publishes_outside_cached_shards(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Put the final bundle under docs/reports even when aggregation reads a cached directory.

    Args:
        tmp_path (Path): Isolated checkout containing downloaded shard reports.
        monkeypatch (pytest.MonkeyPatch): Resolve default publication paths in the checkout.

    Returns:
        None: Only the final report directory is published; cached shard ownership is unchanged.
    """
    monkeypatch.chdir(tmp_path)
    source = Path(".cache/downloaded")
    for index, record in enumerate(records(), 1):
        directory = source / "shards" / str(index)
        directory.mkdir(parents=True)
        (directory / "report.json").write_text(json.dumps(record))
    assert main(["aggregate", str(source), "--shards", "2", "--run-id", "pipeline-42-attempt-1"]) == 0
    assert Path("docs/reports/aggregate/report.pdf").is_file()
    assert not (source / "final").exists()
    assert len(list(source.glob("shards/*/report.json"))) == 2


@pytest.mark.parametrize("damage", ["missing", "duplicate", "run-id", "suite", "checksum", "inventory", "traversal", "ignored-rules"])
def test_incompatible_reports_never_publish(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, damage: str) -> None:
    """
    Reject missing or mixed pipeline artifacts before publishing any final report.

    Args:
        tmp_path (Path): Final report destination.
        monkeypatch (pytest.MonkeyPatch): Replace standard input.
        damage (str): Evidence to invalidate.

    Returns:
        None: Aggregation fails explicitly and leaves no final bundle.
    """
    reports = records()
    if damage == "missing":
        reports.pop()
    elif damage == "duplicate":
        reports[1] = reports[0]
    elif damage == "run-id":
        reports[1]["run_id"] = "another-attempt"
    elif damage == "suite":
        reports[1]["suite_fingerprint"] = "another-source"
    elif damage == "checksum":
        reports[1]["junit_xml"] = "<testsuites/>"
    elif damage == "ignored-rules":
        reports[1]["ignored_rules"] = ["HH1106"]
    elif damage == "traversal":
        reports[1]["traversal_strategy"] = "random"
    else:
        for record in reports:
            assignment = record["shard"]
            assert isinstance(assignment, dict)
            assignment["matched_digest"] = "same-but-wrong-in-both-shards"
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(reports)))
    output = tmp_path / "final"
    assert (
        main(
            [
                "aggregate",
                "--shards",
                "2",
                "--run-id",
                "pipeline-42-attempt-1",
                "--output-dir",
                str(output),
            ]
        )
        == 2
    )
    assert not output.exists()
