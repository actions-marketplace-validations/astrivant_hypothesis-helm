"""
Identify object domains whose schema supplies no field structure for generation.
"""

import logging
from pathlib import Path

from hypothesis_helm.findings.severity import ACTIVE_POLICY, for_paths, level, log_level
from hypothesis_helm.reporting.console.progress import format_path
from hypothesis_helm.rules import ignored
from hypothesis_helm.schemas.contracts import sequence
from hypothesis_helm.schemas.paths import ValuePath, dereference, enumerate_paths

__all__ = ("MESSAGE", "described", "opaque_paths", "warn_opaque")


LOGGER = logging.getLogger(__name__)
MESSAGE = (
    "Object permits unspecified entries without describing their field types. "
    "Tests can sample this domain, but cannot enumerate it or infer intended field types from this declaration. "
    "Declare properties, patternProperties or a typed additionalProperties schema."
)


def described(node: object, root: dict[str, object], seen: tuple[str, ...] = ()) -> bool:
    """
    Recognize structure or restrictions that rule out an unconstrained object map.

    Args:
        node (object): Reference-expanded schema or boolean schema.
        root (dict[str, object]): Original schema for references inside root-level branches.
        seen (tuple[str, ...]): References already considered at this object path.

    Returns:
        bool: Whether this declaration describes fields or excludes arbitrary objects.
    """
    if not isinstance(node, dict):
        return node is False
    if "$ref" in node:
        reference = str(node["$ref"])
        if reference in seen:
            return True  # A recursive declaration is not evidence of an opaque map.
        return described(dereference(node, root), root, (*seen, reference))
    kind = node.get("type")
    if kind is not None and kind != "object" and not (isinstance(kind, list) and "object" in kind):
        return True
    if "enum" in node or "const" in node or node.get("maxProperties") == 0 or node.get("propertyNames") is False:
        return True
    if node.get("properties") or node.get("patternProperties") or node.get("additionalProperties") is False:
        return True
    extra = node.get("additionalProperties")
    if isinstance(extra, dict) and (
        any(key in extra for key in ("type", "enum", "const", "$ref", "properties")) or described(extra, root, seen)
    ):
        return True
    if any(described(branch, root, seen) for branch in sequence(node.get("allOf", []))):
        return True
    for keyword in ("anyOf", "oneOf"):
        if keyword in node and all(described(branch, root, seen) for branch in sequence(node[keyword])):
            return True
    return False


def opaque_paths(schema: dict[str, object]) -> list[tuple[str | int, ...]]:
    """
    Find opaque objects, including root objects, referenced fields and array items.

    Args:
        schema (dict[str, object]): Original declared or inferred input schema.

    Returns:
        list[tuple[str | int, ...]]: Unique schema paths with no described object structure.
    """
    entries = [ValuePath((), dereference(schema, schema)), *enumerate_paths(schema)]
    paths: list[tuple[str | int, ...]] = []
    found: set[tuple[str | int, ...]] = set()
    for entry in entries:
        if not described(entry.schema, schema) and not any(entry.path[:depth] in found for depth in range(len(entry.path) + 1)):
            paths.append(entry.path)
            found.add(entry.path)
    return paths


def warn_opaque(schema: dict[str, object], chart: str) -> None:
    """
    Warn once per opaque path at chart planning time, honoring the finding policy.

    Args:
        schema (dict[str, object]): Original schema before generation restrictions.
        chart (str): Chart name or source directory for terminal context.

    Returns:
        None: Warnings do not restrict generation or change the chart's schema.
    """
    try:
        paths = opaque_paths(schema)
    except ValueError as exc:
        LOGGER.debug("Opaque-object inspection unavailable for %s: %s", chart, exc)
        return
    for path in paths:
        if ignored("HH2006", chart=Path(chart), paths=(path,)):
            continue
        severity = level("HH2006", settings=ACTIVE_POLICY.get() or for_paths(Path(chart), (path,)))
        LOGGER.log(log_level(severity), "[HH2006] Opaque object: chart=%s; path=%s; %s", chart, format_path(path), MESSAGE)
