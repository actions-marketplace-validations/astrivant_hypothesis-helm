"""
Render Helm charts and validate complete manifest bundles.
"""

from __future__ import annotations

import json
import logging
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.values import parsers as manifest_parsers
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.environment import env
from hypothesis_helm.exceptions.rendering import ManifestParseError, RenderFailure
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.execution.state.render_hashes import RenderHashes, process_hashes
from hypothesis_helm.findings.generator import FindingGenerator
from hypothesis_helm.findings.policy import RuleScope
from hypothesis_helm.reporting.console.output import emit_manifest
from hypothesis_helm.rules import check, effective_ignored_codes, ignored
from hypothesis_helm.schemas.contracts import (
    mapping,
    sequence,
)
from hypothesis_helm.schemas.kubernetes.conformity import ENVIRONMENT, validate
from hypothesis_helm.schemas.kubernetes.resources import resource_schemas

__all__ = ("render", "render_output", "validate_resources")


LOGGER = logging.getLogger(__name__)


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
            check(False, "HH1102", "rendered document is not an object")
            continue
        for key in ("apiVersion", "kind"):
            if not isinstance(resource.get(key), str) or not resource[key]:
                check(False, "HH1103", f"resource has no nonempty {key}")
        if resource.get("kind") == "List":
            if not isinstance(resource.get("items"), list):
                check(False, "HH1104", "List resource has no items array")
                continue
            validate_resources(sequence(resource["items"]))
            continue
        metadata = resource.get("metadata")
        if not isinstance(metadata, dict) or not isinstance(metadata.get("name"), str) or not metadata["name"]:
            check(False, "HH1105", "resource has no metadata.name")
            continue
        identity = (
            resource.get("apiVersion"),
            resource.get("kind"),
            metadata.get("namespace"),
            metadata["name"],
        )
        if identity in identities:
            check(False, "HH1106", f"duplicate resource: {identity}")
        identities.add(identity)
        if not ignored("HH1108"):
            from jsonschema.exceptions import ValidationError

            from hypothesis_helm.schemas.kubernetes.resources import validate_custom

            try:
                validate_custom(resource)
            except (ValueError, ValidationError) as exc:
                check(False, "HH1108", str(exc))


def render_output(
    chart: Chart,
    values: dict[str, object],
    *,
    helm: str = "helm",
    timeout: float = 30.0,
    release: str = "hypothesis",
    namespace: str = "default",
    kube_version: str | None = None,
    processes: Processes | None = None,
) -> str:
    """
    Execute Helm and retain raw output for validation by the owning coordinator.

    Args:
        chart (Chart): Prepared chart with dependencies available.
        values (dict[str, object]): Overrides for this input.
        helm (str): Helm executable.
        timeout (float): Maximum subprocess duration.
        release (str): Fixed release name.
        namespace (str): Fixed namespace.
        kube_version (str | None): Optional Kubernetes capability version.
        processes (Processes | None): Explicit subprocess owner for parallel cancellation.

    Returns:
        str: Unvalidated rendered YAML; nonzero Helm exits remain reproducible failures.
    """
    chart.require_source()
    from hypothesis_helm.compiler.randomness import rendering as random_rendering
    from hypothesis_helm.compiler.randomness.model import CURRENT, RandomInputs

    random_case = CURRENT.get()
    if random_case is not None or random_rendering.enabled(chart):
        try:
            return random_rendering.render(
                chart,
                values,
                random_case if random_case is not None else RandomInputs(),
                timeout=timeout,
                release=release,
                namespace=namespace,
                kube_version=kube_version,
                processes=processes,
            )
        except subprocess.TimeoutExpired as exc:
            raise RenderFailure(f"random-input renderer exceeded {timeout}s", "HH1201") from exc
    with tempfile.TemporaryDirectory(prefix="hypothesis-helm-") as directory:
        value_file = Path(directory) / "values.json"
        value_file.write_text(yamlio.json_for_helm(values), encoding="utf-8")
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
            process = (processes if processes is not None else Processes()).run(command, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise RenderFailure(f"helm exceeded {timeout}s", "HH1201") from exc
        if process.returncode:
            # The source can disappear after dispatch. Do not classify that race
            # as a template defect or feed it back into Hypothesis shrinking.
            chart.require_source()
            finding = FindingGenerator.helm(process.stderr.strip() or f"helm exited {process.returncode}")
            raise RenderFailure(finding.evidence, finding.rule.code)
        return process.stdout


def _render(
    chart: Chart,
    values: dict[str, object],
    *,
    helm: str = "helm",
    timeout: float = 30.0,
    release: str = "hypothesis",
    namespace: str = "default",
    kube_version: str | None = None,
    hashes: RenderHashes | None = None,
    stream: bool = True,
    rendered_output: str | None = None,
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

        hashes (RenderHashes | None): Run index, or the current process index by default.
        stream (bool): Emit manifests to the configured output stream.
        rendered_output (str | None): Exact output prefetched for these values, or execute Helm when absent.

    Returns:
        list[dict[str, object]]: Result of the documented operation.
    """
    with RuleScope.for_values(chart, values):
        output = (
            rendered_output
            if rendered_output is not None
            else render_output(
                chart,
                values,
                helm=helm,
                timeout=timeout,
                release=release,
                namespace=namespace,
                kube_version=kube_version,
            )
        )
        try:
            resources = [item for item in yamlio.load_all(output) if item is not None]
        except ManifestParseError as exc:
            raise RenderFailure(f"invalid rendered YAML: {exc}", "HH1101") from exc
        if stream:
            for resource in resources:
                emit_manifest(resource)

        def validate_bundle() -> None:
            """
            Validate the complete output before committing a successful cache entry.

            Returns:
                None: Manifest checks pass or their failure propagates.
            """
            validate_resources(resources)
            try:
                validate(resources, timeout)
            except AssertionError as exc:
                raise RenderFailure(str(exc), "HH1108") from exc

        context = json.dumps(
            {
                "resource_contract": 1,
                "yaml_parser": manifest_parsers.identity(),
                "conformity": env.get(ENVIRONMENT),
                "timeout": timeout,
                "ignored_rules": effective_ignored_codes(),
                "input_policy": env.get("HYPOTHESIS_HELM_INPUT_POLICY", "{}"),
                "resource_schemas": resource_schemas(),
            },
            sort_keys=True,
        )
        try:
            (hashes if hashes is not None else process_hashes()).check(resources, context, validate_bundle)
        except RenderFailure as exc:
            exc.resources = resources
            raise
        except (TypeError, ValueError) as exc:
            failure = RenderFailure(f"invalid rendered manifest: {exc}", "HH1011")
            failure.resources = resources
            raise failure from exc
        return [mapping(resource) for resource in resources if isinstance(resource, dict)]


def render(
    chart: Chart,
    values: dict[str, object],
    *,
    helm: str = "helm",
    timeout: float = 30.0,
    release: str = "hypothesis",
    namespace: str = "default",
    kube_version: str | None = None,
    hashes: RenderHashes | None = None,
    stream: bool = True,
    rendered_output: str | None = None,
) -> list[dict[str, object]]:
    """
    Validate native output while retaining synthetic draws if any validation step fails.

    Args:
        chart (Chart): Source chart with prepared dependencies.
        values (dict[str, object]): Ordinary values overrides.
        helm (str): Native Helm executable outside synthetic-input mode.
        timeout (float): Total render deadline.
        release (str): Helm release name.
        namespace (str): Helm release namespace.
        kube_version (str | None): Kubernetes capability version.
        hashes (RenderHashes | None): Run-local manifest validation cache.
        stream (bool): Emit rendered resources to the requested output stream.
        rendered_output (str | None): Already rendered output from a parallel worker.

    Returns:
        list[dict[str, object]]: Validated manifest bundle.
    """
    from contextlib import nullcontext

    from hypothesis_helm.compiler.randomness.model import CURRENT, RandomInputs
    from hypothesis_helm.compiler.randomness.rendering import enabled

    scope = RandomInputs() if CURRENT.get() is None and enabled(chart) else nullcontext()
    with scope:
        return _render(
            chart,
            values,
            helm=helm,
            timeout=timeout,
            release=release,
            namespace=namespace,
            kube_version=kube_version,
            hashes=hashes,
            stream=stream,
            rendered_output=rendered_output,
        )
