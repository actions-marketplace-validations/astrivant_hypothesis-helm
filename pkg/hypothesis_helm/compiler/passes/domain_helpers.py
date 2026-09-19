"""
Inline pure helper bindings before projecting manifest destinations to values paths.
"""

from __future__ import annotations

import json
from pathlib import Path

from attrs import frozen

from hypothesis_helm.compiler.asts.contracts import ASSIGNMENT, Contracts, FieldAccess, Unknown, expression
from hypothesis_helm.compiler.asts.templates import Node


@frozen
class Reference:
    """
    Keep a symbolic expression distinct from a literal helper argument.

    Attributes:
        text (str): Canonical expression in the calling chart's values context.
    """

    text: str


def select(value: object, fields: tuple[str, ...]) -> object:
    """
    Follow a symbolic field chain through literal helper dictionaries and values references.

    Args:
        value (object): Resolved symbolic receiver.
        fields (tuple[str, ...]): Consecutive field names.

    Returns:
        object: Selected literal or symbolic reference.

    Raises:
        Unknown: A field cannot be resolved without evaluating an unsupported operation.
    """
    for part in fields:
        if isinstance(value, Reference):
            value = Reference(value.text + "." + part)
        elif isinstance(value, dict) and part in value:
            value = value[part]
        else:
            raise Unknown("unresolved helper argument path")
    if value is None:
        raise Unknown("unresolved helper alias")
    return value


def argument(expr: object, context: object, variables: dict[str, object]) -> object:
    """
    Resolve literal dictionaries and direct aliases without evaluating Helm functions.

    Args:
        expr (object): Parsed helper argument expression.
        context (object): Current dot and dollar context.
        variables (dict[str, object]): Locally declared aliases.

    Returns:
        object: Literal argument or a symbolic reference preserving its source path.
    """
    if isinstance(expr, FieldAccess):
        return select(argument(expr.receiver, context, variables), expr.fields)
    if isinstance(expr, tuple):
        if expr and expr[0] == "dict" and len(expr) % 2 == 1:
            pairs = [
                (argument(k, context, variables), argument(v, context, variables)) for k, v in zip(expr[1::2], expr[2::2], strict=True)
            ]
            if all(isinstance(k, str) for k, _ in pairs):
                return {str(k): v for k, v in pairs}
        raise Unknown("helper argument needs unsupported evaluation")
    if not isinstance(expr, str):
        raise Unknown("invalid helper argument")
    if expr.startswith('"'):
        return json.loads(expr)
    if expr.startswith("`") and expr.endswith("`"):
        return expr[1:-1]
    if expr in {"true", "false"}:
        return expr == "true"
    if expr.lstrip("-").isdigit():
        return int(expr)
    if expr.startswith((".", "$")):
        if expr in {".", "$"}:
            return context
        head, *parts = expr.split(".")
        value = context if head in {"", "$"} else variables.get(head)
        return select(value, tuple(parts))
    raise Unknown("unsupported helper argument")


def rewrite(expr: object, context: object, variables: dict[str, object]) -> str:
    """
    Substitute direct input references while preserving expression structure.

    Args:
        expr (object): Parsed expression or literal token.
        context (object): Symbolic helper context.
        variables (dict[str, object]): Helper-local aliases.

    Returns:
        str: Expression suitable for the existing conservative projection pass.
    """
    if isinstance(expr, tuple):
        return " ".join(
            "(" + rewrite(item, context, variables) + ")" if isinstance(item, tuple) else rewrite(item, context, variables) for item in expr
        )
    if isinstance(expr, FieldAccess) or (isinstance(expr, str) and expr.startswith((".", "$"))):
        return symbolic_argument(argument(expr, context, variables))
    return str(expr)


def symbolic_argument(value: object) -> str:
    """
    Preserve input references inside helper dictionaries without JSON-encoding symbolic objects.

    Args:
        value (object): Supported literal, symbolic reference, or helper argument dictionary.

    Returns:
        str: A grouped Helm expression retaining each known input origin.
    """
    if isinstance(value, Reference):
        return value.text
    if isinstance(value, dict):
        fields = " ".join(f"{json.dumps(key)} {symbolic_argument(child)}" for key, child in value.items())
        return f"(dict {fields})"
    return json.dumps(value)


def inline(chart: Path, nodes: tuple[Node, ...], contracts: Contracts) -> tuple[Node, ...]:
    """
    Inline statically named pure helpers, keeping ambiguous or transformed outputs opaque.

    Args:
        chart (Path): Calling chart, retained for source diagnostics.
        nodes (tuple[Node, ...]): Root template nodes.
        contracts (Contracts): Unique helper definitions, including prepared dependencies.

    Returns:
        tuple[Node, ...]: Rebound nodes accepted only if the downstream projection understands every operation.
    """
    remaining = contracts.limits["max_discovery_nodes"]

    def expand(items: tuple[Node, ...], context: object, variables: dict[str, object], stack: tuple[str, ...]) -> tuple[Node, ...]:
        """
        Expand bounded helper calls with fresh lexical aliases at each invocation.

        Args:
            items (tuple[Node, ...]): Nodes in the current template scope.
            context (object): Argument supplied to this helper.
            variables (dict[str, object]): Local aliases.
            stack (tuple[str, ...]): Current helper call chain.

        Returns:
            tuple[Node, ...]: Pure nodes with references rebound to the root chart.
        """
        nonlocal remaining
        result: list[Node] = []
        for node in items:
            remaining -= 1
            if remaining < 0:
                raise Unknown(
                    f"helper projection statement budget exceeded: compiler.max_discovery_nodes={contracts.limits['max_discovery_nodes']}"
                )
            if node.kind == "text":
                if node.text:
                    result.append(node)
                continue
            if node.kind == "opaque":
                raise Unknown(f"helper projection cannot resolve {node.text} in {chart.name}")
            if node.kind == "if":
                result.append(
                    Node(
                        "if",
                        rewrite(expression(node.text), context, variables),
                        node.line,
                        expand(node.children, context, dict(variables), stack),
                        expand(node.otherwise, context, dict(variables), stack),
                    )
                )
                continue
            binding = ASSIGNMENT.fullmatch(node.text)
            if binding:
                if binding[2] != ":=":
                    raise Unknown("helper projection cannot resolve assignment effects")
                variables[binding[1]] = argument(expression(binding[3]), context, variables)
                continue
            parsed = expression(node.text)
            wrappers: list[tuple[object, ...]] = []
            call = parsed
            while isinstance(call, tuple) and call[0] in {"quote", "toYaml", "nindent", "indent"}:
                wrappers.append(call[:-1])
                call = call[-1]
            if isinstance(call, tuple) and len(call) == 3 and call[0] in {"include", "template"}:
                name = argument(call[1], context, variables)
                if not isinstance(name, str) or name not in contracts.helpers or name in stack:
                    raise Unknown("helper is missing, ambiguous or recursive")
                if len(stack) >= contracts.max_call_depth:
                    raise Unknown(f"helper call depth exceeds compiler limit {contracts.max_call_depth}")
                bound = argument(call[2], context, variables)
                expanded = expand(contracts.helpers[name][1], bound, {}, (*stack, name))
                if wrappers:
                    # Formatting a multi-statement helper needs output semantics beyond
                    # direct projection. A single emit is a transparent composition.
                    if len(expanded) != 1 or expanded[0].kind != "emit":
                        raise Unknown("formatted helper has nontrivial output")
                    inner = expression(expanded[0].text)
                    for wrapper in reversed(wrappers):
                        inner = (*wrapper, inner)
                    expanded = (Node("emit", rewrite(inner, {"Values": Reference(".Values")}, {}), node.line),)
                result.extend(expanded)
            else:
                result.append(Node("emit", rewrite(parsed, context, variables), node.line))
        return tuple(result)

    return expand(nodes, {"Values": Reference(".Values"), "Chart": Reference(".Chart"), "Release": Reference(".Release")}, {}, ())
