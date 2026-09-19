"""
Verify parallel security scans use local schemas and preserve shard ownership and failures.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.execution.processes import Processes
from hypothesis_helm.integrations import kubesec
from hypothesis_helm.integrations.sharding import Shard


@pytest.mark.parametrize("validate_rest", [False, True])
@pytest.mark.parametrize("pre_sharded", [False, True])
def test_parallel_scan(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, pre_sharded: bool, validate_rest: bool) -> None:
    """
    Run the real GNU scheduler with local schema arguments and one failing security scan.

    Args:
        tmp_path (Path): Isolated binary and reports.
        monkeypatch (pytest.MonkeyPatch): Substitute a fixed available CPU count.
        pre_sharded (bool): Whether to scan every incoming record or assign a partition.
        validate_rest (bool): Whether to validate unsupported resources with native schema validation.

    Returns:
        None: Resource ownership, CPU-sized concurrency and failure propagation are correct.
    """
    if not shutil.which("parallel"):
        pytest.skip("GNU Parallel is required")
    binary = tmp_path / "kubesec"
    binary.write_text(
        dedent(
            """
            #!/usr/bin/env python3
            import json, pathlib, sys
            args = sys.argv[1:]
            assert args[0] == "scan"
            assert args[args.index("--exit-code") + 1] == "0"
            assert args[args.index("--schema-location") + 1].startswith("/")
            assert args[args.index("--kubernetes-version") + 1] == "1.35.0"
            resource = json.loads(pathlib.Path(args[-1]).read_text())
            bad = resource["metadata"]["name"] == "bad"
            print(json.dumps([{
                "object": resource["metadata"]["name"], "valid": True, "score": -1 if bad else 0,
                "scoring": {"critical": [{"points": -1}] if bad else [], "advise": [{"points": 1}]},
            }]))
            sys.exit(2 if bad else 0)
            """
        ).lstrip()
    )
    binary.chmod(0o755)
    monkeypatch.setattr(os, "process_cpu_count", lambda: 3)
    source = tmp_path / "manifests.jsonl"
    source.write_text(
        "\n".join(
            json.dumps({"apiVersion": "v1", "kind": kind, "metadata": {"name": name}})
            for kind, name in [
                ("Pod", "bad"),
                ("Pod", "good"),
                ("ConfigMap", "ignored"),
                ("Pod", "last"),
            ]
        )
        + "\n"
    )
    schemas = tmp_path / "schemas {}"
    schemas.mkdir()
    (schemas / "configmap-v1.json").write_text('{"type":"object"}')
    config = json.dumps(
        {
            "version": "1.35.0",
            "schemas": str(tmp_path / "schemas {}"),
            "identity": "test-snapshot",
        }
    )
    assert (
        kubesec.scan(
            source,
            tmp_path / "results with spaces",
            config,
            executable=str(binary),
            shard=Shard(1, 2),
            pre_sharded=pre_sharded,
            validate_rest=validate_rest,
        )
        == 1
    )
    output = tmp_path / "results with spaces/shards/1-of-2"
    summary = json.loads((output / "summary.json").read_text())
    assert summary["score_minimum"] == 0
    assert summary["statistics"]["failed_checks"] == 1
    assert summary["statistics"]["below_minimum"] == 1
    assert summary["statistics"]["invalid_resources"] == 0
    assert summary["statistics"]["report_errors"] == 0
    assert summary["statistics"]["critical"] == 1
    assert summary["jobs"] == 3
    assert summary["scanned"] == (3 if pre_sharded else 1)
    assert summary["skipped"] == (0 if validate_rest else 1)
    assert summary["schema_scanned"] == int(validate_rest)
    if validate_rest:
        assert json.loads((output / "schema-validation.json").read_text())["status"] == "passed"
    assert len((output / "joblog.tsv").read_text().splitlines()) == summary["scanned"] + 1
    assert len(list((output / "manifests").glob("*.json"))) == summary["scanned"]
    assert summary["schema_identity"] == "test-snapshot"


def test_worker_override() -> None:
    """
    Enforce a finite positive number of security workers.

    Returns:
        None: User limits override automatic detection and invalid values fail.
    """
    assert kubesec.worker_count("2") == 2
    for value in ("0", "-1", "all"):
        with pytest.raises(ValueError):
            kubesec.worker_count(value)


def test_fallback_failure(tmp_path: Path) -> None:
    """
    Fail a routed scan when only an unsupported resource violates its schema.

    Args:
        tmp_path (Path): Isolated executable, input, and artifacts.

    Returns:
        None: native schema validation failures propagate without any Kubesec tasks.
    """
    if not shutil.which("parallel"):
        pytest.skip("GNU Parallel is required")
    binary = tmp_path / "validator"
    binary.write_text("#!/bin/sh\necho invalid-schema\nexit 1\n")
    binary.chmod(0o755)
    source = tmp_path / "manifests.jsonl"
    source.write_text('{"apiVersion":"v1","kind":"Service"}\n')
    configuration = json.dumps(
        {
            "version": "1.35.0",
            "schemas": str(tmp_path),
            "identity": "test",
        }
    )
    output = tmp_path / "reports"
    assert kubesec.scan(source, output, configuration, executable=str(binary), validate_rest=True) == 1
    summary = json.loads((output / "summary.json").read_text())
    assert summary["scanned"] == 0
    assert summary["schema_scanned"] == 1
    assert summary["schema_exit_code"] == 1
    assert summary["status"] == "failed"
    assert not (output / "joblog.tsv").exists()


@pytest.mark.parametrize("minimum", [0, 5, 6])
def test_minimum_score_with_successful_scanner(tmp_path: Path, minimum: int) -> None:
    """
    Enforce the score floor even when every Kubesec process exits zero.

    Args:
        tmp_path (Path): Scanner executable, input and reports.
        minimum (int): Threshold below, equal to or above the observed score.

    Returns:
        None: Equality passes and raising the floor independently fails the gate.
    """
    if not shutil.which("parallel"):
        pytest.skip("GNU Parallel is required")
    binary = tmp_path / "kubesec"
    binary.write_text('#!/bin/sh\nprintf \'[{"object":"Pod/demo","valid":true,"score":5}]\\n\'\n')
    binary.chmod(0o755)
    source = tmp_path / "manifests.jsonl"
    source.write_text('{"apiVersion":"v1","kind":"Pod","metadata":{"name":"demo"}}\n')
    configuration = json.dumps({"version": "1.35.0", "schemas": str(tmp_path), "identity": "snapshot"})
    output = tmp_path / "reports"
    assert kubesec.scan(source, output, configuration, executable=str(binary), score_minimum=minimum) == int(minimum > 5)
    summary = json.loads((output / "summary.json").read_text())
    assert summary["parallel_exit_code"] == 0
    assert summary["statistics"]["below_minimum"] == int(minimum > 5)
    # Reusing an output directory must not count results from the earlier attempt.
    source.write_text("")
    assert kubesec.scan(source, output, configuration, executable=str(binary), shard=Shard(3, 3)) == 0
    idle = json.loads((output / "shards/3-of-3/summary.json").read_text())
    assert idle["statistics"]["resources"] == idle["statistics"]["checks"] == 0


def test_interrupted_scan_retains_missing_work(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Publish incomplete security evidence after the process owner handles interruption.

    Args:
        tmp_path (Path): Input and reports.
        monkeypatch (pytest.MonkeyPatch): Interrupt the GNU Parallel invocation.

    Returns:
        None: The wrapper returns 130 and missing work cannot appear successful.
    """

    def run(self: Processes, command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        """
        Identify GNU Parallel and interrupt the actual scan.

        Args:
            self (Processes): Process owner.
            command (list[str]): Version probe or scan command.
            **kwargs (object): Process options.

        Returns:
            subprocess.CompletedProcess[str]: Version probe response only.
        """
        if "--version" in command:
            return subprocess.CompletedProcess(command, 0, "GNU parallel", "")
        Path(command[command.index("--joblog") + 1]).write_text("Seq\tExitval\tSignal\n1\t")
        raise KeyboardInterrupt

    monkeypatch.setattr(Processes, "run", run)
    monkeypatch.setattr(shutil, "which", lambda name: sys.executable)
    source = tmp_path / "manifests.jsonl"
    source.write_text('{"apiVersion":"v1","kind":"Pod"}\n')
    configuration = json.dumps({"version": "1.35.0", "schemas": str(tmp_path), "identity": "snapshot"})
    assert kubesec.scan(source, tmp_path / "reports", configuration) == 130
    summary = json.loads((tmp_path / "reports/summary.json").read_text())
    assert summary["status"] == "failed"
    assert summary["statistics"]["resources"] == summary["statistics"]["report_errors"] == 1
    assert summary["statistics"]["checks"] == 0
