"""
Translate supported symbolic origins and branch predicates into generation constraints.
"""

import copy
import json
import re

from hypothesis_helm.compiler.asts.projections import Input, LocalMap, Operation, Piece, output
from hypothesis_helm.compiler.constants import COPIES
from hypothesis_helm.compiler.limits import active_limits
from hypothesis_helm.compiler.passes.domain_fragments import contribution, literal_region
from hypothesis_helm.compiler.passes.domain_guards import integer_comparison, rendered_truth, type_condition
from hypothesis_helm.schemas.configuration.policy import intersect
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("at", "combine", "constraints", "guard_bounds", "input_origins", "literal_domain", "normalize", "predicate")


def at(path: tuple[str, ...], schema: dict[str, object]) -> dict[str, object]:
    """
    Require a values path when expressing a predicate about its value.

    Args:
        path (tuple[str, ...]): Referenced input.
        schema (dict[str, object]): Leaf predicate.

    Returns:
        dict[str, object]: Predicate including existence of every parent.
    """
    result = copy.deepcopy(schema)
    for segment in reversed(path):
        result = (
            {"type": "array", "items": result}
            if segment == "*"
            else {"type": "object", "required": [segment], "properties": {segment: result}}
        )
    return result


def input_origins(value: object) -> set[tuple[str, ...]]:
    """
    Locate the input bindings involved in a symbolic condition.

    Args:
        value (object): Predicate or scalar expression.

    Returns:
        set[tuple[str, ...]]: Referenced paths, including representative array items.
    """
    if isinstance(value, Input):
        return {value.path}
    if isinstance(value, Operation):
        return set().union(*(input_origins(arg) for arg in value.arguments))
    return set()


def predicate(value: object, *, root: tuple[str, ...] = ()) -> dict[str, object] | None:
    """
    Express Go emptiness and supported Boolean operations without guessing unknown conditions.

    Args:
        value (object): Symbolic Boolean or value tested for truth.
        root (tuple[str, ...]): Item binding against which a local predicate is expressed.

    Returns:
        dict[str, object] | None: JSON Schema predicate, or an unresolved condition.
    """
    if value is None or type(value) in {str, int, float, bool}:
        return {} if value else {"not": {}}
    if isinstance(value, Input):
        if value.path[: len(root)] != root or "*" in value.path[len(root) :]:
            return None
        empty = {
            "anyOf": [
                {"enum": [None, False, 0, ""]},
                {"type": "array", "maxItems": 0},
                {"type": "object", "maxProperties": 0},
            ]
        }
        return at(value.path[len(root) :], {"not": empty})
    if not isinstance(value, Operation):
        return None
    name, args = value.name, value.arguments
    if name == "render-text" and len(args) == 1:
        return predicate(rendered_truth(args[0]), root=root)
    if name in {"kindIs", "typeIs"}:
        test = type_condition(value)
        if test != value:
            return predicate(test, root=root)
    if name in {"truth", "not", "empty"} and len(args) == 1:
        child = predicate(args[0], root=root)
        return child if name == "truth" else {"not": child} if child is not None else None
    if name == "choose" and len(args) == 3:
        condition, yes, no = (predicate(arg, root=root) for arg in args)
        if condition is None or yes is None or no is None:
            return None
        # Test the selected value, retaining the condition on the original map.
        # Coalescing a map does not independently coalesce each of its fields.
        return combine(
            [combine([condition, yes], conjunction=True), combine([{"not": condition}, no], conjunction=True)],
            conjunction=False,
        )
    if name in {"and", "or"}:
        children = [predicate(arg, root=root) for arg in args]
        if any(child is None for child in children):
            return None
        return {"allOf" if name == "and" else "anyOf": children}
    if name in {"eq", "ne"} and len(args) == 2:
        left, right = args
        if isinstance(right, Input):
            left, right = right, left
        if isinstance(left, Input) and (right is None or type(right) in {str, int, bool}):
            if left.path[: len(root)] != root or "*" in left.path[len(root) :]:
                return None
            path = left.path[len(root) :]
            result = at(path, {"const": right})
            if right is None:
                result = {"anyOf": [result, {"not": at(path, {})}]}
            return {"not": result} if name == "ne" else result
    if name in {"kindIs", "typeIs"} and len(args) == 2 and isinstance(args[1], Input):
        path = args[1].path
        kinds = {"string": "string", "bool": "boolean"}
        if name == "kindIs":
            kinds.update(map="object", slice="array")
        kind = kinds.get(str(args[0]))
        if kind and path[: len(root)] == root and "*" not in path[len(root) :]:
            return at(path[len(root) :], {"type": kind})
    if name in {"contains", "hasPrefix", "hasSuffix"} and len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], Input):
        if args[1].path[: len(root)] != root or "*" in args[1].path[len(root) :]:
            return None
        pattern = re.escape(args[0])
        pattern = "^" + pattern if name == "hasPrefix" else pattern + r"(?![\s\S])" if name == "hasSuffix" else pattern
        return at(args[1].path[len(root) :], {"type": "string", "pattern": pattern})
    return None


def guard_bounds(value: object) -> tuple[dict[str, object], dict[str, object]]:
    """
    Establish sufficient true and false regions when part of a Boolean condition is unknown.

    Args:
        value (object): Symbolic condition, possibly containing renderer-dependent operands.

    Returns:
        tuple[dict[str, object], dict[str, object]]: Disjoint sufficient truth and falsity predicates; neither covers uncertainty.
    """
    if isinstance(value, Operation):
        name, args = value.name, value.arguments
        numeric = integer_comparison(value)
        if numeric is not None:
            path, yes, no = numeric
            return (at(path, yes), at(path, no)) if "*" not in path else ({"not": {}}, {"not": {}})
        if name == "render-text" and len(args) == 1:
            return guard_bounds(rendered_truth(args[0]))
        if name in {"kindIs", "typeIs"}:
            test = type_condition(value)
            if test != value:
                return guard_bounds(test)
        if name in {"not", "empty", "truth"} and len(args) == 1:
            yes, no = guard_bounds(args[0])
            return (yes, no) if name == "truth" else (no, yes)
        if name == "choose" and len(args) == 3:
            exact = predicate(value)
            if exact is not None:
                return exact, {"not": exact}
            condition, yes_bounds, no_bounds = (guard_bounds(arg) for arg in args)
            regions = []
            for outcome in (0, 1):
                regions.append(
                    combine(
                        [
                            combine([condition[0], yes_bounds[outcome]], conjunction=True),
                            combine([condition[1], no_bounds[outcome]], conjunction=True),
                            # An unresolved selector is harmless only where both arms agree.
                            combine([yes_bounds[outcome], no_bounds[outcome]], conjunction=True),
                        ],
                        conjunction=False,
                    )
                )
            return regions[0], regions[1]
        if name in {"and", "or"} and args:
            children = [guard_bounds(arg) for arg in args]
            return (
                combine([pair[0] for pair in children], conjunction=name == "and"),
                combine([pair[1] for pair in children], conjunction=name != "and"),
            )
    known = predicate(value)
    if known is None:
        return {"not": {}}, {"not": {}}
    return known, {"not": known}


def combine(predicates: list[dict[str, object]], *, conjunction: bool) -> dict[str, object]:
    """
    Simplify Boolean schema constants without weakening their logical meaning.

    Args:
        predicates (list[dict[str, object]]): Boolean clauses over the values document.
        conjunction (bool): Require all clauses rather than any clause.

    Returns:
        dict[str, object]: A constant, single clause, or explicit conjunction/disjunction.
    """
    neutral: dict[str, object] = {} if conjunction else {"not": {}}
    absorbing: dict[str, object] = {"not": {}} if conjunction else {}
    if absorbing in predicates:
        return absorbing
    selected = [item for item in predicates if item != neutral]
    if not selected:
        return neutral
    return selected[0] if len(selected) == 1 else {"allOf" if conjunction else "anyOf": selected}


def literal_domain(schema: dict[str, object]) -> dict[str, object] | None:
    """
    Restrict a finite destination shape to values that tpl cannot interpret as template code.

    Args:
        schema (dict[str, object]): Self-contained downstream domain.

    Returns:
        dict[str, object] | None: Literal-only generation domain, or unknown for open recursive shapes.
    """
    result = copy.deepcopy(schema)
    kinds = result.get("type", [])
    kinds = [kinds] if isinstance(kinds, str) else sequence(kinds)
    if not kinds:
        return None
    if "string" in kinds:
        result = intersect(result, {"not": {"type": "string", "pattern": r"\{\{"}})
    if "object" in kinds:
        key_domain = {"not": {"pattern": r"\{\{"}}
        result["propertyNames"] = {"allOf": [result["propertyNames"], key_domain]} if "propertyNames" in result else key_domain
        for key in ("properties",):
            if isinstance(result.get(key), dict):
                children = {name: literal_domain(mapping(child)) for name, child in mapping(result[key]).items()}
                if any(child is None for child in children.values()):
                    return None
                result[key] = children
        extra = result.get("additionalProperties", True)
        if extra is True:
            return None
        if isinstance(extra, dict):
            child = literal_domain(mapping(extra))
            if child is None:
                return None
            result["additionalProperties"] = child
    if "array" in kinds:
        if not isinstance(result.get("items"), dict):
            return None
        child = literal_domain(mapping(result["items"]))
        if child is None:
            return None
        result["items"] = child
    return result


def normalize(value: object) -> object:
    """
    Remove reversible serialization boundaries while retaining tpl's literal-input obligation.

    Args:
        value (object): Symbolic output or intermediate map.

    Returns:
        object: Equivalent provenance expression for backward domain propagation.
    """
    if isinstance(value, Piece):
        return Piece(normalize(value.value), value.file, value.line)
    if not isinstance(value, Operation):
        return value
    args = tuple(normalize(arg) for arg in value.arguments)
    if value.name in COPIES and len(args) == 1:
        return args[0]
    if value.name == "text":
        pieces = [arg for arg in args if isinstance(arg, Piece)]
        return output(pieces)
    if value.name == "fromYaml" and len(args) == 1:
        child = args[0]
        if isinstance(child, Operation) and child.name == "render-text":
            return normalize(Operation("fromYaml", child.arguments))
        if isinstance(child, Operation) and child.name == "toYaml":
            return child.arguments[0]
        if isinstance(child, Operation) and child.name == "choose":
            test, yes, no = child.arguments
            return normalize(Operation("choose", (test, Operation("fromYaml", (yes,)), Operation("fromYaml", (no,)))))
        if isinstance(child, Operation) and child.name in {"tpl", "literal"}:
            return Operation("literal", (normalize(Operation("fromYaml", child.arguments[:1])),))
    if value.name == "choose" and len(args) == 3:
        test, yes, no = args
        known = predicate(test)
        if known == {}:
            return yes
        if known == {"not": {}}:
            return no
        if yes == no:
            return yes
        # tpl is the identity on the generated literal domain. Both branches
        # must refer to the same value; this never recognizes a helper by name.
        for templated, plain in ((yes, no), (no, yes)):
            if isinstance(templated, Operation) and templated.name in {"tpl", "literal"} and templated.arguments[0] == plain:
                return Operation("literal", (plain,))
    return Operation(value.name, args)


def constraints(
    value: object,
    schema: dict[str, object],
    *,
    guards: tuple[dict[str, object], ...] = (),
    conditions: tuple[object, ...] = (),
    quoted: bool = False,
    serialized: bool = False,
) -> list[dict[str, object]]:
    """
    Propagate destination requirements through supported transformations and branches.

    Args:
        value (object): Symbolic output expression.
        schema (dict[str, object]): Required downstream shape.
        guards (tuple[dict[str, object], ...]): Conditions selecting this output.
        conditions (tuple[object, ...]): Symbolic conditions, including item-local branch predicates.
        quoted (bool): The renderer converts this input into a quoted string.
        serialized (bool): The renderer emits a structured YAML or JSON value.

    Returns:
        list[dict[str, object]]: Guarded input restrictions; unsupported preimages remain unconstrained.
    """
    value = normalize(value)
    if isinstance(value, Input):
        return _input_constraints(value, schema, guards=guards, conditions=conditions, quoted=quoted, serialized=serialized)
    if isinstance(value, LocalMap):
        return _map_constraints(value, schema, guards=guards, conditions=conditions, quoted=quoted, serialized=serialized)
    if not isinstance(value, Operation):
        return []
    name, args = value.name, value.arguments
    if name == "yaml-fragment" and len(args) == 1:
        # The surrounding template can supply required sibling fields or other
        # sequence entries. Only each contributed field/item inherits its full
        # contract; collection-wide requirements belong to the finished render.
        return constraints(args[0], contribution(schema), guards=guards, conditions=conditions, quoted=quoted, serialized=serialized)
    if name in {"toYaml", "toJson", "quote", "tpl", "literal", "string-identity", "render-text"} and args:
        return _transformation_constraints(value, schema, guards=guards, conditions=conditions, quoted=quoted, serialized=serialized)
    if name == "choose" and len(args) == 3:
        return _choice_constraints(value, schema, guards=guards, conditions=conditions, quoted=quoted, serialized=serialized)
    return []


def _input_constraints(
    value: Input,
    schema: dict[str, object],
    *,
    guards: tuple[dict[str, object], ...] = (),
    conditions: tuple[object, ...] = (),
    quoted: bool = False,
    serialized: bool = False,
) -> list[dict[str, object]]:
    """
    Attach global and item-local guards to an original values path.

    Args:
        value (Input): Symbolic output expression.
        schema (dict[str, object]): Required downstream shape.
        guards (tuple[dict[str, object], ...]): Conditions selecting this output.
        conditions (tuple[object, ...]): Symbolic conditions, including item-local branch predicates.
        quoted (bool): The renderer converts this input into a quoted string.
        serialized (bool): The renderer emits a structured YAML or JSON value.

    Returns:
        list[dict[str, object]]: Guarded input restrictions; unsupported preimages remain unconstrained.
    """
    if "*" in value.path:
        # Each item chooses its own branch. A predicate over the entire
        # array would incorrectly accept mixed valid/invalid elements.
        if quoted or value.path.count("*") != 1:
            return []
        index = value.path.index("*")
        root = value.path[: index + 1]
        local, global_guards = [], list(guards)
        for condition in conditions:
            origins = input_origins(condition)
            if any("*" in path for path in origins):
                test = predicate(condition, root=root)
                if test is None:
                    return []
                local.append(test)
            else:
                test = guard_bounds(condition)[0]
                if test == {"not": {}}:
                    return []
                global_guards.append(test)
        item = at(value.path[index + 1 :], schema)
        if local:
            item = {"if": combine(local, conjunction=True), "then": item}
        return [
            {
                "path": list(value.path[:index]),
                "schema": {"type": "array", "items": item},
                "guards": global_guards,
                "quoted": False,
                "serialized": True,
                "element_path": list(value.path),
                "element_schema": schema,
            }
        ]
    for condition in conditions:
        test = guard_bounds(condition)[0]
        if test == {"not": {}}:
            return []
        guards = (*guards, test)
    return [{"path": list(value.path), "schema": schema, "guards": list(guards), "quoted": quoted, "serialized": serialized}]


def _map_constraints(
    value: LocalMap,
    schema: dict[str, object],
    *,
    guards: tuple[dict[str, object], ...] = (),
    conditions: tuple[object, ...] = (),
    quoted: bool = False,
    serialized: bool = False,
) -> list[dict[str, object]]:
    """
    Trace independent map contributors while preserving overwrite uncertainty.

    Args:
        value (LocalMap): Symbolic output expression.
        schema (dict[str, object]): Required downstream shape.
        guards (tuple[dict[str, object], ...]): Conditions selecting this output.
        conditions (tuple[object, ...]): Symbolic conditions, including item-local branch predicates.
        quoted (bool): The renderer converts this input into a quoted string.
        serialized (bool): The renderer emits a structured YAML or JSON value.

    Returns:
        list[dict[str, object]]: Guarded input restrictions; unsupported preimages remain unconstrained.
    """
    if not serialized:
        return []
    result = []
    # Validate contributors to homogeneous maps (annotations, labels), where
    # scalar replacement preserves the output type regardless of precedence.
    extra = schema.get("additionalProperties")
    types = extra.get("type", []) if isinstance(extra, dict) else []
    types = [types] if isinstance(types, str) else sequence(types)
    homogeneous = bool(types) and set(types) <= {"string", "boolean", "integer", "number", "null"}
    if value.sources and homogeneous and not schema.get("required") and not schema.get("properties"):
        for source in value.sources:
            result.extend(constraints(source, schema, guards=guards, conditions=conditions, quoted=quoted, serialized=serialized))
    if not value.sources:
        properties = mapping(schema.get("properties", {}))
        for key, child in value.entries.items():
            restriction = properties.get(key, extra)
            if isinstance(restriction, dict):
                result.extend(constraints(child, restriction, guards=guards, conditions=conditions, serialized=serialized))
    return result


def _transformation_constraints(
    value: Operation,
    schema: dict[str, object],
    *,
    guards: tuple[dict[str, object], ...] = (),
    conditions: tuple[object, ...] = (),
    quoted: bool = False,
    serialized: bool = False,
) -> list[dict[str, object]]:
    """
    Carry destination constraints across supported serialization boundaries.

    Args:
        value (Operation): Symbolic output expression.
        schema (dict[str, object]): Required downstream shape.
        guards (tuple[dict[str, object], ...]): Conditions selecting this output.
        conditions (tuple[object, ...]): Symbolic conditions, including item-local branch predicates.
        quoted (bool): The renderer converts this input into a quoted string.
        serialized (bool): The renderer emits a structured YAML or JSON value.

    Returns:
        list[dict[str, object]]: Guarded input restrictions; unsupported preimages remain unconstrained.
    """
    name, args = value.name, value.arguments
    kinds = schema.get("type", [])
    kinds = [kinds] if isinstance(kinds, str) else sequence(kinds)
    structured = any(kind in kinds for kind in ("array", "object"))
    target = (None if structured else literal_domain(schema)) if name in {"tpl", "literal"} else schema
    if target is None:
        # An open destination cannot prove every generated value literal.
        # Instead, constrain only the bounded region proven free of tpl
        # delimiters. Raw YAML strings keep their original input domain.
        limits = active_limits()
        region = literal_region(limits["max_fragment_depth"], limits["max_discovery_nodes"])
        candidates = constraints(args[0], schema, guards=guards, conditions=conditions, quoted=quoted, serialized=serialized)
        return [
            {
                **rule,
                "guards": [*sequence(rule["guards"]), at(tuple(str(part) for part in sequence(rule["path"])), region)],
                "literal_fragment": True,
            }
            for rule in candidates
            if rule["serialized"] and not rule["quoted"]
        ]
    return constraints(
        args[0],
        target,
        guards=guards,
        conditions=conditions,
        quoted=quoted or name in {"quote", "string-identity"},
        serialized=serialized or name in {"toYaml", "toJson"},
    )


def _choice_constraints(
    value: Operation,
    schema: dict[str, object],
    *,
    guards: tuple[dict[str, object], ...] = (),
    conditions: tuple[object, ...] = (),
    quoted: bool = False,
    serialized: bool = False,
) -> list[dict[str, object]]:
    """
    Constrain only the branches whose activation region can be established.

    Args:
        value (Operation): Symbolic output expression.
        schema (dict[str, object]): Required downstream shape.
        guards (tuple[dict[str, object], ...]): Conditions selecting this output.
        conditions (tuple[object, ...]): Symbolic conditions, including item-local branch predicates.
        quoted (bool): The renderer converts this input into a quoted string.
        serialized (bool): The renderer emits a structured YAML or JSON value.

    Returns:
        list[dict[str, object]]: Guarded input restrictions; unsupported preimages remain unconstrained.
    """
    args = value.arguments
    condition = predicate(args[0])
    item_roots = {path[: path.index("*") + 1] for path in input_origins(args[0]) if "*" in path}
    local_condition = len(item_roots) == 1 and predicate(args[0], root=next(iter(item_roots))) is not None
    if condition is None and not local_condition:
        # Shared restrictions hold everywhere. Other restrictions need a
        # sufficient region proving which arm is selected, not an exact guard.
        branches = [
            constraints(arg, schema, guards=guards, conditions=conditions, quoted=quoted, serialized=serialized) for arg in args[1:]
        ]
        other = {json.dumps(rule, sort_keys=True) for rule in branches[1]}
        shared = [rule for rule in branches[0] if json.dumps(rule, sort_keys=True) in other]
        selected = [
            {**rule, "guards": [*sequence(rule["guards"]), bound]}
            for branch, bound in zip(branches, guard_bounds(args[0]), strict=True)
            if bound != {"not": {}}
            for rule in branch
        ]
        return [*shared, *selected]
    return [
        rule
        for branch, guard in ((args[1], args[0]), (args[2], Operation("not", (args[0],))))
        for rule in constraints(branch, schema, guards=guards, conditions=(*conditions, guard), quoted=quoted, serialized=serialized)
    ]
