"""Schema generation, bounded rendering, and extensible manifest properties."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

import yaml
from attrs import define
from hypothesis import HealthCheck, Phase, given, seed, settings
from hypothesis_jsonschema import from_schema
from jsonschema import validators

from .finite import enumerate_values
from .templates import discover


@define
class Chart:
    path: Path
    schema: dict
    defaults: dict

    @classmethod
    def load(cls, path: str | Path) -> Chart:
        path = Path(path).resolve()
        metadata = yaml.safe_load((path / "Chart.yaml").read_text())
        if not isinstance(metadata, dict) or not metadata.get("name"):
            raise ValueError("Chart.yaml must contain a chart name")
        schema = json.loads((path / "values.schema.json").read_text())
        if not isinstance(schema, dict) or schema.get("type") != "object":
            raise ValueError("values.schema.json must declare type: object")

        # Do not allow implicit network resolution or files outside the chart.
        def refs(node):
            if isinstance(node, dict):
                if "$ref" in node and not node["$ref"].startswith("#"):
                    raise ValueError("only local JSON Pointer schema references are supported")
                for value in node.values():
                    refs(value)
            elif isinstance(node, list):
                for value in node:
                    refs(value)

        refs(schema)
        validators.validator_for(schema).check_schema(schema)
        defaults = yaml.safe_load((path / "values.yaml").read_text()) or {}
        if not isinstance(defaults, dict):
            raise ValueError("values.yaml must contain an object")
        return cls(path, schema, defaults)

    def strategy(self):
        """Generate schema-valid overrides; Helm still merges chart defaults."""
        return from_schema(self.schema)


def merge_values(defaults, overrides):
    """Model ordinary Helm map merging and null deletion for schema preflight.

    Helm is authoritative, especially for dependency coalescing and globals.
    """
    result = copy.deepcopy(defaults)
    for key, value in overrides.items():
        if value is None:
            result.pop(key, None)
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_values(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _schema_nodes(schema, path, root, seen=frozenset()):
    if not isinstance(schema, dict):
        return []
    marker = (id(schema), path)
    if marker in seen:
        return []
    seen = seen | {marker}
    found = []
    if "$ref" in schema:
        target = root
        for part in schema["$ref"].removeprefix("#/").split("/"):
            if schema["$ref"] == "#":
                break
            target = target[part.replace("~1", "/").replace("~0", "~")]
        found += _schema_nodes(target, path, root, seen)
    for keyword in ("allOf", "anyOf", "oneOf"):
        for branch in schema.get(keyword, []):
            found += _schema_nodes(branch, path, root, seen)
    if not path:
        return found + [schema]
    key, *rest = path
    if key in schema.get("properties", {}):
        found += _schema_nodes(schema["properties"][key], tuple(rest), root, seen)
    if key == "*" and isinstance(schema.get("items"), dict):
        found += _schema_nodes(schema["items"], tuple(rest), root, seen)
    # Explicitly typed map entries count as documentation; open maps do not.
    if isinstance(schema.get("additionalProperties"), dict):
        found += _schema_nodes(schema["additionalProperties"], tuple(rest), root, seen)
    import re

    for pattern, branch in schema.get("patternProperties", {}).items():
        if key == "*" or re.search(pattern, key):
            found += _schema_nodes(branch, tuple(rest), root, seen)
    return found


def _default_paths(value, prefix=()):
    if isinstance(value, dict):
        for key, child in value.items():
            path = prefix + (str(key),)
            yield path
            yield from _default_paths(child, path)
    elif isinstance(value, list):
        for child in value:
            yield from _default_paths(child, prefix + ("*",))


def audit(chart: Chart) -> dict:
    """Inventory referenced/default paths and documentation gaps without rendering."""
    from attrs import asdict

    references, diagnostics = discover(chart.path)
    defaults = set(_default_paths(chart.defaults))
    paths = defaults | {r.path for r in references if r.path}
    findings = []
    for path in sorted(paths):
        nodes = _schema_nodes(chart.schema, path, chart.schema)
        locations = [asdict(r) for r in references if r.path == path]
        if not nodes:
            findings.append({"path": list(path), "issue": "undocumented", "references": locations})
        elif not any("type" in n or "enum" in n or "const" in n for n in nodes):
            findings.append({"path": list(path), "issue": "untyped", "references": locations})
        elif not any(n.get("description") for n in nodes):
            findings.append(
                {"path": list(path), "issue": "missing-description", "references": locations}
            )
        if locations and path not in defaults and "*" not in path:
            findings.append({"path": list(path), "issue": "no-default", "references": locations})
    return {
        "chart": str(chart.path),
        "references": [asdict(r) for r in references],
        "findings": findings,
        "unresolved": [asdict(d) for d in diagnostics],
    }


class RenderFailure(AssertionError):
    """A reproducible values input failed the rendering contract."""


def validate_resources(resources: list[dict]) -> None:
    """Check resource envelopes; callers can add Kubernetes or domain validation."""
    identities = set()
    for resource in resources:
        if not isinstance(resource, dict):
            raise RenderFailure("rendered document is not an object")
        for key in ("apiVersion", "kind"):
            if not isinstance(resource.get(key), str) or not resource[key]:
                raise RenderFailure(f"resource has no nonempty {key}")
        if resource["kind"] == "List":
            if not isinstance(resource.get("items"), list):
                raise RenderFailure("List resource has no items array")
            validate_resources(resource["items"])
            continue
        metadata = resource.get("metadata")
        if (
            not isinstance(metadata, dict)
            or not isinstance(metadata.get("name"), str)
            or not metadata["name"]
        ):
            raise RenderFailure("resource has no metadata.name")
        identity = (
            resource["apiVersion"],
            resource["kind"],
            metadata.get("namespace"),
            metadata["name"],
        )
        if identity in identities:
            raise RenderFailure(f"duplicate resource: {identity}")
        identities.add(identity)


def render(
    chart: Chart,
    values: dict,
    *,
    helm="helm",
    timeout=30.0,
    release="hypothesis",
    namespace="default",
    kube_version=None,
) -> list[dict]:
    """Render locally with Helm schema checks enabled and a subprocess deadline."""
    with tempfile.TemporaryDirectory(prefix="hypothesis-helm-") as directory:
        value_file = Path(directory) / "values.json"
        value_file.write_text(json.dumps(values, ensure_ascii=True))
        command = [
            helm,
            "template",
            release,
            str(chart.path),
            "--namespace",
            namespace,
            "--values",
            str(value_file),
        ]
        if kube_version:
            command += ["--kube-version", kube_version]
        try:
            process = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise RenderFailure(f"helm exceeded {timeout}s") from exc
        if process.returncode:
            raise RenderFailure(process.stderr.strip() or f"helm exited {process.returncode}")
        try:
            resources = [item for item in yaml.safe_load_all(process.stdout) if item is not None]
        except yaml.YAMLError as exc:
            raise RenderFailure(f"invalid rendered YAML: {exc}") from exc
    validate_resources(resources)
    return resources


def check_chart(
    chart: Chart | str | Path,
    *,
    max_examples=100,
    random_seed=0,
    timeout=30.0,
    helm="helm",
    release="hypothesis",
    namespace="default",
    kube_version=None,
    allow_empty=False,
    artifact_dir: Path | None = None,
    exhaustive=False,
    max_cases=1000,
    properties: tuple[Callable[[list[dict]], None], ...] = (),
) -> dict:
    """Check defaults then generated overrides, shrinking failing inputs.

    Custom properties receive rendered resources and should raise AssertionError on
    failure. The report is evidence from a bounded sample, never a proof of totality.
    """
    if not isinstance(chart, Chart):
        chart = Chart.load(chart)
    if max_examples < 1 or timeout <= 0:
        raise ValueError("max_examples and timeout must be positive")
    finite_values = enumerate_values(chart.schema, max_cases) if exhaustive else None
    count = 0
    last_failure = None

    def check(values):
        nonlocal count, last_failure
        count += 1
        try:
            effective = merge_values(chart.defaults, values)
            validators.validator_for(chart.schema)(chart.schema).validate(effective)
            resources = render(
                chart,
                values,
                helm=helm,
                timeout=timeout,
                release=release,
                namespace=namespace,
                kube_version=kube_version,
            )
            if not resources and not allow_empty:
                raise RenderFailure("chart rendered no resources (use allow_empty explicitly)")
            for prop in properties:
                prop(resources)
        except Exception as exc:
            last_failure = (values, str(exc))
            raise

    def save_failure(exc):
        values, message = last_failure or ({}, str(exc))
        result = {
            "status": "failed",
            "chart": str(chart.path),
            "seed": random_seed,
            "attempts": count,
            "error": message,
            "values": values,
            "failure_type": type(exc).__name__,
        }
        if artifact_dir is not None:
            artifact_dir.mkdir(parents=True, exist_ok=True)
            (artifact_dir / "values.json").write_text(json.dumps(values, indent=2) + "\n")
            (artifact_dir / "report.json").write_text(json.dumps(result, indent=2) + "\n")
        return result

    try:
        check({})
    except Exception as exc:
        return save_failure(exc)

    if finite_values is not None:
        try:
            for values in finite_values:
                check(values)
        except Exception as exc:
            return save_failure(exc)
        return {
            "status": "passed",
            "chart": str(chart.path),
            "attempts": count,
            "mode": "exhaustive",
            "domain_size": len(finite_values),
            "scope": "all schema-valid overrides in this finite domain, current Helm environment",
            "proof_of_totality": False,
        }

    @seed(random_seed)
    @settings(
        max_examples=max_examples,
        deadline=None,
        database=None,
        phases=(Phase.generate, Phase.shrink),
        report_multiple_bugs=False,
        suppress_health_check=(HealthCheck.too_slow,),
    )
    @given(chart.strategy())
    def property_test(values):
        check(values)

    try:
        property_test()
    except Exception as exc:
        return save_failure(exc)
    return {
        "status": "passed",
        "chart": str(chart.path),
        "seed": random_seed,
        "attempts": count,
        "max_examples": max_examples,
        "mode": "sampled",
        "proof_of_totality": False,
    }
