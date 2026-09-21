"""
Drive a single native Helm render with Hypothesis-controlled draws and strict replay.
"""

import hashlib
import json
import time
from pathlib import Path

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.builtins import EFFECTS
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.compiler.randomness.model import RandomInputs, RandomOutput
from hypothesis_helm.compiler.randomness.policy import compatible, enabled, observed, policy
from hypothesis_helm.compiler.randomness.protocol import exchange
from hypothesis_helm.compiler.randomness.toolchain import build, identity
from hypothesis_helm.exceptions.rendering import RandomInputUnavailable, RendererUnavailable, RenderFailure
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.findings.generator import FindingGenerator
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("enabled", "render")


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
    helm: str = "helm",
) -> str:
    """
    Execute Helm once, requesting each draw only when native control flow reaches its call.

    Args:
        chart (Chart): Unmodified chart with its prepared dependency artifacts.
        values (dict[str, object]): Ordinary overrides, without synthetic keys.
        case (RandomInputs): Hypothesis draws or strict saved replay.
        timeout (float): Total execution budget across all draw exchanges.
        release (str): Helm release name.
        namespace (str): Helm release namespace.
        kube_version (str | None): Optional Kubernetes capability version.
        processes (Processes | None): Parent owner used for cancellation and joining.
        helm (str): Selected native Helm executable whose version must match the SDK.

    Returns:
        str: Rendered manifests with replay provenance from the pinned Helm SDK.
    """
    deadline = time.monotonic() + timeout
    compatible(helm, timeout=timeout)
    binary = Path(".cache/random-renderer").resolve() / identity() / "renderer"
    if not binary.is_file() and (policy(chart) == "strict" or case.replay is not None):
        binary = build()
    if not binary.is_file():
        raise RendererUnavailable("Controlled renderer is not prepared; run hypothesis-helm-renderer --build")
    limits = active_limits(chart.path)
    case.records.clear()
    case.context.clear()
    case.fallback_reason = None
    payload: dict[str, object] = {
        "chart": str(chart.path),
        "values": json.loads(yamlio.json_for_helm(values)),
        "release": release,
        "namespace": namespace,
        "kube_version": kube_version or "",
        "max_chars": limits["max_string_chars"],
        "max_calls": limits["max_steps"],
        # Even effects with no supplied random values must be stopped before a tape can claim replayability.
        "unsupported": sorted((EFFECTS["randomness"] | EFFECTS["clock-or-timezone"] | EFFECTS["external-state"]) - {"randAlphaNum"}),
    }
    context: dict[str, object] = {
        "source_digest": identity(),
        "values_digest": hashlib.sha256(yamlio.json_for_helm(values).encode()).hexdigest(),
        "release": release,
        "namespace": namespace,
        "kube_version": kube_version,
    }

    def receive(response: dict[str, object]) -> dict[str, object] | None:
        """
        Validate provenance before drawing, and reject effects that cannot be replayed.

        Args:
            response (dict[str, object]): Native renderer's next protocol frame.

        Returns:
            dict[str, object] | None: A draw reply, or None for an identity or final frame.
        """
        if response.get("ready"):
            case.context = {**context, "chart_digest": response["chart_digest"]}
            if case.expected_context is not None and case.context != case.expected_context:
                raise RandomInputUnavailable("Random replay chart, values, renderer or release context changed")
        elif response.get("request"):
            if not case.context:
                raise RandomInputUnavailable("Controlled renderer requested input before source verification")
            return case.next(mapping(response["request"]))
        return None

    owner = processes if processes is not None else Processes()
    process = owner.run(
        [str(binary)],
        exchange=lambda child: exchange(child, payload, receive, deadline),
        timeout=max(0, deadline - time.monotonic()),
        check=True,
    )
    response = mapping(json.loads(process.stdout))
    if response.get("invalid"):
        raise RandomInputUnavailable(str(response["invalid"]))
    if response.get("unavailable"):
        raise RendererUnavailable(str(response["unavailable"]))
    if case.replay is not None and len(case.records) != len(case.replay):
        raise RandomInputUnavailable("Random replay contains unused draws")
    observed(chart, case.document())
    if response.get("error"):
        finding = FindingGenerator.helm(str(response["error"]))
        failure = RenderFailure(finding.evidence, finding.rule.code)
        failure.random_inputs = case.document()
        raise failure
    return RandomOutput(str(response.get("output", "")), case.document())
