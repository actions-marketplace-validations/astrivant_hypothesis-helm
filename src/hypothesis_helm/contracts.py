"""
Typed boundaries for JSON schemas and round-trip YAML values.
"""

from typing import cast

from hypothesis.strategies import SearchStrategy
from hypothesis_jsonschema import from_schema

type Json = None | bool | int | float | str | list[Json] | dict[str, Json]


def mapping(value: object) -> dict[str, object]:
    """
    Require an object mapping at a schema or YAML boundary.

    Args:
        value (object): Candidate value supplied by the property strategy.

    Returns:
        dict[str, object]: Resulting schema, values mapping, or structured report.
    """
    if not isinstance(value, dict):
        raise ValueError("expected an object mapping")
    return cast(dict[str, object], value)


def sequence(value: object) -> list[object]:
    """
    Require a JSON array at a schema or YAML boundary.

    Args:
        value (object): Candidate value supplied by the property strategy.

    Returns:
        list[object]: Result of the documented operation.
    """
    if not isinstance(value, list):
        raise ValueError("expected an array")
    return cast(list[object], value)


def number(value: object) -> int | float:
    """
    Require a numeric schema bound.

    Args:
        value (object): Candidate value supplied by the property strategy.

    Returns:
        int | float: Result of the documented operation.
    """
    if not isinstance(value, (int, float)):
        raise ValueError("expected a numeric schema bound")
    return value


def text(value: object) -> str:
    """
    Require a string schema reference or key.

    Args:
        value (object): Candidate value supplied by the property strategy.

    Returns:
        str: Serialized output or resolved strategy expression.
    """
    if not isinstance(value, str):
        raise ValueError("expected a string")
    return value


def json_value(value: object) -> Json:
    """
    Adapt parsed JSON and YAML values to the validator's recursive input type.

    Args:
        value (object): Candidate value supplied by the property strategy.

    Returns:
        Json: Result of the documented operation.
    """
    return cast(Json, value)


def schema_strategy(schema: dict[str, object]) -> SearchStrategy[object]:
    """
    Adapt the schema library's JSON strategy to the public object boundary.

    Args:
        schema (dict[str, object]): JSON Schema defining the accepted value domain.

    Returns:
        SearchStrategy[object]: Result of the documented operation.
    """
    return from_schema(cast(dict[str, Json], schema))
