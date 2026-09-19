"""
Warn about unstructured object inputs without treating an intentional map as a chart defect.
"""

import copy
import json
import logging
from pathlib import Path

import pytest

from hypothesis_helm.charts.inspection.audit import audit
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.rules import ENVIRONMENT, load_ignored
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.opaque import opaque_paths, warn_opaque


@pytest.mark.parametrize(
    "node",
    [
        {"type": "object"},
        {"type": "object", "properties": {}},
        {"type": ["object", "null"], "additionalProperties": True},
        {"type": "object", "additionalProperties": {}},
        {"type": "object", "propertyNames": {"enum": ["enabled"]}},
        {"anyOf": [{"type": "string"}, {"type": "object"}]},
        {"allOf": [{"type": "object"}, {"description": "Arbitrary settings"}]},
        {},
    ],
)
def test_opaque_declarations(node: dict[str, object]) -> None:
    """
    Detect generic objects even when nullable or hidden in a schema branch.

    Args:
        node (dict[str, object]): Opaque field declaration.

    Returns:
        None: Only the unstructured field is identified, not its structured parent.
    """
    assert opaque_paths({"type": "object", "properties": {"settings": node}}) == [("settings",)]


@pytest.mark.parametrize(
    "node",
    [
        {"type": "object", "additionalProperties": False},
        {"type": "object", "maxProperties": 0},
        {"type": "object", "propertyNames": False},
        {"type": "object", "enum": [{"enabled": True}]},
        {"type": "object", "const": {}},
        {"type": "string"},
        {"type": "object", "properties": {"enabled": {"type": "boolean"}}},
        {"type": "object", "patternProperties": {"^label-": {"type": "string"}}},
        {"type": "object", "additionalProperties": {"type": "string"}},
        {"type": "object", "additionalProperties": {"allOf": [{"type": "string"}, {"minLength": 1}]}},
        {"allOf": [{"type": "object"}, {"additionalProperties": False}]},
        {"allOf": [{"type": "object"}, {"properties": {"enabled": {"type": "boolean"}}}]},
        {"anyOf": [{"type": "string"}, {"type": "object", "additionalProperties": {"type": "integer"}}]},
    ],
)
def test_described_or_closed_domains(node: dict[str, object]) -> None:
    """
    Distinguish opaque maps from meaningful declarations whose domains may still be infinite.

    Args:
        node (dict[str, object]): Field with described structure or a non-object domain.

    Returns:
        None: Valid typed maps, closed objects and scalar domains do not warn.
    """
    assert opaque_paths({"type": "object", "properties": {"settings": node}}) == []


def test_root_references_and_items() -> None:
    """
    Inspect root maps, local references, typed map entries and array item objects.

    Returns:
        None: Warnings carry useful paths and reference metadata does not cause duplicates.
    """
    assert opaque_paths({"type": "object"}) == [()]
    schema: dict[str, object] = {
        "type": "object",
        "$defs": {"opaque": {"type": "object"}},
        "properties": {
            "config": {"$ref": "#/$defs/opaque", "description": "Runtime configuration"},
            "items": {"type": "array", "items": {"$ref": "#/$defs/opaque"}},
            "map": {"type": "object", "additionalProperties": {"type": "object"}},
        },
    }
    assert opaque_paths(schema) == [("config",), ("items", "*"), ("map", "*")]
    assert opaque_paths({"$defs": {"named": {"properties": {"enabled": {"type": "boolean"}}}}, "allOf": [{"$ref": "#/$defs/named"}]}) == []


def test_audit_and_ignore_preserve_input_space(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    """
    Record HH2006 in audits and suppress it explicitly without altering the input contract.

    Args:
        tmp_path (Path): Chart directory and user policy.
        monkeypatch (pytest.MonkeyPatch): Inherited ignore policy.
        caplog (pytest.LogCaptureFixture): Warning evidence and suppression.

    Returns:
        None: Ignored findings remain disclosed and the same paths are still testable.
    """
    chart = Chart(tmp_path, {"type": "object", "properties": {"settings": {"type": "object"}}}, {"settings": {}})
    original = copy.deepcopy(chart.schema)
    with caplog.at_level(logging.WARNING):
        report = audit(chart)
    findings = [mapping(item) for item in sequence(report["findings"]) if mapping(item)["code"] == "HH2006"]
    assert len(findings) == 1 and findings[0]["path"] == ["settings"]
    assert mapping(findings[0]["finding"])["kind"] == "warning"
    assert "[HH2006]" in caplog.text and "$.settings" in caplog.text
    policy = tmp_path / "config.yaml"
    policy.write_text("ignored: [HH2006]\n")
    monkeypatch.setenv(ENVIRONMENT, json.dumps(load_ignored(policy, [])))
    caplog.clear()
    suppressed = audit(chart)
    assert not any(mapping(item)["code"] == "HH2006" for item in sequence(suppressed["findings"]))
    assert any(mapping(item)["code"] == "HH2006" for item in sequence(suppressed["ignored_findings"]))
    assert "HH2006" not in caplog.text
    assert chart.schema == original
    assert report["input_inventory"] == suppressed["input_inventory"]
    warn_opaque(chart.schema, "example")
    assert "HH2006" not in caplog.text


def test_warning_does_not_block_unsupported_analysis(caplog: pytest.LogCaptureFixture) -> None:
    """
    Leave unsupported recursive-schema handling to the caller's existing execution checks.

    Args:
        caplog (pytest.LogCaptureFixture): Analysis diagnostics.

    Returns:
        None: Optional warning inspection neither raises nor invents an opaque-object finding.
    """
    with caplog.at_level(logging.DEBUG):
        warn_opaque({"type": "object", "properties": {"child": {"$ref": "#"}}}, "recursive")
    assert "inspection unavailable" in caplog.text
    assert "[HH2006]" not in caplog.text
