"""
Project known manifest scalar domains back through direct values references.
"""

import itertools
from pathlib import Path

from ruamel.yaml.scalarstring import ScalarString

from hypothesis_helm.charts.model import _schema_nodes
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.conditions import parse_condition
from hypothesis_helm.compiler.asts.contracts import Contracts, expression
from hypothesis_helm.compiler.asts.templates import Node, fold, lower, value_path
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.compiler.passes.domain_helpers import inline
from hypothesis_helm.schemas.contracts import mapping
from hypothesis_helm.schemas.policy import restrict
from hypothesis_helm.schemas.resources import destination


def project(chart: Path, schema: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """
    Find direct scalar destinations in bounded, fully understood template branches.

    Args:
        chart (Path): Chart directory; helpers, loops and transformed values remain opaque.
        schema (dict[str, object]): Known values types used to justify branch predicates.

    Returns:
        tuple[list[dict[str, object]], list[dict[str, object]]]: Guarded restrictions and explicit analysis limitations.
    """
    rules: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    contracts = Contracts.build(chart)
    for file in sorted((chart / "templates").rglob("*")):
        if file.is_file() and file.suffix in {".yaml", ".yml"}:
            found, notes = project_file(chart, file, schema, contracts)
            rules.extend(found)
            diagnostics.extend(notes)
    return rules, diagnostics


def project_file(
    chart: Path, file: Path, schema: dict[str, object], contracts: Contracts | None = None
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """
    Analyze one template without carrying mutable state into another source file.

    Args:
        chart (Path): Root used for source-relative evidence.
        file (Path): Complete template file.
        schema (dict[str, object]): Known input types.
        contracts (Contracts | None): Shared helper definitions for this chart.

    Returns:
        tuple[list[dict[str, object]], list[dict[str, object]]]: Restrictions and conservative analysis diagnostics.
    """
    rules: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    references: dict[str, tuple[tuple[str, ...], int, bool, bool]] = {}
    name = str(file.relative_to(chart))
    source = file.read_text()
    limits = contracts.limits if contracts is not None else active_limits()
    prefix = "HHINPUTDOMAINMARKER"
    if prefix in source:
        diagnostics.append({"file": name, "reason": "reserved analysis marker occurs in source"})
        return [], diagnostics

    def variants(nodes: tuple[Node, ...]) -> list[tuple[str, list[dict[str, object]]]]:
        """
        Expand supported branches while retaining exact guard requirements.

        Args:
            nodes (tuple[Node, ...]): Structured, constant-folded template nodes.

        Returns:
            list[tuple[str, list[dict[str, object]]]]: Symbolic YAML and its guards, bounded by the configured variant limit.
        """
        result: list[tuple[str, list[dict[str, object]]]] = [("", [])]
        for node in nodes:
            choices: list[tuple[str, list[dict[str, object]]]] = []
            if node.kind == "text":
                choices = [(node.text, [])]
            elif node.kind == "if":
                condition = parse_condition(node.text)
                if condition is None or condition.path is None:
                    raise ValueError(f"unsupported condition at line {node.line}")
                kinds = {node.get("type") for node in _schema_nodes(schema, condition.path, schema) if isinstance(node.get("type"), str)}
                expected = "boolean" if type(condition.literal) is bool else "string"
                if kinds != {expected}:
                    raise ValueError(f"condition has no proved {expected} input type at line {node.line}")
                literal = condition.literal
                if condition.operator in {"truth", "not"}:
                    literal = True
                guard = restrict({"type": "object"}, condition.path, {"const": literal})
                # Existence is needed because properties alone also accepts omission.
                current = guard
                for segment in condition.path:
                    current["required"] = [segment]
                    current = mapping(mapping(current["properties"])[segment])
                if condition.operator in {"not", "ne"}:
                    guard = {"not": guard}
                for branch, clause in ((node.children, guard), (node.otherwise, {"not": guard})):
                    choices.extend((text, [mapping(clause), *guards]) for text, guards in variants(branch))
            elif node.kind == "emit":
                parsed = expression(node.text)
                prefixes: list[str] = []
                while isinstance(parsed, tuple) and parsed[0] in {"nindent", "indent"} and len(parsed) == 3:
                    if not isinstance(parsed[1], str) or not parsed[1].isdigit():
                        raise ValueError("unresolved indentation")
                    if int(parsed[1]) > limits["max_indent_width"]:
                        raise ValueError(f"indentation exceeds compiler.max_indent_width={limits['max_indent_width']}")
                    prefixes.append(("\n" if parsed[0] == "nindent" else "") + " " * int(parsed[1]))
                    parsed = parsed[2]
                quoted = isinstance(parsed, tuple) and len(parsed) == 2 and parsed[0] == "quote"
                serialized = isinstance(parsed, tuple) and len(parsed) == 2 and parsed[0] == "toYaml"
                if quoted or serialized:
                    assert isinstance(parsed, tuple)
                    parsed = parsed[1]
                path = value_path(parsed) if isinstance(parsed, str) else None
                if path is None:
                    if parsed not in {".Release.Name", ".Release.Namespace", ".Chart.Name", ".Chart.Version"}:
                        raise ValueError(f"helper or transformed output at line {node.line}")
                    choices = [("hh-static-context", [])]
                else:
                    marker = f"{prefix}{len(references)}"
                    references[marker] = (path, node.line, quoted, serialized)
                    choices = [("".join(prefixes) + marker, [])]
            else:
                raise ValueError(f"unsupported template block at line {node.line}")
            if len(result) * len(choices) > limits["max_symbolic_variants"]:
                raise ValueError(f"symbolic branch variants exceed compiler.max_symbolic_variants={limits['max_symbolic_variants']}")
            result = [(a + b, [*ga, *gb]) for (a, ga), (b, gb) in itertools.product(result, choices)]
        return result

    collected: list[dict[str, object]] = []
    try:
        nodes = inline(chart, fold(lower(source)), contracts or Contracts.build(chart))
        for text, guards in variants(nodes):
            for raw in yamlio.load_all(text):
                if not isinstance(raw, dict):
                    continue
                document = mapping(raw)
                identity = f"{document.get('apiVersion')}/{document.get('kind')}"

                def walk(
                    value: object, output: tuple[str, ...], resource: str = identity, conditions: list[dict[str, object]] = guards
                ) -> None:
                    """
                    Match only entire scalar markers, excluding concatenation and keys.

                    Args:
                        value (object): Symbolically parsed YAML value.
                        output (tuple[str, ...]): Current manifest path.
                        resource (str): Exact resource identity in this branch.
                        conditions (list[dict[str, object]]): Activation guards for this branch.

                    Returns:
                        None: Append constraints with source and destination evidence.
                    """
                    if isinstance(value, dict):
                        for key, child in value.items():
                            if prefix in str(key):
                                continue
                            walk(child, (*output, str(key)))
                    elif isinstance(value, list):
                        for child in value:
                            walk(child, (*output, "*"))
                    elif isinstance(value, str) and value in references:
                        path, line, quoted, serialized = references[value]
                        quoted = quoted or isinstance(value, ScalarString)
                        match = destination(resource, output)
                        if match is not None:
                            schema, provenance = match
                            collected.append(
                                {
                                    "path": list(path),
                                    "schema": schema,
                                    "guards": conditions,
                                    "quoted": quoted,
                                    "serialized": serialized,
                                    "destination": f"{resource}:$.{'.'.join(output)}",
                                    "file": name,
                                    "line": line,
                                    "source": provenance,
                                }
                            )

                walk(document, ())
    except Exception as exc:
        diagnostics.append({"file": name, "reason": str(exc)})
        return [], diagnostics
    rules.extend(collected)

    return rules, diagnostics
