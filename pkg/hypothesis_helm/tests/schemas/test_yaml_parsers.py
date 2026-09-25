"""
Exercise parser selection, independent YAML engines and validation/cache boundaries.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.suites.generate import generate_tests
from hypothesis_helm.charts.suites.runtime import prepared_chart
from hypothesis_helm.charts.testing.paths import check_paths
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import parsers, yamlio
from hypothesis_helm.cli import argument_parser
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.exceptions.rendering import ManifestParseError, RenderFailure
from hypothesis_helm.execution.state.cache import fingerprint
from hypothesis_helm.execution.state.render_hashes import RenderHashes
from hypothesis_helm.schemas.configuration.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests.execution.test_path_workers import fixture_chart


@pytest.mark.parametrize("backend", parsers.BACKENDS)
def test_duplicates_merges_anchors_and_multiple_documents(backend: str) -> None:
    """
    Reject duplicate keys without rejecting ordinary anchor-based defaults and merge overrides.

    Args:
        backend (str): Selected manifest reader.

    Returns:
        None: Independent engines retain stream structure and strict duplicate checking.
    """
    source = dedent("""
    base: &base
      key: original
    merged:
      <<: *base
      key: override
    ---
    =: =
    """)
    documents = parsers.load_all(source, backend=backend)
    assert documents == [{"base": {"key": "original"}, "merged": {"key": "override"}}, {"=": "="}]
    for invalid in ("a: 1\na: 2", "outer: {key: first, key: second}", "base: &b {x: 1}\nnext: {<<: *b, x: 2, x: 3}"):
        with pytest.raises(ManifestParseError, match=backend):
            parsers.load_all(invalid, backend=backend)
    with pytest.raises(ManifestParseError):
        parsers.load_all("x: [", backend=backend)


def test_independent_parser_exposes_round_trip_disagreement() -> None:
    """
    Reproduce Zipkin's whitespace-only leading block line without any chart-specific logic.

    Returns:
        None: PyYAML accepts the valid block while the current round-trip reader reports its parser error.
    """
    source = "items:\n  - args:\n      - |\n  \n        hello\n"
    assert parsers.load_all(source, backend="pyyaml") == [{"items": [{"args": ["\nhello\n"]}]}]
    with pytest.raises(ManifestParseError, match="ruamel:"):
        parsers.load_all(source, backend="ruamel")


@pytest.mark.parametrize("backend", ["ruamel-safe", "pyyaml"])
def test_safe_backends_reject_object_construction(backend: str, tmp_path: Path) -> None:
    """
    Never execute a Python object tag embedded in a rendered manifest.

    Args:
        backend (str): Safe parser implementation.
        tmp_path (Path): Sentinel whose creation would indicate unsafe evaluation.

    Returns:
        None: Construction tags fail as syntax/constructor errors without side effects.
    """
    target = tmp_path / "executed"
    source = f"!!python/object/apply:pathlib.Path.touch [!!python/object/apply:pathlib.Path [{json.dumps(str(target))}]]"
    with pytest.raises(ManifestParseError):
        parsers.load_all(source, backend=backend)
    assert not target.exists()


@pytest.mark.parametrize("command", ["audit", "generate", "test", "scan", "run"])
def test_cli_accepts_parser_selection(command: str) -> None:
    """
    Expose the backend for local, remote and saved-suite workflows.

    Args:
        command (str): Chart-facing CLI command.

    Returns:
        None: Parser options are available without executing a scan.
    """
    args = argument_parser().parse_args([command, "example", "--yaml-parser", "pyyaml"])
    assert args.yaml_parser == "pyyaml"


def test_policy_overrides_cache_identity_and_keeps_values_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Carry validated configuration into cache keys while leaving values-file editing unchanged.

    Args:
        tmp_path (Path): Configuration file and cache fingerprint root.
        monkeypatch (pytest.MonkeyPatch): Isolate parser configuration.

    Returns:
        None: Overrides take precedence and cached validations cannot cross parser choices.
    """
    config = tmp_path / "config.yaml"
    config.write_text("yaml_parser: pyyaml\n")
    policy = load_policy(config)
    monkeypatch.setenv(ENVIRONMENT, json.dumps(policy))
    refresh_env()
    assert parsers.selected() == "pyyaml"
    first = fingerprint(tmp_path, 0, None, "none")
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(config, yaml_parser="ruamel-safe")))
    refresh_env()
    assert parsers.selected() == "ruamel-safe"
    assert fingerprint(tmp_path, 0, None, "none") != first
    original = "# retained comment\nfirst: &shared {name: value}\nsecond: *shared\n"
    loaded = yamlio.load(original)
    assert mapping(loaded)["first"] is mapping(loaded)["second"]
    assert "# retained comment" in yamlio.dump(loaded)
    assert "&shared" in yamlio.dump(loaded)
    config.write_text("yaml_parser: unsafe\n")
    with pytest.raises(ValueError, match="yaml_parser"):
        load_policy(config)


@pytest.mark.parametrize("backend", parsers.BACKENDS)
def test_manifest_checks_and_cache_context_use_selected_parser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, backend: str) -> None:
    """
    Keep resource validation independent of syntax-engine choice and label parser failures.

    Args:
        tmp_path (Path): Minimal chart model.
        monkeypatch (pytest.MonkeyPatch): Install the parser as coordinator policy.
        backend (str): Manifest reader under test.

    Returns:
        None: Wrong manifest types and duplicate keys remain findings across all parsers.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"yaml_parser": backend}))
    refresh_env()
    chart = Chart(tmp_path, {}, {})
    with pytest.raises(RenderFailure, match="HH1101") as error:
        render(chart, {}, rendered_output="kind: Pod\nkind: ConfigMap\n", stream=False)
    assert backend in str(error.value)
    with pytest.raises(RenderFailure, match="HH1105"):
        render(chart, {}, rendered_output="apiVersion: v1\nkind: ConfigMap\nmetadata: {name: 0}\n", stream=False)
    hashes = RenderHashes()
    output = "apiVersion: v1\nkind: ConfigMap\nmetadata: {name: valid}\n"
    render(chart, {}, rendered_output=output, hashes=hashes, stream=False)
    render(chart, {}, rendered_output=output, hashes=hashes, stream=False)
    assert hashes.snapshot()["validation_cache_hits"] == 1
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"yaml_parser": "pyyaml" if backend != "pyyaml" else "ruamel"}))
    refresh_env()
    render(chart, {}, rendered_output=output, hashes=hashes, stream=False)
    assert hashes.snapshot()["validation_cache_hits"] == 1


def test_saved_suite_restores_parser_and_explicit_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Replay the recorded reader by default and honor a deliberate run-time override.

    Args:
        tmp_path (Path): Chart and generated suite directories.
        monkeypatch (pytest.MonkeyPatch): Set and clear explicit run policy.

    Returns:
        None: Suite-local parser context resets on exit and both domain identities are distinct.
    """
    source = tmp_path / "chart"
    source.mkdir()
    chart = fixture_chart(source)
    generated = tmp_path / "suite"
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"yaml_parser": "pyyaml"}))
    refresh_env()
    generate_tests(chart, generated)
    frozen = json.loads((generated / "input-domains.json").read_text())
    assert frozen["yaml_parser"] == "pyyaml"
    monkeypatch.delenv(ENVIRONMENT)
    refresh_env()
    with prepared_chart(source, generated) as replay:
        assert parsers.selected() == "pyyaml"
        saved_identity = replay.input_domains().identity
    assert parsers.selected() == "ruamel"
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"yaml_parser": "ruamel-safe"}))
    refresh_env()
    with prepared_chart(source, generated) as replay:
        assert parsers.selected() == "ruamel-safe"
        assert replay.input_domains().identity != saved_identity


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_path_workers_inherit_manifest_parser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Use the independent parser in actual child workers, not only in the coordinator.

    Args:
        tmp_path (Path): Chart and worker output directory.
        monkeypatch (pytest.MonkeyPatch): Expose worker entry points and coordinator policy.

    Returns:
        None: Worker phases accept a block rejected by the default round-trip parser.
    """
    monkeypatch.setenv("PATH", f"{Path(sys.executable).parent}:{os.environ['PATH']}")
    refresh_env()
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"yaml_parser": "pyyaml"}))
    refresh_env()
    chart = fixture_chart(tmp_path)
    template = chart.path / "templates/config.yaml"
    template.write_text(template.read_text() + "  script: |\n \n    hello\n")
    result = check_paths(chart, budget=30, max_examples=1, seed=0, jobs=2, artifacts=tmp_path / "results", helm="helm", timeout=10)
    assert result["status"] == "passed", result.get("error")
    phases = [mapping(phase) for phase in sequence(result["phases"]) if "worker_pid" in mapping(phase)]
    assert phases
    assert all(mapping(phase["input_domains"])["yaml_parser"] == "pyyaml" for phase in phases)
