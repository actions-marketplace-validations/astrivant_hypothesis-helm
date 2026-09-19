"""
Resolve statically available inputs to Helm's tpl function for discovery.
"""

import json
from collections.abc import Callable
from pathlib import Path

from hypothesis_helm.charts.values import yamlio


def arguments(tokens: list[str]) -> list[list[str]]:
    """
    Split function arguments while retaining parenthesized expressions.

    Args:
        tokens (list[str]): Tokens following the function name.

    Returns:
        list[list[str]]: Arguments before a pipeline or enclosing closing parenthesis.
    """
    result: list[list[str]] = []
    depth = 0
    for token in tokens:
        if depth == 0:
            if token in ("|", ")"):
                break
            result.append([])
        result[-1].append(token)
        depth += (token == "(") - (token == ")")
    return result


def source_text(
    tokens: list[str],
    chart: Path,
    defaults: object,
    resolve: Callable[[list[str]], tuple[str, ...] | None],
) -> str:
    """
    Read literal, values-backed, serialized, or chart-file template text.

    Args:
        tokens (list[str]): Template string argument tokens.
        chart (Path): Chart root restricting file access.
        defaults (object): Original parsed values document.
        resolve (Callable[[list[str]], tuple[str, ...] | None]): Lexical path resolver.

    Returns:
        str: Statically available template text; unsupported inputs raise ValueError.
    """
    if tokens and tokens[0] == "(" and tokens[-1] == ")":
        return source_text(tokens[1:-1], chart, defaults, resolve)
    if len(tokens) == 1 and tokens[0].startswith(('"', "`")):
        return tokens[0][1:-1] if tokens[0].startswith("`") else str(json.loads(tokens[0]))
    if len(tokens) == 2 and tokens[0] in (".Files.Get", "$.Files.Get"):
        if resolve(tokens[:1]) != ("Files", "Get"):
            raise ValueError("tpl file context is unresolved")
        filename = source_text(tokens[1:], chart, defaults, resolve)
        file = (chart / filename).resolve()
        if (
            Path(filename).is_absolute()
            or ".." in Path(filename).parts
            or not file.is_relative_to(chart.resolve())
            or file == chart.resolve()
            or file.relative_to(chart.resolve()).parts[0] in ("templates", "charts")
        ):
            raise ValueError("tpl file is outside chart-accessible files")
        try:
            return file.read_text()
        except OSError as exc:
            raise ValueError("tpl file cannot be read: " + filename) from exc
    serialize = bool(tokens and tokens[0] in ("toYaml", "toJson"))
    path = resolve(tokens[1:] if serialize else tokens)
    if path is None or not path or path[0] != "Values":
        raise ValueError("tpl source is dynamic or unsupported")
    value = defaults
    for key in path[1:]:
        if not isinstance(value, dict) or key not in value:
            raise ValueError("tpl source is absent or dynamically indexed")
        value = value[key]
    if serialize:
        return yamlio.dump(value) if tokens[0] == "toYaml" else json.dumps(value)
    if not isinstance(value, str):
        raise ValueError("tpl source is not a string")
    return value
