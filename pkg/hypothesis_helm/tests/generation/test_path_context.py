"""
Verify dependent path generation across JSON Schema array dialects.
"""

import copy
from pathlib import Path

import pytest
from hypothesis import find, given, settings
from hypothesis import strategies as st
from hypothesis.errors import NoSuchExample, Unsatisfiable
from jsonschema import validators

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.suites.runtime import _constraint, path_values
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.generation.domains import InputDomains
from hypothesis_helm.schemas.generation.strategies import schema_strategy

METASCHEMAS = (
    None,
    "http://json-schema.org/schema#",
    "http://json-schema.org/draft-07/schema#",
    "https://json-schema.org/draft/2019-09/schema",
    "https://json-schema.org/draft/2020-12/schema",
)


@pytest.mark.parametrize("metaschema", METASCHEMAS)
@pytest.mark.parametrize("value", [None, 2147483647, "HTTPS"])
def test_positional_constraint_preserves_other_indices(metaschema: str | None, value: object) -> None:
    """
    Validate the helper's schema and restrict exactly one nested array position.

    Args:
        metaschema (str | None): Declared dialect, including default and unversioned forms.
        value (object): Concrete target, including the null candidate in the reported crash.

    Returns:
        None: The schema is valid and requires only the requested indices and leaf.
    """
    root: dict[str, object] = {"$schema": metaschema} if metaschema else {}
    dialect = validators.validator_for(root)
    keyword = "prefixItems" if "prefixItems" in dialect.VALIDATORS else "items"
    root.update(_constraint(("rows", 1, 2, "value"), value, positional_keyword=keyword))
    dialect.check_schema(root)
    validator = dialect(root)
    candidate: dict[str, object] = {"rows": ["unrelated", [False, {}, {"value": value}, "extra"]]}
    assert validator.is_valid(json_value(candidate))
    assert not validator.is_valid({"rows": ["unrelated", [False, {}]]})
    assert not validator.is_valid(json_value({"rows": ["unrelated", [False, {}, {"other": value}]]}))
    assert not validator.is_valid(json_value({"rows": ["unrelated", [False, {}, {"value": [value]}]]}))


def context_chart(directory: Path, metaschema: str | None, field: str) -> Chart:
    """
    Require a sibling change whenever an initially empty container list gains an entry.

    Args:
        directory (Path): Synthetic chart location; rendering is unnecessary for schema generation.
        metaschema (str | None): Root schema dialect.
        field (str): Startup period or HTTP scheme path from the reported failures.

    Returns:
        Chart: Finite container structure that must enter the dependent-context fallback.
    """
    target: dict[str, object] = {"type": "integer", "minimum": 1, "maximum": 2147483647}
    if field == "scheme":
        target = {"enum": ["HTTP", "HTTPS"]}
    leaf_path = ("startupProbe", "periodSeconds") if field == "periodSeconds" else ("livenessProbe", "httpGet", "scheme")
    container: dict[str, object] = {"$ref": "#/$defs/target"}
    for part in reversed(leaf_path):
        container = {"type": "object", "properties": {part: container}, "required": [part], "additionalProperties": False}
    schema: dict[str, object] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["primary", "enabled"],
        "properties": {
            "enabled": {"type": "boolean"},
            "primary": {
                "type": "object",
                "additionalProperties": False,
                "required": ["initContainers"],
                "properties": {"initContainers": {"type": "array", "maxItems": 1, "items": {"$ref": "#/$defs/container"}}},
            },
        },
        "$defs": {"container": container, "target": target},
        "if": {"properties": {"primary": {"properties": {"initContainers": {"minItems": 1}}}}},
        "then": {"properties": {"enabled": {"const": True}}},
    }
    if metaschema:
        schema["$schema"] = metaschema
    chart = Chart(directory, schema, {"primary": {"initContainers": []}, "enabled": False})
    chart.domains = InputDomains([], [], "context-test")
    return chart


@pytest.mark.parametrize("metaschema", METASCHEMAS)
@pytest.mark.parametrize("field", ["periodSeconds", "scheme"])
def test_array_path_draws_valid_dependent_context(tmp_path: Path, metaschema: str | None, field: str) -> None:
    """
    Keep a selected wildcard leaf while satisfying constraints outside its parent array.

    Args:
        tmp_path (Path): Synthetic chart location.
        metaschema (str | None): Root schema dialect.
        field (str): Probe leaf to bind inside the new container.

    Returns:
        None: Generation preserves the chosen value, local references, schema and defaults.
    """
    chart = context_chart(tmp_path, metaschema, field)
    original_schema, original_defaults = copy.deepcopy(chart.schema), copy.deepcopy(chart.defaults)
    tail = ("startupProbe", "periodSeconds") if field == "periodSeconds" else ("livenessProbe", "httpGet", "scheme")
    value = 2147483647 if field == "periodSeconds" else "HTTPS"
    validator = validators.validator_for(chart.schema)(chart.schema)

    @settings(max_examples=8, deadline=None, derandomize=True)
    @given(st.data())
    def check(data: st.DataObject) -> None:
        """
        Draw a dependent context without falling back to unconstrained positional sampling.

        Args:
            data (st.DataObject): Hypothesis draw context.

        Returns:
            None: Full-schema validation and exact target preservation both hold.
        """
        result = path_values(chart, ("primary", "initContainers", "*", *tail), value, data)
        assert validator.is_valid(json_value(result))
        assert result["enabled"] is True
        selected: object = sequence(mapping(result["primary"])["initContainers"])[0]
        for segment in tail:
            selected = mapping(selected)[segment]
        assert selected == value

    check()
    assert chart.schema == original_schema
    assert chart.defaults == original_defaults


def test_impossible_null_path_rejects_example_without_schema_error(tmp_path: Path) -> None:
    """
    Treat null outside the field domain as an impossible candidate, not a malformed schema.

    Args:
        tmp_path (Path): Synthetic chart location.

    Returns:
        None: Hypothesis rejects the candidate using its normal unsatisfiable-example handling.
    """
    chart = context_chart(tmp_path, "http://json-schema.org/schema#", "periodSeconds")

    @st.composite
    def candidate(draw: st.DrawFn) -> dict[str, object]:
        """
        Exercise the same null-valued array context recorded in the scan report.

        Args:
            draw (st.DrawFn): Hypothesis strategy draw function.

        Returns:
            dict[str, object]: Only reachable if an invalid null was incorrectly admitted.
        """
        return path_values(chart, ("primary", "initContainers", "*", "startupProbe", "periodSeconds"), None, draw(st.data()))

    with pytest.raises((NoSuchExample, Unsatisfiable)):
        find(candidate(), lambda _: True, settings=settings(max_examples=10, deadline=None, derandomize=True))


def test_generator_view_does_not_replace_authoritative_validation() -> None:
    """
    Apply newer constraints even when the generator receives a simpler compatible view.

    Returns:
        None: Neither generated nor normalized candidates can bypass the original validator.
    """
    authoritative: dict[str, object] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "array",
        "prefixItems": [{"const": 7}],
        "minItems": 1,
        "items": False,
    }
    generating: dict[str, object] = {"type": "array", "items": {"enum": [1, 7]}, "minItems": 1, "maxItems": 1}

    @settings(max_examples=5, deadline=None, derandomize=True)
    @given(schema_strategy(authoritative, generation_schema=generating))
    def check(value: object) -> None:
        """
        Check the value after generation and text normalization.

        Args:
            value (object): Candidate that passed both stages.

        Returns:
            None: Authoritative prefix and tail rules are still enforced.
        """
        assert value == [7]

    check()
