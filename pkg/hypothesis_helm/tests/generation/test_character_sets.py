"""
Verify character-domain defaults, overrides, schema literals, and saved suites.
"""

import json
import os
import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from hypothesis import find, given, settings
from hypothesis import strategies as st
from jsonschema import validate

from hypothesis_helm.charts.suites.generate import generate_tests, strategy_source
from hypothesis_helm.charts.suites.runtime import prepared_chart
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.cli import main
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.execution.state.cache import fingerprint
from hypothesis_helm.schemas.configuration.characters import character_sets
from hypothesis_helm.schemas.configuration.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.generation.strategies import schema_strategy, supported_generated_text
from hypothesis_helm.tests.fixtures.cli import result_text


@pytest.mark.parametrize("schema", [{}, {"type": "object", "minProperties": 1}, {"type": "array", "items": {}, "minItems": 1}])
def test_ascii_in_unconstrained_json(schema: dict[str, object], monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Cover library fallbacks that can ignore the requested codec inside generic JSON.

    Args:
        schema (dict[str, object]): Open input domain.
        monkeypatch (pytest.MonkeyPatch): Isolate the default policy.

    Returns:
        None: Every sampled key and string is ASCII and schema-valid.
    """
    monkeypatch.delenv(ENVIRONMENT, raising=False)
    refresh_env()

    @settings(max_examples=80, deadline=None, derandomize=True)
    @given(schema_strategy(schema))
    def check(value: object) -> None:
        """
        Inspect all descendants of one generated JSON value.

        Args:
            value (object): Arbitrarily nested candidate.

        Returns:
            None: ASCII and control-character restrictions hold throughout the tree.
        """
        validate(value, schema)
        assert supported_generated_text(value)
        pending = [value]
        while pending:
            child = pending.pop()
            if isinstance(child, str):
                assert child.isascii()
            elif isinstance(child, dict):
                pending.extend(child)
                pending.extend(child.values())
            elif isinstance(child, list):
                pending.extend(child)

    check()


def test_unicode_is_explicit_and_preserves_controls_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Permit meaningful Unicode while retaining the existing control-character exclusion.

    Args:
        monkeypatch (pytest.MonkeyPatch): Enable Unicode in the inherited input policy.

    Returns:
        None: Native and generated Python strategies can produce non-ASCII text.
    """
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"character_sets": "unicode"}))
    refresh_env()
    schema = {"type": "string", "minLength": 1, "maxLength": 3}
    for strategy in (schema_strategy(schema), eval(strategy_source(schema), {"st": st})):
        found = find(
            strategy,
            lambda value: isinstance(value, str) and not value.isascii(),
            settings=settings(max_examples=100, deadline=None, derandomize=True),
        )
        assert supported_generated_text(found)


def test_authored_unicode_is_not_rewritten(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep declared Unicode keys and constants while restricting unrelated generated text.

    Args:
        monkeypatch (pytest.MonkeyPatch): Select the default ASCII mode.

    Returns:
        None: Literal Unicode survives, generated sibling text stays ASCII, and the schema holds.
    """
    monkeypatch.delenv(ENVIRONMENT, raising=False)
    refresh_env()
    schema = {
        "type": "object",
        "properties": {"日本語": {"const": "café"}, "free": {"type": "string", "minLength": 1}},
        "required": ["日本語", "free"],
        "additionalProperties": False,
    }

    @settings(max_examples=30, deadline=None, derandomize=True)
    @given(schema_strategy(schema))
    def check(value: object) -> None:
        """
        Verify one mixed authored and generated input.

        Args:
            value (object): Validated generated mapping.

        Returns:
            None: Declared literals are preserved without allowing unrestricted Unicode.
        """
        validate(value, schema)
        assert isinstance(value, dict)
        assert value["日本語"] == "café"
        assert value["free"].isascii() or value["free"] in {"日本語", "café"}

    check()


@pytest.mark.parametrize(
    "configured,override,expected",
    [(None, None, "ascii"), ("unicode", None, "unicode"), ("unicode", "ascii", "ascii"), ("ascii", "unicode", "unicode")],
)
def test_cli_character_precedence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, configured: str | None, override: str | None, expected: str
) -> None:
    """
    Exercise real CLI configuration resolution and generated policy snapshots.

    Args:
        tmp_path (Path): Policy and generated suite destination.
        monkeypatch (pytest.MonkeyPatch): Preserve a caller's unrelated inherited setting.
        configured (str | None): Optional YAML selection.
        override (str | None): Optional CLI selection.
        expected (str): Resolved character domain.

    Returns:
        None: The CLI wins, generated suites record the result, and the caller's environment is restored.
    """
    config = tmp_path / "config.yaml"
    config.write_text(yamlio.dump({"hypothesis": {"character_sets": configured}} if configured is not None else {}))
    previous = json.dumps({"character_sets": "unicode"})
    monkeypatch.setenv(ENVIRONMENT, previous)
    refresh_env()
    output = tmp_path / "suite"
    arguments = ["generate", "examples/workload", "--output", str(output), "--config", str(config)]
    if override is not None:
        arguments.extend(["--character-sets", override])
    assert main(arguments) == 0
    assert json.loads((output / "input-domains.json").read_text())["character_sets"] == expected
    assert os.environ[ENVIRONMENT] == previous


@pytest.mark.parametrize("invalid", ["latin", ["ascii"], True, None])
def test_invalid_character_config(tmp_path: Path, invalid: object) -> None:
    """
    Reject malformed character policies before testing starts.

    Args:
        tmp_path (Path): Configuration directory.
        invalid (object): Unsupported YAML option.

    Returns:
        None: The configuration error names the two supported modes.
    """
    config = tmp_path / "config.yaml"
    config.write_text(yamlio.dump({"hypothesis": {"character_sets": invalid}}))
    with pytest.raises(ValueError, match="character_sets must be 'ascii' or 'unicode'"):
        load_policy(config)


def test_saved_character_policy_and_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Retain Unicode for dependent generation in saved suites and separate cached successes.

    Args:
        tmp_path (Path): Generated suite destination.
        monkeypatch (pytest.MonkeyPatch): Change the caller's policy after generation.

    Returns:
        None: Standalone replay restores its alphabet temporarily and cache keys distinguish modes.
    """
    chart = Path("examples/workload").resolve()
    suite = tmp_path / "suite"
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"character_sets": "unicode"}))
    refresh_env()
    generate_tests(chart, suite, max_examples=3)
    unicode_key = fingerprint(suite, 0, None, "none")
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"character_sets": "ascii"}))
    refresh_env()
    assert fingerprint(suite, 0, None, "none") != unicode_key
    assert character_sets() == "ascii"
    with prepared_chart(chart, suite):
        assert character_sets() == "unicode"
        found = find(schema_strategy({"type": "string", "pattern": "^[éΩ]$"}), lambda value: True)
        assert found in {"é", "Ω"}
    assert character_sets() == "ascii"


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("helm") is None, reason="Helm is required")
def test_unicode_policy_reaches_path_workers(tmp_path: Path, capfd: pytest.CaptureFixture[str]) -> None:
    """
    Pass an explicit Unicode policy to real worker processes on two generated paths.

    Args:
        tmp_path (Path): Minimal chart and worker artifacts.
        capfd (pytest.CaptureFixture[str]): Capture the CLI's final JSON report.

    Returns:
        None: Both Unicode-only properties complete using the requested policy.
    """
    chart = tmp_path / "chart"
    (chart / "templates").mkdir(parents=True)
    (chart / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "unicode-workers", "version": "0.1.0"}))
    (chart / "values.yaml").write_text(yamlio.dump({"first": "é", "second": "Ω"}))
    (chart / "values.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {name: {"type": "string", "pattern": "^[éΩ]$"} for name in ("first", "second")},
                "required": ["first", "second"],
                "additionalProperties": False,
            }
        )
    )
    (chart / "templates/configmap.yaml").write_text(
        dedent("""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: unicode-workers
            data:
              first: {{ .Values.first | quote }}
              second: {{ .Values.second | quote }}
        """).lstrip()
    )
    assert (
        main(
            [
                "test",
                str(chart),
                "--character-sets",
                "unicode",
                "--jobs",
                "2",
                "--max-examples",
                "2",
                "--no-cache",
                "--shard",
                "none",
                "--chart-timeout",
                "30s",
                "--artifact-dir",
                str(tmp_path / "artifacts"),
                "--log-file",
                "/dev/stderr",
            ]
        )
        == 0
    )
    output = capfd.readouterr()
    report = json.loads(result_text(output.out))
    assert report["settings"]["input_policy"]["character_sets"] == "unicode"
    assert report["charts"][0]["traversal"]["completed_paths"] == 2
