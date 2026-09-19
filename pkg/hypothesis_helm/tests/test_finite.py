"""
Verify finite.
"""

import pytest

from hypothesis_helm.charts.testing.runner import Chart
from hypothesis_helm.schemas.finite import NonFiniteSchema, enumerate_values


def test_workload_domain() -> None:
    """
    Verify workload domain.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    schema = Chart.load("examples/workload").schema
    assert len(enumerate_values(schema)) == 24


def test_optional_and_null() -> None:
    """
    Verify optional and null.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {"x": {"enum": [None, True, False]}},
    }
    assert enumerate_values(schema) == [{}, {"x": None}, {"x": True}, {"x": False}]


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "string"},
        {"type": "object"},
        {"type": "integer", "minimum": 0, "maximum": 10000},
        {"type": "object", "additionalProperties": False, "properties": {"x": {"$ref": "#"}}},
    ],
)
def test_refuses_partial_enumeration(schema: dict[str, object]) -> None:
    """
    Verify refuses partial enumeration.

    Args:
        schema (dict[str, object]): JSON Schema defining the accepted value domain.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
    with pytest.raises(NonFiniteSchema):
        enumerate_values(schema, 10)
