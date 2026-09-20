"""
Project downstream domains through source-derived helper and control-flow provenance.
"""

import json
from pathlib import Path

from hypothesis_helm.compiler.asts.contract_scope import Scope
from hypothesis_helm.compiler.asts.contracts import Contracts
from hypothesis_helm.compiler.asts.dependencies import Dependency
from hypothesis_helm.compiler.asts.projections import Input, Operation
from hypothesis_helm.compiler.asts.templates import Node, walk
from hypothesis_helm.compiler.passes.dependencies import Dependencies
from hypothesis_helm.compiler.passes.domain_constraints import at
from hypothesis_helm.compiler.passes.domain_interpreter import Interpreter
from hypothesis_helm.compiler.passes.domain_layout import Layout
from hypothesis_helm.schemas.contracts import sequence

__all__ = ("activation", "project")


def activation(node: Dependency) -> dict[str, object]:
    """
    Describe dependency condition precedence and tag fallback as a values predicate.

    Args:
        node (Dependency): One aliased dependency and its root-relative controls.

    Returns:
        dict[str, object]: Activation guard, including the default enabled state.
    """
    enabled: dict[str, object] = (
        {
            "not": {
                "allOf": [
                    {"anyOf": [at(path, {"const": False}) for path in node.tags]},
                    {"not": {"anyOf": [at(path, {"const": True}) for path in node.tags]}},
                ]
            }
        }
        if node.tags
        else {}
    )
    # Build from the fallback outward so the first usable Boolean condition has Helm's precedence.
    for path in reversed(node.conditions):
        enabled = {"anyOf": [at(path, {"const": True}), {"allOf": [{"not": at(path, {"type": "boolean"})}, enabled]}]}
    return enabled


def project(
    chart: Path, schema: dict[str, object], dependencies: Dependencies | None = None
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """
    Follow established destinations across root templates and prepared dependency namespaces.

    Args:
        chart (Path): Prepared chart directory.
        schema (dict[str, object]): Coalesced input types used for symbolic type tests.
        dependencies (Dependencies | None): Reusable parsed dependency inventory.

    Returns:
        tuple[list[dict[str, object]], list[dict[str, object]]]: Generation rules and unresolved analysis locations.
    """
    contracts = Contracts.build(chart, dependencies)
    alternatives: dict[str, list[tuple[str, tuple[Node, ...]]]] = {}
    for file, tree in contracts.templates.items():
        for node in walk(tree):
            if node.kind == "opaque" and node.text.startswith('define "'):
                helper = node.text.split('"')[1]
                if helper in contracts.ambiguous_helpers:
                    alternatives.setdefault(helper, []).append((file, node.children))
    rules: list[dict[str, object]] = []
    notes: list[dict[str, object]] = [{"reason": message} for message in contracts.diagnostics]
    imports = [note for note in contracts.dependencies.diagnostics if "import-values forwarding" in str(note.get("message", ""))]
    if imports:
        # A constraint on a forwarded value cannot be assigned to a caller until its input origin is known.
        return [], [{**note, "reason": "imported input origins unresolved; domain unchanged"} for note in imports]
    for name, nodes in sorted(contracts.templates.items()):
        if Path(name).name.startswith("_") or Path(name).suffix not in {".yaml", ".yml"}:
            continue
        if any("HHINPUTDOMAINMARKER" in node.text for node in walk(nodes)):
            notes.append({"file": name, "reason": "reserved analysis marker occurs in source"})
            continue
        namespace = contracts.scopes[name]
        ancestors = [node for node in contracts.dependencies.nodes if namespace[: len(node.path)] == node.path]
        if any(node.reason for node in ancestors):
            notes.append({"file": name, "reason": "dependency activation or namespace unresolved; domain unchanged"})
            continue
        interpreter = Interpreter(contracts, schema, alternatives=alternatives)
        layout = Layout(contracts.limits)
        base = name.split("/templates/")[0] + "/templates" if "/templates/" in name else "templates"
        context = {
            "Values": Input(namespace),
            "Release": Operation("renderer-context"),
            "Chart": Operation("renderer-context"),
            "Capabilities": Operation("renderer-context"),
            "Files": Operation("renderer-context"),
            "Template": {"BasePath": base, "Name": name},
        }
        try:
            pieces = interpreter.visit(nodes, name, context, Scope({"$": context}))
            if interpreter.mutated:
                notes.append({"file": name, "reason": "shared input mutation unresolved; template domains unchanged"})
                continue
            found = layout.collect(pieces)
            for rule in found:
                # Parent globals and import-values can override a child origin.
                # Do not assert a unique origin until forwarding is established.
                path = tuple(str(part) for part in sequence(rule["path"]))
                if namespace and path[: len(namespace) + 1] == (*namespace, "global"):
                    notes.append({"file": name, "path": list(path), "reason": "forwarded global input origin unresolved"})
                    continue
                rule["guards"] = [*(activation(node) for node in ancestors), *sequence(rule["guards"])]
                rules.append(rule)
        except (ValueError, RecursionError) as error:
            notes.append({"file": name, "reason": str(error)})
        finally:
            notes.extend(interpreter.notes)
            notes.extend(layout.notes)
    unique_rules = {json.dumps(rule, sort_keys=True): rule for rule in rules}
    unique_notes = {json.dumps(note, sort_keys=True): note for note in notes}
    return list(unique_rules.values()), list(unique_notes.values())
