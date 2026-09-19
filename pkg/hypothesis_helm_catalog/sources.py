"""
Rebuild portable domains from pinned Kubernetes Go sources and verify their boundaries.
"""

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

from hypothesis_helm.execution.processes import Processes
from hypothesis_helm.schemas.contracts import json_value, mapping, sequence
from hypothesis_helm.schemas.policy import intersect
from jsonschema import validators

REVISION = "66452049f3d692768c39c797b21b793dce80314e"
VERSION = "1.35.0"
REPOSITORY = "https://github.com/kubernetes/kubernetes.git"
TOOL = Path(__file__).with_name("upstream")

# Bindings identify reviewed API types, not similarly named Helm inputs. The Go
# extractor supplies the actual patterns and bounds from the pinned validators.
BINDINGS = {
    "io.k8s.api.core.v1.ConfigMapVolumeSource/name": "dns1123-subdomain",
    "io.k8s.api.core.v1.ConfigMapKeySelector/name": "dns1123-subdomain",
    "io.k8s.api.core.v1.ConfigMapEnvSource/name": "dns1123-subdomain",
    "io.k8s.api.core.v1.ConfigMapProjection/name": "dns1123-subdomain",
    "io.k8s.api.core.v1.SecretVolumeSource/secretName": "dns1123-subdomain",
    "io.k8s.api.core.v1.SecretKeySelector/name": "dns1123-subdomain",
    "io.k8s.api.core.v1.SecretEnvSource/name": "dns1123-subdomain",
    "io.k8s.api.core.v1.SecretProjection/name": "dns1123-subdomain",
    "io.k8s.api.core.v1.ContainerPort/containerPort": "port-number",
    "io.k8s.api.core.v1.ServicePort/port": "port-number",
}


def checkout(cache: Path, *, offline: bool) -> Path:
    """
    Acquire a locked, immutable source checkout containing only catalog inputs.

    Args:
        cache (Path): User-owned schema cache.
        offline (bool): Forbid downloads and require an existing source checkout.

    Returns:
        Path: Pinned Kubernetes source root.
    """
    import fcntl

    from hypothesis_helm.schemas.conformity import git

    cache.mkdir(parents=True, exist_ok=True)
    target = cache / "kubernetes" / REVISION
    with (cache / "source.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if target.is_dir():
            if git(target, "rev-parse", "HEAD") != REVISION or git(target, "status", "--porcelain", "--untracked-files=no"):
                raise ValueError("Cached Kubernetes sources changed; remove the source checkout and rebuild")
            return target
        if offline:
            raise ValueError("Pinned Kubernetes sources are not cached; rebuild once online")
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
            root = Path(temporary)
            git(root, "init")
            git(root, "remote", "add", "origin", REPOSITORY)
            git(root, "config", "remote.origin.promisor", "true")
            git(root, "config", "remote.origin.partialclonefilter", "blob:none")
            git(root, "fetch", "--depth=1", "--filter=blob:none", "origin", REVISION)
            git(root, "sparse-checkout", "set", "staging/src/k8s.io/api", "staging/src/k8s.io/apimachinery", "pkg/apis", "api/openapi-spec")
            git(root, "checkout", "--detach", "FETCH_HEAD")
            root.rename(target)
        return target


def verify(binary: Path, profiles: dict[str, object], owner: Processes) -> dict[str, object]:
    """
    Compare Python generation domains with real Go validators on deterministic boundary cases.

    Args:
        binary (Path): Built source extractor and validator oracle.
        profiles (dict[str, object]): Exported primitive schemas.
        owner (Processes): Owner of bounded child processes.

    Returns:
        dict[str, object]: Reproducible verification counts and corpus identity, not a completeness proof.
    """
    cases: list[dict[str, object]] = []
    for name, raw in sorted(profiles.items()):
        schema = mapping(mapping(raw)["schema"])
        if schema.get("type") == "integer":
            lo, hi = int(str(schema["minimum"])), int(str(schema["maximum"]))
            values: list[object] = [lo - 1, lo, lo + 1, hi - 1, hi, hi + 1, -1, 0]
        else:
            maximum = int(str(schema["maxLength"]))
            values = ["", "a", "0", "config-map", "config.map", "I\n&", ">0", "a\n", "a\r", "a\t", "é", "-a", "a-", ".a", "a.", "a..b"]
            values.extend("a" * size for size in (maximum - 1, maximum, maximum + 1))
            values.extend(prefix + chr(char) + suffix for prefix, suffix in (("", ""), ("a", "z")) for char in range(128))
        cases.extend({"profile": name, "value": value} for value in values)
    corpus = "".join(json.dumps(case) + "\n" for case in cases)
    process = owner.run([str(binary), "--oracle"], input=corpus, capture_output=True, check=True, timeout=60)
    observed = [json.loads(line) for line in process.stdout.splitlines()]
    if len(observed) != len(cases):
        raise ValueError("Upstream validation oracle returned an incomplete result")
    for case, accepted in zip(cases, observed, strict=True):
        schema = mapping(mapping(profiles[str(case["profile"])])["schema"])
        expected = validators.validator_for(schema)(schema).is_valid(json_value(case["value"]))
        if expected != accepted:
            raise ValueError(f"Upstream validator disagrees with exported domain: {case!r}")
    return {"cases": len(cases), "corpus_sha256": hashlib.sha256(corpus.encode()).hexdigest(), "status": "passed"}


def destinations(source: Path, extracted: dict[str, object]) -> dict[str, object]:
    """
    Follow OpenAPI references to exact resource fields with exportable source constraints.

    Args:
        source (Path): Pinned Kubernetes checkout.
        extracted (dict[str, object]): Parsed Go annotations and primitive validators.

    Returns:
        dict[str, object]: Resource identities mapped to field paths and their constraint evidence.
    """
    document = mapping(json.loads((source / "api/openapi-spec/swagger.json").read_text()))
    definitions = mapping(document["definitions"])
    fields = mapping(extracted["fields"])
    profiles = mapping(extracted["profiles"])
    resources: dict[str, object] = {}
    for type_name, raw in sorted(definitions.items()):
        root = mapping(raw)
        kinds = sequence(root.get("x-kubernetes-group-version-kind", []))
        if not kinds:
            continue
        paths: dict[str, object] = {}

        def walk(
            node: dict[str, object], path: tuple[str, ...], owner: str, ancestry: frozenset[str], target: dict[str, object] = paths
        ) -> None:
            """
            Expand finite type references, preserving recursion as an unresolved boundary.

            Args:
                node (dict[str, object]): Current OpenAPI node.
                path (tuple[str, ...]): Manifest destination path.
                owner (str): Containing Go type identity.
                ancestry (frozenset[str]): Recursive reference guard.
                target (dict[str, object]): Destination index for the current resource.

            Returns:
                None: Append known independent scalar bounds.
            """
            if "$ref" in node:
                owner = str(node["$ref"]).removeprefix("#/definitions/")
                if owner in ancestry:
                    return
                walk(mapping(definitions[owner]), path, owner, ancestry | {owner})
                return
            for field, child in mapping(node.get("properties", {})).items():
                child = mapping(child)
                identity = f"{owner}/{field}"
                rules = [mapping(rule) for rule in sequence(fields.get(identity, []))]
                if identity in BINDINGS:
                    profile = BINDINGS[identity]
                    rules.append({"schema": mapping(profiles[profile])["schema"], "profile": profile, "type_field": identity})
                schema: dict[str, object] = {}
                for rule in rules:
                    schema = intersect(schema, mapping(rule["schema"]))
                if schema:
                    # Upstream nullable scalar fields are still intersected with the chart's own type.
                    if "type" in schema:
                        schema["type"] = [schema["type"], "null"]
                    target["/".join((*path, field))] = {"schema": schema, "evidence": rules}
                walk(child, (*path, field), "", ancestry)
            if isinstance(node.get("items"), dict):
                walk(mapping(node["items"]), (*path, "*"), "", ancestry)

        walk(root, (), type_name, frozenset({type_name}))
        for raw_kind in kinds:
            kind = mapping(raw_kind)
            api = "/".join(str(kind[key]) for key in ("group", "version") if kind.get(key))
            resources[f"{api}/{kind['kind']}"] = paths
    return resources


def rebuild(source: Path, cache: Path, go: str = "go", *, offline: bool = False) -> dict[str, object]:
    """
    Compile the pinned extractor, derive domains, and check them against upstream Go implementations.

    Args:
        source (Path): Kubernetes sources corresponding to the pinned release.
        cache (Path): Writable Go build and module cache root.
        go (str): Installed Go toolchain executable.
        offline (bool): Disable Go dependency and toolchain downloads.

    Returns:
        dict[str, object]: Verified portable catalog supplement with source evidence and unresolved annotations.
    """
    lock = mapping(json.loads((Path(__file__).with_name("data") / "kubernetes-source-lock.json").read_text()))
    for relative, digest in mapping(lock["sha256"]).items():
        file = source / relative
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Kubernetes source differs from pinned {VERSION}: {relative}; review the source lock before rebuilding")
    binary = shutil.which(go)
    if binary is None:
        raise ValueError("Catalog rebuilds require Go 1.25 or newer; run scripts/setup-dev.sh")
    cache = cache.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    environment = {**os.environ, "GOMODCACHE": str(cache / "go/modules"), "GOCACHE": str(cache / "go/build"), "GOTOOLCHAIN": "local"}
    if offline:
        environment.update(GOPROXY="off", GOSUMDB="off")
    owner = Processes()
    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        tool = Path(temporary) / "catalog-source"
        owner.run(
            [binary, "build", "-mod=readonly", "-o", str(tool), "."],
            cwd=TOOL,
            env=environment,
            capture_output=True,
            check=True,
            timeout=300,
        )
        output = owner.run([str(tool), "--source", str(source.resolve())], capture_output=True, check=True, timeout=60)
        result = mapping(json.loads(output.stdout))
        if result["source_hashes"] != lock["sha256"]:
            raise ValueError("Kubernetes source inventory differs from the pinned release; review the source lock before rebuilding")
        result["verification"] = verify(tool, mapping(result["profiles"]), owner)
    result.update(version=VERSION, revision=REVISION, repository=REPOSITORY, resources=destinations(source, result))
    return result
