"""
Select controlled execution without confusing native fallback with a replay proof.
"""

import re
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

from hypothesis_helm.charts.model import Chart
from hypothesis_helm.compiler.asts.actions import TOKEN
from hypothesis_helm.compiler.asts.templates import lower, walk
from hypothesis_helm.compiler.builtins import EFFECTS
from hypothesis_helm.compiler.passes.dependencies import Dependencies
from hypothesis_helm.compiler.randomness.toolchain import SOURCE, build, identity
from hypothesis_helm.exceptions.rendering import RendererUnavailable
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.schemas.configuration.settings import generation_settings, settings_at
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("enabled", "policy", "prepare", "compatible", "SDK_VERSION", "observed")

_SDK_MATCH = re.search(r"helm.sh/helm/v4 v([^\s]+)", (SOURCE / "go.mod").read_text())
assert _SDK_MATCH is not None
SDK_VERSION = _SDK_MATCH[1]


def policy(chart: Chart) -> str:
    """
    Resolve the chart-wide execution policy, including saved-suite configuration.

    Args:
        chart (Chart): Chart whose generation settings apply.

    Returns:
        str: Auto, native or strict execution policy.
    """
    generation = chart.domains.generation if chart.domains is not None else generation_settings(chart.path)
    return str(mapping(settings_at(generation, ()).get("hypothesis", {})).get("renderer_policy", "auto"))


def enabled(chart: Chart) -> bool:
    """
    Inspect potential runtime effects once per prepared chart, including dependency templates.

    Args:
        chart (Chart): Immutable prepared chart used by this test job.

    Returns:
        bool: Whether controlled rendering and its synthetic property are applicable.
    """
    mode = policy(chart)
    if mode == "native":
        return False
    if mode == "strict":
        return True
    if chart.renderer_effects is None:
        effects = EFFECTS["randomness"] | EFFECTS["clock-or-timezone"] | EFFECTS["external-state"] | {"tpl"}
        try:
            dependencies = chart.dependency_model or Dependencies.build(chart.path)
            chart.dependency_model = dependencies
            trees = [lower(path.read_text()) for path in sorted((chart.path / "templates").rglob("*")) if path.is_file()]
            trees.extend(nodes for dependency in dependencies.nodes for _, nodes in dependency.syntax)
            # Unknown sources and dynamic tpl may conceal calls; absence is only established for inspected source.
            chart.renderer_effects = bool(dependencies.diagnostics) or any(
                effects.intersection(TOKEN.findall(node.text)) for tree in trees for node in walk(tree) if node.kind != "text"
            )
        except (OSError, ValueError, UnicodeError, RecursionError):
            chart.renderer_effects = True
    return chart.renderer_effects


@lru_cache(maxsize=64)
def _version(binary: str, modified: int, size: int, timeout: float) -> str:
    """
    Probe a resolved Helm executable once per file identity.

    Args:
        binary (str): Absolute executable filename.
        modified (int): Modification timestamp invalidating a replaced executable.
        size (int): File size used with the timestamp.
        timeout (float): Probe budget, capped by the active render deadline.

    Returns:
        str: Helm's semantic version, including any prerelease suffix.
    """
    result = Processes().run([binary, "version", "--template", "{{.Version}}"], capture_output=True, check=True, timeout=timeout)
    return result.stdout.strip().removeprefix("v").split("+", 1)[0]


def compatible(helm: str, *, timeout: float = 5) -> None:
    """
    Require the reviewed SDK version before replacing the user's selected Helm binary.

    Args:
        helm (str): Configured native Helm command.
        timeout (float): Remaining render budget for an uncached version probe.

    Returns:
        None: The selected executable matches the pinned SDK version.

    Raises:
        RendererUnavailable: The executable is unavailable, unidentifiable or incompatible.
    """
    try:
        binary = shutil.which(helm)
        if binary is None:
            raise RendererUnavailable(f"Helm executable unavailable: {helm}")
        stat = Path(binary).stat()
        version = _version(binary, stat.st_mtime_ns, stat.st_size, min(5, timeout))
    except (OSError, subprocess.SubprocessError) as exc:
        raise RendererUnavailable(f"Cannot establish Helm compatibility: {helm}") from exc
    if version != SDK_VERSION:
        raise RendererUnavailable(f"Selected Helm {version} differs from controlled renderer {SDK_VERSION}")


def prepare(chart: Chart, helm: str = "helm") -> Path | None:
    """
    Find a prepared renderer; automatic runs never compile tools inside a chart's time budget.

    Args:
        chart (Chart): Chart with inherited execution policy.
        helm (str): Configured Helm executable to compare with the SDK.

    Returns:
        Path | None: Compatible renderer, or None when automatic mode must use native Helm.

    Raises:
        RendererUnavailable: Strict execution cannot provide its required renderer.
    """
    if not enabled(chart):
        return None
    try:
        compatible(helm)
        binary = Path(".cache/random-renderer").resolve() / identity() / "renderer"
        if not binary.is_file():
            if policy(chart) == "strict":
                return build()
            raise RendererUnavailable("Controlled renderer is not built; run hypothesis-helm-renderer --build")
        return binary
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        if policy(chart) == "strict":
            raise RendererUnavailable(str(exc)) from exc
        return None


def observed(chart: Chart, document: dict[str, object]) -> None:
    """
    Count actual renderer outcomes, separating native fallbacks from controlled samples.

    Args:
        chart (Chart): Job whose report owns these counters.
        document (dict[str, object]): Executed output's provenance, never the aborted controlled attempt.

    Returns:
        None: Report counters retain fallback reasons without claiming random-space coverage.
    """
    key = "native_renders" if document.get("replayable") is False else "controlled_renders"
    chart.renderer_statistics[key] = int(str(chart.renderer_statistics.get(key, 0))) + 1
    reason = document.get("fallback_reason")
    if reason is not None:
        reasons = mapping(chart.renderer_statistics.setdefault("fallback_reasons", {}))
        reasons[str(reason)] = int(str(reasons.get(str(reason), 0))) + 1
        chart.renderer_statistics["fallback_reasons"] = reasons
