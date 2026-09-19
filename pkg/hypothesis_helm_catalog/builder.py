"""
Rebuild reproducible destination domains from pinned schemas and reviewed descriptions.
"""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.schemas.policy import intersect

REVISION = "970cc70507e1880a7a3b64184b6aad417a1d8d85"
DATA = Path(__file__).with_name("data")
LIBRARY = DATA / "input-domains.json"
KEYWORDS = {
    "type",
    "enum",
    "const",
    "pattern",
    "minLength",
    "maxLength",
    "minimum",
    "maximum",
    "exclusiveMinimum",
    "exclusiveMaximum",
    "multipleOf",
    "required",
    "minItems",
    "maxItems",
    "uniqueItems",
    "minProperties",
    "maxProperties",
}


def scalar_domain(node: dict[str, object]) -> dict[str, object]:
    """
    Preserve self-contained scalar alternatives without moving unresolved references into input schemas.

    Args:
        node (dict[str, object]): Destination field schema or one of its scalar alternatives.

    Returns:
        dict[str, object]: Scalar bounds and supported composition; opaque compositions remain unrestricted.
    """
    result = {key: value for key, value in node.items() if key in KEYWORDS}
    compositions = {"allOf", "anyOf", "oneOf"}
    allowed = KEYWORDS | compositions | {"description", "title", "default", "examples", "format"}

    def supported(value: object) -> bool:
        """
        Require complete scalar alternatives so omission cannot change oneOf exclusivity.

        Args:
            value (object): Candidate alternative, including nested compositions.

        Returns:
            bool: Every validation keyword belongs to the supported scalar subset.
        """
        if not isinstance(value, dict) or value.keys() - allowed:
            return False
        return all(isinstance(value[key], list) and all(supported(child) for child in value[key]) for key in compositions & value.keys())

    for key in compositions:
        alternatives = node.get(key)
        if isinstance(alternatives, list) and all(supported(child) for child in alternatives):
            result[key] = [scalar_domain(mapping(child)) for child in alternatives]
    return result


def build(directory: Path, version: str, *, upstream: dict[str, object] | None = None) -> dict[str, object]:
    """
    Extract scalar bounds and attach reviewed rules only to matching source descriptions.

    Args:
        directory (Path): Standalone strict Kubernetes schema snapshot.
        version (str): Kubernetes version represented by the snapshot.
        upstream (dict[str, object] | None): Verified constraints extracted from matching Kubernetes Go sources.

    Returns:
        dict[str, object]: Deterministic catalog, with source hashes and review provenance.
    """
    reviewed = [mapping(row) for row in sequence(json.loads((DATA / "reviewed-domains.json").read_text()))]
    by_description: dict[str, dict[str, object]] = {}
    for row in reviewed:
        node = mapping(json.loads((directory / str(row["file"])).read_text()))
        for key in sequence(row["path"]):
            node = mapping(mapping(node["properties"])[str(key)])
        if node.get("description") != row["description"]:
            raise ValueError(f"Source description changed for {row['id']}; review its domain before rebuilding")
        by_description[str(row["description"])] = row
    domains: dict[str, object] = {}
    resources: dict[str, object] = {}
    sources: dict[str, str] = {}
    for file in sorted(directory.glob("*.json")):
        contents = file.read_bytes()
        document = mapping(json.loads(contents))
        kinds = document.get("x-kubernetes-group-version-kind", [])
        if not kinds:
            continue
        paths: dict[str, str] = {}

        def walk(node: dict[str, object], path: tuple[str, ...], target: dict[str, str] = paths) -> None:
            """
            Record only unconditional scalar constraints at exact schema destinations.

            Args:
                node (dict[str, object]): Current schema node.
                path (tuple[str, ...]): Manifest path, with * for array items.
                target (dict[str, str]): Destination index for this resource.

            Returns:
                None: Populate the shared deduplicated domain table and resource index.
            """
            schema = scalar_domain(node)
            origins = ["json-schema"]
            if node.get("format") in {"int32", "int64"}:
                bits = int(str(node["format"])[3:])
                schema = intersect(schema, {"minimum": -(2 ** (bits - 1)), "maximum": 2 ** (bits - 1) - 1})
                origins.append(str(node["format"]))
            review = by_description.get(str(node.get("description", "")))
            if review:
                schema = intersect(schema, mapping(review["schema"]))
                origins.append(str(review["id"]))
            if schema:
                record = {"schema": schema, "sources": origins}
                key = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:20]
                domains[key] = record
                target["/".join(path)] = key
            for name, child in mapping(node.get("properties", {})).items():
                if isinstance(child, dict):
                    walk(mapping(child), (*path, name))
            if isinstance(node.get("items"), dict):
                walk(mapping(node["items"]), (*path, "*"))
            if isinstance(node.get("additionalProperties"), dict):
                walk(mapping(node["additionalProperties"]), (*path, "*"))

        walk(document, ())
        sources[file.name] = hashlib.sha256(contents).hexdigest()
        for raw in sequence(kinds):
            kind = mapping(raw)
            api = "/".join(str(kind[key]) for key in ("group", "version") if kind.get(key))
            resources[f"{api}/{kind['kind']}"] = paths
    if not resources:
        raise ValueError("No Kubernetes resource schemas found in the source snapshot")
    catalog: dict[str, object] = {
        "version": version,
        "revision": REVISION,
        "repository": "https://github.com/yannh/kubernetes-json-schema",
        "reviewed": reviewed,
        "source_hashes": sources,
        "domains": domains,
        "resources": resources,
    }
    if upstream is not None:
        if upstream["version"] != version:
            raise ValueError("Kubernetes source and schema versions must match")
        for identity, raw in mapping(upstream["resources"]).items():
            if identity not in resources:
                continue
            projected_paths = mapping(resources[identity])
            for path, raw_rule in mapping(raw).items():
                rule = mapping(raw_rule)
                previous = mapping(domains[str(projected_paths[path])]) if path in projected_paths else {"schema": {}, "sources": []}
                record = {
                    "schema": intersect(mapping(previous["schema"]), mapping(rule["schema"])),
                    "sources": [*sequence(previous["sources"]), f"kubernetes-go:{upstream['revision']}"],
                    "evidence": rule["evidence"],
                }
                key = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:20]
                domains[key] = record
                projected_paths[path] = key
        catalog["upstream"] = {key: value for key, value in upstream.items() if key not in {"resources", "fields"}}
    return catalog


def main(argv: list[str] | None = None) -> int:
    """
    Rebuild or verify the shipped catalog during release preparation.

    Args:
        argv (list[str] | None): Command-line arguments, or the process arguments.

    Returns:
        int: Zero for success, one when --check finds a stale catalog.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema-dir", type=Path, help="local standalone-strict schema snapshot")
    parser.add_argument("--schema-version", default="1.35.0")
    parser.add_argument("--cache-dir", type=Path, default=Path("schemas"), help="local versioned schemas, source checkouts and Go caches")
    parser.add_argument("--kubernetes-source-dir", type=Path, help="existing checkout of the pinned Kubernetes release")
    parser.add_argument("--go", default="go", help="Go 1.25+ executable used only for catalog rebuilding")
    parser.add_argument("--offline", action="store_true", help="require cached sources and Go dependencies; do not download")
    parser.add_argument(
        "--output", type=Path, help="catalog destination; defaults to the versioned cache, or the bundled catalog with --check"
    )
    parser.add_argument("--check", action="store_true", help="compare without writing; fail if release data is stale")
    args = parser.parse_args(argv)
    from hypothesis_helm.schemas.conformity import prepare

    from hypothesis_helm_catalog.sources import VERSION, checkout, rebuild

    if args.schema_version != VERSION:
        parser.error(f"Go source bindings are pinned to Kubernetes {VERSION}; review the source pin before changing versions")
    source = args.kubernetes_source_dir or checkout(args.cache_dir, offline=args.offline)
    print("Extracting Kubernetes constraints and checking upstream validators")
    upstream = rebuild(source, args.cache_dir, args.go, offline=args.offline)
    if args.schema_dir is not None:
        catalog = build(args.schema_dir, args.schema_version, upstream=upstream)
    else:
        configuration = mapping(json.loads(prepare(args.cache_dir, args.schema_version, args.offline, revision=REVISION)))
        catalog = build(Path(str(configuration["schemas"])), args.schema_version, upstream=upstream)
    cache_catalog = args.cache_dir / "catalogs" / args.schema_version / "input-domains.json"
    args.output = args.output or (LIBRARY if args.check else cache_catalog)
    contents = json.dumps(catalog, sort_keys=True, indent=2) + "\n"
    if args.check:
        return int(not args.output.is_file() or args.output.read_text() != contents)
    for destination in {cache_catalog, args.output}:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
            staged = Path(temporary) / "input-domains.json"
            staged.write_text(contents)
            staged.replace(destination)
    print(f"Wrote {len(mapping(catalog['resources']))} resource domains to {args.output}")
    return 0
