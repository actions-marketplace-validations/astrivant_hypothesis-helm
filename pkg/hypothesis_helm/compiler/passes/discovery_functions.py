"""
Track result shapes, literal operations and dependencies without rendering templates.
"""

from hypothesis_helm.compiler.asts.origins import (
    Choice,
    Derived,
    Dictionary,
    Literal,
    Origin,
    Projection,
    Record,
    Sequence,
    Text,
    join,
    paths,
    select,
)
from hypothesis_helm.compiler.asts.transformations import FUNCTIONS, UnsupportedTransformation, calculate
from hypothesis_helm.compiler.builtins import BUILTINS
from hypothesis_helm.compiler.passes.discovery_flow import truth

CERTIFICATES = frozenset(
    {"genCA", "genCAWithKey", "genSelfSignedCert", "genSelfSignedCertWithKey", "genSignedCert", "genSignedCertWithKey"}
)
SCALARS = frozenset({"toString", "quote", "squote", "b64enc", "b64dec", "toYaml", "toJson", "trim", "lower", "upper", "sha256sum"})


def result(function: str, arguments: list[Origin], *, offline: bool = False) -> Origin:
    """
    Propagate supported literal results and origins without inferring global input constraints.

    Args:
        function (str): Statically named template function.
        arguments (list[Origin]): Symbolic input arguments in Helm call order.
        offline (bool): Executor guarantees plain helm template, without cluster or DNS access.

    Returns:
        Origin: Supported shape and source dependencies, or explicit uncertainty.
    """
    inputs = tuple(sorted({path for argument in arguments for path in paths(argument)}))
    scalar = Derived(inputs)
    if function in FUNCTIONS and all(isinstance(argument, Literal) for argument in arguments):
        try:
            value = calculate(function, tuple(argument.value for argument in arguments if isinstance(argument, Literal)))
            if not isinstance(value, (dict, list)):
                return Literal(value)
            # Collection-producing functions need the structured origins below;
            # folding their result into a scalar loses exact loop/key traversal.
        except UnsupportedTransformation:
            pass  # Share the reviewed Go-compatible subset; never fall back to Python coercion.
    if function in {"toString", "toYaml", "toJson"} and len(arguments) == 1:
        return Text(arguments[0], function)
    if function in SCALARS and len(arguments) == 1:
        return scalar
    if function in {"include", "template"}:
        return scalar  # Template output is text, never another Values context.
    if function == "semver" and len(arguments) == 1:
        return Record({name: scalar for name in ("Major", "Minor", "Patch", "Prerelease", "Metadata", "Original")})
    if function in CERTIFICATES or function == "buildCustomCert":
        return Record({"Cert": scalar, "Key": scalar})
    if function == "lookup" and len(arguments) == 4:
        return Dictionary({}) if offline else Derived(inputs, external=True)
    if function == "getHostByName" and len(arguments) == 1 and offline:
        return Literal("")
    aliases = {
        "tuple": "list",
        "push": "append",
        "mustAppend": "append",
        "mustPush": "append",
        "mustPrepend": "prepend",
        "mustFirst": "first",
        "mustLast": "last",
        "mustReverse": "reverse",
        "mustUniq": "uniq",
    }
    function = aliases.get(function, function)
    if function == "list":
        return Sequence(tuple(arguments))
    if function == "concat":
        members = tuple(item for arg in arguments for item in (arg.items if isinstance(arg, Sequence) else (select(arg, ("*",)),)))
        return Sequence(members, exact=all(isinstance(arg, Sequence) and arg.exact for arg in arguments))
    if function in {"splitList", "split"} and len(arguments) == 2:
        separator, value = arguments
        if (
            isinstance(separator, Literal)
            and isinstance(separator.value, str)
            and isinstance(value, Literal)
            and isinstance(value.value, str)
        ):
            pieces = value.value.split(separator.value) if separator.value else list(value.value)
            if function == "split":
                return Dictionary({f"_{index}": Literal(piece) for index, piece in enumerate(pieces)})
            return Sequence(tuple(Literal(piece) for piece in pieces))
        if function == "split":
            # Unknown number of numbered keys; their string values still depend on the input.
            return Dictionary({"*": scalar}, uncertain=True)
        return Sequence((scalar,), exact=False)
    if function == "splitn" and len(arguments) == 3:
        separator, count, value = arguments
        if (
            isinstance(separator, Literal)
            and isinstance(separator.value, str)
            and isinstance(count, Literal)
            and type(count.value) is int
            and isinstance(value, Literal)
            and isinstance(value.value, str)
        ):
            if count.value == 0:
                pieces = []
            elif not separator.value:
                pieces = list(value.value)
                if count.value > 0 and len(pieces) > count.value:
                    pieces = [*pieces[: count.value - 1], "".join(pieces[count.value - 1 :])]
            else:
                pieces = value.value.split(separator.value, maxsplit=count.value - 1 if count.value > 0 else -1)
            return Dictionary({f"_{index}": Literal(piece) for index, piece in enumerate(pieces)})
        return None
    if function == "ternary" and len(arguments) == 3:
        if isinstance(arguments[2], Literal) and isinstance(arguments[2].value, bool):
            return arguments[0] if arguments[2].value else arguments[1]
        return join(*arguments[:2])
    if function == "default" and len(arguments) == 2:
        known = truth(arguments[1])
        return arguments[1] if known is True else arguments[0] if known is False else join(*arguments)
    if function == "coalesce":
        possible: list[Origin] = []
        for argument in arguments:
            known = truth(argument)
            if known is not False:
                possible.append(argument)
            if known is True:
                return join(*possible)
        return join(*possible, Literal(None))
    if function in {"not", "empty"} and len(arguments) == 1:
        known = truth(arguments[0])
        return scalar if known is None else Literal(not known)
    if function in {"and", "or"} and arguments:
        possible = []
        for argument in arguments:
            known = truth(argument)
            if known is None:
                possible.append(argument)
            elif known == (function == "or"):
                return join(*possible, argument)
        return join(*possible, arguments[-1])
    if function in {"eq", "ne"} and len(arguments) == 2:
        left, right = arguments
        if isinstance(left, Literal) and isinstance(right, Literal) and type(left.value) is type(right.value):
            return Literal((left.value == right.value) == (function == "eq"))
        return scalar
    if function == "hasKey" and len(arguments) == 2:
        source, key = arguments
        if isinstance(key, Literal) and isinstance(key.value, str):
            if isinstance(source, Dictionary) and not source.uncertain:
                return Literal(key.value in source.fields)
            if isinstance(source, Projection) and not source.uncertain and (key.value in source.keys) != source.include:
                return Literal(False)
        return scalar
    if function in {"omit", "pick", "append", "prepend", "first", "last", "reverse", "uniq", "sortAlpha"} and arguments:
        source = arguments[0]
        if isinstance(source, Choice):
            return join(*(result(function, [item, *arguments[1:]]) for item in source.alternatives))
        if function in {"omit", "pick"}:
            keys = frozenset(arg.value for arg in arguments[1:] if isinstance(arg, Literal) and isinstance(arg.value, str))
            if len([arg for arg in arguments[1:] if isinstance(arg, Literal) and isinstance(arg.value, str)]) != len(arguments) - 1:
                return None
            if isinstance(source, Dictionary) and not source.uncertain:
                return Dictionary({key: value for key, value in source.fields.items() if (key in keys) == (function == "pick")})
            return Projection(source, keys, include=function == "pick")
        if function in {"append", "prepend"} and len(arguments) == 2:
            members = source.items if isinstance(source, Sequence) else (select(source, ("*",)),)
            members = (*members, arguments[1]) if function == "append" else (arguments[1], *members)
            return Sequence(members, exact=isinstance(source, Sequence) and source.exact)
        if len(arguments) == 1:
            if function in {"first", "last"}:
                if isinstance(source, Sequence) and source.exact:
                    return source.items[0 if function == "first" else -1] if source.items else Literal(None)
                return join(select(source, ("*",)), Literal(None))
            if function == "reverse":
                return (
                    Sequence(tuple(reversed(source.items)), source.exact)
                    if isinstance(source, Sequence)
                    else Sequence((select(source, ("*",)),), False)
                )
            if (
                isinstance(source, Sequence)
                and source.exact
                and all(isinstance(item, Literal) and isinstance(item.value, str) for item in source.items)
            ):
                strings = [item.value for item in source.items if isinstance(item, Literal) and isinstance(item.value, str)]
                strings = sorted(strings) if function == "sortAlpha" else list(dict.fromkeys(strings))
                return Sequence(tuple(Literal(item) for item in strings))
            return Sequence((select(source, ("*",)),), exact=False)
    if function == "print" and all(isinstance(arg, Literal) and isinstance(arg.value, str) for arg in arguments):
        return Literal("".join(str(arg.value) for arg in arguments if isinstance(arg, Literal)))
    if function in {"print", "printf"}:
        return scalar
    specification = BUILTINS.get(function)
    if specification is not None and specification.shape == "scalar" and not specification.effects & {"mutation", "dynamic-code"}:
        # A known result type does not establish a value, truthiness, enum, or equality proof.
        return scalar
    if specification is not None and not specification.effects & {"mutation", "dynamic-code"}:
        if specification.shape == "record" and specification.fields:
            return Record({name: Derived(inputs, external=True) for name in specification.fields})
        if specification.shape == "sequence":
            return Sequence((Derived(inputs, external=True),), exact=False)
    return None
