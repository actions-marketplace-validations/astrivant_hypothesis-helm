import pytest

from hypothesis_helm.finite import NonFiniteSchema, enumerate_values
from hypothesis_helm.runner import Chart


def test_workload_domain():
    schema = Chart.load("examples/workload").schema
    assert len(enumerate_values(schema)) == 24


def test_optional_and_null():
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
def test_refuses_partial_enumeration(schema):
    with pytest.raises(NonFiniteSchema):
        enumerate_values(schema, 10)
