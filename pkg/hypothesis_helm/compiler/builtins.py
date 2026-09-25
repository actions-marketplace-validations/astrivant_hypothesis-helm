"""
Load source-derived facts for the pinned Helm, Sprig and Go template engines.

Effects describe analysis barriers, not a promise to evaluate every function in Python.
Unresolved source calls remain explicit. Concrete semantics belong to individual passes.
"""

import json
from importlib.resources import files

from attrs import frozen

from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = (
    "BUILTINS",
    "Builtin",
    "EFFECTS",
    "MUTATIONS",
    "NATIVE_STATE",
    "UNRESOLVED_EFFECTS",
    "inventory",
    "reference",
    "runtime_dependency",
)


@frozen
class Builtin:
    """
    Describe a function's output family and effects independently of exact evaluation.

    Attributes:
        name (str): Template function identifier.
        provider (str): Pinned source that supplies or overrides the function.
        meaning (str): Implementation identity extracted from upstream source.
        shape (str): Result family derived from the upstream Go return declaration.
        effects (frozenset[str]): Detected effects; an empty set does not prove purity.
        signature (str): Upstream declaration, if resolved within the provider package.
        fields (tuple[str, ...]): Exported fields of a locally declared record result.
        unresolved (tuple[str, ...]): Calls and writes requiring further semantic analysis.
        source (str): Provider-relative source filename.
        line (int): One-based source declaration line.
    """

    name: str
    provider: str
    meaning: str
    shape: str
    effects: frozenset[str]
    signature: str
    fields: tuple[str, ...]
    unresolved: tuple[str, ...]
    source: str
    line: int


def inventory() -> dict[str, Builtin]:
    """
    Load generated source facts, rejecting obsolete or incomplete inventory formats.

    Returns:
        dict[str, Builtin]: Pinned function registry with explicit analysis boundaries.

    Raises:
        ValueError: The source inventory format is unsupported or lacks provenance.
    """
    snapshot = mapping(json.loads(files("hypothesis_helm.compiler.assets").joinpath("builtin_inventory.json").read_text(encoding="utf-8")))
    if snapshot.get("format") != 2 or not snapshot.get("sources") or not snapshot.get("extractor_sha256"):
        raise ValueError("Rebuild the compiler inventory with hypothesis-helm-builtins")
    result: dict[str, Builtin] = {}
    for name, raw in mapping(snapshot["functions"]).items():
        record = mapping(raw)
        result[name] = Builtin(
            name=name,
            provider=str(record["provider"]),
            meaning="Upstream implementation: " + str(record["implementation"]),
            shape=str(record["shape"]),
            effects=frozenset(str(effect) for effect in sequence(record["effects"])),
            signature=str(record["signature"]),
            fields=tuple(str(field) for field in sequence(record["fields"])),
            unresolved=tuple(str(call) for call in sequence(record["unresolved"])),
            source=str(record["source"]),
            line=int(str(record["line"])),
        )
    return result


# These sets are derived from pinned upstream facts, unlike the implementation families in constants.py.
BUILTINS = inventory()
EFFECTS = {
    effect: frozenset(name for name, spec in BUILTINS.items() if effect in spec.effects)
    for effect in {effect for spec in BUILTINS.values() for effect in spec.effects}
}
UNRESOLVED_EFFECTS = frozenset(name for name, spec in BUILTINS.items() if spec.unresolved)
MUTATIONS = EFFECTS["mutation"]
NATIVE_STATE = frozenset.union(*(members for effect, members in EFFECTS.items() if effect not in {"mutation", "rejection", "dynamic-code"}))


def runtime_dependency(name: str) -> str | None:
    """
    Explain recognized runtime effects separately from missing function implementations.

    Args:
        name (str): Function whose result the static evaluator cannot establish.

    Returns:
        str | None: Source-derived explanation, or None when no runtime dependency was identified.
    """
    spec = BUILTINS.get(name)
    if spec is None:
        return None
    labels = {
        "randomness": "randomness",
        "clock-or-timezone": "the clock or timezone",
        "external-state": "external state",
    }
    effects = [label for effect, label in labels.items() if effect in spec.effects]
    if not effects:
        return None
    # Sampling supplies concrete execution inputs, never a universal fact for a
    # rejection guard. Keep this distinction even while a replay tape is active.
    if name == "randAlphaNum":
        return (
            "randAlphaNum produces a runtime random string; --renderer-policy auto or strict supports sampling and replay, "
            "but sampled strings cannot prove a static rejection"
        )
    return f"{name} may depend on {', '.join(effects)}; its result requires native rendering"


def reference() -> str:
    """
    Generate the source-derived matrix without confusing recognition with evaluator support.

    Returns:
        str: Markdown table of upstream implementations, result families, effects and unresolved calls.
    """
    lines = [
        "| Function | Upstream implementation | Result | Detected effects | Unresolved calls/writes |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for name, spec in sorted(BUILTINS.items()):
        effects = ", ".join(sorted(spec.effects)) or "None detected (not a purity proof)"
        implementation = spec.meaning.removeprefix("Upstream implementation: ").split("\n", 1)[0].replace("|", "&#124;")
        lines.append(f"| `{name}` | `{implementation}` | {spec.shape} | {effects} | {len(spec.unresolved)} |")
    return "\n".join(lines)
