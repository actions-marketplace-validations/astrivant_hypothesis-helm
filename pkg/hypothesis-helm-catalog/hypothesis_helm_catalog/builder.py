"""
Rebuild reproducible destination domains from pinned schemas and reviewed descriptions.
"""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from hypothesis_helm.execution.processes import Processes
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
}


def build(directory: Path, version: str) -> dict[str, object]:
    """
    Extract scalar bounds and attach reviewed rules only to matching source descriptions.

    Args:
        directory (Path): Kubeconform standalone-strict schema snapshot.
        version (str): Kubernetes version represented by the snapshot.

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
            schema = {key: value for key, value in node.items() if key in KEYWORDS}
            origins = ["json-schema"]
            if node.get("format") in {"int32", "int64"}:
                bits = int(str(node["format"])[3:])
                schema = intersect(schema, {"minimum": -(2 ** (bits - 1)), "maximum": 2 ** (bits - 1) - 1})
                origins.append(str(node["format"]))
            review = by_description.get(str(node.get("description", "")))
            if review:
                schema = intersect(schema, mapping(review["schema"]))
                origins.append(str(review["id"]))
            if set(schema) - {"type"}:
                record = {"schema": schema, "sources": origins}
                key = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:20]
                domains[key] = record
                target["/".join(path)] = key
            for name, child in mapping(node.get("properties", {})).items():
                if isinstance(child, dict):
                    walk(mapping(child), (*path, name))
            if isinstance(node.get("items"), dict):
                walk(mapping(node["items"]), (*path, "*"))

        walk(document, ())
        sources[file.name] = hashlib.sha256(contents).hexdigest()
        for raw in sequence(kinds):
            kind = mapping(raw)
            api = "/".join(str(kind[key]) for key in ("group", "version") if kind.get(key))
            resources[f"{api}/{kind['kind']}"] = paths
    if not resources:
        raise ValueError("No Kubernetes resource schemas found in the source snapshot")
    return {
        "version": version,
        "revision": REVISION,
        "repository": "https://github.com/yannh/kubernetes-json-schema",
        "reviewed": reviewed,
        "source_hashes": sources,
        "domains": domains,
        "resources": resources,
    }


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
    parser.add_argument("--output", type=Path, default=LIBRARY)
    parser.add_argument("--check", action="store_true", help="compare without writing; fail if release data is stale")
    args = parser.parse_args(argv)
    if args.schema_dir is not None:
        catalog = build(args.schema_dir, args.schema_version)
    else:
        with tempfile.TemporaryDirectory(prefix="hypothesis-helm-domain-sources-") as temporary:
            root = Path(temporary)
            folder = f"v{args.schema_version}-standalone-strict"
            owner = Processes()
            owner.run(["git", "init", str(root)], check=True, capture_output=True, text=True, timeout=30)
            owner.run(
                ["git", "-C", str(root), "remote", "add", "origin", "https://github.com/yannh/kubernetes-json-schema.git"],
                check=True,
                timeout=30,
            )
            owner.run(["git", "-C", str(root), "config", "remote.origin.promisor", "true"], check=True, timeout=30)
            owner.run(["git", "-C", str(root), "config", "remote.origin.partialclonefilter", "blob:none"], check=True, timeout=30)
            owner.run(["git", "-C", str(root), "fetch", "--depth=1", "--filter=blob:none", "origin", REVISION], check=True, timeout=180)
            owner.run(["git", "-C", str(root), "sparse-checkout", "set", "--no-cone", f"/{folder}/"], check=True, timeout=30)
            owner.run(["git", "-C", str(root), "checkout", "--detach", "FETCH_HEAD"], check=True, timeout=180)
            catalog = build(root / folder, args.schema_version)
    contents = json.dumps(catalog, sort_keys=True, indent=2) + "\n"
    if args.check:
        return int(not args.output.is_file() or args.output.read_text() != contents)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(contents)
    print(f"Wrote {len(mapping(catalog['resources']))} resource domains to {args.output}")
    return 0
