"""
Drive native Helm with Hypothesis-controlled randAlphaNum results and strict replay.
"""

import hashlib
import json
import time

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.builtins import EFFECTS
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.compiler.randomness.model import RandomInputs, RandomOutput
from hypothesis_helm.compiler.randomness.toolchain import build, identity
from hypothesis_helm.exceptions.rendering import RandomInputUnavailable, RenderFailure
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.findings.generator import FindingGenerator
from hypothesis_helm.schemas.configuration.settings import generation_settings, settings_at
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("enabled", "render")


def enabled(chart: Chart) -> bool:
    """
    Resolve the opt-in renderer mode through existing chart-specific configuration inheritance.

    Args:
        chart (Chart): Source chart whose root-level Hypothesis policy applies.

    Returns:
        bool: Whether this chart should expose randAlphaNum results as synthetic inputs.
    """
    # Saved suites retain their policy even when replayed outside the original checkout.
    generation = chart.domains.generation if chart.domains is not None else generation_settings(chart.path)
    return mapping(settings_at(generation, ()).get("hypothesis", {})).get("random_inputs", False) is True


def render(
    chart: Chart,
    values: dict[str, object],
    case: RandomInputs,
    *,
    timeout: float,
    release: str,
    namespace: str,
    kube_version: str | None,
    processes: Processes | None = None,
) -> str:
    """
    Extend a replay prefix until native Helm completes or reaches a real chart failure.

    Args:
        chart (Chart): Unmodified chart with its prepared dependency artifacts.
        values (dict[str, object]): Ordinary overrides, without synthetic keys.
        case (RandomInputs): Hypothesis draws or strict saved replay.
        timeout (float): Total execution budget across all prefix renders.
        release (str): Helm release name.
        namespace (str): Helm release namespace.
        kube_version (str | None): Optional Kubernetes capability version.
        processes (Processes | None): Parent owner used for cancellation and joining.

    Returns:
        str: Rendered manifests from the pinned Helm SDK.
    """
    binary = build()
    limits = active_limits(chart.path)
    case.records.clear()
    deadline = time.monotonic() + timeout
    payload: dict[str, object] = {
        "chart": str(chart.path),
        "values": json.loads(yamlio.json_for_helm(values)),
        "release": release,
        "namespace": namespace,
        "kube_version": kube_version or "",
        "max_chars": limits["max_string_chars"],
        "max_calls": limits["max_steps"],
        "draws": case.records,
        "unsupported": sorted((EFFECTS["randomness"] | EFFECTS["clock-or-timezone"]) - {"randAlphaNum", "getHostByName"}),
    }
    owner = processes if processes is not None else Processes()
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RenderFailure(f"random-input renderer exceeded {timeout}s", "HH1201")
        process = owner.run([str(binary)], input=json.dumps(payload), capture_output=True, timeout=remaining, check=True)
        response = mapping(json.loads(process.stdout))
        case.context = {
            "source_digest": identity(),
            "chart_digest": response.get("chart_digest"),
            "values_digest": hashlib.sha256(yamlio.json_for_helm(values).encode()).hexdigest(),
            "release": release,
            "namespace": namespace,
            "kube_version": kube_version,
        }
        if case.expected_context is not None and case.context != case.expected_context:
            raise RandomInputUnavailable("Random replay chart, values, renderer or release context changed")
        if response.get("invalid"):
            # A bad tape or exhausted instrumentation budget is not a chart defect.
            raise RandomInputUnavailable(str(response["invalid"]))
        if response.get("request"):
            case.next(mapping(response["request"]))
            continue
        if case.replay is not None and len(case.records) != len(case.replay):
            raise RandomInputUnavailable("Random replay contains unused draws")
        if response.get("error"):
            finding = FindingGenerator.helm(str(response["error"]))
            failure = RenderFailure(finding.evidence, finding.rule.code)
            failure.random_inputs = case.document()
            raise failure
        return RandomOutput(str(response.get("output", "")), case.document())
