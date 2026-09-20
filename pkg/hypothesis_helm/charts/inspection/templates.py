"""
Small Go-template action AST and conservative, scope-aware value discovery.

This analyzer discovers template structure and input references. Helm renders the templates.
Unknown contexts are represented by None, never silently treated as the root.
"""

from __future__ import annotations

import json
from pathlib import Path

from attrs import define

from hypothesis_helm.charts.inspection import tpl
from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.actions import TOKEN
from hypothesis_helm.compiler.asts.actions import Action as Action
from hypothesis_helm.compiler.asts.actions import parse as parse
from hypothesis_helm.compiler.asts.origins import Derived, Dictionary, Literal, Origin, identity, join, paths, select, unresolved
from hypothesis_helm.compiler.builtins import BUILTINS, MUTATIONS, NATIVE_STATE
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.compiler.passes.discovery_flow import invalidate, iterations, key_guards, truth, widen
from hypothesis_helm.compiler.passes.discovery_functions import CERTIFICATES
from hypothesis_helm.compiler.passes.discovery_functions import result as function_result
from hypothesis_helm.compiler.passes.discovery_sources import DiscoverySources
from hypothesis_helm.compiler.passes.discovery_tpl import sources as tpl_sources

__all__ = ("Action", "Diagnostic", "Reference", "discover", "parse")


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


def discover(
    path: Path, *, prune_literals: bool = False, offline: bool = False, limits: dict[str, int] | None = None
) -> tuple[list[Reference], list[Diagnostic]]:
    """
    Resolve direct fields, aliases, with/range scopes, and literal key access.

    Args:
        path (Path): Value path or chart location to inspect.
        prune_literals (bool): Skip branches controlled by literal true/false conditions.
        offline (bool): Analyze plain helm template with neither a cluster connection nor DNS enabled.
        limits (dict[str, int] | None): Captured parent budgets for dependency inspection, or this chart's settings.

    Returns:
        tuple[list[Reference], list[Diagnostic]]: Result of the documented operation.
    """
    values_file = path / "values.yaml"
    defaults = yamlio.load(values_file.read_text()) if values_file.is_file() else {}
    active_tpl: set[tuple[str, tuple[object, ...]]] = set()
    active_helpers: list[str] = []
    visited_helpers: dict[tuple[object, ...], bool] = {}
    mutations = 0
    limits = active_limits(path) if limits is None else limits
    remaining = limits["max_discovery_nodes"]
    sources = DiscoverySources.build(path, limits=limits)
    refs: list[Reference] = []
    diagnostics = [Diagnostic(*item) for item in sources.diagnostics]
    for name, nodes in sources.roots.items():

        def walk(
            nodes: list[Action],
            dot: Origin,
            env: dict[str, Origin],
            source_name: str = name,
            guards: frozenset[tuple[object, ...]] = frozenset(),
        ) -> dict[str, Origin]:
            """
            Resolve value references in the current lexical scope.

            Args:
                nodes (list[Action]): Template actions to inspect in lexical order.
                dot (Origin): Current dot origin, literal dictionary, or unresolved context.
                env (dict[str, Origin]): Variable aliases available in the current lexical scope.
                source_name (str): Filename captured for this traversal.
                guards (frozenset[tuple[object, ...]]): Key-membership facts established by enclosing branches.

            Returns:
                dict[str, Origin]: Assignments to variables declared outside this lexical block.
            """
            nonlocal remaining, mutations
            env = dict(env)
            outward: dict[str, Origin] = {}
            declared: set[str] = set()
            for node in nodes:
                if remaining <= 0:
                    diagnostics.append(
                        Diagnostic(
                            source_name,
                            node.line,
                            f"template discovery statement budget exceeded: compiler.max_discovery_nodes={limits['max_discovery_nodes']}",
                        )
                    )
                    return {}
                remaining -= 1
                tokens = node.tokens
                if tokens[0] == "define":
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
                    value = select(base, tuple(suffix.split("."))) if suffix else base
                    if value == ("Template", "BasePath"):
                        return Literal(sources.base_path)
                    return value

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
                    for origin in paths(value):
                        if origin and origin[0] == "Values":
                            refs.append(Reference(origin[1:], filename, line, has_fallback))

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
                    stages: list[list[str]] = [[]]
                    for token in ts:
                        if token == "|" and nesting == 0:
                            stages.append([])
                            continue
                        stages[-1].append(token)
                        nesting += (token == "(") - (token == ")")
                    if len(stages) > 1:
                        value = expression(stages[0])
                        for stage in stages[1:]:
                            if not stage:
                                return None
                            arguments = [expression(arg) for arg in tpl.arguments(stage[1:])]
                            value = function_result(stage[0], [*arguments, value], offline=offline, limits=limits)
                        return value
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
                            warn("dict has an unpaired key; Helm supplies an empty final value; helper context cannot be established")
                            return None
                        bound: dict[str, Origin] = {}
                        for key_tokens, item in zip(args[::2], args[1::2], strict=True):
                            if len(key_tokens) != 1 or not key_tokens[0].startswith(('"', "`")):
                                return None
                            name = literal(key_tokens[0])
                            if name is None:
                                return None
                            bound[name] = expression(item)
                        return Dictionary(bound)
                    if ts[0] in ("index", "get") and len(ts) >= 3:
                        args = tpl.arguments(ts[1:])
                        if len(args) < 2:
                            return None
                        base = expression(args[0])
                        if base is None:
                            warn("unresolved lookup target: " + action_text)
                            return None
                        for argument in args[1:]:
                            key_value = expression(argument)
                            key = str(key_value.value) if isinstance(key_value, Literal) else None
                            if isinstance(base, Dictionary) and isinstance(key_value, Literal) and isinstance(key_value.value, str):
                                # A literal '*' is a real dictionary key, not the range-member wildcard.
                                selected = base.fields.get(key_value.value, Literal(None))
                                base = join(selected, None) if base.uncertain else selected
                                continue
                            if len(argument) == 1 and argument[0].isdigit():
                                key = "*"
                            if key is None:
                                if isinstance(base, Dictionary) and not base.uncertain:
                                    # A closed table has finitely many possible results even when the key is an input.
                                    # Resolve immediately against the live epoch, including preceding helper effects.
                                    present = (identity(base), identity(key_value), mutations) in guards  # noqa: B023
                                    base = join(*base.fields.values(), *(() if present else (Literal(None),)))
                                    continue
                                if not isinstance(base, Derived) or not base.external:
                                    warn("dynamic key requires manual review: " + action_text)
                                base = select(base, ("*",))
                            else:
                                base = select(base, (key,))
                        return base
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
                            if ts[0].lstrip("-").startswith("0") and len(ts[0].lstrip("-")) > 1:
                                return None  # Go octal and alternate numeric spellings need their own parser.
                            return Literal(None if ts[0] == "nil" else ts[0] == "true" if ts[0] in ("true", "false") else int(ts[0]))
                        if ts[0].startswith((".", "$")):
                            return resolve(ts[0])
                    return function_result(ts[0], [expression(arg) for arg in tpl.arguments(ts[1:])], offline=offline, limits=limits)

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

                token_matches = list(TOKEN.finditer(node.text))
                selectors = {
                    i
                    for i in range(1, len(token_matches))
                    if token_matches[i - 1][0] == ")"
                    and token_matches[i][0].startswith(".")
                    and token_matches[i - 1].end() == token_matches[i].start()
                }
                for i, t in enumerate(tokens):
                    if i in selectors:
                        continue  # The enclosing expression supplies this selector's receiver.
                    value = resolve(t)
                    emit(value)
                    if t.startswith(".") and unresolved(value):
                        warn("unresolved dot context: " + t)
                    if t.startswith("$") and "." in t and unresolved(value):
                        warn("unresolved variable context: " + t)
                for j, t in enumerate(tokens):
                    if t in ("index", "get", "dig"):
                        emit(expression([t, *(token for arg in tpl.arguments(tokens[j + 1 :]) for token in arg)]))
                    if t == "(":
                        depth = 0
                        for end in range(j, len(tokens)):
                            depth += (tokens[end] == "(") - (tokens[end] == ")")
                            if depth == 0:
                                stop = end + 1
                                if stop in selectors:
                                    stop += 1
                                selected = expression(tokens[j:stop])
                                emit(selected)
                                if stop - 1 in selectors and unresolved(selected):
                                    warn("unresolved parenthesized context: " + " ".join(tokens[j:stop]))
                                break
                    if t == "tpl":
                        try:
                            args = tpl.arguments(tokens[j + 1 :])
                            if len(args) != 2 or (j > 0 and tokens[j - 1] == "|"):
                                raise ValueError("tpl requires a resolvable string and context")
                            contents: tuple[str, ...]
                            incomplete = False
                            try:
                                contents = (tpl.source_text(args[0], path, defaults, origin_path),)
                            except ValueError as exc:
                                contents, incomplete = tpl_sources(expression(args[0]), defaults)
                                if incomplete:
                                    warn(str(exc))
                            context = expression(args[1])
                            if context is None:
                                raise ValueError("tpl context is dynamic or unsupported")
                            for content in contents:
                                if len(content.encode("utf-8")) > limits["max_template_bytes"]:
                                    warn(f"tpl source exceeds compiler.max_template_bytes={limits['max_template_bytes']}")
                                    continue
                                tpl_identity = (content, identity(context))
                                if tpl_identity in active_tpl:
                                    warn("recursive tpl expansion requires review")
                                    continue
                                if len(active_tpl) >= limits["max_tpl_depth"]:
                                    warn(f"tpl expansion exceeds compiler.max_tpl_depth={limits['max_tpl_depth']}")
                                    continue
                                try:
                                    nested = parse(content)
                                except ValueError as exc:
                                    warn(str(exc))
                                    continue
                                active_tpl.add(tpl_identity)
                                try:
                                    walk(
                                        nested,
                                        context,
                                        {"$": context},
                                        f"{source_name}:{node.line} (tpl)",
                                        guards,
                                    )
                                finally:
                                    active_tpl.remove(tpl_identity)
                            if incomplete or paths(expression(args[0])):
                                # Values-backed code can mutate its context in a later candidate.
                                invalidate(context)
                                mutations += 1
                        except ValueError as exc:
                            warn(str(exc))
                    if t in ("include", "template", "block"):
                        args = tpl.arguments(tokens[j + 1 :])
                        name_value = expression(args[0]) if args else None
                        helper = name_value.value if isinstance(name_value, Literal) and isinstance(name_value.value, str) else None
                        if helper is None or len(args) not in (1, 2) or (j > 0 and tokens[j - 1] == "|"):
                            warn("helper name or call context is dynamic: " + node.text)
                            for argument in args[1:]:
                                invalidate(expression(argument))
                            mutations += 1
                            continue
                        target = sources.helpers.get(helper) or sources.templates.get(helper)
                        if target is None or helper in sources.ambiguous:
                            warn(f"{t} helper is missing or ambiguous: {helper}")
                            continue
                        if helper in active_helpers or len(active_helpers) >= limits["max_call_depth"]:
                            warn("helper is recursive or exceeds compiler call depth: " + helper)
                            if len(args) == 2:
                                invalidate(expression(args[1]))
                            mutations += 1
                            continue
                        before_context_diagnostics = len(diagnostics)
                        bound_context = expression(args[1]) if len(args) == 2 else Literal(None)
                        if bound_context is None:
                            if len(diagnostics) == before_context_diagnostics:
                                warn("helper context is dynamic or unsupported: " + helper)
                            continue
                        visit = (helper, identity(bound_context), tuple(active_helpers), frozenset(active_tpl), guards)
                        if visit in visited_helpers:
                            if visited_helpers[visit]:
                                invalidate(bound_context)
                                mutations += 1
                            continue
                        helper_file, helper_nodes = target
                        active_helpers.append(helper)
                        before_mutations = mutations
                        try:
                            walk(helper_nodes, bound_context, {"$": bound_context}, helper_file, guards)
                        finally:
                            active_helpers.pop()
                        if remaining > 0:
                            visited_helpers[visit] = mutations != before_mutations
                    if t in MUTATIONS or t == "call":
                        warn("dynamic template/context or mutation requires review: " + t)
                        args = tpl.arguments(tokens[j + 1 :])
                        if args and t != "call":
                            invalidate(expression(args[0]))
                        else:
                            invalidate(dot)
                            for origin in env.values():
                                invalidate(origin)
                        mutations += 1
                    if t == "lookup" and not offline:
                        warn("lookup reads external cluster state; result left to Helm")
                    if t in CERTIFICATES:
                        warn(f"{t} generates certificate material; result left to Helm")
                    elif t in NATIVE_STATE and t != "lookup" and not (offline and t == "getHostByName"):
                        warn(f"{t} depends on {', '.join(sorted(BUILTINS[t].effects))}; result left to Helm")
                head = tokens[0]
                rhs = tokens[1:] if head in ("if", "range", "with") else tokens
                assignment = next((j for j, t in enumerate(rhs) if t in (":=", "=")), None)
                names = []
                operator = None
                if assignment is not None:
                    operator = rhs[assignment]
                    names = [t for t in rhs[:assignment] if t.startswith("$")]
                    rhs = rhs[assignment + 1 :]
                value = expression(rhs)
                emit(value)
                child_env = dict(env)
                for position, variable in enumerate(names):
                    if head == "range" and len(names) == 2 and position == 0:
                        child_env[variable] = Derived(paths(value))
                        continue
                    child_env[variable] = select(value, ("*",)) if head == "range" else value
                if head not in ("if", "range", "with"):
                    if operator == "=":
                        for variable in names:
                            if variable not in env:
                                warn("assignment to undeclared variable: " + variable)
                            elif variable not in declared:
                                outward[variable] = child_env[variable]
                    env.update(child_env)
                    if operator == ":=":
                        declared.update(names)
                elif operator == "=":
                    for variable in names:
                        if variable not in env:
                            warn("assignment to undeclared variable: " + variable)
                        else:
                            if head != "range":
                                env[variable] = child_env[variable]
                                if variable not in declared:
                                    outward[variable] = env[variable]
                child_dot = dot
                if head in ("with", "range"):
                    child_dot = value
                    if head == "range" and value is not None:
                        child_dot = select(value, ("*",))
                if head == "block":
                    continue
                if head == "range":
                    members = iterations(value)
                    if members is not None:
                        carried = dict(env)
                        changed: set[str] = set()
                        if not members:
                            carried.update(walk(node.otherwise, dot, child_env, source_name, guards))
                            changed.update(carried.keys())
                        for key, member in members:
                            if remaining <= 0:
                                warn("template discovery statement budget exceeded")
                                carried.update({variable: join(item, None) for variable, item in carried.items()})
                                changed.update(carried)
                                break
                            iteration = dict(carried)
                            for position, variable in enumerate(names):
                                iteration[variable] = key if len(names) == 2 and position == 0 else member
                            updates = walk(node.children, member, iteration, source_name, guards)
                            if operator == "=":
                                for variable in names:
                                    updates.setdefault(variable, iteration[variable])
                            updates = {key: item for key, item in updates.items() if key in env and not (operator == ":=" and key in names)}
                            carried.update(updates)
                            changed.update(updates)
                        for variable in changed & env.keys():
                            if operator == ":=" and variable in names:
                                continue
                            env[variable] = carried[variable]
                            if variable not in declared:
                                outward[variable] = env[variable]
                        continue
                    carried = dict(env)
                    changed = set(names if operator == "=" else ()) & env.keys()
                    for _ in range(8):
                        iteration = {**carried, **{key: child_env[key] for key in names}}
                        updates = walk(node.children, child_dot, iteration, source_name, guards)
                        if operator == "=":
                            for variable in names:
                                updates.setdefault(variable, child_env[variable])
                        updates = {key: item for key, item in updates.items() if key in env and not (operator == ":=" and key in names)}
                        changed.update(updates)
                        following = {**carried, **{key: widen(carried[key], item) for key, item in updates.items()}}
                        if all(identity(following[key]) == identity(carried[key]) for key in updates):
                            break
                        carried = following
                    else:
                        warn("loop input origins did not converge within 8 passes; unresolved alternatives retained")
                        carried.update({key: join(carried[key], None) for key in changed})
                    empty = walk(node.otherwise, dot, child_env, source_name, guards)
                    for variable in changed | (empty.keys() & env.keys()):
                        if operator == ":=" and variable in names:
                            continue
                        env[variable] = join(carried[variable], empty.get(variable, env[variable]))
                        if variable not in declared:
                            outward[variable] = env[variable]
                else:
                    known = truth(value) if head in ("if", "with") else None
                    if not prune_literals and tokens in (["if", "true"], ["if", "false"]):
                        known = None
                    if known is not None:
                        facts = guards | (key_guards(rhs, expression, mutations, known) if head == "if" else frozenset())
                        branches = [
                            walk(node.children if known else node.otherwise, child_dot if known else dot, child_env, source_name, facts)
                        ]
                    else:
                        yes = guards | (key_guards(rhs, expression, mutations) if head == "if" else frozenset())
                        no = guards | (key_guards(rhs, expression, mutations, False) if head == "if" else frozenset())
                        branches = [
                            walk(node.children, child_dot, child_env, source_name, yes),
                            walk(node.otherwise, dot, child_env, source_name, no),
                        ]
                    for variable in {key for branch in branches for key in branch} & env.keys():
                        if operator == ":=" and variable in names:
                            continue
                        env[variable] = join(*(branch.get(variable, env[variable]) for branch in branches))
                        if variable not in declared:
                            outward[variable] = env[variable]
            return outward

        walk(nodes, (), {"$": ()})
    return list(dict.fromkeys(refs)), list(dict.fromkeys(diagnostics))
