"""
Look up manifest destinations in supplied, cached, or bundled Kubernetes schemas.
"""

import hashlib
import json
from contextvars import ContextVar
from functools import lru_cache
from pathlib import Path

from hypothesis_helm_catalog.builder import KEYWORDS, LIBRARY, scalar_domain
from jsonschema import validators

from hypothesis_helm.environment import env
from hypothesis_helm.schemas.configuration.policy import inherited_policy, intersect
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.paths import dereference

__all__ = ("cached_catalog", "catalog_domain", "collection_domain", "destination", "library", "resource_schemas", "validate_custom")


SUITE_RESOURCE_SCHEMAS: ContextVar[dict[str, object] | None] = ContextVar("suite_resource_schemas", default=None)


def collection_domain(node: dict[str, object], root: dict[str, object], depth: int = 0) -> dict[str, object]:
    """
    Retain bounded collection structure while resolving local schema references.

    Args:
        node (dict[str, object]): Destination schema node.
        root (dict[str, object]): Resource schema used for local references.
        depth (int): Current expansion depth; recursive structures remain unresolved.

    Returns:
        dict[str, object]: Self-contained restrictions for a serialized collection.
    """
    if depth > 16:
        raise ValueError("recursive or deeply nested destination schema")
    node = dereference(node, root)
    result = {key: value for key, value in node.items() if key in KEYWORDS}
    for key in ("items", "additionalProperties"):
        child = node.get(key)
        if isinstance(child, dict):
            result[key] = collection_domain(mapping(child), root, depth + 1)
        elif isinstance(child, bool):
            result[key] = child
    if isinstance(node.get("properties"), dict):
        result["properties"] = {
            key: collection_domain(mapping(value), root, depth + 1) for key, value in mapping(node["properties"]).items()
        }
    for key in ("allOf", "anyOf", "oneOf"):
        if isinstance(node.get(key), list):
            result[key] = [collection_domain(mapping(value), root, depth + 1) for value in sequence(node[key])]
    return result


def catalog_domain(catalog: dict[str, object], identity: str, path: tuple[str, ...], depth: int = 0) -> dict[str, object] | None:
    """
    Reconstruct collection types from the catalog's indexed field schemas.

    Args:
        catalog (dict[str, object]): Selected version's destination catalog.
        identity (str): API version and kind.
        path (tuple[str, ...]): Selected field path.
        depth (int): Bounded recursion through collection members.

    Returns:
        dict[str, object] | None: Known type and child domains, or an unresolved destination.
    """
    paths = mapping(mapping(catalog["resources"]).get(identity, {}))
    key = paths.get("/".join(path))
    if key is None or depth > 16:
        return None
    result = dict(mapping(mapping(mapping(catalog["domains"])[str(key)])["schema"]))
    kinds = result.get("type", [])
    kinds = [kinds] if isinstance(kinds, str) else kinds
    if not isinstance(kinds, list):
        return result
    kind = next((kind for kind in ("object", "array") if kind in kinds), None)
    if kind is None:
        return result
    prefix = "/".join(path) + "/" if path else ""
    children = sorted({name[len(prefix) :].split("/")[0] for name in paths if name.startswith(prefix) and name != prefix})
    for child in children:
        domain = catalog_domain(catalog, identity, (*path, child), depth + 1)
        if domain is None:
            continue
        if child == "*":
            result["items" if kind == "array" else "additionalProperties"] = domain
        elif kind == "object":
            mapping(result.setdefault("properties", {}))[child] = domain
    return result


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


@lru_cache(maxsize=16)
def cached_catalog(file: Path, digest: str) -> dict[str, object]:
    """
    Load a prepared catalog once and reject content changes to its recorded snapshot.

    Args:
        file (Path): Local catalog snapshot.
        digest (str): Content hash fixed by schema preparation.

    Returns:
        dict[str, object]: Verified catalog data shared by destination lookups in this process.
    """
    contents = file.read_bytes()
    if hashlib.sha256(contents).hexdigest() != digest:
        raise ValueError("Cached input catalog changed after preparation; prepare schemas again")
    return mapping(json.loads(contents))


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
    live = mapping(json.loads(env.get("HYPOTHESIS_HELM_CONFORMITY", "{}")))
    catalog = library()
    if live.get("catalog"):
        candidate = cached_catalog(Path(str(live["catalog"])), str(live["catalog_digest"]))
        if candidate.get("version") != live.get("version"):
            raise ValueError("Cached input catalog does not match the selected Kubernetes schema version")
        catalog = candidate
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
            source = f"schema-cache:{live.get('version')}:{live.get('identity')}"
    if root is not None:
        node = root
        for key in path:
            node = dereference(node, root)
            child = node.get("items", {}) if key == "*" else mapping(node.get("properties", {})).get(key, {})
            if not isinstance(child, dict):
                return None
            node = mapping(child)
        node = dereference(node, root)
        result = scalar_domain(node)
        kinds = node.get("type", [])
        kinds = [kinds] if isinstance(kinds, str) else kinds
        if isinstance(kinds, list) and any(kind in kinds for kind in ("object", "array")):
            try:
                result = collection_domain(node, root)
            except ValueError:
                return None
        if node.get("format") in {"int32", "int64"}:
            bits = int(str(node["format"])[3:])
            result = intersect(result, {"minimum": -(2 ** (bits - 1)), "maximum": 2 ** (bits - 1) - 1})
        # Only the version-matched catalog establishes exact API destinations for supplements.
        if identity not in custom:
            if catalog.get("version") == live.get("version"):
                record_id = mapping(mapping(catalog["resources"]).get(identity, {})).get("/".join(path))
                if record_id is not None:
                    record = mapping(mapping(catalog["domains"])[str(record_id)])
                    result = intersect(result, mapping(record["schema"]))
                    source += f"+catalog:{record_id}"
        return (result, source) if result else None
    # A missing field in the selected schema must not silently borrow a rule from the bundled version.
    if live or identity in custom:
        return None
    record_id = mapping(mapping(catalog["resources"]).get(identity, {})).get("/".join(path))
    if record_id is None:
        return None
    record = mapping(mapping(catalog["domains"])[str(record_id)])
    return catalog_domain(catalog, identity, path) or mapping(record["schema"]), f"bundled:{catalog['version']}:{record_id}"


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
