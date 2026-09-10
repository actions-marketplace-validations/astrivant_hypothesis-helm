"""
Schema generation, bounded rendering, and extensible manifest properties.
"""

from __future__ import annotations

import copy
import json
import logging
import subprocess
import tempfile
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path

from attrs import define
from hypothesis import HealthCheck, Phase, given, seed, settings
from hypothesis.strategies import SearchStrategy
from jsonschema import validators
from ruamel.yaml.error import YAMLError

from hypothesis_helm.charts import yamlio
from hypothesis_helm.charts.presence import has_path
from hypothesis_helm.charts.templates import discover
from hypothesis_helm.reporting.output import emit_manifest
from hypothesis_helm.reporting.progress import format_path
from hypothesis_helm.schemas.conformity import validate
from hypothesis_helm.schemas.contracts import json_value, mapping, schema_strategy, sequence
from hypothesis_helm.schemas.finite import enumerate_values

LOGGER = logging.getLogger(__name__)


@define
class Chart:
    """
    Hold the chart location, documented schema, and round-trip defaults.

    Attributes:
        path (Path): Resolved value path or chart location.
        schema (dict[str, object]): Schema describing accepted values.
        defaults (dict[str, object]): Values loaded from the source chart.
    """

    path: Path
    schema: dict[str, object]
    defaults: dict[str, object]

    @classmethod
    def load(cls, path: str | Path) -> Chart:
        """
        Check load.

        Args:
            path (str | Path): Value path or chart location to inspect.

        Returns:
            Chart: Result of the documented operation.
        """
        path = Path(path).resolve()
        metadata = yamlio.load((path / "Chart.yaml").read_text())
        if not isinstance(metadata, dict) or not metadata.get("name"):
            raise ValueError("Chart.yaml must contain a chart name")
        schema = json.loads((path / "values.schema.json").read_text())
        if not isinstance(schema, dict) or schema.get("type") != "object":
            raise ValueError("values.schema.json must declare type: object")

        # Do not allow implicit network resolution or files outside the chart.
        def refs(node: object) -> None:
            """
            Reject external schema references before strategy construction.

            Args:
                node (object): Current schema or template node.

            Returns:
                None: None. The operation completes through its documented side effects.
            """
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
        defaults = yamlio.load((path / "values.yaml").read_text()) or {}
        if not isinstance(defaults, dict):
            raise ValueError("values.yaml must contain an object")
        return cls(path, schema, defaults)

    def strategy(self) -> SearchStrategy[dict[str, object]]:
        """
        Generate schema-valid overrides; Helm still merges chart defaults.

        Returns:
            SearchStrategy[dict[str, object]]: Result of the documented operation.
        """
        return schema_strategy(self.schema).map(mapping)


def merge_values(defaults: dict[str, object], overrides: dict[str, object]) -> dict[str, object]:
    """
    Model ordinary Helm map merging and null deletion for schema preflight.

    Helm is authoritative, especially for dependency coalescing and globals.

    Args:
        defaults (dict[str, object]): Existing chart defaults that take precedence during
            coalescing.
        overrides (dict[str, object]): Incoming Helm overrides, including null deletion markers.

    Returns:
        dict[str, object]: Resulting schema, values mapping, or structured report.
    """
    result = copy.deepcopy(defaults)
    for key, value in overrides.items():
        if value is None:
            result.pop(key, None)
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_values(mapping(result[key]), value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _schema_nodes(
    schema: object,
    path: tuple[str, ...],
    root: dict[str, object],
    seen: frozenset[tuple[int, tuple[str, ...]]] = frozenset(),
) -> list[dict[str, object]]:
    """
    Check  schema nodes.

    Args:
        schema (object): JSON Schema defining the accepted value domain.
        path (tuple[str, ...]): Value path or chart location to inspect.
        root (dict[str, object]): Root schema used to resolve local references.
        seen (frozenset[tuple[int, tuple[str, ...]]]): References already visited while resolving
            this schema.

    Returns:
        list[dict[str, object]]: Result of the documented operation.
    """
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
            target = mapping(target[part.replace("~1", "/").replace("~0", "~")])
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


def _default_paths(value: object, prefix: tuple[str, ...] = ()) -> Iterator[tuple[str, ...]]:
    """
    Check  default paths.

    Args:
        value (object): Candidate value supplied by the property strategy.
        prefix (tuple[str, ...]): Resolved parent path for the current value.

    Yields:
        tuple[str, ...]: Next value path in the document.
    """
    if isinstance(value, dict):
        for key, child in value.items():
            path = prefix + (str(key),)
            yield path
            yield from _default_paths(child, path)
    elif isinstance(value, list):
        for child in value:
            yield from _default_paths(child, prefix + ("*",))


def audit(chart: Chart) -> dict[str, object]:
    """
    Inventory schema, template, and default paths against the original values document.

    Args:
        chart (Chart): Loaded chart and its schema and defaults.

    Returns:
        dict[str, object]: Resulting schema, values mapping, or structured report.
    """
    from attrs import asdict

    from hypothesis_helm.charts.generate import enumerate_paths

    references, diagnostics = discover(chart.path)
    defaults = set(_default_paths(chart.defaults))
    declared = {entry.path: entry.schema for entry in enumerate_paths(chart.schema)}
    paths = defaults | {r.path for r in references if r.path} | declared.keys()
    findings = []
    for path in sorted(paths, key=repr):
        LOGGER.info("Auditing path %s", format_path(path))
        nodes = _schema_nodes(chart.schema, tuple(str(segment) for segment in path), chart.schema)
        if not nodes and path in declared:
            nodes = [declared[path]]
        locations = [asdict(r) for r in references if r.path == path]
        if not nodes:
            findings.append({"path": list(path), "issue": "undocumented", "references": locations})
        elif not any("type" in n or "enum" in n or "const" in n for n in nodes):
            findings.append({"path": list(path), "issue": "untyped", "references": locations})
        elif not any(n.get("description") for n in nodes):
            findings.append(
                {"path": list(path), "issue": "missing-description", "references": locations}
            )
        if not has_path(chart.defaults, path):
            findings.append(
                {
                    "path": list(path),
                    "issue": "no-default",
                    "references": locations,
                    "message": "Configurable field is absent from the original values.yaml",
                }
            )
    return {
        "chart": str(chart.path),
        "references": [asdict(r) for r in references],
        "findings": findings,
        "unresolved": [asdict(d) for d in diagnostics],
    }


class RenderFailure(AssertionError):
    """
    A reproducible values input failed the rendering contract.
    """


def validate_resources(resources: Sequence[object]) -> None:
    """
    Check resource envelopes; callers can add Kubernetes or domain validation.

    Args:
        resources (Sequence[object]): Rendered Kubernetes resource documents.

    Returns:
        None: None. The operation completes through its documented side effects.
    """
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
            validate_resources(sequence(resource["items"]))
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
    values: dict[str, object],
    *,
    helm: str = "helm",
    timeout: float = 30.0,
    release: str = "hypothesis",
    namespace: str = "default",
    kube_version: str | None = None,
) -> list[dict[str, object]]:
    """
    Render locally with Helm schema checks enabled and a subprocess deadline.

    Args:
        chart (Chart): Loaded chart and its schema and defaults.
        values (dict[str, object]): Values document used as the rendering baseline.
        helm (str): Helm executable used to render the chart.
        timeout (float): Maximum seconds allowed for each Helm invocation.
        release (str): Release name supplied to Helm.
        namespace (str): Release namespace supplied to Helm.
        kube_version (str | None): Optional Kubernetes capability version supplied to Helm.

    Returns:
        list[dict[str, object]]: Result of the documented operation.
    """
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
            resources = [item for item in yamlio.load_all(process.stdout) if item is not None]
        except YAMLError as exc:
            raise RenderFailure(f"invalid rendered YAML: {exc}") from exc
    for resource in resources:
        emit_manifest(resource)
    validate_resources(resources)
    try:
        validate(process.stdout, timeout)
    except AssertionError as exc:
        raise RenderFailure(str(exc)) from exc
    return [mapping(resource) for resource in resources]


def check_chart(
    chart: Chart | str | Path,
    *,
    max_examples: int = 100,
    random_seed: int = 0,
    timeout: float = 30.0,
    helm: str = "helm",
    release: str = "hypothesis",
    namespace: str = "default",
    kube_version: str | None = None,
    allow_empty: bool = False,
    artifact_dir: Path | None = None,
    exhaustive: bool = False,
    max_cases: int = 1000,
    properties: tuple[Callable[[list[dict[str, object]]], None], ...] = (),
) -> dict[str, object]:
    """
    Check defaults then generated overrides, shrinking failing inputs.

    Custom properties receive rendered resources and should raise AssertionError on
    failure. The report is evidence from a bounded sample, never a proof of totality.

    Args:
        chart (Chart | str | Path): Loaded chart and its schema and defaults.
        max_examples (int): Maximum number of generated examples per property.
        random_seed (int): Seed for reproducible property generation.
        timeout (float): Maximum seconds allowed for each Helm invocation.
        helm (str): Helm executable used to render the chart.
        release (str): Release name supplied to Helm.
        namespace (str): Release namespace supplied to Helm.
        kube_version (str | None): Optional Kubernetes capability version supplied to Helm.
        allow_empty (bool): Whether a render with no resource documents is accepted.
        artifact_dir (Path | None): Optional destination for failing values and report artifacts.
        exhaustive (bool): Whether to enumerate the entire supported finite input domain.
        max_cases (int): Maximum finite-domain size allowed before enumeration is refused.
        properties (tuple[Callable[[list[dict[str, object]]], None], ...]): Additional assertions
            over rendered resources.

    Returns:
        dict[str, object]: Resulting schema, values mapping, or structured report.
    """
    if not isinstance(chart, Chart):
        chart = Chart.load(chart)
    if max_examples < 1 or timeout <= 0:
        raise ValueError("max_examples and timeout must be positive")
    finite_values = enumerate_values(chart.schema, max_cases) if exhaustive else None
    count = 0
    last_failure = None

    def check(values: dict[str, object]) -> None:
        """
        Render one candidate and retain failure details for replay.

        Args:
            values (dict[str, object]): Values document used as the rendering baseline.

        Returns:
            None: None. The operation completes through its documented side effects.
        """
        nonlocal count, last_failure
        count += 1
        try:
            effective = merge_values(chart.defaults, values)
            validators.validator_for(chart.schema)(chart.schema).validate(json_value(effective))
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

    def save_failure(exc: Exception) -> dict[str, object]:
        """
        Persist the final counterexample and construct its failure report.

        Args:
            exc (Exception): Failure raised while checking or generating a chart input.

        Returns:
            dict[str, object]: Resulting schema, values mapping, or structured report.
        """
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
    def property_test(values: dict[str, object]) -> None:
        """
        Exercise a schema-generated candidate through the render contract.

        Args:
            values (dict[str, object]): Values document used as the rendering baseline.

        Returns:
            None: None. The operation completes through its documented side effects.
        """
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
