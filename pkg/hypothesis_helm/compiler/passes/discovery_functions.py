"""
Describe function-result shapes and dependencies without evaluating template functions.
"""

from hypothesis_helm.compiler.asts.origins import Derived, Literal, Origin, Record, Sequence, join, paths

CERTIFICATES = frozenset(
    {"genCA", "genCAWithKey", "genSelfSignedCert", "genSelfSignedCertWithKey", "genSignedCert", "genSignedCertWithKey"}
)
SCALARS = frozenset({"toString", "quote", "squote", "b64enc", "b64dec", "toYaml", "toJson", "trim", "lower", "upper", "sha256sum"})


def result(function: str, arguments: list[Origin]) -> Origin:
    """
    Propagate known result shapes without inferring constraints or rendering any content.

    Args:
        function (str): Statically named template function.
        arguments (list[Origin]): Symbolic input arguments in Helm call order.

    Returns:
        Origin: Supported shape and source dependencies, or explicit uncertainty.
    """
    inputs = tuple(sorted({path for argument in arguments for path in paths(argument)}))
    scalar = Derived(inputs)
    if function in SCALARS and len(arguments) == 1:
        return scalar
    if function in {"include", "template"}:
        return scalar  # Template output is text, never another Values context.
    if function == "semver" and len(arguments) == 1:
        return Record({name: scalar for name in ("Major", "Minor", "Patch", "Prerelease", "Metadata", "Original")})
    if function in CERTIFICATES:
        return Record({"Cert": scalar, "Key": scalar})
    if function == "lookup" and len(arguments) == 4:
        return Derived(inputs, external=True)
    if function == "list":
        return Sequence(tuple(arguments))
    if function == "splitList" and len(arguments) == 2:
        return Sequence((scalar,))
    if function == "ternary" and len(arguments) == 3:
        return join(*arguments[:2])
    if function in {"default", "coalesce"} and arguments:
        return join(*arguments)
    if function in {"uniq", "sortAlpha"} and len(arguments) == 1:
        return arguments[0]
    if function == "print" and all(isinstance(arg, Literal) and isinstance(arg.value, str) for arg in arguments):
        return Literal("".join(str(arg.value) for arg in arguments if isinstance(arg, Literal)))
    if function in {"print", "printf"}:
        return scalar
    return None
