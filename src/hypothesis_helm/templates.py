"""Small Go-template action AST and conservative, scope-aware value discovery.

This is an analyzer, not a Go-template interpreter. Helm remains the renderer.
Unknown contexts are represented by None, never silently treated as the root.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from attrs import define, field


@define
class Action:
    text: str
    line: int
    tokens: list[str]
    children: list[Action] = field(factory=list)
    otherwise: list[Action] = field(factory=list)


@define(frozen=True)
class Reference:
    path: tuple[str, ...]
    file: str
    line: int
    fallback: bool = False


@define(frozen=True)
class Diagnostic:
    file: str
    line: int
    message: str


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|`[^`]*`|\x27(?:\\.|[^\x27\\])*\x27|:=|[()|,=]|[^\s()|,=]+')


def parse(source: str) -> list[Action]:
    """Parse actions and block nesting, respecting quoted delimiters and comments."""
    root: list[Action] = []
    current = root
    stack: list[tuple[Action, list[Action]]] = []
    pos = 0
    while (start := source.find("{{", pos)) >= 0:
        i = start + 2
        quote = None
        comment = False
        while i < len(source):
            if comment:
                if source.startswith("*/", i):
                    comment = False
                    i += 2
                else:
                    i += 1
                continue
            char = source[i]
            if quote:
                if char == "\\" and quote != "`":
                    i += 2
                    continue
                if char == quote:
                    quote = None
            elif source.startswith("/*", i):
                comment = True
                i += 2
                continue
            elif char in ('"', "`", "'"):
                quote = char
            elif source.startswith("}}", i):
                break
            i += 1
        if i >= len(source):
            raise ValueError(
                f"unterminated template action at line {source.count(chr(10), 0, start) + 1}"
            )
        text = source[start + 2 : i].strip()
        if text.startswith("-"):
            text = text[1:].lstrip()
        if text.endswith("-"):
            text = text[:-1].rstrip()
        pos = i + 2
        if text.startswith("/*"):
            continue
        tokens = TOKEN.findall(text)
        if not tokens:
            continue
        node = Action(text, source.count("\n", 0, start) + 1, tokens)
        if tokens[0] == "end":
            if not stack:
                raise ValueError(f"unmatched end at line {node.line}")
            _, current = stack.pop()
        elif tokens[0] == "else":
            if not stack:
                raise ValueError(f"unmatched else at line {node.line}")
            current = stack[-1][0].otherwise
            if len(tokens) > 1:
                # Keep chained conditions visible; their dot context is conservatively unknown.
                current.append(Action(" ".join(tokens[1:]), node.line, tokens[1:]))
        else:
            current.append(node)
            if tokens[0] in ("if", "with", "range", "define", "block"):
                stack.append((node, current))
                current = node.children
    if stack:
        raise ValueError(f"unclosed block at line {stack[-1][0].line}")
    return root


def discover(path: Path) -> tuple[list[Reference], list[Diagnostic]]:
    """Resolve direct fields, aliases, with/range scopes, and literal key access."""
    refs: list[Reference] = []
    diagnostics: list[Diagnostic] = []
    for file in sorted((path / "templates").rglob("*")):
        if not file.is_file():
            continue
        name = str(file.relative_to(path))
        try:
            nodes = parse(file.read_text())
        except ValueError as exc:
            diagnostics.append(Diagnostic(name, 1, str(exc)))
            continue

        def walk(nodes, dot, env):
            env = dict(env)
            for node in nodes:
                tokens = node.tokens
                fallback = any(t in ("default", "coalesce", "dig") for t in tokens)

                def warn(message):
                    diagnostics.append(Diagnostic(name, node.line, message))

                def resolve(token):
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
                    return base + tuple(suffix.split(".")) if suffix else base

                def emit(value):
                    if value and value[0] == "Values":
                        refs.append(Reference(value[1:], name, node.line, fallback))

                def literal(token):
                    if token.startswith('"'):
                        return json.loads(token)
                    if token.startswith("`"):
                        return token[1:-1]
                    if token.isdigit():
                        return "*"
                    return None

                def expression(ts):
                    # Remove a wrapping pair only; support (index ...).field below.
                    if not ts:
                        return None
                    if ts[0] == "(":
                        depth = 0
                        for j, t in enumerate(ts):
                            depth += (t == "(") - (t == ")")
                            if depth == 0:
                                base = expression(ts[1:j])
                                if (
                                    base is not None
                                    and j + 1 < len(ts)
                                    and ts[j + 1].startswith(".")
                                ):
                                    return base + tuple(ts[j + 1][1:].split("."))
                                return base
                        return None
                    if ts[0] in ("index", "get") and len(ts) >= 3:
                        base = resolve(ts[1])
                        if base is None:
                            warn("unresolved lookup target: " + node.text)
                            return None
                        keys = []
                        for t in ts[2:]:
                            if t in ("|", ")"):
                                break
                            key = literal(t)
                            if key is None:
                                warn("dynamic key requires manual review: " + node.text)
                                keys.append("*")
                            else:
                                keys.append(key)
                        return base + tuple(keys)
                    if ts[0] == "dig" and len(ts) >= 4:
                        base = resolve(ts[-1])
                        keys = [literal(t) for t in ts[1:-2]]
                        if base is not None and all(k is not None for k in keys):
                            return base + tuple(keys)
                        warn("unresolved dig: " + node.text)
                        return None
                    if len(ts) == 1:
                        return resolve(ts[0])
                    return None

                for t in tokens:
                    value = resolve(t)
                    emit(value)
                    if t.startswith(".") and value is None:
                        warn("unresolved dot context: " + t)
                    if t.startswith("$") and "." in t and value is None:
                        warn("unresolved variable context: " + t)
                for j, t in enumerate(tokens):
                    if t in ("index", "get", "dig"):
                        emit(expression(tokens[j:]))
                    if t == "(":
                        emit(expression(tokens[j:]))
                    if t in (
                        "tpl",
                        "include",
                        "template",
                        "block",
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
                    names = [t for t in rhs[:assignment] if t.startswith("$")]
                    rhs = rhs[assignment + 1 :]
                value = expression(rhs)
                emit(value)
                child_env = dict(env)
                for variable in names:
                    child_env[variable] = (
                        value + ("*",) if value is not None and head == "range" else value
                    )
                if head not in ("if", "range", "with"):
                    env.update(child_env)
                child_dot = dot
                if head in ("with", "range"):
                    child_dot = value
                    if head == "range" and value is not None:
                        child_dot = value + ("*",)
                if head in ("define", "block"):
                    child_dot, child_env = None, {"$": None}
                    warn("named template context is resolved only at runtime")
                walk(node.children, child_dot, child_env)
                walk(node.otherwise, dot, env)

        walk(nodes, (), {"$": ()})
    return list(dict.fromkeys(refs)), list(dict.fromkeys(diagnostics))
