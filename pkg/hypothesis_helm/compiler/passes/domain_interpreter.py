"""
Follow helper arguments and lexical bindings into symbolic manifest output.
"""

from __future__ import annotations

import copy
import json

from attrs import define, field

from hypothesis_helm.charts.model import _schema_nodes
from hypothesis_helm.compiler.asts.contract_maps import dictionary
from hypothesis_helm.compiler.asts.contract_scope import UNRESOLVED, Scope
from hypothesis_helm.compiler.asts.contracts import ASSIGNMENT, RANGE_ASSIGNMENT, Contracts, FieldAccess, context_effects, expression
from hypothesis_helm.compiler.asts.projections import Collection, Input, LocalMap, Member, Operation, Piece, output
from hypothesis_helm.compiler.asts.templates import Node, walk
from hypothesis_helm.compiler.asts.transformations import FUNCTIONS, calculate
from hypothesis_helm.compiler.builtins import MUTATIONS
from hypothesis_helm.compiler.passes.domain_collections import additions, members, truth
from hypothesis_helm.exceptions.compiler import Unknown, UnsupportedTransformation

__all__ = ("Interpreter", "emits", "fresh")


@define
class Interpreter:
    """
    Build bounded symbolic output while keeping unsupported expressions explicit.

    Attributes:
        contracts (Contracts): Shared parsed helpers and compiler budgets.
        schema (dict[str, object]): Effective values types in the root namespace.
        notes (list[dict[str, object]]): Unsupported constructs with source locations.
        steps (int): Work already spent expanding the current root template.
        stack (tuple[str, ...]): Active helper names, for cycle detection.
        mutated (bool): An input or unknown shared context may have been modified.
        alternatives (dict[str, list[tuple[str, tuple[Node, ...]]]]): Possible definitions of conflicting helper names.
    """

    contracts: Contracts
    schema: dict[str, object]
    notes: list[dict[str, object]] = field(factory=list)
    steps: int = 0
    stack: tuple[str, ...] = ()
    mutated: bool = False
    alternatives: dict[str, list[tuple[str, tuple[Node, ...]]]] = field(factory=dict)

    def select(self, value: object, fields: tuple[str, ...]) -> object:
        """
        Select fields while retaining their absolute input origin.

        Args:
            value (object): Symbolic receiver or helper argument map.
            fields (tuple[str, ...]): Selected field names.

        Returns:
            object: Input reference, literal, or explicit unresolved selection.
        """
        for key in fields:
            if isinstance(value, Input):
                if key == "global" and any(node.path == value.path for node in self.contracts.dependencies.nodes):
                    value = Operation("forwarded-global", (value,))
                else:
                    value = Input((*value.path, key))
            elif isinstance(value, LocalMap) and not value.sources:
                value = value.entries.get(key)
            elif isinstance(value, dict):
                value = value.get(key)
            elif isinstance(value, Operation) and value.name == "choose":
                test, yes, no = value.arguments
                value = Operation("choose", (test, self.select(yes, (key,)), self.select(no, (key,))))
            else:
                value = Operation("get", (value, key))
        return value

    def evaluate(self, expr: object, context: object, scope: Scope) -> object:
        """
        Resolve known operations without inventing values for unsupported ones.

        Args:
            expr (object): Parsed Helm expression.
            context (object): Current dot context.
            scope (Scope): Lexical variables, including the invocation's dollar root.

        Returns:
            object: Symbolic transformation, origin, literal, or fresh local collection.

        Raises:
            Unknown: Helper expansion exceeds its budget or source is ambiguous.
        """
        if isinstance(expr, FieldAccess):
            return self.select(self.evaluate(expr.receiver, context, scope), expr.fields)
        if isinstance(expr, str):
            if expr.startswith('"'):
                return json.loads(expr)
            if expr.startswith("`") and expr.endswith("`"):
                return expr[1:-1]
            if expr in {"true", "false", "nil"}:
                return {"true": True, "false": False, "nil": None}[expr]
            if expr.lstrip("-").isdigit():
                return int(expr)
            if expr == "dict":
                return LocalMap()
            if expr == "list":
                return []
            if expr in {".", "$"}:
                return context if expr == "." else scope.lookup("$")
            if expr.startswith((".", "$")):
                head, *parts = expr.split(".")
                return self.select(context if head == "" else scope.lookup(head), tuple(parts))
            return Operation(expr)
        if not isinstance(expr, tuple) or not expr:
            return Operation("unknown")
        name = str(expr[0])
        args = tuple(self.evaluate(arg, context, scope) for arg in expr[1:])
        if name in {"include", "template"} and len(args) == 2:
            helper, argument = args
            if not isinstance(helper, str) or helper in self.stack:
                self.mutated = True
                self.notes.append({"reason": "helper is dynamic or recursive; shared-context effects unresolved"})
                return Operation("unresolved", ("helper is dynamic or recursive",))
            options = self.alternatives.get(helper, [])
            if helper in self.contracts.helpers:
                options = [self.contracts.helpers[helper]]
            elif helper in self.contracts.templates:
                options = [(helper, self.contracts.templates[helper])]
            if not options:
                self.mutated = True
                self.notes.append({"reason": "helper is missing or ambiguous; shared-context effects unresolved"})
                return Operation("unresolved", ("helper is missing or ambiguous",))
            if len(self.stack) >= self.contracts.max_call_depth:
                self.mutated = True
                self.notes.append({"reason": f"helper call depth exceeds compiler limit {self.contracts.max_call_depth}"})
                return Operation("unresolved", (f"helper call depth exceeds compiler limit {self.contracts.max_call_depth}",))
            if len(options) > self.contracts.limits["max_symbolic_variants"]:
                raise Unknown("helper alternatives exceed compiler.max_symbolic_variants")
            self.stack = (*self.stack, helper)
            try:
                outputs = []
                for source, nodes in options:
                    local = copy.deepcopy(argument) if len(options) > 1 else argument
                    outputs.append(output(self.visit(nodes, source, local, Scope({"$": local}))))
                    if len(options) > 1 and local != argument:
                        self.mutated = True
                result = outputs[-1]
                for choice in reversed(outputs[:-1]):
                    if choice != result:
                        result = Operation("choose", (Operation("unknown-helper-selection"), choice, result))
                if isinstance(result, str):
                    return result
                if type(result) in {bool, int, float}:
                    return json.dumps(result)
                if isinstance(result, Input):
                    kinds = {
                        node.get("type")
                        for node in _schema_nodes(self.schema, result.path, self.schema)
                        if isinstance(node.get("type"), str)
                    }
                    if kinds == {"string"}:
                        return result
                return Operation("render-text", (result,))
            finally:
                self.stack = self.stack[:-1]
        if name == "dict":
            try:
                return LocalMap(dictionary(tuple(args)))
            except UnsupportedTransformation as exc:
                raise Unknown(str(exc)) from exc
        if name == "list":
            return list(args)
        if name in {"append", "mustAppend"} and len(args) == 2:
            return Operation(name, args)
        if name in {"uniq", "mustUniq"} and len(args) == 1:
            return Operation(name, args)
        if name == "empty" and len(args) == 1 and members(args[0]) is not None:
            return Operation("not", (truth(args[0]),))
        if name in {"index", "get"} and len(args) == 2 and isinstance(args[1], str):
            return self.select(args[0], (args[1],))
        if name in {"merge", "mustMerge", "mergeOverwrite", "mustMergeOverwrite"} and args:
            target = args[0]
            if fresh(target):
                target = LocalMap(sources=[target])
            if not isinstance(target, LocalMap):
                self.mutated = True
                return Operation("unknown-mutation")
            target.sources.extend(copy.deepcopy(args[1:]))
            return target
        if name == "set" and len(args) == 3 and isinstance(args[0], LocalMap) and isinstance(args[1], str):
            args[0].entries[args[1]] = args[2]
            return args[0]
        if name in {"set", "unset"} and args and fresh(args[0]):
            return Operation("unknown-local-mutation", args)
        if name in MUTATIONS:
            self.mutated = True
            return Operation("unknown-mutation")
        if name in {"kindIs", "typeIs"} and len(args) == 2 and isinstance(args[1], Operation):
            if args[1].name in {"toYaml", "toJson", "quote", "tpl", "render-text"} and args[0] in {"string", "map", "slice", "bool"}:
                return args[0] == "string"
        if name in {"print", "toString"} and len(args) == 1:
            return args[0] if isinstance(args[0], str) else Operation("string-identity", args)
        if name == "printf" and len(args) == 2 and args[0] == "%s":
            return Operation("string-identity", args[1:])
        if name in {"kindIs", "typeIs"} and len(args) == 2 and isinstance(args[1], Input):
            kinds = {
                node.get("type") for node in _schema_nodes(self.schema, args[1].path, self.schema) if isinstance(node.get("type"), str)
            }
            names = {"string": "string", "bool": "boolean"}
            if name == "kindIs":
                names.update(map="object", slice="array")
            wanted = names.get(str(args[0]))
            if wanted is not None and kinds:
                if kinds == {wanted}:
                    return True
                if wanted not in kinds:
                    return False
        if name in {"default", "coalesce"} and len(args) >= 2:
            choices = args if name == "coalesce" else (args[1], args[0])
            result = choices[-1]
            for value in reversed(choices[:-1]):
                result = Operation("choose", (Operation("truth", (value,)), value, result))
            return result
        if name == "ternary" and len(args) == 3:
            return args[0 if args[2] else 1] if type(args[2]) is bool else Operation("choose", (args[2], args[0], args[1]))
        if name in {"fromYaml", "fromJson", "deepCopy", "mustDeepCopy", "pick", "omit"}:
            return Operation(name, args)
        if name == "not" and len(args) == 1 and (args[0] is None or type(args[0]) in {str, bool, int}):
            return not args[0]
        if name in {"eq", "ne"} and len(args) == 2 and all(value is None or type(value) in {str, bool, int} for value in args):
            same = type(args[0]) is type(args[1]) and args[0] == args[1]
            return same if name == "eq" else not same
        if name in FUNCTIONS and all(value is None or type(value) in {str, bool, int, float} for value in args):
            try:
                return calculate(name, args, limits=self.contracts.limits)
            except UnsupportedTransformation:
                pass
        return Operation(name, args)

    def collection_range(self, node: Node, values: object, source: str, context: object, scope: Scope) -> list[Piece]:
        """
        Analyze representative items while summarizing only proven append-only recurrences.

        Args:
            node (Node): Range block whose runtime collection size is unknown.
            values (object): Input array or supported local collection expression.
            source (str): Template source for diagnostics.
            context (object): Dot context outside the loop.
            scope (Scope): Enclosing lexical bindings.

        Returns:
            list[Piece]: Guarded representative output, without enumerating the array's values.

        Raises:
            Unknown: Collection type, loop control or analysis budget is unsupported.
        """
        nonempty = truth(values)
        candidates = members(values)
        if isinstance(values, Input):
            kinds = {item.get("type") for item in _schema_nodes(self.schema, values.path, self.schema) if isinstance(item.get("type"), str)}
            if kinds == {"array"}:
                candidates = (Member(Input((*values.path, "*"))),)
        if candidates is None:
            raise Unknown("projection range requires an array with established element origins")
        if len(candidates) > self.contracts.limits["max_range_items"]:
            raise Unknown("collection origins exceed compiler.max_range_items")
        binding = RANGE_ASSIGNMENT.fullmatch(node.text.removeprefix("range "))
        escaping_else = any((assignment := ASSIGNMENT.fullmatch(child.text)) and assignment[2] == "=" for child in walk(node.otherwise))
        if binding and binding[3] == "=" or escaping_else or any(child.text in {"break", "continue"} for child in walk(node.children)):
            raise Unknown("symbolic range control or escaping iteration bindings require review")
        # Snapshot outer bindings so an unknown-length loop never leaves behind
        # the apparent result of executing exactly one iteration.
        owners = []
        owner: Scope | None = scope
        while owner is not None:
            owners.append((owner, copy.deepcopy(owner.bindings)))
            owner = owner.parent
        body = []
        for member in candidates:
            previous_bindings = [(owner, copy.deepcopy(owner.bindings)) for owner, _ in owners]
            local = Scope(parent=scope)
            if binding:
                names = [key for key in (binding[1], binding[2]) if key]
                operands = (Operation("iteration-index"), member.value) if len(names) == 2 else (member.value,)
                for key, item in zip(names, operands, strict=True):
                    local.bind(key, item)
            selected = output(self.visit(node.children, source, member.value, local))
            for condition in reversed(member.conditions):
                selected = Operation("choose", (condition, selected, ""))
                for owner, before_bindings in previous_bindings:
                    for key, before_member in before_bindings.items():
                        if owner.bindings[key] != before_member:
                            owner.bindings[key] = Operation("choose", (condition, owner.bindings[key], before_member))
            body.append(Piece(selected, source, node.line))
        for owner, before in owners:
            for key, previous in before.items():
                current = owner.bindings[key]
                if current == previous:
                    continue
                delta = additions(previous, current)
                initial = members(previous)
                if delta is None or initial is None:
                    owner.bindings[key] = Operation("unknown-loop-assignment")
                    self.notes.append(
                        {"file": source, "line": node.line, "reason": f"non-append loop assignment to {key}; origin unresolved"}
                    )
                    continue
                added, definite = delta
                if len(initial) + len(added) > self.contracts.limits["max_range_items"]:
                    raise Unknown("collection origins exceed compiler.max_range_items")
                active = nonempty if definite else Operation("unknown-collection-cardinality")
                owner.bindings[key] = Collection((*initial, *added), Operation("or", (truth(previous), active)))
        otherwise = output(self.visit(node.otherwise, source, context, Scope(parent=scope))) if node.otherwise else ""
        return [Piece(Operation("choose", (nonempty, output(body), otherwise)), source, node.line)]

    def visit(self, nodes: tuple[Node, ...], source: str, context: object, scope: Scope) -> list[Piece]:
        """
        Expand lexical control flow into symbolic output choices.

        Args:
            nodes (tuple[Node, ...]): Current template or helper body.
            source (str): Source filename for retained locations.
            context (object): Current dot context.
            scope (Scope): Owning lexical scope.

        Returns:
            list[Piece]: Ordered output segments; unrelated unsupported expressions remain local.

        Raises:
            Unknown: Expansion exceeds the chart's inspection budget.
        """
        pieces: list[Piece] = []
        for node in nodes:
            self.steps += 1
            if self.steps > self.contracts.limits["max_discovery_nodes"]:
                raise Unknown(f"projection exceeds compiler.max_discovery_nodes={self.contracts.limits['max_discovery_nodes']}")
            if "HHINPUTDOMAINMARKER" in node.text:
                raise Unknown("reserved analysis marker occurs in source")
            if node.kind == "text":
                pieces.append(Piece(node.text, source, node.line))
                continue
            if node.kind == "opaque" and node.text.startswith("define "):
                continue
            try:
                if node.kind == "if" or node.kind == "opaque" and node.text.startswith("with "):
                    changed_dot = node.kind == "opaque"
                    test = self.evaluate(expression(node.text[5:] if changed_dot else node.text), context, scope)
                    nested = test if changed_dot else context
                    if isinstance(test, Collection) or isinstance(test, Operation) and members(test) is not None:
                        test = truth(test)
                    if test is None or type(test) in {str, int, list, dict}:
                        test = bool(test)
                    elif isinstance(test, LocalMap) and not test.sources:
                        test = bool(test.entries)
                    if type(test) is bool:
                        pieces.extend(
                            self.visit(node.children if test else node.otherwise, source, nested if test else context, Scope(parent=scope))
                        )
                    else:
                        if self.contracts.limits["max_symbolic_variants"] < 2:
                            raise Unknown("branch join exceeds compiler.max_symbolic_variants=1")
                        copies = [copy.deepcopy((scope, nested, context)) for _ in range(2)]
                        branches = [item[0] for item in copies]
                        yes = output(self.visit(node.children, source, copies[0][1], Scope(parent=branches[0])))
                        no = output(self.visit(node.otherwise, source, copies[1][2], Scope(parent=branches[1])))
                        if isinstance(context, LocalMap):
                            left, right = copies[0][2], copies[1][2]
                            if isinstance(left, LocalMap) and isinstance(right, LocalMap):
                                if left.sources == right.sources:
                                    context.entries = {
                                        key: a if a == b else Operation("choose", (test, a, b))
                                        for key in sorted(left.entries.keys() | right.entries.keys())
                                        for a, b in [(left.entries.get(key), right.entries.get(key))]
                                    }
                                else:
                                    context.entries = {}
                                    context.sources = [Operation("choose", (test, left, right))]
                        current: Scope | None = scope
                        owners: list[Scope | None] = list(branches)
                        while current is not None:
                            for key in current.bindings:
                                a, b = (owner.bindings.get(key, UNRESOLVED) if owner else UNRESOLVED for owner in owners)
                                if a is not UNRESOLVED and b is not UNRESOLVED:
                                    current.bindings[key] = a if a == b else Operation("choose", (test, a, b))
                            current = current.parent
                            owners = [owner.parent if owner else None for owner in owners]
                        pieces.append(Piece(Operation("choose", (test, yes, no)), source, node.line))
                    continue
                if node.kind == "opaque" and node.text.startswith("range "):
                    body = node.text.removeprefix("range ")
                    binding = RANGE_ASSIGNMENT.fullmatch(body)
                    values = self.evaluate(expression(binding[4] if binding else body), context, scope)
                    if not isinstance(values, list):
                        pieces.extend(self.collection_range(node, values, source, context, scope))
                        continue
                    if not isinstance(values, list) or len(values) > self.contracts.limits["max_range_items"]:
                        raise Unknown("projection range requires a bounded literal list")
                    if not values:
                        pieces.extend(self.visit(node.otherwise, source, context, Scope(parent=scope)))
                    for index, value in enumerate(values):
                        local = Scope(parent=scope)
                        if binding:
                            names = [key for key in (binding[1], binding[2]) if key]
                            for key, item in zip(names, (index, value) if len(names) == 2 else (value,), strict=True):
                                local.bind(key, item, assign=binding[3] == "=")
                        pieces.extend(self.visit(node.children, source, value, local))
                    continue
                if node.kind == "opaque":
                    raise Unknown(f"unsupported projection block: {node.text}")
                assignment = ASSIGNMENT.fullmatch(node.text)
                parsed = expression(assignment[3] if assignment else node.text)
                value = self.evaluate(parsed, context, scope)
                if assignment:
                    scope.bind(assignment[1], value, assign=assignment[2] == "=")
                else:
                    pieces.append(Piece(copy.deepcopy(value), source, node.line))
            except (Unknown, KeyError, ValueError) as exc:
                self.notes.append({"file": source, "line": node.line, "reason": str(exc)})
                assignment = ASSIGNMENT.fullmatch(node.text)
                if assignment:
                    scope.bind(assignment[1], Operation("unknown"), assign=assignment[2] == "=")
                else:
                    # An unvisited body may assign an outer variable. Do not let
                    # its old value establish a destination after this block.
                    unvisited = (*node.children, *node.otherwise)
                    try:
                        self.mutated = self.mutated or context_effects(unvisited)
                    except Unknown:
                        self.mutated = True
                    for child in walk(unvisited):
                        binding = ASSIGNMENT.fullmatch(child.text)
                        if binding and binding[2] == "=" and scope.lookup(binding[1]) is not UNRESOLVED:
                            scope.bind(binding[1], Operation("unknown"), assign=True)
                    if emits(node):
                        pieces.append(Piece(Operation("unknown"), source, node.line))
        return pieces


def fresh(value: object) -> bool:
    """
    Recognize allocation boundaries so local map mutations do not taint the caller's values.

    Args:
        value (object): Symbolic collection being used as a mutation target.

    Returns:
        bool: Whether the operation allocates its own root map.
    """
    if not isinstance(value, Operation):
        return False
    if value.name in {"fromYaml", "fromJson", "deepCopy", "mustDeepCopy", "pick", "omit", "unknown-local-mutation"}:
        return True
    return value.name == "choose" and all(isinstance(child, LocalMap) or fresh(child) for child in value.arguments[1:])


def emits(node: Node) -> bool:
    """
    Distinguish unresolved bookkeeping loops from fragments that can emit manifest text.

    Args:
        node (Node): Unresolved statement or control-flow region.

    Returns:
        bool: Whether any reachable syntax can write non-whitespace output.
    """
    if node.kind == "text":
        return bool(node.text.strip())
    if node.kind == "emit":
        return ASSIGNMENT.fullmatch(node.text) is None
    return any(emits(child) for child in (*node.children, *node.otherwise))
