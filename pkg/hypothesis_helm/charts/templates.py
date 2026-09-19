"""
Small Go-template action AST and conservative, scope-aware value discovery.

This analyzer discovers template structure and input references. Helm renders the templates.
Unknown contexts are represented by None, never silently treated as the root.
"""

from __future__ import annotations

import json
from pathlib import Path

from attrs import define

from hypothesis_helm.charts import tpl, yamlio
from hypothesis_helm.compiler.asts.actions import Action as Action
from hypothesis_helm.compiler.asts.actions import parse as parse
from hypothesis_helm.compiler.asts.origins import Literal, Origin, identity, select
from hypothesis_helm.compiler.limits import call_depth
from hypothesis_helm.compiler.passes.discovery_sources import DiscoverySources


@define(frozen=True)
class Reference:
    """
    Record a resolved value path and its template source location.

    Attributes:
        path (tuple[str, ...]): Resolved value path or chart location.
        file (str): Chart-relative template filename.
        line (int): One-based source line number.
        fallback (bool): Whether the action contains a fallback expression.
    """

    path: tuple[str, ...]
    file: str
    line: int
    fallback: bool = False


@define(frozen=True)
class Diagnostic:
    """
    Describe a template construct requiring manual review.

    Attributes:
        file (str): Chart-relative template filename.
        line (int): One-based source line number.
        message (str): Human-readable diagnostic detail.
    """

    file: str
    line: int
    message: str


def discover(path: Path, *, prune_literals: bool = False) -> tuple[list[Reference], list[Diagnostic]]:
    """
    Resolve direct fields, aliases, with/range scopes, and literal key access.

    Args:
        path (Path): Value path or chart location to inspect.
        prune_literals (bool): Skip branches controlled by literal true/false conditions.

    Returns:
        tuple[list[Reference], list[Diagnostic]]: Result of the documented operation.
    """
    values_file = path / "values.yaml"
    defaults = yamlio.load(values_file.read_text()) if values_file.is_file() else {}
    active_tpl: set[tuple[str, tuple[str, ...] | None]] = set()
    active_helpers: list[str] = []
    visited_helpers: set[tuple[object, ...]] = set()
    remaining = 10000
    sources = DiscoverySources.build(path)
    refs: list[Reference] = []
    diagnostics = [Diagnostic(*item) for item in sources.diagnostics]
    for name, nodes in sources.roots.items():

        def walk(
            nodes: list[Action],
            dot: Origin,
            env: dict[str, Origin],
            source_name: str = name,
        ) -> None:
            """
            Resolve value references in the current lexical scope.

            Args:
                nodes (list[Action]): Template actions to inspect in lexical order.
                dot (Origin): Current dot origin, literal dictionary, or unresolved context.
                env (dict[str, Origin]): Variable aliases available in the current lexical scope.
                source_name (str): Filename captured for this traversal.

            Returns:
                None: None. The operation completes through its documented side effects.
            """
            nonlocal remaining
            env = dict(env)
            for node in nodes:
                if remaining <= 0:
                    diagnostics.append(Diagnostic(source_name, node.line, "template discovery statement budget exceeded"))
                    return
                remaining -= 1
                tokens = node.tokens
                if tokens[0] == "define":
                    continue
                if prune_literals and tokens in (["if", "true"], ["if", "false"]):
                    walk(
                        node.children if tokens[1] == "true" else node.otherwise,
                        dot,
                        env,
                        source_name,
                    )
                    continue
                fallback = any(t in ("default", "coalesce", "dig") for t in tokens)

                def warn(message: str, filename: str = source_name, line: int = node.line) -> None:
                    """
                    Record an unresolved construct at its template source location.

                    Args:
                        message (str): Diagnostic detail for the current source location.
                        filename (str): Filename used by this operation.
                        line (int): Line used by this operation.

                    Returns:
                        None: None. The operation completes through its documented side effects.
                    """
                    diagnostics.append(Diagnostic(filename, line, message))

                def resolve(token: str) -> Origin:
                    """
                    Resolve a field token against dot and variable aliases.

                    Args:
                        token (str): Template token to resolve.

                    Returns:
                        Origin: Selected input origin, literal, context dictionary, or unknown result.
                    """
                    if token == ".":
                        return dot
                    if token.startswith("."):
                        base, suffix = dot, token[1:]
                    elif token.startswith("$"):
                        head, _, suffix = token.partition(".")
                        base = env.get(head)
                    else:
                        return None
                    if base is None:
                        return None
                    return select(base, tuple(suffix.split("."))) if suffix else base

                def emit(
                    value: Origin,
                    filename: str = source_name,
                    line: int = node.line,
                    has_fallback: bool = fallback,
                ) -> None:
                    """
                    Record a resolved reference rooted in chart values.

                    Args:
                        value (Origin): Candidate input origin or helper context.
                        filename (str): Filename used by this operation.
                        line (int): Line used by this operation.
                        has_fallback (bool): Has fallback used by this operation.

                    Returns:
                        None: None. The operation completes through its documented side effects.
                    """
                    if isinstance(value, tuple) and value and value[0] == "Values":
                        refs.append(Reference(value[1:], filename, line, has_fallback))

                def literal(token: str) -> str | None:
                    """
                    Decode a literal map key or recognize an array index.

                    Args:
                        token (str): Template token to resolve.

                    Returns:
                        str | None: Result of the documented operation.
                    """
                    if token.startswith('"'):
                        return str(json.loads(token))
                    if token.startswith("`"):
                        return token[1:-1]
                    if token.isdigit():
                        return "*"
                    return None

                def expression(ts: list[str], action_text: str = node.text) -> Origin:
                    """
                    Resolve literal lookups and simple template expressions.

                    Args:
                        ts (list[str]): Tokens forming a template expression.
                        action_text (str): Action text used by this operation.

                    Returns:
                        Origin: Resolved path, dictionary or literal; unsupported expressions remain unknown.
                    """
                    if not ts:
                        return None
                    nesting = 0
                    for token in ts:
                        if token == "|" and nesting == 0:
                            return None
                        nesting += (token == "(") - (token == ")")
                    if ts[0] == "(":
                        depth = 0
                        for j, t in enumerate(ts):
                            depth += (t == "(") - (t == ")")
                            if depth == 0:
                                base = expression(ts[1:j])
                                if j + 2 == len(ts) and ts[j + 1].startswith("."):
                                    return select(base, tuple(ts[j + 1][1:].split(".")))
                                return base if j + 1 == len(ts) else None
                        return None
                    if ts[0] == "dict":
                        args = tpl.arguments(ts[1:])
                        if len(args) % 2:
                            return None
                        bound: dict[str, Origin] = {}
                        for key_tokens, item in zip(args[::2], args[1::2], strict=True):
                            if len(key_tokens) != 1 or not key_tokens[0].startswith(('"', "`")):
                                return None
                            name = literal(key_tokens[0])
                            if name is None:
                                return None
                            bound[name] = expression(item)
                        return bound
                    if ts[0] in ("index", "get") and len(ts) >= 3:
                        base = resolve(ts[1])
                        if base is None:
                            warn("unresolved lookup target: " + action_text)
                            return None
                        keys = []
                        for t in ts[2:]:
                            if t in ("|", ")"):
                                break
                            key = literal(t)
                            if key is None:
                                warn("dynamic key requires manual review: " + action_text)
                                keys.append("*")
                            else:
                                keys.append(key)
                        return select(base, tuple(keys))
                    if ts[0] == "dig" and len(ts) >= 4:
                        ts = ts[: next((i for i, t in enumerate(ts) if t in ("|", ")")), len(ts))]
                        base = resolve(ts[-1])
                        dig_keys = [literal(t) for t in ts[1:-2]]
                        if base is not None and all(k is not None for k in dig_keys):
                            return select(base, tuple(k for k in dig_keys if k is not None))
                        warn("unresolved dig: " + action_text)
                        return None
                    if len(ts) == 1:
                        if ts[0].startswith(('"', "`")):
                            return Literal(literal(ts[0]))
                        if ts[0] in ("true", "false", "nil") or ts[0].lstrip("-").isdigit():
                            return Literal(ts[0])
                        return resolve(ts[0])
                    return None

                def origin_path(ts: list[str]) -> tuple[str, ...] | None:
                    """
                    Expose only path origins to concrete tpl source lookup.

                    Args:
                        ts (list[str]): Source or context expression tokens.

                    Returns:
                        tuple[str, ...] | None: Resolved path, excluding literals and constructed dictionaries.
                    """
                    value = expression(ts)
                    return value if isinstance(value, tuple) else None

                for t in tokens:
                    value = resolve(t)
                    emit(value)
                    if t.startswith(".") and value is None:
                        warn("unresolved dot context: " + t)
                    if t.startswith("$") and "." in t and value is None:
                        warn("unresolved variable context: " + t)
                for j, t in enumerate(tokens):
                    if t in ("index", "get", "dig"):
                        emit(expression([t, *(token for arg in tpl.arguments(tokens[j + 1 :]) for token in arg)]))
                    if t == "(":
                        emit(expression(tokens[j:]))
                    if t == "tpl":
                        try:
                            args = tpl.arguments(tokens[j + 1 :])
                            if len(args) != 2 or (j > 0 and tokens[j - 1] == "|"):
                                raise ValueError("tpl requires a resolvable string and context")
                            content = tpl.source_text(args[0], path, defaults, origin_path)
                            context = origin_path(args[1])
                            if context is None:
                                raise ValueError("tpl context is dynamic or unsupported")
                            tpl_identity = (content, context)
                            if tpl_identity in active_tpl or len(active_tpl) >= 32:
                                raise ValueError("recursive tpl expansion requires review")
                            nested = parse(content)
                            active_tpl.add(tpl_identity)
                            try:
                                walk(
                                    nested,
                                    context,
                                    {"$": context},
                                    f"{source_name}:{node.line} (tpl)",
                                )
                            finally:
                                active_tpl.remove(tpl_identity)
                        except ValueError as exc:
                            warn(str(exc))
                    if t in ("include", "template", "block"):
                        args = tpl.arguments(tokens[j + 1 :])
                        helper = literal(args[0][0]) if args and len(args[0]) == 1 and args[0][0].startswith(('"', "`")) else None
                        if helper is None or len(args) not in (1, 2) or (j > 0 and tokens[j - 1] == "|"):
                            warn("helper name or call context is dynamic: " + node.text)
                            continue
                        if helper not in sources.helpers:
                            warn(f"{t} helper is missing or ambiguous: {helper}")
                            continue
                        if helper in active_helpers or len(active_helpers) >= call_depth():
                            warn("helper is recursive or exceeds compiler call depth: " + helper)
                            continue
                        bound_context = expression(args[1]) if len(args) == 2 else Literal(None)
                        if bound_context is None:
                            warn("helper context is dynamic or unsupported: " + helper)
                            continue
                        visit = (helper, identity(bound_context), tuple(active_helpers), frozenset(active_tpl))
                        if visit in visited_helpers:
                            continue
                        helper_file, helper_nodes = sources.helpers[helper]
                        active_helpers.append(helper)
                        try:
                            walk(helper_nodes, bound_context, {"$": bound_context}, helper_file)
                        finally:
                            active_helpers.pop()
                        if remaining > 0:
                            visited_helpers.add(visit)
                    if t in (
                        "set",
                        "unset",
                        "merge",
                        "mergeOverwrite",
                    ):
                        warn("dynamic template/context or mutation requires review: " + t)
                head = tokens[0]
                rhs = tokens[1:] if head in ("if", "range", "with") else tokens
                assignment = next((j for j, t in enumerate(rhs) if t in (":=", "=")), None)
                names = []
                if assignment is not None:
                    if rhs[assignment] == "=":
                        warn("variable reassignment requires review: " + node.text)
                    names = [t for t in rhs[:assignment] if t.startswith("$")]
                    rhs = rhs[assignment + 1 :]
                value = expression(rhs)
                emit(value)
                child_env = dict(env)
                for position, variable in enumerate(names):
                    if head == "range" and len(names) == 2 and position == 0:
                        child_env[variable] = None
                        continue
                    child_env[variable] = select(value, ("*",)) if head == "range" else value
                if head not in ("if", "range", "with"):
                    env.update(child_env)
                child_dot = dot
                if head in ("with", "range"):
                    child_dot = value
                    if head == "range" and value is not None:
                        child_dot = select(value, ("*",))
                if head == "block":
                    continue
                walk(node.children, child_dot, child_env, source_name)
                walk(node.otherwise, dot, child_env, source_name)

        walk(nodes, (), {"$": ()})
    return list(dict.fromkeys(refs)), list(dict.fromkeys(diagnostics))
