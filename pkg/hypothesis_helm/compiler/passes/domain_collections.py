"""
Summarize element-preserving collection operations and append-only loop accumulators.
"""

from hypothesis_helm.compiler.asts.projections import Collection, Member, Operation

__all__ = ("additions", "members", "truth")


def truth(value: object) -> object:
    """
    Preserve unknown collection cardinality when following a truth test.

    Args:
        value (object): Concrete list or symbolic collection expression.

    Returns:
        object: Boolean or symbolic nonempty condition.
    """
    if isinstance(value, Collection):
        return value.nonempty
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, Operation):
        if value.name in {"append", "mustAppend"}:
            return True
        if value.name in {"uniq", "mustUniq"}:
            return truth(value.arguments[0])
        if value.name == "choose":
            test, yes, no = value.arguments
            left, right = truth(yes), truth(no)
            return left if left == right else Operation("choose", (test, left, right))
    return Operation("truth", (value,))


def members(value: object) -> tuple[Member, ...] | None:
    """
    Follow origins through append and deduplication without evaluating element equality.

    Args:
        value (object): Collection expression built from supported local operations.

    Returns:
        tuple[Member, ...] | None: All possible contributors, or unresolved collection semantics.
    """
    if isinstance(value, Collection):
        return value.members
    if isinstance(value, list):
        return tuple(Member(item) for item in value)
    if not isinstance(value, Operation):
        return None
    name, args = value.name, value.arguments
    if name in {"append", "mustAppend"} and len(args) == 2:
        previous = members(args[0])
        return None if previous is None else (*previous, Member(args[1]))
    if name in {"uniq", "mustUniq"} and len(args) == 1:
        return members(args[0])
    if name == "choose":
        test, yes, no = args
        left, right = members(yes), members(no)
        if left is None or right is None:
            return None
        return (
            *(Member(item.value, (test, *item.conditions)) for item in left),
            *(Member(item.value, (Operation("not", (test,)), *item.conditions)) for item in right),
        )
    return None


def additions(before: object, after: object) -> tuple[tuple[Member, ...], bool] | None:
    """
    Recognize an append-only iteration independently of its previous accumulator contents.

    Args:
        before (object): Binding before the representative iteration.
        after (object): Binding after joining its branches.

    Returns:
        tuple[tuple[Member, ...], bool] | None: New origins and whether every branch appends, or an unsupported recurrence.
    """
    if before == after:
        return (), False
    if not isinstance(after, Operation):
        return None
    name, args = after.name, after.arguments
    if name in {"append", "mustAppend"} and len(args) == 2:
        previous = additions(before, args[0])
        return None if previous is None else ((*previous[0], Member(args[1])), True)
    if name == "choose":
        test, yes, no = args
        left, right = additions(before, yes), additions(before, no)
        if left is None or right is None:
            return None
        return (
            (
                *(Member(item.value, (test, *item.conditions)) for item in left[0]),
                *(Member(item.value, (Operation("not", (test,)), *item.conditions)) for item in right[0]),
            ),
            left[1] and right[1],
        )
    return None
