"""
Resolve partial compiler overrides independently for each chart and its workers.
"""

import json
from pathlib import Path

import pytest

from hypothesis_helm.charts.inspection.templates import discover
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.asts.renderer import RendererContext
from hypothesis_helm.compiler.limits import DEFAULT_LIMITS, active_limits
from hypothesis_helm.compiler.passes.complexity import measure
from hypothesis_helm.compiler.passes.dependencies import Dependencies
from hypothesis_helm.compiler.passes.domains import project
from hypothesis_helm.compiler.passes.pruning import snapshot
from hypothesis_helm.environment import refresh_env
from hypothesis_helm.execution.state.cache import fingerprint
from hypothesis_helm.schemas.configuration.policy import ENVIRONMENT, load_policy
from hypothesis_helm.schemas.configuration.selectors import SourceScope
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests.compiler.test_compiler_limits import helper_chart


@pytest.mark.parametrize("invalid", [None, [], {"unknown": 2}, {"max_call_depth": 0}, {"max_steps": True}])
def test_invalid_chart_compiler_configuration(tmp_path: Path, invalid: object) -> None:
    """
    Validate chart overrides even when no discovered chart matches their selector.

    Args:
        tmp_path (Path): Configuration directory.
        invalid (object): Invalid compiler mapping or budget.

    Returns:
        None: Bad policies fail before chart execution.
    """
    config = tmp_path / "config.yaml"
    config.write_text(yamlio.dump({"input_constraints": [{"charts": ["unmatched"], "path": "$", "compiler": invalid}]}))
    with pytest.raises(ValueError, match="compiler"):
        load_policy(config)


def test_compiler_rules_require_chart_root(tmp_path: Path) -> None:
    """
    Reject per-field budgets because analysis includes the complete chart.

    Args:
        tmp_path (Path): Configuration directory.

    Returns:
        None: A values-branch rule cannot silently change chart-wide resource limits.
    """
    config = tmp_path / "config.yaml"
    config.write_text(yamlio.dump({"input_constraints": [{"charts": ["helpers"], "path": "$.name", "compiler": {"max_call_depth": 32}}]}))
    with pytest.raises(ValueError, match="require path"):
        load_policy(config)


def test_chart_selectors_isolation_and_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Compose partial matching rules without changing defaults or neighboring charts.

    Args:
        tmp_path (Path): Chart and configuration directory.
        monkeypatch (pytest.MonkeyPatch): Install the coordinator policy.

    Returns:
        None: Remote/local source matching, repeated chart visits and snapshots remain isolated.
    """
    root = tmp_path / "chart"
    root.mkdir()
    chart = helper_chart(root, 20)
    config = tmp_path / "config.yaml"
    document: dict[str, object] = {
        "compiler": {"max_call_depth": 1, "max_steps": 23456},
        "input_constraints": [
            {
                "charts": [{"sources": ["./chart", "https://example.test/charts.git"], "names": ["help*"]}],
                "path": "$",
                "compiler": {"max_call_depth": 32},
            },
            {"charts": ["helpers"], "path": "$", "compiler": {"max_files": 1234}},
            {"charts": ["elsewhere"], "path": "$", "compiler": {"max_steps": 1}},
        ],
    }
    config.write_text(yamlio.dump(document))
    policy = load_policy(config)
    serialized = json.dumps(policy)
    monkeypatch.setenv(ENVIRONMENT, serialized)
    refresh_env()
    expected = {**DEFAULT_LIMITS, "max_call_depth": 32, "max_steps": 23456, "max_files": 1234}
    assert active_limits(chart.path) == expected
    assert active_limits()["max_call_depth"] == 1
    with SourceScope("https://example.test/charts.git"):
        assert active_limits(chart.path) == expected
    with SourceScope("https://another.test/charts.git"):
        assert active_limits(chart.path) == {**expected, "max_call_depth": 1}
    assert active_limits(chart.path) == expected
    captured = RendererContext(chart.path)
    before = fingerprint(chart.path, 0, None, "none")
    mapping(sequence(document["input_constraints"])[0])["compiler"] = {"max_call_depth": 64}
    config.write_text(yamlio.dump(document))
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_policy(config)))
    refresh_env()
    assert captured.limits == expected
    assert active_limits(chart.path)["max_call_depth"] == 64
    assert fingerprint(chart.path, 0, None, "none") != before
    assert mapping(policy["compiler"])["max_call_depth"] == 1


@pytest.mark.parametrize("reverse", [False, True])
def test_conflicting_compiler_overrides(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, reverse: bool) -> None:
    """
    Reject conflicting matching limits independently of configuration order.

    Args:
        tmp_path (Path): Chart directory.
        monkeypatch (pytest.MonkeyPatch): Install the inherited policy.
        reverse (bool): Reverse equally applicable override rules.

    Returns:
        None: Overlapping selectors cannot silently pick a compiler budget.
    """
    chart = helper_chart(tmp_path, 1)
    rows = [
        {"charts": [pattern], "path": "$", "compiler": {"max_call_depth": limit}} for pattern, limit in (("help*", 32), ("helpers", 64))
    ]
    monkeypatch.setenv(ENVIRONMENT, json.dumps({"input_constraints": rows[::-1] if reverse else rows}))
    refresh_env()
    with pytest.raises(ValueError, match="Conflicting compiler.max_call_depth.*helpers"):
        active_limits(chart.path)


def test_analysis_passes_use_chart_budgets(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Exercise discovery, projection, rejection, complexity and proof limits using one override.

    Args:
        tmp_path (Path): Chart directory.
        monkeypatch (pytest.MonkeyPatch): Install the inherited policy.

    Returns:
        None: Compiler passes honor the same selected budgets without broadening global defaults.
    """
    chart = helper_chart(tmp_path, 20)
    configured = {"max_call_depth": 32, "max_complexity_cases": 7, "max_complexity_seconds": 2, "max_proof_bytes": 1}
    monkeypatch.setenv(
        ENVIRONMENT,
        json.dumps(
            {
                "compiler": {"max_call_depth": 1},
                "input_constraints": [{"charts": ["helpers"], "path": "$", "compiler": configured}],
            }
        ),
    )
    refresh_env()
    contracts = Contracts.build(chart.path)
    assert contracts.max_call_depth == 32
    assert contracts.predict({**chart.defaults, "name": "reject"}) is not None
    rules, _ = project(chart.path, chart.schema)
    assert any(rule["path"] == ["name"] for rule in rules)
    refs, _ = discover(chart.path)
    assert any(ref.path == ("name",) for ref in refs)
    assert RendererContext(chart.path).limits == contracts.limits
    assert contracts.dependencies.limits == contracts.limits
    assert measure(chart)["limits"] == {"max_cases": 7, "seconds": 2.0}
    with pytest.raises(ValueError, match="compiler.max_proof_bytes=1"):
        snapshot(chart.path)


def test_dependencies_use_containing_chart_budgets(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Retain parent budgets while inspecting dependency templates under another chart name.

    Args:
        tmp_path (Path): Parent and dependency source.
        monkeypatch (pytest.MonkeyPatch): Install different parent and standalone child policies.

    Returns:
        None: The child policy applies only when the child is the chart under test.
    """
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "parent", "version": "1.0.0"}))
    child = tmp_path / "charts" / "child"
    child.mkdir(parents=True)
    helper_chart(child, 20)
    monkeypatch.setenv(
        ENVIRONMENT,
        json.dumps(
            {
                "compiler": {"max_call_depth": 1},
                "input_constraints": [{"charts": ["parent"], "path": "$", "compiler": {"max_call_depth": 32}}],
            }
        ),
    )
    refresh_env()
    dependencies = Dependencies.build(tmp_path)
    assert dependencies.limits["max_call_depth"] == 32
    assert any(ref.path == ("helpers", "name") for ref in dependencies.references)
    assert not any("budget" in str(note) or "depth" in str(note) for note in dependencies.diagnostics)
    assert Dependencies.build(child).limits["max_call_depth"] == 1
