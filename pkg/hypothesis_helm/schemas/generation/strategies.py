"""
Build Hypothesis strategies with configured text domains and authoritative schema checks.
"""

import copy
import re
from typing import cast

from hypothesis.strategies import SearchStrategy
from hypothesis_jsonschema import from_schema
from jsonschema import validators

from hypothesis_helm.schemas.configuration.characters import declared_text, validate_character_sets
from hypothesis_helm.schemas.contracts import Json, json_value, mapping, sequence

__all__ = ("CONTROL_CHARACTERS", "ordinary_generated_text", "schema_strategy", "supported_generated_text")


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


def schema_strategy(
    schema: dict[str, object],
    *,
    generation_schema: dict[str, object] | None = None,
    character_sets: str | None = None,
    generation: dict[str, object] | None = None,
    path: tuple[str | int, ...] = (),
) -> SearchStrategy[object]:
    """
    Generate schema-valid samples without control-character fuzzing.

    Args:
        schema (dict[str, object]): JSON Schema defining the accepted value domain.
        generation_schema (dict[str, object] | None): Optional library-compatible generation view; schema still validates every result.
        character_sets (str | None): Saved character domain, or the active worker policy.
        generation (dict[str, object] | None): Chart-specific text settings and branch overrides.
        path (tuple[str | int, ...]): Root path of the schema fragment within chart values.

    Returns:
        SearchStrategy[object]: Result of the documented operation.
    """
    from hypothesis_helm.schemas.configuration.settings import global_settings, normalize_text, settings_at

    validator = validators.validator_for(schema)(schema)
    frozen: dict[str, object] = copy.deepcopy(generation) if generation else {"defaults": global_settings(), "rules": []}
    if character_sets is not None:
        mapping(frozen["defaults"])["character_sets"] = validate_character_sets(character_sets)
    selected = settings_at(frozen, path)["character_sets"]
    literals = declared_text(schema)
    unicode_branches = any(mapping(rule).get("character_sets") == "unicode" for rule in sequence(frozen.get("rules", [])))
    codec = "ascii" if selected == "ascii" and not unicode_branches and all(value.isascii() for value in literals) else "utf-8"
    generating = copy.deepcopy(schema if generation_schema is None else generation_schema)
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
