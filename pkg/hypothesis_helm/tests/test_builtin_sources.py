"""
Verify source acquisition, release comparisons and source-derived compiler facts.
"""

import hashlib
import json
from pathlib import Path

import pytest
from hypothesis_helm_catalog import builtins as builder
from hypothesis_helm_catalog import toolchain

from hypothesis_helm.compiler import builtins
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.asts.origins import Derived, Sequence
from hypothesis_helm.compiler.passes.discovery_functions import result
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests.test_templates import scan


def test_corrupt_cached_source_is_rejected(tmp_path: Path) -> None:
    """
    Reject a damaged artifact instead of silently generating different release facts.

    Args:
        tmp_path (Path): Isolated source cache.

    Returns:
        None: Both missing and corrupt offline inputs produce actionable failures.
    """
    record: dict[str, object] = {"name": "fixture", "version": "1", "sha256": hashlib.sha256(b"source").hexdigest()}
    with pytest.raises(ValueError, match="not cached"):
        builder.acquire(record, tmp_path, offline=True)
    (tmp_path / str(record["sha256"])).write_bytes(b"corrupt")
    with pytest.raises(ValueError, match="checksum mismatch"):
        builder.acquire(record, tmp_path, offline=True)


def test_check_mode_preserves_inventory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep comparison mode read-only and publish a rebuilt inventory atomically.

    Args:
        tmp_path (Path): Temporary generated registry.
        monkeypatch (pytest.MonkeyPatch): Replace the separately tested Go extraction step.

    Returns:
        None: A stale inventory fails checking and a rebuild makes it current.
    """
    monkeypatch.setattr(builder, "rebuild", lambda *args, **kwargs: {"functions": {"hello": {}}})
    output = tmp_path / "inventory.json"
    output.write_text("stale")
    arguments = ["--output", str(output), "--cache-dir", str(tmp_path), "--offline"]
    assert builder.main([*arguments, "--check"]) == 1
    assert output.read_text() == "stale"
    assert builder.main(arguments) == 0
    assert builder.main([*arguments, "--check"]) == 0


def test_extractor_matches_generated_inventory() -> None:
    """
    Require regeneration whenever extraction logic or the source lock changes.

    Returns:
        None: Checked-in facts identify this extractor and every locked source artifact.
    """
    inventory = mapping(json.loads(builder.LIBRARY.read_text()))
    assert inventory["extractor_sha256"] == toolchain.fingerprint()
    locked = json.loads(builder.LOCK.read_text())["sources"]
    assert [source["sha256"] for source in (mapping(raw) for raw in sequence(inventory["sources"]))] == [
        source["sha256"] for source in locked
    ]


@pytest.mark.parametrize("filename", ["main.go", "helm.go", "kubernetes.go", "go.mod", "go.sum"])
def test_extractor_identity_covers_all_compiled_sources(tmp_path: Path, filename: str) -> None:
    """
    Invalidate generated facts when either extraction mode or a pinned dependency changes.

    Args:
        tmp_path (Path): Isolated minimal Go module.
        filename (str): Compiled source or dependency manifest changed in this case.

    Returns:
        None: Production edits change the digest; test-only files do not.
    """
    for name in ("main.go", "helm.go", "kubernetes.go", "go.mod", "go.sum"):
        (tmp_path / name).write_text(name)
    baseline = toolchain.fingerprint(tmp_path)
    (tmp_path / "main_test.go").write_text("test-only change")
    assert toolchain.fingerprint(tmp_path) == baseline
    (tmp_path / filename).write_text("changed implementation or dependency")
    assert toolchain.fingerprint(tmp_path) != baseline


def test_generated_effects_and_shapes_enter_analysis() -> None:
    """
    Preserve native effects while allowing source-declared collections to retain their input origins.

    Returns:
        None: Alias effects agree, native random sources are retained and collection sizes remain unknown.
    """
    assert builtins.BUILTINS["mustMerge"].effects == builtins.BUILTINS["merge"].effects
    assert "randomness" in builtins.BUILTINS["encryptAES"].effects
    assert "external-state" in builtins.BUILTINS["getHostByName"].effects
    assert builtins.BUILTINS["fromYamlArray"].shape == "sequence"
    argument = Derived((("Values", "document"),))
    output = result("fromYamlArray", [argument])
    assert isinstance(output, Sequence) and not output.exact
    assert output.items == (Derived(argument.inputs, external=True),)


def test_unresolved_source_call_prevents_later_rejection(tmp_path: Path) -> None:
    """
    Do not turn a source-known return type into a concrete value for a rejection guard.

    Args:
        tmp_path (Path): Template using an unresolved deep-copy result in a guard.

    Returns:
        None: No rejection is predicted from the unresolved result.
    """
    scan(tmp_path, '{{ $copy := mustDeepCopy .Values }}{{ if not $copy.valid }}{{ fail "invalid" }}{{ end }}')
    contracts = Contracts.build(tmp_path)
    assert contracts.predict({"valid": False}) is None
    assert contracts.fallbacks
