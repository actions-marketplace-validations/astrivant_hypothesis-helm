"""
Verify the complete builtin inventory and conservative behavior at native-effect boundaries.
"""

import json
import shutil
import subprocess
from importlib.resources import files
from pathlib import Path
from textwrap import dedent

import pytest

from hypothesis_helm.charts.inspection.templates import discover
from hypothesis_helm.charts.model import Chart
from hypothesis_helm.charts.testing.rendering import render
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler import builtins
from hypothesis_helm.compiler.asts.contracts import Contracts, context_effects
from hypothesis_helm.compiler.asts.origins import Dictionary, Literal, Sequence, paths
from hypothesis_helm.compiler.asts.renderer import RendererContext
from hypothesis_helm.compiler.asts.templates import lower
from hypothesis_helm.compiler.passes.discovery_flow import iterations
from hypothesis_helm.compiler.passes.discovery_functions import result
from hypothesis_helm.schemas.contracts import mapping, sequence
from hypothesis_helm.tests.compiler.test_templates import scan


def test_inventory_covers_every_upstream_entry() -> None:
    """
    Require generated definitions for all pinned engine functions and every detected effect alias.

    Returns:
        None: Generated definitions, source hashes and compiler specifications agree exactly.
    """
    snapshot = mapping(json.loads(files("hypothesis_helm.compiler.assets").joinpath("builtin_inventory.json").read_text(encoding="utf-8")))
    names = set(mapping(snapshot["functions"]))
    assert snapshot["format"] == 2
    assert all(mapping(source)["files"] and mapping(source)["sha256"] for source in sequence(snapshot["sources"]))
    assert names == builtins.BUILTINS.keys()
    assert len(names) == 251
    assert set().union(*builtins.EFFECTS.values()) <= names
    assert {"env", "expandenv", "template", "block"}.isdisjoint(names)
    assert all(spec.meaning and spec.shape and spec.provider for spec in builtins.BUILTINS.values())
    assert result("aFutureUnreviewedFunction", [Literal("example")]) is None


@pytest.mark.parametrize(
    ("expression", "reason"),
    [
        ("randAlphaNum 8", "--renderer-policy auto or strict supports sampling and replay"),
        ("randAlpha 8", "randomness"),
        ("now", "clock or timezone"),
    ],
)
def test_runtime_effects_explain_static_analysis_limits(tmp_path: Path, expression: str, reason: str) -> None:
    """
    Identify supported native effects without assigning a sampled result to a rejection guard.

    Args:
        tmp_path (Path): Template-only chart containing a runtime-dependent condition.
        expression (str): Call or zero-argument builtin controlling rejection.
        reason (str): Explanation expected from the pinned effect inventory.

    Returns:
        None: Analysis retains the candidate, deduplicates its warning and explains the runtime dependency.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/runtime.yaml").write_text("{{ if " + expression + ' }}{{ fail "runtime-dependent failure" }}{{ end }}')
    contracts = Contracts.build(tmp_path)
    assert contracts.predict({}) is None
    assert contracts.predict({}) is None
    assert len(contracts.fallbacks) == 1
    diagnostic = contracts.fallbacks[0]
    assert diagnostic["code"] == "HH2007"
    assert reason in str(diagnostic["reason"])
    assert "unsupported function" not in str(diagnostic["reason"])
    assert "unsupported expression" not in str(diagnostic["reason"])
    assert builtins.runtime_dependency("unregisteredFunction") is None
    assert builtins.runtime_dependency("upper") is None


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_pinned_functions_are_recognized_by_native_helm(tmp_path: Path) -> None:
    """
    Ask the pinned native parser to resolve every function without executing expensive operations.

    Args:
        tmp_path (Path): Isolated inventory probe chart.

    Returns:
        None: All 251 names parse, including Helm overrides and same-line Sprig aliases.
    """
    version = subprocess.run(["helm", "version", "--short"], check=True, capture_output=True, text=True).stdout
    if not version.startswith("v4.3."):
        pytest.skip("the complete source inventory is pinned to Helm 4.3")
    (tmp_path / "templates").mkdir()
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "builtins", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text("{}\n")
    body = "{{ if false }}" + "".join("{{ " + name + " }}" for name in sorted(builtins.BUILTINS)) + "{{ end }}"
    (tmp_path / "templates/probe.yaml").write_text(
        body
        + dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: probe
        """)
    )
    assert render(Chart(tmp_path, {"type": "object"}, {}), {})[0]["kind"] == "ConfigMap"


@pytest.mark.parametrize("function", sorted(builtins.MUTATIONS | {"call"}))
@pytest.mark.parametrize("block", [False, True])
def test_mutation_aliases_are_barriers_inside_conditions(function: str, block: bool) -> None:
    """
    Detect writes inside conditional pipelines as well as standalone assignments.

    Args:
        function (str): Mutating or dynamically dispatched function.
        block (bool): Whether the function occurs in a condition.

    Returns:
        None: Every form blocks using stale facts to predict a later rejection.
    """
    expression = function + ' .Values "key" true'
    source = "{{ if " + expression + " }}literal{{ end }}" if block else "{{ $_ := " + expression + " }}"
    assert context_effects(lower(source))


@pytest.mark.parametrize("function", ["shuffle", "randInt", "encryptAES", "htpasswd", "getHostByName", "genCAWithKey", "keys"])
def test_effectful_calls_remain_visible(tmp_path: Path, function: str) -> None:
    """
    Retain input-controlled branches and diagnostics for previously unclassified effects.

    Args:
        tmp_path (Path): Isolated discovery-only fixture.
        function (str): Function with randomness, external state, or unspecified ordering.

    Returns:
        None: Neither return-shape tracking nor builtin recognition proves branch truth.
    """
    refs, diagnostics = scan(
        tmp_path,
        "{{ $value := " + function + " .Values.source }}{{ if .Values.enabled }}{{ .Values.left }}{{ else }}{{ .Values.right }}{{ end }}",
    )
    assert {("source",), ("left",), ("right",)} <= {item.path for item in refs}
    assert any(function in item.message and "Helm" in item.message for item in diagnostics)
    assert function in builtins.NATIVE_STATE


def test_collection_shapes_preserve_members_and_map_iteration_order() -> None:
    """
    Respect lexical map-key order and preserve origins through concatenation and aliases.

    Returns:
        None: Map key ten precedes key two, and uncertain lists never become exact enumerations.
    """
    split = result("split", [Literal("."), Literal(".".join(str(i) for i in range(12)))])
    members = iterations(split)
    assert members is not None
    assert [item.value for _, item in members if isinstance(item, Literal)][:5] == ["0", "1", "10", "11", "2"]
    assert result("splitn", [Literal("."), Literal(2), Literal("a.b.c")]) == Dictionary({"_0": Literal("a"), "_1": Literal("b.c")})
    assert result("splitn", [Literal(""), Literal(1), Literal("abc")]) == Dictionary({"_0": Literal("abc")})
    assert result("splitn", [Literal("."), Literal(0), Literal("a.b")]) == Dictionary({})
    source = Sequence((("Values", "first"),))
    combined = result("concat", [source, Sequence((("Values", "second"),))])
    assert paths(combined) == (("Values", "first"), ("Values", "second"))
    assert result("mustPush", [source, Literal("last")]) == result("append", [source, Literal("last")])
    assert iterations(result("concat", [source, None])) is None


def test_compact_control_flow_and_scalar_helper_arguments(tmp_path: Path) -> None:
    """
    Lower Go's compact block syntax and trace scalar helper dependencies without false context errors.

    Args:
        tmp_path (Path): Chart containing adjacent field expressions and a scalar helper.

    Returns:
        None: Both compiler trees retain control structure and scalar arguments retain their inputs.
    """
    source = dedent("""
        {{ define "label" }}{{ . | upper }}{{ end }}
        {{ if.Values.enabled }}{{ include "label" (printf "%s" .Values.name) }}
        {{ else if.Values.alternative }}{{ with.Values.other }}{{ .name }}{{ end }}{{ end }}
        """)
    refs, diagnostics = scan(tmp_path, source)
    assert not diagnostics
    assert {("name",), ("other", "name")} <= {item.path for item in refs}
    nodes = lower("{{ if.Values.enabled }}yes{{ else if.Values.alternative }}other{{ end }}")
    assert nodes[1].kind == "if" and nodes[1].text == ".Values.enabled"
    assert nodes[1].otherwise[0].text == ".Values.alternative"


@pytest.mark.parametrize("offline", [False, True])
def test_lookup_requires_an_explicit_offline_contract(tmp_path: Path, offline: bool) -> None:
    """
    Use empty lookups only when execution settings guarantee no Kubernetes connection.

    Args:
        tmp_path (Path): Chart whose rejection depends on an absent resource.
        offline (bool): Whether the renderer explicitly has no cluster connection.

    Returns:
        None: Online lookup stays unknown; offline lookup permits a context-dependent prediction.
    """
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/probe.yaml").write_text(
        '{{ if not (lookup "v1" "Secret" "default" "example") }}{{ fail "secret absent" }}{{ end }}'
    )
    contracts = Contracts.build(tmp_path)
    contracts.renderer = RendererContext(tmp_path, offline=offline)
    rejection = contracts.predict({})
    assert (rejection is not None) is offline
    if offline:
        assert rejection is not None and rejection.contextual
        assert not contracts.fallbacks
    else:
        assert contracts.fallbacks


def test_malformed_helper_dictionary_remains_a_finding(tmp_path: Path) -> None:
    """
    Explain an odd helper dictionary without disguising it as a compiler limitation alone.

    Args:
        tmp_path (Path): Chart with the malformed multi-map helper call found in Airflow.

    Returns:
        None: Findings identify Helm's implicit empty value and retain all supplied inputs.
    """
    refs, diagnostics = scan(
        tmp_path,
        '{{ define "merge" }}{{ range .values }}{{ . }}{{ end }}{{ end }}'
        '{{ include "merge" (dict "values" .Values.first .Values.second "context" .) }}',
    )
    assert {("first",), ("second",)} <= {item.path for item in refs}
    assert any("unpaired key" in item.message for item in diagnostics)


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
def test_offline_discovery_matches_native_lookup_and_dns(tmp_path: Path) -> None:
    """
    Match the tool's actual renderer mode while leaving standalone discovery conservative.

    Args:
        tmp_path (Path): Isolated chart using both optional external integrations.

    Returns:
        None: Offline branches match Helm and input arguments remain in the discovered surface.
    """
    defaults: dict[str, object] = {"name": "example", "offline": "local", "online": "cluster"}
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "offline", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text(yamlio.dump(defaults))
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/result.yaml").write_text(
        dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: example
        data:
          value: {{ if lookup "v1" "Secret" "default" .Values.name }}{{ .Values.online }}{{ else }}{{ .Values.offline }}{{ end }}
          dns: {{ getHostByName "does-not-exist.invalid" | quote }}
        """)
    )
    generic_refs, generic_diagnostics = discover(tmp_path)
    assert ("online",) in {ref.path for ref in generic_refs}
    assert generic_diagnostics
    refs, diagnostics = discover(tmp_path, offline=True)
    assert not diagnostics
    assert {ref.path for ref in refs} == {("name",), ("offline",)}
    output = render(Chart(tmp_path, {"type": "object"}, defaults), {})
    assert mapping(output[0]["data"]) == {"value": "local", "dns": ""}


@pytest.mark.skipif(shutil.which("helm") is None, reason="requires Helm")
@pytest.mark.parametrize("function", ["mergeOverwrite", "mustMergeOverwrite"])
def test_conditional_writes_cannot_produce_a_false_rejection(tmp_path: Path, function: str) -> None:
    """
    Prevent an apparently irrelevant condition from hiding writes before a rejection guard.

    Args:
        tmp_path (Path): Isolated chart that becomes valid through a conditional map write.
        function (str): Native map update or its error-propagating alias.

    Returns:
        None: Helm succeeds and the compiler follows the owned map's updated value without uncertainty.
    """
    (tmp_path / "Chart.yaml").write_text(yamlio.dump({"apiVersion": "v2", "name": "mutation", "version": "1.0.0"}))
    (tmp_path / "values.yaml").write_text("{}\n")
    (tmp_path / "templates").mkdir()
    body = (
        '{{ $ctx := dict "valid" false }}{{ if ' + function + ' $ctx (dict "valid" true) }}{{ end }}'
        '{{ if not $ctx.valid }}{{ fail "invalid context" }}{{ end }}'
    )
    (tmp_path / "templates/result.yaml").write_text(
        body
        + dedent("""
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: example
        """)
    )
    contracts = Contracts.build(tmp_path)
    assert contracts.predict({}) is None
    assert not contracts.fallbacks
    assert render(Chart(tmp_path, {"type": "object"}, {}), {})[0]["kind"] == "ConfigMap"
