"""
Compute conservative branch, collection and mutation facts for values discovery.
"""

from collections.abc import Callable

from hypothesis_helm.charts import tpl
from hypothesis_helm.compiler.asts.origins import (
    Choice,
    Dictionary,
    Literal,
    Origin,
    Projection,
    Record,
    Sequence,
    identity,
    join,
)


def key_guards(
    tokens: list[str], resolve: Callable[[list[str]], Origin], epoch: int, positive: bool = True
) -> frozenset[tuple[object, ...]]:
    """
    Record key-membership facts guaranteed by a supported condition and branch.

    Args:
        tokens (list[str]): Condition tokens from the action tree.
        resolve (Callable[[list[str]], Origin]): Current lexical origin resolver.
        epoch (int): Mutation generation invalidating earlier guard facts.
        positive (bool): Whether this branch requires the condition to be true.

    Returns:
        frozenset[tuple[object, ...]]: Guaranteed table/key pairs, excluding unsupported predicates.
    """
    while tokens[:1] == ["("] and tokens[-1:] == [")"]:
        groups = tpl.arguments(tokens)
        if len(groups) != 1:
            break
        tokens = tokens[1:-1]
    if not tokens:
        return frozenset()
    arguments = tpl.arguments(tokens[1:])
    if tokens[0] == "hasKey" and len(arguments) == 2 and positive:
        return frozenset({(identity(resolve(arguments[0])), identity(resolve(arguments[1])), epoch)})
    if tokens[0] == "not" and len(arguments) == 1:
        return key_guards(arguments[0], resolve, epoch, not positive)
    if tokens[0] == ("and" if positive else "or"):
        return frozenset(fact for argument in arguments for fact in key_guards(argument, resolve, epoch, positive))
    return frozenset()


def truth(origin: Origin) -> bool | None:
    """
    Decide emptiness from template construction without consulting values defaults.

    Args:
        origin (Origin): Symbolic value used in a condition or fallback.

    Returns:
        bool | None: Proven truth value, or unknown when input values can change it.
    """
    if isinstance(origin, Literal):
        return bool(origin.value)
    if isinstance(origin, Dictionary) and not origin.uncertain:
        return bool(origin.fields)
    if isinstance(origin, Sequence) and origin.exact:
        return bool(origin.items)
    if isinstance(origin, Record):
        return True  # Go structs, including a semver value, are not empty.
    if isinstance(origin, Projection) and not origin.uncertain and origin.include and not origin.keys:
        return False
    if isinstance(origin, Choice):
        alternatives = {truth(item) for item in origin.alternatives}
        return alternatives.pop() if len(alternatives) == 1 else None
    return None


def iterations(origin: Origin) -> tuple[tuple[Origin, Origin], ...] | None:
    """
    Enumerate only collections whose contents and Go iteration order are statically known.

    Args:
        origin (Origin): Range input computed from template syntax.

    Returns:
        tuple[tuple[Origin, Origin], ...] | None: Ordered key/value pairs, or unknown cardinality.
    """
    if isinstance(origin, Literal) and origin.value is None:
        return ()
    if isinstance(origin, Sequence) and origin.exact:
        return tuple((Literal(index), value) for index, value in enumerate(origin.items))
    if isinstance(origin, Dictionary) and not origin.uncertain:
        return tuple((Literal(key), value) for key, value in sorted(origin.fields.items()))
    return None


def widen(previous: Origin, following: Origin) -> Origin:
    """
    Bound growing list accumulators while retaining every possible member origin.

    Args:
        previous (Origin): Origins carried from preceding loop iterations.
        following (Origin): Origins following one additional iteration.

    Returns:
        Origin: Joined origins with repeated list growth summarized by possible members.
    """
    if identity(previous) == identity(following):
        return previous
    combined = join(previous, following)
    alternatives = combined.alternatives if isinstance(combined, Choice) else (combined,)
    sequences = [item for item in alternatives if isinstance(item, Sequence)]
    if not sequences:
        return combined
    members = join(*(member for sequence in sequences for member in sequence.items))
    items = members.alternatives if isinstance(members, Choice) else (members,)
    return join(Sequence(items, exact=False), *(item for item in alternatives if not isinstance(item, Sequence)))


def invalidate(origin: Origin) -> None:
    """
    Withdraw map facts after an unsupported mutation, including shared nested aliases.

    Args:
        origin (Origin): Possible mutation target or cached helper argument.

    Returns:
        None: Existing map origins become uncertain without losing their known input sources.
    """
    if isinstance(origin, Dictionary):
        origin.uncertain = True
        for value in origin.fields.values():
            invalidate(value)
    elif isinstance(origin, Projection):
        origin.uncertain = True
        invalidate(origin.source)
    elif isinstance(origin, Choice):
        for value in origin.alternatives:
            invalidate(value)
    elif isinstance(origin, Sequence):
        for value in origin.items:
            invalidate(value)
