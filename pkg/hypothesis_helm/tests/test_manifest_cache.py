"""
Verify incremental runs preserve the complete manifest stream for external validators.
"""

import json
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.execution.manifests import ManifestStore
from hypothesis_helm.execution.suite import run_suite
from hypothesis_helm.integrations.sharding import Shard
from hypothesis_helm.reporting.output import MANIFEST_FD, MANIFEST_FORMAT
from hypothesis_helm.reporting.shards import aggregate
from hypothesis_helm.schemas.contracts import mapping, sequence


def execute(directory: Path, output: Path, *, jobs: int, format: str = "json", shard: Shard | None = None) -> tuple[int, dict[str, object]]:
    """
    Run a saved suite with a real output descriptor and read its current report.

    Args:
        directory (Path): Suite and cache root.
        output (Path): Manifest destination.
        jobs (int): Worker count.
        format (str): JSON or YAML stream encoding.
        shard (Shard | None): Optional ownership partition.

    Returns:
        tuple[int, dict[str, object]]: Exit status and current report.
    """
    with output.open("w") as stream:
        descriptor = MANIFEST_FD.set(stream.fileno())
        encoding = MANIFEST_FORMAT.set(format)
        try:
            status = run_suite(directory, jobs=jobs, rerun="failed", shard=shard, run_id="current")
        finally:
            MANIFEST_FORMAT.reset(encoding)
            MANIFEST_FD.reset(descriptor)
    results = directory / "shards" / shard.name if shard else directory
    return status, json.loads((results / "report.json").read_text())


@pytest.mark.parametrize("jobs", [1, 2])
@pytest.mark.parametrize("format", ["json", "yaml"])
def test_partial_retries_replay_and_corrupt_streams_rerun(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int, format: str) -> None:
    """
    Keep both properties' resources while rerunning failures or corrupt cached streams.

    Args:
        tmp_path (Path): Isolated generated suite.
        monkeypatch (pytest.MonkeyPatch): Enable CI defaults around explicit incremental selection.
        jobs (int): Serial or parallel execution.
        format (str): Current downstream output format.

    Returns:
        None: Cold, partial, fully cached and corrupt-cache runs preserve complete output.
    """
    monkeypatch.setenv("CI", "true")
    (tmp_path / "test_chart_values.py").write_text(
        dedent("""
        from pathlib import Path
        import pytest
        from hypothesis_helm.reporting.output import emit_manifest

        @pytest.mark.parametrize("name", ["a", "b"])
        def test_resource(name):
            with Path("calls").open("a") as stream:
                stream.write(name + "\\n")
            emit_manifest({"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": name}})
            assert name == "a" or Path("fixed").exists()
        """)
    )
    output = tmp_path / "manifests"
    for expected_status, expected_reused in ((1, 0), (0, 1), (0, 2)):
        status, report = execute(tmp_path, output, jobs=jobs, format=format)
        assert status == expected_status
        assert report["replayed_manifests"] == expected_reused
        assert len(sequence(report["reused_properties"])) == expected_reused
        resources = (
            list(yamlio.load_all(output.read_text()))
            if format == "yaml"
            else [json.loads(line) for line in output.read_text().splitlines()]
        )
        assert sorted(str(mapping(mapping(resource)["metadata"])["name"]) for resource in resources) == ["a", "b"]
        (tmp_path / "fixed").touch()
    assert (tmp_path / "calls").read_text().splitlines() in (["a", "b", "b"], ["b", "a", "b"])
    store = ManifestStore(Path(str(report["cache"])).with_suffix(".manifests"))
    blob = store.verified(str(sequence(report["reused_properties"])[0]))
    assert blob is not None
    blob.write_text("corrupt")
    status, report = execute(tmp_path, output, jobs=jobs, format=format)
    assert status == 0
    assert len(sequence(report["reused_properties"])) == report["replayed_manifests"] == 1
    assert len((tmp_path / "calls").read_text().splitlines()) == 4
    blob.unlink()
    status, report = execute(tmp_path, output, jobs=jobs, format=format)
    assert status == 0
    assert len(sequence(report["reused_properties"])) == report["replayed_manifests"] == 1
    assert len((tmp_path / "calls").read_text().splitlines()) == 5


def test_cached_and_empty_shards_still_aggregate(tmp_path: Path) -> None:
    """
    Publish current reports for idle shards and stream each cached property exactly once.

    Args:
        tmp_path (Path): Shared suite and isolated shard reports.

    Returns:
        None: Two properties across three shards aggregate after a fully cached rerun.
    """
    (tmp_path / "test_chart_values.py").write_text(
        dedent("""
        import pytest
        from hypothesis_helm.reporting.output import emit_manifest

        @pytest.mark.parametrize("name", ["a", "b"])
        def test_resource(name):
            emit_manifest({"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": name}})
        """)
    )
    for iteration in range(2):
        names: list[str] = []
        for index in range(1, 4):
            output = tmp_path / f"output-{index}.jsonl"
            status, report = execute(tmp_path, output, jobs=2, shard=Shard(index, 3))
            assert status == 0
            if iteration:
                assert report["workers"] == 0
                assert len(sequence(report["reused_properties"])) == mapping(report["shard"])["selected"]
            names.extend(json.loads(line)["metadata"]["name"] for line in output.read_text().splitlines())
        assert sorted(names) == ["a", "b"]
    assert aggregate([tmp_path], 3, "current", tmp_path / "aggregate") == 0


def test_metadata_cannot_point_outside_manifest_store(tmp_path: Path) -> None:
    """
    Treat malformed pointers as cache misses rather than reading arbitrary local files.

    Args:
        tmp_path (Path): Private manifest store.

    Returns:
        None: Untrusted pointer paths and mismatched property IDs never verify.
    """
    store = ManifestStore(tmp_path)
    for digest in ("../outside", "a" * 64):
        store.index("node").write_text(json.dumps({"version": 1, "node": "node", "sha256": digest}))
        assert store.verified("node") is None
