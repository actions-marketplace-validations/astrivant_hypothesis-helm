"""
Describe sufficient numeric regions and the truth of helper output text.
"""

from hypothesis_helm.compiler.asts.projections import Input, Operation, Piece

__all__ = ("integer_comparison", "rendered_truth", "type_condition")


def integer_comparison(value: Operation) -> tuple[tuple[str, ...], dict[str, object], dict[str, object]] | None:
    """
    Bound comparisons of explicit integer conversions without guessing string or overflow behavior.

    Args:
        value (Operation): Comparison with one converted input and one integer constant.

    Returns:
        tuple[tuple[str, ...], dict[str, object], dict[str, object]] | None: Input path and disjoint sufficient true/false domains.
    """
    reverse = {"gt": "lt", "ge": "le", "lt": "gt", "le": "ge", "eq": "eq", "ne": "ne"}
    if value.name not in reverse or len(value.arguments) != 2:
        return None
    left, right = value.arguments
    operator = value.name
    if type(left) is int:
        left, right, operator = right, left, reverse[operator]
    if not isinstance(left, Operation) or left.name not in {"int", "int64"} or len(left.arguments) != 1 or type(right) is not int:
        return None
    origin = left.arguments[0]
    if not isinstance(origin, Input):
        return None
    # int must fit even on a 32-bit renderer. int64 stays within exact JSON
    # integer precision as values can cross floating-point decoding boundaries.
    bits = 31 if left.name == "int" else 53
    minimum, maximum = -(2**bits) + (left.name == "int64"), 2**bits - 1
    if not minimum <= right <= maximum:
        return None
    region: dict[str, object] = {"type": "integer", "minimum": minimum, "maximum": maximum}
    keys = {"gt": "exclusiveMinimum", "ge": "minimum", "lt": "exclusiveMaximum", "le": "maximum", "eq": "const", "ne": "const"}
    comparison: dict[str, object] = {keys[operator]: right}
    if operator == "ne":
        comparison = {"not": comparison}
    return origin.path, {"allOf": [region, comparison]}, {"allOf": [region, {"not": comparison}]}


def rendered_truth(value: object) -> object:
    """
    Follow the emptiness of rendered helper text rather than the truth of its unrendered values.

    Args:
        value (object): Helper output before its string-returning boundary.

    Returns:
        object: Boolean, symbolic choice, or explicit unresolved text condition.
    """
    if isinstance(value, Piece):
        return rendered_truth(value.value)
    if isinstance(value, str):
        return bool(value)
    if type(value) in {bool, int, float}:
        return True  # Rendering false and zero produces nonempty text.
    if isinstance(value, Operation):
        if value.name == "choose" and len(value.arguments) == 3:
            condition, yes, no = value.arguments
            return Operation("choose", (condition, rendered_truth(yes), rendered_truth(no)))
        if value.name == "text":
            return Operation("or", tuple(rendered_truth(piece) for piece in value.arguments))
        if value.name == "render-text" and len(value.arguments) == 1:
            return rendered_truth(value.arguments[0])
    return Operation("unknown-rendered-truth", (value,))


def type_condition(value: Operation) -> object:
    """
    Distribute a supported type test over a conditional value without losing branch selection.

    Args:
        value (Operation): kindIs or typeIs operation.

    Returns:
        object: Equivalent conditional predicate or the unchanged unresolved operation.
    """
    if len(value.arguments) != 2:
        return value
    kind, selected = value.arguments
    if isinstance(selected, Operation) and selected.name == "choose":
        condition, yes, no = selected.arguments
        return Operation("choose", (condition, Operation(value.name, (kind, yes)), Operation(value.name, (kind, no))))
    kinds = {str: "string", bool: "bool"}
    if value.name == "kindIs":
        kinds.update({dict: "map", list: "slice"})
    if selected is None:
        return False if kind in {"string", "bool", "map", "slice"} else value
    if type(selected) in kinds and kind in kinds.values():
        return kinds[type(selected)] == kind
    return value
