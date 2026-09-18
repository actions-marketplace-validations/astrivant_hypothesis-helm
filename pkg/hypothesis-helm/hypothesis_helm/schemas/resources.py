"""
Look up manifest destinations in supplied, cached, or bundled Kubernetes schemas.
"""

import json
import os
from contextvars import ContextVar
from functools import lru_cache
from pathlib import Path

from hypothesis_helm_catalog.builder import KEYWORDS, LIBRARY
from jsonschema import validators

from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.paths import dereference
from hypothesis_helm.schemas.policy import inherited_policy, intersect

SUITE_RESOURCE_SCHEMAS: ContextVar[dict[str, object] | None] = ContextVar("suite_resource_schemas", default=None)


def resource_schemas() -> dict[str, object]:
    """
    Combine saved output contracts with any explicit current configuration.

    Returns:
        dict[str, object]: Schema registrations; current configuration overrides saved entries for the same identity.
    """
    return {**(SUITE_RESOURCE_SCHEMAS.get() or {}), **mapping(inherited_policy().get("resource_schemas", {}))}


@lru_cache(maxsize=1)
def library() -> dict[str, object]:
    """
    Load the packaged immutable destination catalog once per process.

    Returns:
        dict[str, object]: Versioned resources and deduplicated domains.
    """
    return mapping(json.loads(LIBRARY.read_text()))


def destination(identity: str, path: tuple[str, ...]) -> tuple[dict[str, object], str] | None:
    """
    Resolve a direct field's scalar constraints without guessing a custom resource contract.

    Args:
        identity (str): apiVersion/Kind identity from the manifest.
        path (tuple[str, ...]): Manifest field path, with * for array positions.

    Returns:
        tuple[dict[str, object], str] | None: Scalar restriction and provenance, or unknown.
    """
    custom = resource_schemas()
    live = mapping(json.loads(os.environ.get("HYPOTHESIS_HELM_CONFORMITY", "{}")))
    catalog = library()
    root: dict[str, object] | None = None
    source = ""
    if identity in custom:
        root = mapping(custom[identity])
        source = "supplied-resource-schema"
    elif live.get("schemas"):
        api, kind = identity.rsplit("/", 1)
        group, version = api.rsplit("/", 1) if "/" in api else ("", api)
        suffix = f"-{group.split('.')[0]}" if group else ""
        file = Path(str(live["schemas"])) / f"{kind.lower()}{suffix}-{version.lower()}.json"
        if file.is_file():
            root = mapping(json.loads(file.read_text()))
            source = f"kubeconform:{live.get('version')}:{live.get('identity')}"
    if root is not None:
        node = root
        for key in path:
            node = dereference(node, root)
            child = node.get("items", {}) if key == "*" else mapping(node.get("properties", {})).get(key, {})
            if not isinstance(child, dict):
                return None
            node = mapping(child)
        node = dereference(node, root)
        result = {key: value for key, value in node.items() if key in KEYWORDS}
        if node.get("format") in {"int32", "int64"}:
            bits = int(str(node["format"])[3:])
            result = intersect(result, {"minimum": -(2 ** (bits - 1)), "maximum": 2 ** (bits - 1) - 1})
        # Reviewed descriptions supplement upstream gaps only when the description still matches.
        if identity not in custom:
            for item in sequence(catalog["reviewed"]):
                review = mapping(item)
                if node.get("description") == review["description"]:
                    result = intersect(result, mapping(review["schema"]))
                    source += f"+reviewed:{review['id']}"
        return (result, source) if result else None
    if live or identity in custom:
        return None
    record_id = mapping(mapping(catalog["resources"]).get(identity, {})).get("/".join(path))
    if record_id is None:
        return None
    record = mapping(mapping(catalog["domains"])[str(record_id)])
    return mapping(record["schema"]), f"bundled:{catalog['version']}:{record_id}"


def validate_custom(resource: dict[str, object]) -> bool:
    """
    Validate an explicitly supplied custom resource schema and reject missing custom contracts.

    Args:
        resource (dict[str, object]): Parsed manifest with apiVersion and kind.

    Returns:
        bool: True for a supplied schema, false for a known built-in API; otherwise raise ValueError.
    """
    identity = f"{resource.get('apiVersion')}/{resource.get('kind')}"
    custom = resource_schemas()
    if identity in custom:
        schema = mapping(custom[identity])
        validators.validator_for(schema)(schema).validate(json_value(resource))
        return True
    api = str(resource.get("apiVersion", ""))
    group = api.rsplit("/", 1)[0] if "/" in api else ""
    groups = {key.rsplit("/", 2)[0] for key in mapping(library()["resources"]) if key.count("/") == 2}
    if group and group not in groups:
        raise ValueError(f"Custom resource {identity} requires an explicit JSON schema in resource_schemas")
    return False
