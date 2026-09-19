"""
Exercise branch-specific generation, example budgets, source matrices and saved policies.
"""

import json
import os
from pathlib import Path

import pytest
from hypothesis import find, given, settings
from jsonschema import validators

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.generate import generate_tests, strategy_source
from hypothesis_helm.charts.generated import prepared_chart
from hypothesis_helm.charts.paths import check_paths
from hypothesis_helm.findings.configuration import COMPLETE_EXAMPLE
from hypothesis_helm.schemas.contracts import json_value, mapping, schema_strategy, sequence
from hypothesis_helm.schemas.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.selectors import SOURCE_ENVIRONMENT, SourceScope, matching_rules, selectors
from hypothesis_helm.schemas.settings import DEFAULT_CONTROLS, generation_settings, hypothesis_parameters, settings_at, validate_settings
from hypothesis_helm.tests.test_path_workers import fixture_chart


def install_policy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, document: dict[str, object]) -> dict[str, object]:
    """
    Resolve a real configuration file and expose it to native and generated workers.

    Args:
        tmp_path (Path): Directory for a configuration file.
        monkeypatch (pytest.MonkeyPatch): Restore the caller's policy after the test.
        document (dict[str, object]): User-facing configuration.

    Returns:
        dict[str, object]: Validated policy shared through the normal environment contract.
    """
    config = tmp_path / "policy.yaml"
    config.write_text(yamlio.dump(document))
    policy = load_policy(config)
    monkeypatch.setenv(ENVIRONMENT, json.dumps(policy))
    return policy


@pytest.mark.parametrize(
    "invalid",
    [
        {"hypothesis": {"max_examples": True}},
        {"hypothesis": {"max_examples": 0}},
        {"hypothesis": {"deadline_ms": float("inf")}},
        {"hypothesis": {"deadline_ms": -1}},
        {"hypothesis": {"phases": ["shrink"]}},
        {"hypothesis": {"phases": ["reuse", "generate"]}},
        {"hypothesis": {"suppress_health_check": ["unknown"]}},
        {"hypothesis": {"derandomize": True}},
        {"hypothesis": {"control_characters": {"exclude": "yes"}}},
        {"hypothesis": {"control_characters": {"allow": ["ab"]}}},
        {"hypothesis": {"control_characters": {"allow": ["a"]}}},
        {"hypothesis": {"control_characters": {"allowed": []}}},
        {"hypothesis": {"exclude_characters": [">", "|"]}},
    ],
)
def test_invalid_generation_settings(invalid: dict[str, object]) -> None:
    """
    Reject unsupported or malformed knobs before any chart tests run.

    Args:
        invalid (dict[str, object]): One invalid setting mapping.

    Returns:
        None: All malformed settings produce a configuration error.
    """
    with pytest.raises(ValueError):
        validate_settings(invalid)


def test_branch_inheritance_and_conflicts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Inherit each setting independently and reject ambiguous same-depth overrides.

    Args:
        tmp_path (Path): Chart and local configuration.
        monkeypatch (pytest.MonkeyPatch): Isolate inherited policy.

    Returns:
        None: Deep overrides keep inherited siblings and budgets resolve per property.
    """
    chart = fixture_chart(tmp_path)
    install_policy(
        tmp_path,
        monkeypatch,
        {
            "hypothesis": {"max_examples": 12, "deadline_ms": 4000},
            "input_constraints": [
                {"charts": ["workers"], "path": "$", "hypothesis": {"max_examples": 14}},
                {"charts": ["workers"], "path": "$.items", "hypothesis": {"character_sets": "unicode", "max_examples": 20}},
                {"charts": ["workers"], "path": "$.items[*].text", "hypothesis": {"control_characters": {"allow": []}}},
            ],
        },
    )
    snapshot = generation_settings(chart.path)
    assert hypothesis_parameters(snapshot, ("field0",), 1)["max_examples"] == 14
    assert hypothesis_parameters(snapshot, ("items", 3, "text"), 1) == {
        "max_examples": 20,
        "deadline_ms": 4000,
        "phases": ["generate", "shrink"],
        "suppress_health_check": ["too_slow"],
    }
    selected = settings_at(snapshot, ("items", 3, "text"))
    assert selected["character_sets"] == "unicode"
    assert selected["control_characters"] == {"exclude": True, "allow": []}
    assert settings_at(snapshot, ("items", 3, "other"))["control_characters"] == DEFAULT_CONTROLS
    sequence(snapshot["rules"]).append({"path": "$.items", "hypothesis": {"max_examples": 30}})
    with pytest.raises(ValueError, match="Conflicting"):
        settings_at(snapshot, ("items",))


def test_mixed_text_domains_and_shrinking(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep sibling alphabets independent when one candidate contains a whole nested object.

    Args:
        tmp_path (Path): Configuration directory.
        monkeypatch (pytest.MonkeyPatch): Isolate global generation settings.

    Returns:
        None: Generation and shrinking retain schema validity and deliberate tab allowances.
    """
    chart = fixture_chart(tmp_path)
    install_policy(
        tmp_path,
        monkeypatch,
        {
            "hypothesis": {"control_characters": {"allow": []}},
            "input_constraints": [
                {"charts": ["workers"], "path": "$.nested.label", "hypothesis": {"character_sets": "unicode", "exclude_characters": ">|"}},
                {"charts": ["workers"], "path": "$.nested.tabs", "hypothesis": {"control_characters": {"allow": ["\t"]}}},
            ],
        },
    )
    schema: dict[str, object] = {
        "type": "object",
        "required": ["ascii", "nested"],
        "additionalProperties": False,
        "properties": {
            "ascii": {"type": "string", "maxLength": 12},
            "nested": {
                "type": "object",
                "required": ["label", "tabs"],
                "additionalProperties": False,
                "properties": {"label": {"type": "string", "pattern": "^[éΩ]$"}, "tabs": {"const": "\t"}},
            },
        },
    }
    strategy = schema_strategy(schema, generation=generation_settings(chart.path))
    validator = validators.validator_for(schema)(schema)

    def accepted(value: object) -> bool:
        """
        Check every generated or shrunk candidate before selecting a witness.

        Args:
            value (object): Candidate generated from the nested schema.

        Returns:
            bool: Whether a nonempty ASCII sibling has been found.
        """
        assert validator.is_valid(json_value(value))
        row = mapping(value)
        assert str(row["ascii"]).isascii()
        assert all(ord(char) >= 32 and ord(char) != 127 for char in str(row["ascii"]))
        assert mapping(row["nested"])["tabs"] == "\t"
        assert mapping(row["nested"])["label"] in {"é", "Ω"}
        return bool(row["ascii"])

    find(strategy, accepted, settings=settings(max_examples=50, database=None, deadline=None))
    # Exclusions must apply to unconstrained Unicode strings too, not just regex literals.
    nested = schema_strategy({"type": "string", "maxLength": 30}, generation=generation_settings(chart.path), path=("nested", "label"))

    @settings(max_examples=30, database=None, deadline=None)
    @given(nested)
    def check_text(value: object) -> None:
        """
        Validate explicit character exclusions independently of alphabet selection.

        Args:
            value (object): Generated string within the Unicode branch.

        Returns:
            None: Neither additional exclusions nor controls occur.
        """
        assert not any(char in ">|" or ord(char) < 32 or 127 <= ord(char) <= 159 for char in str(value))

    check_text()
    # Saved suites must not reapply the fixed default tab filter to this branch.
    expression = strategy_source({"const": "\t"}, generation=generation_settings(chart.path), path=("nested", "tabs"))
    assert "supported_generated_text" not in expression
    compiled = eval(expression, {"from_schema": schema_strategy})
    assert find(compiled, lambda value: True, settings=settings(max_examples=2, database=None)) == "\t"


def test_source_matrix_survives_saved_suite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Distinguish repositories with equal chart names and freeze their matching rules.

    Args:
        tmp_path (Path): Chart, configuration and generated suite.
        monkeypatch (pytest.MonkeyPatch): Restore environment variables after source scopes.

    Returns:
        None: The selected source and generation policy survive a later policy change.
    """
    chart = fixture_chart(tmp_path)
    source = "https://example.org/team/charts.git"
    monkeypatch.delenv(SOURCE_ENVIRONMENT, raising=False)
    install_policy(
        tmp_path,
        monkeypatch,
        {
            "input_constraints": [
                {
                    "charts": [{"sources": [source, "git@example.org:team/charts.git"], "names": ["workers", "another"]}],
                    "path": "$.field0",
                    "hypothesis": {"max_examples": 3, "phases": ["generate"]},
                    "ignored": ["HH2001"],
                }
            ]
        },
    )
    assert not matching_rules(chart.path)
    output = tmp_path / "suite"
    with SourceScope(source):
        assert len(matching_rules(chart.path)) == 1
        generate_tests(chart, output)
        original = chart.input_domains().generation
    assert SOURCE_ENVIRONMENT not in os.environ
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"character_sets": "unicode"}))
    with prepared_chart(chart.path, output) as saved:
        assert saved.input_domains().generation == original
        assert hypothesis_parameters(saved.input_domains().generation, ("field0",), 100)["max_examples"] == 3
    paths = json.loads((output / "paths.json").read_text())["paths"]
    row = next(row for row in paths if row["path"] == ["field0"])
    assert row["hypothesis"]["max_examples"] == 3
    assert "max_examples=3" in (output / "test_chart_values.py").read_text()


@pytest.mark.parametrize("jobs", [1, 2])
def test_branch_example_budgets_in_native_workers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, jobs: int) -> None:
    """
    Apply local budgets during real Helm execution, including isolated worker interpreters.

    Args:
        tmp_path (Path): Chart and artifacts.
        monkeypatch (pytest.MonkeyPatch): Resolve the same policy that workers inherit.
        jobs (int): Serial or parallel execution mode.

    Returns:
        None: Selected paths receive their own budgets while siblings retain the global default.
    """
    chart = fixture_chart(tmp_path)
    install_policy(
        tmp_path,
        monkeypatch,
        {
            "hypothesis": {"max_examples": 2},
            "input_constraints": [{"charts": ["workers"], "path": "$.field0", "hypothesis": {"max_examples": 4}}],
        },
    )
    result = check_paths(
        chart, budget=45, max_examples=10, seed=2, helm="helm", timeout=5, artifacts=tmp_path / "results", jobs=jobs, filtering=True
    )
    assert result["status"] == "passed"
    phases = {str(mapping(phase)["phase"]): mapping(phase) for phase in sequence(result["phases"])}
    assert phases["$.field0"]["attempts"] == 4
    assert all(phase["attempts"] == 2 for name, phase in phases.items() if name != "$.field0")
    assert result["attempts"] == 19


def test_complete_documented_configuration(tmp_path: Path) -> None:
    """
    Load the published complete example against a real local resource schema.

    Args:
        tmp_path (Path): Example configuration directory.

    Returns:
        None: Every documented field is accepted, and explicit CLI defaults take precedence.
    """
    config = tmp_path / "policy.yaml"
    config.write_text(COMPLETE_EXAMPLE)
    (tmp_path / "schemas").mkdir()
    root = Path(__file__).resolve().parents[3]
    (tmp_path / "schemas/widget.json").write_text((root / "docs/input-domains/schemas/widget.json").read_text())
    policy = load_policy(config, max_examples=5, character_sets="unicode")
    assert mapping(policy["hypothesis"])["max_examples"] == 5
    assert policy["character_sets"] == "unicode"
    assert len(sequence(policy["input_constraints"])) == 5
    assert mapping(policy["resource_schemas"])["example.org/v1/Widget"]
    assert mapping(policy["control_characters"])["allow"] == ["\n", "\r"]


@pytest.mark.parametrize("key", ["character_sets", "control_characters", "exclude_characters"])
def test_generation_controls_require_hypothesis_key(tmp_path: Path, key: str) -> None:
    """
    Reject the old flat spelling globally and within individual constraints.

    Args:
        tmp_path (Path): User configuration directory.
        key (str): Text setting that belongs under hypothesis.

    Returns:
        None: Misplaced settings cannot be silently ignored.
    """
    config = tmp_path / "policy.yaml"
    for document in ({key: "ascii"}, {"input_constraints": [{"charts": ["workers"], "path": "$", key: "ascii"}]}):
        config.write_text(yamlio.dump(document))
        with pytest.raises(ValueError, match="[Uu]nknown"):
            load_policy(config)


def test_local_matrix_and_scope_restoration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Resolve local selectors relative to the config and restore identity after cancellation.

    Args:
        tmp_path (Path): Chart and configuration root.
        monkeypatch (pytest.MonkeyPatch): Isolate inherited source and policy.

    Returns:
        None: Local globs and names match independently and interrupt scopes restore their parent.
    """
    chart = fixture_chart(tmp_path)
    monkeypatch.delenv(SOURCE_ENVIRONMENT, raising=False)
    install_policy(
        tmp_path,
        monkeypatch,
        {"input_constraints": [{"charts": [{"sources": ["./*"], "names": ["work*"]}], "path": "$", "hypothesis": {"max_examples": 2}}]},
    )
    with SourceScope(str(tmp_path / "children")):
        assert matching_rules(chart.path)
        with pytest.raises(KeyboardInterrupt), SourceScope("https://different.example/repository.git"):
            assert not matching_rules(chart.path)
            raise KeyboardInterrupt()
        assert matching_rules(chart.path)
    assert SOURCE_ENVIRONMENT not in os.environ
    for invalid in ([], [{"sources": ["source"]}], [{"sources": [], "names": ["workers"]}], [{"sources": ["source"], "names": "workers"}]):
        with pytest.raises(ValueError):
            selectors(invalid, tmp_path)
