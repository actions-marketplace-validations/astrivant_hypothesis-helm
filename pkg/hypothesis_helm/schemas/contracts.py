"""
Typed boundaries for JSON schemas and round-trip YAML values.
"""

import copy
import json
import re
from typing import cast

from hypothesis.strategies import SearchStrategy
from hypothesis_jsonschema import from_schema
from jsonschema import validators

from hypothesis_helm.schemas.characters import declared_text, validate_character_sets

__all__ = (
    "CONTROL_CHARACTERS",
    "Json",
    "configuration_key",
    "json_value",
    "mapping",
    "number",
    "ordinary_generated_text",
    "schema_strategy",
    "sequence",
    "supported_generated_text",
    "text",
)


type Json = None | bool | int | float | str | list[Json] | dict[str, Json]

CONTROL_CHARACTERS = re.compile(r"[\x00-\x09\x0b\x0c\x0e-\x1f\x7f-\x9f]")


def supported_generated_text(value: object) -> bool:
    """
    Exclude C0/C1 controls from sampled strings and keys, except LF and CR.

    Character-set restrictions apply while constructing strategies. This final
    control-character check also permits explicitly declared Unicode literals.

    Args:
        value (object): Generated JSON value, including nested objects and arrays.

    Returns:
        bool: Whether every generated string satisfies the text sampling policy.
    """
    if isinstance(value, str):
        return CONTROL_CHARACTERS.search(value) is None
    if isinstance(value, dict):
        return all(supported_generated_text(key) and supported_generated_text(item) for key, item in value.items())
    if isinstance(value, list):
        return all(supported_generated_text(item) for item in value)
    return True


def ordinary_generated_text(value: object, *, ascii_only: bool = False, literals: frozenset[str] = frozenset()) -> object:
    """
    Replace controls in fresh candidate text before validating or testing the candidate.

    Replacements preserve string lengths. Schema validation afterwards rejects
    incompatible patterns, enums, and object constraints.
    This function must not be applied to chart defaults or supplied values.

    Args:
        value (object): Fresh JSON Schema strategy candidate.
        ascii_only (bool): Replace non-ASCII text produced by unconstrained library fallbacks.
        literals (frozenset[str]): Authored text exempt from ASCII replacement.

    Returns:
        object: Candidate containing ordinary text, still requiring schema validation.
    """
    if isinstance(value, str):
        normalized = CONTROL_CHARACTERS.sub("a", value)
        if ascii_only and value not in literals:
            return "".join(char if char.isascii() else "a" for char in normalized)
        return normalized
    if isinstance(value, dict):
        return {
            ordinary_generated_text(key, ascii_only=ascii_only, literals=literals): ordinary_generated_text(
                item, ascii_only=ascii_only, literals=literals
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [ordinary_generated_text(item, ascii_only=ascii_only, literals=literals) for item in value]
    return value


def configuration_key(values: dict[str, object]) -> str:
    """
    Identify a configuration independently of map order while preserving arrays and types.

    Args:
        values (dict[str, object]): Raw or normalized chart values.

    Returns:
        str: Canonical JSON identity retaining scalar types and ordered array contents.
    """
    return json.dumps(values, sort_keys=True, separators=(",", ":"), allow_nan=False)


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


def schema_strategy(
    schema: dict[str, object],
    *,
    character_sets: str | None = None,
    generation: dict[str, object] | None = None,
    path: tuple[str | int, ...] = (),
) -> SearchStrategy[object]:
    """
    Generate schema-valid samples without control-character fuzzing.

    Args:
        schema (dict[str, object]): JSON Schema defining the accepted value domain.
        character_sets (str | None): Saved character domain, or the active worker policy.
        generation (dict[str, object] | None): Chart-specific text settings and branch overrides.
        path (tuple[str | int, ...]): Root path of the schema fragment within chart values.

    Returns:
        SearchStrategy[object]: Result of the documented operation.
    """
    from hypothesis_helm.schemas.settings import global_settings, normalize_text, settings_at

    validator = validators.validator_for(schema)(schema)
    frozen: dict[str, object] = copy.deepcopy(generation) if generation else {"defaults": global_settings(), "rules": []}
    if character_sets is not None:
        mapping(frozen["defaults"])["character_sets"] = validate_character_sets(character_sets)
    selected = settings_at(frozen, path)["character_sets"]
    literals = declared_text(schema)
    unicode_branches = any(mapping(rule).get("character_sets") == "unicode" for rule in sequence(frozen.get("rules", [])))
    codec = "ascii" if selected == "ascii" and not unicode_branches and all(value.isascii() for value in literals) else "utf-8"
    generating = copy.deepcopy(schema)
    if isinstance(generating.get("allOf"), list):
        # Keep bounded fragment proofs out of hypothesis-jsonschema's Boolean
        # canonicalizer, where negating recursive container regions explodes.
        # Removing a root conjunction admits a superset; the full validator
        # below checks every generated and shrunk case before execution.
        retained = [
            clause
            for clause in sequence(generating["allOf"])
            if not (isinstance(clause, dict) and clause.get("x-hypothesis-helm-literal-fragment") is True)
        ]
        if retained:
            generating["allOf"] = retained
        else:
            generating.pop("allOf")
    return (
        from_schema(cast(dict[str, Json], generating), codec=codec)
        .map(lambda value: normalize_text(value, frozen, path, literals))
        .filter(lambda candidate: validator.is_valid(json_value(candidate)))
    )
