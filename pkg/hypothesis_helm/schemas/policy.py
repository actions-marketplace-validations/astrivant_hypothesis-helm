"""
Load explicit generation domains without changing a chart's accepted contract.
"""

from __future__ import annotations

import copy
import json
import os
import re
from pathlib import Path

from hypothesis_helm_catalog.profiles import schema as profile_schema
from jsonschema import validators

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.limits import compiler_limits
from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.schemas.characters import validate_character_sets
from hypothesis_helm.schemas.contracts import json_value, mapping, number, sequence
from hypothesis_helm.schemas.selectors import selectors
from hypothesis_helm.schemas.settings import SETTING_KEYS, validate_settings

ENVIRONMENT = "HYPOTHESIS_HELM_INPUT_POLICY"
PROFILES: dict[str, dict[str, object]] = {
    "kubernetes-secret-name": profile_schema("dns1123-subdomain"),
    "kubernetes-configmap-name": profile_schema("dns1123-subdomain"),
    "absolute-posix-path": {"type": "string", "pattern": r"^/[^\x00\r\n]*(?![\s\S])"},
}


def configuration(config: Path | None) -> dict[str, object]:
    """
    Read the local policy and reject misspelled top-level options.

    Args:
        config (Path | None): Explicit file or working-directory default.

    Returns:
        dict[str, object]: Unresolved configuration, empty when no default file exists.
    """
    path = config or Path(".hypothesis-helm.yaml")
    if config is None and not path.is_file():
        return {}
    document = yamlio.load(path.read_text())
    if not isinstance(document, dict) or set(document) - {
        "ignored",
        "input_constraints",
        "resource_schemas",
        "downstream_inputs",
        "compiler",
        *SETTING_KEYS,
    }:
        raise ValueError(f"{path}: unknown configuration key; see the complete example in docs/input-domains/README.md")
    return mapping(document)


def path_parts(value: str) -> tuple[str, ...]:
    """
    Parse explicit object paths and array-item wildcards without name guessing.

    Args:
        value (str): Dollar-rooted dotted path, with optional [*] array selectors.

    Returns:
        tuple[str, ...]: Object keys and wildcard segments.
    """
    if value == "$":
        return ()
    if not re.fullmatch(r"\$(?:\.[A-Za-z_][A-Za-z_0-9-]*|\[\*\])+", value):
        raise ValueError(f"Invalid input constraint path {value!r}; use $.field.nested or $.items[*].field")
    return tuple(key or "*" for key, _ in re.findall(r"\.([A-Za-z_][A-Za-z_0-9-]*)|(\[\*\])", value[1:]))


def check_schema(schema: dict[str, object], *, inline: bool = False) -> None:
    """
    Validate an independent schema without allowing implicit reference downloads.

    Args:
        schema (dict[str, object]): User-supplied inline or resource schema.
        inline (bool): Reject references whose roots would change when embedded in chart values.

    Returns:
        None: Valid schema, or a configuration error before generation starts.
    """

    def visit(node: object) -> None:
        """
        Reject external references at every schema depth.

        Args:
            node (object): Current schema subtree.

        Returns:
            None: References stay within the supplied document.
        """
        if isinstance(node, dict):
            if inline and any(keyword in node for keyword in ("$ref", "$dynamicRef", "$recursiveRef", "$id")):
                raise ValueError("Inline input constraints must be self-contained without references or schema identifiers")
            for keyword in ("$ref", "$dynamicRef", "$recursiveRef"):
                if keyword in node and (not isinstance(node[keyword], str) or not node[keyword].startswith("#")):
                    raise ValueError("Input and resource schemas must use local references only")
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(schema)
    validators.validator_for(schema).check_schema(schema)


def load_policy(
    config: Path | None,
    *,
    character_sets: str | None = None,
    max_examples: int | None = None,
    compiler_call_depth: int | None = None,
) -> dict[str, object]:
    """
    Resolve chart-scoped restrictions and freeze supplied resource schemas for workers.

    Args:
        config (Path | None): Policy file; schema filenames are relative to this file.
        character_sets (str | None): Optional CLI override for the configured character domain.
        max_examples (int | None): Explicit CLI override for the global Hypothesis example budget.
        compiler_call_depth (int | None): Explicit CLI override for nested helper analysis.

    Returns:
        dict[str, object]: JSON-compatible policy with resource schema contents embedded.
    """
    document = configuration(config)
    limits = compiler_limits(document.get("compiler", {}), max_call_depth=compiler_call_depth)
    defaults = validate_settings(document)
    if max_examples is not None:
        defaults["hypothesis"] = {**mapping(defaults.get("hypothesis", {})), "max_examples": max_examples}
        validate_settings(defaults)
    root = (config or Path(".hypothesis-helm.yaml")).resolve().parent
    selected = validate_character_sets(defaults.get("character_sets", "ascii"))
    if character_sets is not None:
        selected = validate_character_sets(character_sets)
    if type(document.get("downstream_inputs", True)) is not bool:
        raise ValueError("downstream_inputs must be a Boolean")
    rules = document.get("input_constraints", []) or []
    resources = document.get("resource_schemas", {}) or {}
    if not isinstance(rules, list) or not isinstance(resources, dict):
        raise ValueError("input_constraints must be a list; resource_schemas must map apiVersion/Kind to JSON schema files")
    resolved: list[dict[str, object]] = []
    for raw in rules:
        rule = mapping(raw)
        if set(rule) - {"charts", "path", "profile", "schema", "allow_empty", "ignored", "enabled", *SETTING_KEYS}:
            raise ValueError("Unknown input constraint option")
        charts = selectors(rule.get("charts"), root)
        generation = validate_settings(rule)
        path = rule.get("path")
        if not isinstance(path, str):
            raise ValueError("Each input constraint requires a string 'path'")
        path_parts(path)
        controls: dict[str, object] = {}
        for key in ("ignored", "enabled"):
            if key in rule:
                codes = rule[key]
                if not isinstance(codes, list) or any(not isinstance(code, str) or code not in CATALOG for code in codes):
                    raise ValueError(f"Input constraint '{key}' must be a list of known finding codes")
                controls[key] = sorted(set(codes))
        if set(sequence(controls.get("ignored", []))) & set(sequence(controls.get("enabled", []))):
            raise ValueError("An input constraint cannot both ignore and enable the same code")
        constrained = "profile" in rule or "schema" in rule
        if "profile" in rule and "schema" in rule or not constrained and not controls and not generation:
            raise ValueError("Each input constraint requires one of 'profile' or 'schema', or finding/generation settings")
        resolved_rule: dict[str, object] = {"charts": charts, "path": path, **controls, **generation}
        if not constrained:
            if "allow_empty" in rule:
                raise ValueError("allow_empty requires a profile or schema")
            resolved.append(resolved_rule)
            continue
        if "profile" in rule:
            profile = str(rule["profile"])
            if profile not in PROFILES:
                raise ValueError(f"Unknown input profile {profile!r}; choose from {', '.join(PROFILES)}")
            schema = copy.deepcopy(PROFILES[profile])
        else:
            schema = mapping(rule["schema"])
        check_schema(schema, inline=True)
        if type(rule.get("allow_empty", False)) is not bool:
            raise ValueError("allow_empty must be a Boolean")
        if rule.get("allow_empty"):
            if schema.get("type") != "string":
                raise ValueError("allow_empty requires a string constraint")
            schema = {"type": "string", "anyOf": [schema, {"const": ""}]}
        resolved.append({**resolved_rule, "schema": schema, "source": rule.get("profile", "inline")})
    supplied: dict[str, object] = {}
    for identity, filename in resources.items():
        if not isinstance(identity, str) or not re.fullmatch(r"[A-Za-z0-9./-]+/[A-Za-z][A-Za-z0-9]*", identity):
            raise ValueError("Resource schema keys must be apiVersion/Kind, such as example.org/v1/Widget")
        if not isinstance(filename, str):
            raise ValueError(f"Resource schema {identity} must name a JSON schema file")
        schema = mapping(json.loads((root / filename).read_text()))
        check_schema(schema)
        supplied[identity] = schema
    return {
        **defaults,
        "input_constraints": resolved,
        "resource_schemas": supplied,
        "downstream_inputs": document.get("downstream_inputs", True),
        "character_sets": selected,
        "compiler": limits,
    }


def inherited_policy() -> dict[str, object]:
    """
    Read the coordinator's resolved policy, shared by all workers and shards.

    Returns:
        dict[str, object]: Immutable-by-convention JSON policy.
    """
    return mapping(json.loads(os.environ.get(ENVIRONMENT, "{}")))


def intersect(original: dict[str, object], restriction: dict[str, object]) -> dict[str, object]:
    """
    Intersect schemas while retaining simple finite domains when possible.

    Args:
        original (dict[str, object]): Existing authoritative or inferred schema.
        restriction (dict[str, object]): Additional generation restriction.

    Returns:
        dict[str, object]: A subset of both schemas, never a widened domain.
    """
    if "$ref" in original:
        return {"allOf": [copy.deepcopy(original), copy.deepcopy(restriction)]}
    result = copy.deepcopy(original)
    remaining: dict[str, object] = {}
    for key, value in restriction.items():
        if key not in result or result[key] == value:
            result[key] = copy.deepcopy(value)
        elif key in {"minimum", "minLength", "minItems", "minProperties"}:
            result[key] = max(result[key], value, key=number)
        elif key in {"maximum", "maxLength", "maxItems", "maxProperties"}:
            result[key] = min(result[key], value, key=number)
        elif key == "type":
            left = sequence(result[key]) if isinstance(result[key], list) else [result[key]]
            right = sequence(value) if isinstance(value, list) else [value]
            common = [kind for kind in left if kind in right or kind == "integer" and "number" in right]
            if "number" in left and "integer" in right:
                common.append("integer")
            if not common:
                raise ValueError("Input constraint has no types in common with the chart schema")
            result[key] = common[0] if len(common) == 1 else common
        else:
            remaining[key] = copy.deepcopy(value)
    if remaining:
        sequence(result.setdefault("allOf", [])).append(remaining)
    validator = validators.validator_for(result)(result)
    if "enum" in result or "const" in result:
        values = [result["const"]] if "const" in result else sequence(result["enum"])
        allowed = [value for value in values if validator.is_valid(json_value(value))]
        if not allowed:
            raise ValueError("Input constraint excludes every declared enum/const value")
        result["enum"] = allowed
    for lower, upper in (("minimum", "maximum"), ("minLength", "maxLength"), ("minItems", "maxItems")):
        if lower in result and upper in result and number(result[lower]) > number(result[upper]):
            raise ValueError(f"Input constraint has contradictory {lower}/{upper}")
    return result


def restrict(schema: dict[str, object], path: tuple[str, ...], restriction: dict[str, object]) -> dict[str, object]:
    """
    Add a path constraint without making optional parents required.

    Args:
        schema (dict[str, object]): Generation schema to copy.
        path (tuple[str, ...]): Exact object path, with * for homogeneous array items.
        restriction (dict[str, object]): Schema applied where that path exists.

    Returns:
        dict[str, object]: Restricted copy, leaving the supplied document untouched.
    """
    if not path:
        return intersect(schema, restriction)
    if "$ref" in schema:
        return {"allOf": [copy.deepcopy(schema), restrict({}, path, restriction)]}
    result = copy.deepcopy(schema)
    head, *tail = path
    if head == "*":
        result["items"] = restrict(mapping(result.get("items", {})), tuple(tail), restriction)
    else:
        properties = mapping(result.setdefault("properties", {}))
        if head not in properties and result.get("additionalProperties") is False:
            sequence(result.setdefault("allOf", [])).append(restrict({}, path, restriction))
            return result
        properties[head] = restrict(mapping(properties.get(head, {})), tuple(tail), restriction)
    return result
