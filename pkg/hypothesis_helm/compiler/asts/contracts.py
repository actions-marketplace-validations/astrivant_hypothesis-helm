"""
Evaluate explicit template rejection contracts without interpreting arbitrary Helm code.
"""

from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache
from operator import eq, ge, gt, le, lt, ne
from pathlib import Path

from attrs import define, field, frozen

from hypothesis_helm.compiler.asts.contract_values import (
    BoundValue,
    ConstantList,
    ConstantMap,
    ContractText,
    KeyList,
    UnorderedKeys,
    native,
)
from hypothesis_helm.compiler.asts.templates import Node, lower, walk
from hypothesis_helm.compiler.passes.dependencies import Dependencies, lookup

TOKENS = re.compile(r'\s*("(?:\\.|[^"\\])*"|`[^`]*`|[()|]|[^\s()|]+)')
ASSIGNMENT = re.compile(r"(\$\w+)\s*(:=|=)\s*(.*)", re.DOTALL)


def declares_path(schema: object, path: tuple[str, ...]) -> bool:
    """
    Preserve explicitly authored domains and ambiguous schema relationships.

    Args:
        schema (object): Original authored schema, before inference from values.
        path (tuple[str, ...]): Field relative to this schema's chart.

    Returns:
        bool: A declaration or an unresolved schema relationship may constrain this field.
    """
    if not isinstance(schema, dict):
        return schema is not True
    if not path:
        return True
    if any(
        key in schema
        for key in (
            "$ref",
            "$dynamicRef",
            "$recursiveRef",
            "allOf",
            "anyOf",
            "oneOf",
            "not",
            "if",
            "then",
            "else",
            "dependencies",
            "dependentSchemas",
            "dependentRequired",
            "unevaluatedProperties",
            "enum",
            "const",
        )
    ):
        return True
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        return True
    if path[0] in properties:
        return declares_path(properties[path[0]], path[1:])
    if schema.get("patternProperties"):
        return True
    additional = schema.get("additionalProperties", True)
    return declares_path(additional, path[1:]) if isinstance(additional, dict) else additional is not True


class Unknown(ValueError):
    """Indicate that the contract cannot be evaluated in the supported subset."""


@frozen
class Rejection(Exception):
    """
    Retain an evaluated rejection and the input evidence used to reach it.

    Attributes:
        source (str): Template containing the rejection sink.
        line (int): Source line containing fail or required.
        message (str): Explicit chart-authored rejection message.
        inputs (dict[str, object]): Values inspected by the contract, including related fields.
        conditions (tuple[str, ...]): Evaluated branch conditions and their outcomes.
        enums (dict[str, tuple[str, ...]]): Literal allowlists inspected on the rejecting branch.
        text (ContractText | None): Exact message including known unordered key-list fragments.
        declared_schema (bool): The rejecting input belongs to an explicitly declared child schema.
    """

    source: str
    line: int
    message: str
    inputs: dict[str, object]
    conditions: tuple[str, ...]
    enums: dict[str, tuple[str, ...]] = field(factory=dict)
    text: ContractText | None = None
    declared_schema: bool = False

    @property
    def key(self) -> str:
        """
        Identify a rejection independently of candidate values.

        Returns:
            str: Stable source/message fingerprint within this loaded chart.
        """
        domain = json.dumps(self.enums, sort_keys=True) if self.enums else self.message
        return hashlib.sha256(f"{self.source}:{self.line}:{domain}".encode()).hexdigest()[:16]

    def report(self) -> dict[str, object]:
        """
        Export contract evidence separately from manifest failures.

        Returns:
            dict[str, object]: Source, requirement text, evaluated conditions, and joint values.
        """
        return {
            "id": self.key,
            "source": self.source,
            "line": self.line,
            "requirement": self.message.strip(),
            "inputs": dict(reversed(list(self.inputs.items()))),
            "conditions": list(self.conditions),
            "enums": {path: list(values) for path, values in self.enums.items()},
        }


@lru_cache(maxsize=8192)
def expression(source: str) -> object:
    """
    Parse prefix calls, parenthesized arguments, and pipelines into nested tuples.

    Args:
        source (str): One Go-template expression.

    Returns:
        object: Literal token or a nested call tuple.

    Raises:
        Unknown: Tokens or parentheses are malformed.
    """
    tokens = TOKENS.findall(source)
    position = 0

    def pipeline() -> object:
        """
        Parse calls until a parenthesis or the end of the expression.

        Returns:
            object: Nested expression with pipeline arguments appended last.
        """
        nonlocal position
        result: object = None
        while True:
            parts: list[object] = []
            while position < len(tokens) and tokens[position] not in (")", "|"):
                token = tokens[position]
                position += 1
                if token == "(":
                    item = pipeline()
                    if position >= len(tokens) or tokens[position] != ")":
                        raise Unknown("unbalanced expression")
                    position += 1
                    parts.append(item)
                else:
                    parts.append(token)
            if not parts:
                raise Unknown("empty expression")
            if result is not None:
                parts.append(result)
            result = parts[0] if len(parts) == 1 else tuple(parts)
            if position >= len(tokens) or tokens[position] != "|":
                return result
            position += 1

    result = pipeline()
    if position != len(tokens):
        raise Unknown("trailing expression")
    return result


def calls(expr: object) -> set[str]:
    """
    Traverse expression call nodes, ignoring string literals and comments.

    Args:
        expr (object): Parsed expression AST.

    Returns:
        set[str]: Function names and statically named helper-call edges.
    """
    if not isinstance(expr, tuple) or not expr:
        return set()
    result = {str(expr[0])}
    if expr[0] == "include" and len(expr) == 3 and isinstance(expr[1], str) and expr[1].startswith('"'):
        try:
            result.add("include:" + json.loads(expr[1]))
        except (ValueError, TypeError):
            pass
    for argument in expr[1:]:
        result.update(calls(argument))
    return result


@define
class Contracts:
    """
    Hold parsed local helpers and root templates with explicit rejection sinks.

    Attributes:
        helpers (dict[str, tuple[str, tuple[Node, ...]]]): Unique local helper definitions.
        roots (dict[str, tuple[Node, ...]]): Executed chart templates, excluding partials.
        relevant (set[str]): Helpers transitively containing explicit rejection calls.
        diagnostics (list[str]): Unsupported or ambiguous source constructs.
        dependencies (Dependencies): Child namespaces and activation conditions.
        scopes (dict[str, tuple[str, ...]]): Values namespace for each root template.
        schemas (dict[tuple[str, ...], object]): Original authored schemas indexed by chart namespace.
    """

    helpers: dict[str, tuple[str, tuple[Node, ...]]] = field(factory=dict)
    roots: dict[str, tuple[Node, ...]] = field(factory=dict)
    relevant: set[str] = field(factory=set)
    diagnostics: list[str] = field(factory=list)
    dependencies: Dependencies = field(factory=Dependencies)
    scopes: dict[str, tuple[str, ...]] = field(factory=dict)
    schemas: dict[tuple[str, ...], object] = field(factory=dict)

    @classmethod
    def build(cls, chart: Path) -> Contracts:
        """
        Parse local helpers conservatively; duplicate definitions remain unresolved.

        Args:
            chart (Path): Prepared chart directory.

        Returns:
            Contracts: Immutable source nodes with explicit unsupported-source diagnostics.
        """
        result = cls(dependencies=Dependencies.build(chart))
        if (chart / "values.schema.json").is_file():
            result.schemas[()] = json.loads((chart / "values.schema.json").read_text())
        duplicates: set[str] = set()
        sources: list[tuple[str, tuple[Node, ...], tuple[str, ...]]] = []
        for path in sorted((chart / "templates").rglob("*")):
            if not path.is_file():
                continue
            source = path.relative_to(chart).as_posix()
            try:
                nodes = lower(path.read_text())
            except (ValueError, UnicodeError, RecursionError) as exc:
                result.diagnostics.append(f"{source}: {exc}")
                continue
            sources.append((source, nodes, ()))
        for dependency in result.dependencies.nodes:
            sources.extend((source, nodes, dependency.path) for source, nodes in dependency.syntax)
            if dependency.declared_schema:
                result.schemas[dependency.path] = dependency.schema
        for source, nodes, scope in sources:
            for node in nodes:
                match = re.fullmatch(r'define\s+"([^"\\]+)"', node.text) if node.kind == "opaque" else None
                if match:
                    name = match[1]
                    if name in result.helpers and result.helpers[name][1] != node.children:
                        duplicates.add(name)
                    result.helpers[name] = (source, node.children)
            if not Path(source).name.startswith("_"):
                result.roots[source] = tuple(node for node in nodes if not node.text.startswith("define "))
                result.scopes[source] = scope
        for name in duplicates:
            result.helpers.pop(name, None)
            result.diagnostics.append(f"Duplicate helper left unresolved: {name}")
        for _ in range(len(result.helpers) + 1):
            previous = set(result.relevant)
            for name, (_, nodes) in result.helpers.items():
                if result.interesting(nodes):
                    result.relevant.add(name)
            if result.relevant == previous:
                break
        result.roots = {name: nodes for name, nodes in result.roots.items() if result.interesting(nodes)}
        return result

    def interesting(self, nodes: tuple[Node, ...]) -> bool:
        """
        Locate explicit rejection expressions or calls into relevant helpers.

        Args:
            nodes (tuple[Node, ...]): Current template region.

        Returns:
            bool: Whether the region may execute a recognized rejection contract.
        """
        for node in walk(nodes):
            if node.kind == "text":
                continue
            assignment = ASSIGNMENT.fullmatch(node.text)
            try:
                found = calls(expression(assignment[3] if assignment else node.text))
            except (Unknown, RecursionError):
                continue
            if found & {"fail", "required"} or any("include:" + name in found for name in self.relevant):
                return True
        return False

    def predict(self, values: dict[str, object]) -> Rejection | None:
        """
        Evaluate supported contracts; unknown expressions never establish a rejection.

        Args:
            values (dict[str, object]): Effective coalesced Helm values.

        Returns:
            Rejection | None: Evaluated rejection, or no established rejection.
        """
        effective = self.dependencies.context({}, values)
        states = self.dependencies.states({}, values)
        for source, nodes in self.roots.items():
            scope = self.scopes.get(source, ())
            if scope and states.get(scope) is not True:
                continue
            local = lookup(effective, scope)
            if not isinstance(local, dict):
                continue
            evaluator = Evaluation(self, effective, context={"Values": BoundValue(local, scope)}, scope=scope)
            try:
                for node in walk(nodes):
                    if node.kind == "emit":
                        assignment = ASSIGNMENT.fullmatch(node.text)
                        functions = calls(expression(assignment[3] if assignment else node.text))
                        if functions & {"set", "unset", "merge", "mergeOverwrite", "tpl"}:
                            raise Unknown("root template can mutate or dynamically evaluate its context")
                evaluator.visit(nodes, source, {}, strict=False)
            except Rejection as rejection:
                declared = (
                    any(
                        path[: len(namespace)] == namespace and declares_path(schema, path[len(namespace) :])
                        for name in rejection.enums
                        for path in (tuple(name.removeprefix("$.").split(".")),)
                        for namespace, schema in self.schemas.items()
                    )
                    if rejection.enums
                    else any(scope[: len(namespace)] == namespace for namespace in self.schemas)
                )
                if declared:
                    return Rejection(
                        rejection.source,
                        rejection.line,
                        rejection.message,
                        rejection.inputs,
                        rejection.conditions,
                        rejection.enums,
                        rejection.text,
                        True,
                    )
                return rejection
            except (Unknown, TypeError, KeyError, IndexError, OverflowError, RecursionError):
                continue
        return None


@define
class Evaluation:
    """
    Evaluate a closed validator subset with candidate-local variables and evidence.

    Attributes:
        contracts (Contracts): Parsed source and helper definitions.
        values (dict[str, object]): Effective chart input.
        inputs (dict[str, object]): Inspected concrete values paths.
        conditions (list[str]): Conditions traversed by the validator.
        depth (int): Bounded helper recursion depth.
        context (object): Current helper argument; dollar and dot reset together at each include.
        enums (dict[str, tuple[str, ...]]): Literal allowlists observed on active rejecting conditions.
        scope (tuple[str, ...]): Chart namespace used to reject ambiguous global forwarding.
    """

    contracts: Contracts
    values: dict[str, object]
    inputs: dict[str, object] = field(factory=dict)
    conditions: list[str] = field(factory=list)
    depth: int = 0
    context: object = None
    enums: dict[str, tuple[str, ...]] = field(factory=dict)
    scope: tuple[str, ...] = ()

    def resolve(self, expression: str, variables: dict[str, object]) -> object:
        """
        Resolve dot, dollar and lexical aliases while retaining the original values path.

        Args:
            expression (str): Direct context or variable access.
            variables (dict[str, object]): Current lexical bindings.

        Returns:
            object: Literal or path-bound candidate value.

        Raises:
            Unknown: Lookup requires an unsupported context, field name or parent.
        """
        context = self.context if self.context is not None else {"Values": BoundValue(self.values, ())}
        if expression in (".", "$"):
            return context
        parts = expression.split(".")
        head = parts.pop(0)
        if head in ("", "$"):
            current = context
        elif head in variables:
            current = variables[head]
        else:
            raise Unknown("unbound variable")
        for index, key in enumerate(parts):
            container = native(current)
            if not isinstance(container, dict) or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", key):
                raise Unknown("unsupported context lookup")
            if key not in container and index != len(parts) - 1:
                raise Unknown("missing parent context lookup")
            current = BoundValue(container.get(key), (*current.path, key)) if isinstance(current, BoundValue) else container.get(key)
        if isinstance(current, BoundValue) and current.path:
            if self.scope and current.path[: len(self.scope) + 1] == (*self.scope, "global"):
                raise Unknown("forwarded global input origins are unresolved")
            self.inputs["$." + ".".join(current.path)] = current.value
        return current

    def evaluate(self, expr: object, source: str, line: int, variables: dict[str, object]) -> object:
        """
        Evaluate supported expressions using Helm-compatible scalar and string semantics.

        Args:
            expr (object): Parsed expression tree.
            source (str): Template filename for diagnostics.
            line (int): Template line for diagnostics.
            variables (dict[str, object]): Lexically visible local bindings.

        Returns:
            object: Evaluated scalar, list, or helper output.

        Raises:
            Unknown: An expression, conversion, context, or function is unsupported.
            Rejection: An explicit fail or required call rejects this input.
        """
        if isinstance(expr, str):
            if expr.startswith((".", "$")):
                return self.resolve(expr, variables)
            if expr.startswith('"'):
                try:
                    return json.loads(expr)
                except ValueError as exc:
                    raise Unknown("unsupported quoted literal") from exc
            if expr.startswith("`") and expr.endswith("`"):
                return expr[1:-1]
            if expr in ("true", "false"):
                return expr == "true"
            if re.fullmatch(r"-?\d+", expr):
                return int(expr)
            if expr in variables:
                return variables[expr]
            if expr == "list":
                return ConstantList(())
            if expr == "nil":
                return None
            raise Unknown(f"unsupported expression: {expr}")
        if not isinstance(expr, tuple) or not expr:
            raise Unknown("invalid expression")
        function, *arguments = expr
        if function == "include":
            if len(arguments) != 2:
                raise Unknown("include requires a name and context")
            name = self.evaluate(arguments[0], source, line, variables)
            if not isinstance(name, str) or name not in self.contracts.helpers or self.depth >= 16:
                raise Unknown("unknown or recursive include")
            helper_source, nodes = self.contracts.helpers[name]
            context = self.evaluate(arguments[1], source, line, variables)
            if not isinstance(native(context), dict):
                raise Unknown("include requires a supported map context")
            previous_context = self.context
            self.context = context
            self.depth += 1
            try:
                return self.visit(nodes, helper_source, {}, strict=True)
            finally:
                self.depth -= 1
                self.context = previous_context
        if function in ("and", "or"):
            if not arguments:
                raise Unknown("empty boolean call")
            result: object = None
            for argument in arguments:
                result = self.evaluate(argument, source, line, variables)
                if bool(native(result)) == (function == "or"):
                    break
            return result
        evaluated = [self.evaluate(argument, source, line, variables) for argument in arguments]
        args = [native(value) for value in evaluated]
        if function == "fail" and len(args) == 1 and isinstance(args[0], str):
            text = evaluated[0] if isinstance(evaluated[0], ContractText) else None
            raise Rejection(source, line, args[0], dict(self.inputs), tuple(self.conditions), dict(self.enums), text)
        if function == "required" and len(args) == 2 and isinstance(args[0], str):
            # Helm's required accepts false and zero; only nil and empty strings reject.
            if args[1] is None or args[1] == "":
                raise Rejection(source, line, args[0], dict(self.inputs), tuple(self.conditions))
            return args[1]
        if function in ("not", "empty") and len(args) == 1:
            return not bool(args[0])
        if function in ("eq", "ne", "lt", "le", "gt", "ge") and len(args) == 2:
            first, second = args
            if type(first) is not type(second) or type(first) not in (str, bool, int):
                raise Unknown("unsupported comparison types")
            if type(first) is bool and function not in ("eq", "ne"):
                raise Unknown("ordered Boolean comparison")
            assert isinstance(first, str | int) and isinstance(second, str | int)
            return {"eq": eq, "ne": ne, "lt": lt, "le": le, "gt": gt, "ge": ge}[str(function)](first, second)
        if function == "int" and len(args) == 1 and type(args[0]) is int:
            return args[0]
        if function == "list":
            if all(isinstance(item, str) and item.startswith(('"', "`")) for item in arguments):
                return ConstantList(tuple(str(value) for value in args))
            return evaluated
        if function == "dict" and len(args) % 2 == 0 and all(isinstance(key, str) for key in args[::2]):
            entries = {str(args[index]): evaluated[index + 1] for index in range(0, len(args), 2)}
            if all(isinstance(item, str) and item.startswith(('"', "`")) for item in arguments[::2]):
                return ConstantMap(entries)
            return entries
        if function == "hasKey" and len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], str):
            present = args[1] in args[0]
            if not present and isinstance(evaluated[0], ConstantMap) and isinstance(evaluated[1], BoundValue):
                self.enums["$." + ".".join(evaluated[1].path)] = tuple(sorted(args[0]))
            return present
        if function in ("has", "mustHas") and len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], list):
            if not all(isinstance(item, str) for item in args[1]):
                raise Unknown("membership requires a string list")
            present = args[0] in args[1]
            if not present and isinstance(evaluated[0], BoundValue) and isinstance(evaluated[1], ConstantList):
                self.enums["$." + ".".join(evaluated[0].path)] = tuple(sorted(set(evaluated[1].values)))
            return present
        if function == "keys" and len(args) == 1 and isinstance(args[0], dict) and all(isinstance(key, str) for key in args[0]):
            return UnorderedKeys(tuple(args[0]))
        if function == "sortAlpha" and len(args) == 1 and isinstance(args[0], list) and all(isinstance(item, str) for item in args[0]):
            return sorted(args[0])
        if function in ("index", "get") and len(args) == 2 and isinstance(args[0], dict) and isinstance(args[1], str):
            if isinstance(evaluated[0], BoundValue):
                path = (*evaluated[0].path, args[1])
                value = args[0].get(args[1], "" if function == "get" else None)
                self.inputs["$." + ".".join(path)] = value
                return BoundValue(value, path)
            return args[0].get(args[1], "" if function == "get" else None)
        if function == "append" and len(args) == 2 and isinstance(args[0], list):
            return [*args[0], args[1]]
        if function == "without" and args and isinstance(args[0], list):
            return [item for item in args[0] if item not in args[1:]]
        if function == "join" and len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], list):
            if all(isinstance(item, str) for item in args[1]):
                if isinstance(evaluated[1], UnorderedKeys):
                    return ContractText((KeyList(args[0], evaluated[1].values),))
                return args[0].join(args[1])
        if function == "printf" and args and isinstance(args[0], str) and all(isinstance(item, str) for item in args[1:]):
            if args[0].count("%s") == len(args) - 1 and "%" not in args[0].replace("%s", ""):
                parts: list[str | KeyList] = []
                literals = args[0].split("%s")
                for literal, value in zip(literals, evaluated[1:], strict=False):
                    parts.append(literal)
                    parts.extend(value.parts if isinstance(value, ContractText) else (str(native(value)),))
                parts.append(literals[-1])
                return (
                    ContractText(tuple(parts)) if any(isinstance(part, KeyList) for part in parts) else "".join(str(part) for part in parts)
                )
        raise Unknown(f"unsupported function: {function}")

    def visit(self, nodes: tuple[Node, ...], source: str, variables: dict[str, object], *, strict: bool) -> str:
        """
        Execute validator nodes, refusing unsupported scopes and helper statements.

        Args:
            nodes (tuple[Node, ...]): Template region to evaluate.
            source (str): Source filename.
            variables (dict[str, object]): Local variables, copied when entering branches.
            strict (bool): Require every helper statement; root output is outside the contract.

        Returns:
            str: Exact supported helper text, including whitespace.

        Raises:
            Unknown: An executed validator construct cannot be interpreted.
        """
        output = []
        for node in nodes:
            if node.kind == "text":
                output.append(node.text)
                continue
            assignment = ASSIGNMENT.fullmatch(node.text)
            if not strict and not assignment and not self.contracts.interesting((node,)):
                continue
            if node.kind == "if":
                previous_enums = dict(self.enums)
                condition = self.evaluate(expression(node.text), source, node.line, variables)
                self.conditions.append(f"{source}:{node.line}: {node.text} => {bool(native(condition))}")
                output.append(self.visit(node.children if native(condition) else node.otherwise, source, dict(variables), strict=strict))
                self.enums = previous_enums
            elif node.kind == "emit":
                if assignment:
                    if assignment[2] != ":=":
                        raise Unknown("mutation of outer variable")
                    try:
                        variables[assignment[1]] = self.evaluate(expression(assignment[3]), source, node.line, variables)
                    except Unknown:
                        variables.pop(assignment[1], None)
                        if strict:
                            raise
                else:
                    value = native(self.evaluate(expression(node.text), source, node.line, variables))
                    if type(value) not in (str, int, bool):
                        raise Unknown("unsupported output type")
                    output.append(str(value).lower() if type(value) is bool else str(value))
            else:
                raise Unknown("unsupported control flow")
        return "".join(output)
