"""
Verify sparse schema caching and per-render conformity failures.
"""

import json
import shutil
import subprocess
from pathlib import Path
from textwrap import dedent, indent
from unittest.mock import Mock

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.execution.cache import fingerprint
from hypothesis_helm.execution.render_hashes import RenderHashes
from hypothesis_helm.rules import RenderFailure
from hypothesis_helm.schemas import conformity
from hypothesis_helm.schemas.contracts import mapping, sequence


def test_sparse_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Resolve latest stable schemas, retain immutable snapshots, and reuse them offline.

    Args:
        tmp_path (Path): Temporary upstream and cache directories.
        monkeypatch (pytest.MonkeyPatch): Substitute a local schema upstream.

    Returns:
        None: Only the selected release is checked out and cached content stays stable.
    """
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    conformity.git(upstream, "init", "-b", "master")
    for version in ("1.30.0", "1.31.0", "1.32.0-alpha.1"):
        folder = upstream / f"v{version}-standalone-strict"
        folder.mkdir()
        (folder / "configmap-v1.json").write_text('{"type":"object"}')
    conformity.git(upstream, "add", ".")
    conformity.git(
        upstream,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.org",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-m",
        "schemas",
    )
    monkeypatch.setattr(conformity, "REPOSITORY", str(upstream))
    cache = tmp_path / "cache"
    configuration = json.loads(conformity.prepare(cache, "latest"))
    assert configuration["version"] == "1.31.0"
    assert (cache / "repository/v1.31.0-standalone-strict/configmap-v1.json").is_file()
    assert not (cache / "repository/v1.30.0-standalone-strict").exists()
    assert json.loads(conformity.prepare(cache, "latest", True)) == configuration
    old = json.loads(conformity.prepare(cache, "1.30.0"))
    assert Path(configuration["schemas"]).is_dir()
    assert Path(old["schemas"]).is_dir()
    files_before = {p: p.read_bytes() for p in cache.rglob("*") if p.is_file()}
    inspected = json.loads(conformity.prepare(cache, "1.30.0", read_only=True))
    assert inspected == old
    assert files_before == {p: p.read_bytes() for p in cache.rglob("*") if p.is_file()}
    newer = upstream / "v1.32.0-standalone-strict"
    newer.mkdir()
    (newer / "configmap-v1.json").write_text('{"type":"object","title":"new"}')
    conformity.git(upstream, "add", ".")
    conformity.git(
        upstream,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.org",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-m",
        "new release",
    )
    refreshed = json.loads(conformity.prepare(cache, "latest"))
    assert refreshed["version"] == "1.32.0"
    assert Path(configuration["schemas"]).is_dir()
    restored_cache = tmp_path / "restored"
    shutil.copytree(cache, restored_cache)
    restored = json.loads(conformity.prepare(restored_cache, "latest", True))
    assert restored["identity"] == refreshed["identity"]
    assert Path(restored["schemas"]).is_relative_to(restored_cache)
    with pytest.raises(ValueError, match="no published"):
        conformity.prepare(cache, "9.9.9", True)
    with pytest.raises(ValueError, match="exact version"):
        conformity.prepare(cache, "../escape")
    with pytest.raises(ValueError, match="cache is empty"):
        conformity.prepare(tmp_path / "empty", "latest", True)
    catalog = cache / "catalogs/1.30.0/input-domains.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text('{"version":"1.30.0","resources":{}}')
    first = json.loads(conformity.prepare(cache, "1.30.0", True))
    catalog.write_text('{"version":"1.30.0","resources":{"v1/Pod":{}}}')
    second = json.loads(conformity.prepare(cache, "1.30.0", True))
    assert first["catalog_digest"] != second["catalog_digest"]
    assert json.loads(Path(first["catalog"]).read_text())["resources"] == {}
    assert "v1/Pod" in json.loads(Path(second["catalog"]).read_text())["resources"]


def test_validator_boundary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Validate manifests in process and invalidate outcomes when conformity is enabled.

    Args:
        tmp_path (Path): Isolated suite directory.
        monkeypatch (pytest.MonkeyPatch): Select a local schema cache.

    Returns:
        None: Strict local-only validation errors fail the property.
    """
    monkeypatch.delenv(conformity.ENVIRONMENT, raising=False)
    before = fingerprint(tmp_path, 0, None, "none")
    conformity.validate("ignored", 1)
    monkeypatch.setenv(
        conformity.ENVIRONMENT,
        json.dumps(
            {
                "version": "1.31.0",
                "schemas": str(tmp_path),
            }
        ),
    )
    assert fingerprint(tmp_path, 0, None, "none") != before

    (tmp_path / "configmap-v1.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {
                    "apiVersion": {"const": "v1"},
                    "kind": {"const": "ConfigMap"},
                    "data": {"type": "object", "additionalProperties": {"type": "string"}},
                },
                "additionalProperties": False,
            }
        )
    )
    conformity.validate('apiVersion: v1\nkind: ConfigMap\ndata: {answer: "42"}', 1)
    with pytest.raises(AssertionError, match=r"ConfigMap \$\.data\.answer"):
        conformity.validate("apiVersion: v1\nkind: ConfigMap\ndata: {answer: 42}", 1)
    with pytest.raises(AssertionError, match="Additional properties"):
        conformity.validate("apiVersion: v1\nkind: ConfigMap\nunexpected: true", 1)
    with pytest.raises(AssertionError, match="no cached schema"):
        conformity.validate("apiVersion: v1\nkind: Secret", 1)


@pytest.mark.parametrize("valid", [False, True])
@pytest.mark.parametrize("listed", [False, True])
@pytest.mark.parametrize("prefetched", [False, True])
def test_render_parses_once_for_schema_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, valid: bool, listed: bool, prefetched: bool
) -> None:
    """
    Share parsed manifests across envelope checks and API schema validation.

    Args:
        tmp_path (Path): Isolated schema snapshot and chart location.
        monkeypatch (pytest.MonkeyPatch): Track parsing and replace the Helm invocation.
        valid (bool): Whether the rendered data satisfies the string schema.
        listed (bool): Wrap the resource in a Kubernetes List.
        prefetched (bool): Supply output from the parallel renderer's prefetch boundary.

    Returns:
        None: One parse preserves aliases and empty documents while schema failures retain their code and resources.
    """
    (tmp_path / "configmap-v1.json").write_text(
        json.dumps({"type": "object", "properties": {"data": {"type": "object", "additionalProperties": {"type": "string"}}}})
    )
    monkeypatch.setenv(conformity.ENVIRONMENT, json.dumps({"version": "1.35.0", "schemas": str(tmp_path)}))
    output = dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: parse-once
        data:
          answer: &answer "42"
          alias: *answer
    """).lstrip()
    if not valid:
        output = output.replace('"42"', "42")
    if listed:
        output = dedent("""
            apiVersion: v1
            kind: List
            items:
              -
        """).lstrip() + indent(output, "    ")
    output = (
        dedent("""
        ---
        # Empty document
        ---
    """).lstrip()
        + output
        + "---\n"
    )
    parser = Mock(wraps=yamlio.load_all)
    helm = Mock(return_value=output)
    monkeypatch.setattr(yamlio, "load_all", parser)
    monkeypatch.setattr("hypothesis_helm.charts.testing.rendering.render_output", helm)
    chart = Chart(tmp_path, {"type": "object"}, {})
    hashes = RenderHashes()
    if valid:
        resources = render(chart, {}, hashes=hashes, stream=False, rendered_output=output if prefetched else None)
        resource = mapping(sequence(resources[0]["items"])[0]) if listed else resources[0]
        assert resource["data"] == {"answer": "42", "alias": "42"}
        assert hashes.snapshot()["validated_entries"] == 1
    else:
        with pytest.raises(RenderFailure, match=r"HH1108.*ConfigMap.*data\.") as failure:
            render(chart, {}, hashes=hashes, stream=False, rendered_output=output if prefetched else None)
        assert failure.value.resources
        assert hashes.snapshot()["validated_entries"] == 0
    parser.assert_called_once_with(output)
    assert helm.call_count == (0 if prefetched else 1)


def test_cli_validation_scope(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Propagate validator configuration only during an explicitly enabled Helm command.

    Args:
        tmp_path (Path): Saved suite location.
        monkeypatch (pytest.MonkeyPatch): Replace preparation and suite execution.

    Returns:
        None: Collection avoids downloads and configuration does not leak across runs.
    """
    import os

    from hypothesis_helm import cli

    prepared: list[str] = []

    def prepare(cache: Path, version: str, offline: bool = False) -> str:
        """
        Record schema preparation without downloading artifacts.

        Args:
            cache (Path): Schema cache directory.
            version (str): Requested schema version.
            offline (bool): Whether network access is disabled.

        Returns:
            str: Test configuration.
        """
        prepared.append(version)
        return '{"version":"1.31.0"}'

    def run(directory: Path, **kwargs: object) -> int:
        """
        Observe the configuration inherited by the saved-suite runner.

        Args:
            directory (Path): Suite location.
            **kwargs (object): Runner options.

        Returns:
            int: Successful test status.
        """
        assert (conformity.ENVIRONMENT in os.environ) == (not kwargs["collect_only"])
        return 0

    monkeypatch.setattr(cli, "prepare", prepare)
    monkeypatch.setattr(cli, "run_suite", run)
    monkeypatch.delenv(conformity.ENVIRONMENT, raising=False)
    arguments = ["run", str(tmp_path), "--validate-schemas", "--schema-version", "1.31.0"]
    assert cli.main(arguments) == 0
    assert conformity.ENVIRONMENT not in os.environ
    assert cli.main([*arguments, "--collect-only"]) == 0
    assert prepared == ["1.31.0"]
    assert cli.main(["schemas", "--schema-cache-dir", str(tmp_path)]) == 0
    assert prepared == ["1.31.0", "latest"]


def test_memory_snapshot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Verify atomic memory staging, reuse, mount checks, and capacity failures.

    Args:
        tmp_path (Path): Isolated snapshot and simulated mount.
        monkeypatch (pytest.MonkeyPatch): Replace Linux mount detection for portability.

    Returns:
        None: Only complete snapshots are reused and unsuitable mounts are rejected.
    """
    snapshot = tmp_path / "disk" / "identity" / "v1.35.0-standalone-strict"
    snapshot.mkdir(parents=True)
    (snapshot / "pod.json").write_text('{"type":"object"}')
    monkeypatch.delenv("HYPOTHESIS_HELM_SCHEMA_MEMORY_DIR", raising=False)
    assert conformity.memory_snapshot(snapshot) == snapshot
    root = tmp_path / "memory"
    monkeypatch.setenv("HYPOTHESIS_HELM_SCHEMA_MEMORY_DIR", str(root))
    monkeypatch.setattr(
        "hypothesis_helm.schemas.conformity.Processes.run", lambda *args, **kwargs: subprocess.CompletedProcess([], 0, "ext4\n")
    )
    with pytest.raises(ValueError, match="Linux tmpfs"):
        conformity.memory_snapshot(snapshot)
    assert not root.exists()
    monkeypatch.setattr(
        "hypothesis_helm.schemas.conformity.Processes.run", lambda *args, **kwargs: subprocess.CompletedProcess([], 0, "tmpfs\n")
    )
    staged = conformity.memory_snapshot(snapshot)
    assert staged == root / snapshot.parent.name / snapshot.name
    assert (staged / "pod.json").read_bytes() == (snapshot / "pod.json").read_bytes()
    timestamp = (staged / "pod.json").stat().st_mtime_ns
    assert conformity.memory_snapshot(snapshot) == staged
    assert (staged / "pod.json").stat().st_mtime_ns == timestamp
    monkeypatch.setenv("HYPOTHESIS_HELM_SCHEMA_MEMORY_DIR", str(tmp_path / "full"))
    usage = shutil.disk_usage(tmp_path)
    monkeypatch.setattr(shutil, "disk_usage", lambda _: usage._replace(free=0))
    with pytest.raises(ValueError, match="free bytes"):
        conformity.memory_snapshot(snapshot)
    assert not (tmp_path / "full" / snapshot.parent.name).exists()
