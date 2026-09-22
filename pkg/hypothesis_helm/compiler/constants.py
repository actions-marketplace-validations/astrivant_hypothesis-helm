"""
Centralize compiler function families, semantic bounds and typed zero factories.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from types import MappingProxyType

__all__ = (
    "ZERO_FACTORIES",
    "CERTIFICATES",
    "SCALARS",
    "FUNCTION_ALIASES",
    "COLLECTIONS",
    "SELECTIONS",
    "TEXT_CONVERSIONS",
    "TEMPLATE_CALLS",
    "TRANSFORMATIONS",
    "FORMAT_TRANSFORMS",
    "SELECTION_TRANSFORMS",
    "COLLECTION_TRANSFORMS",
    "TEXT_TRANSFORMS",
    "MIN_INTEGER",
    "MAX_INTEGER",
    "INTEGER_RESULTS",
    "MERGES",
    "COPIES",
    "SEMVER_FIELDS",
    "CERTIFICATE_FIELDS",
    "CONTEXT_EFFECTS",
    "NATIVE_OPERATIONS",
    "NATIVE_EXTENSIONS",
    "NATIVE_RECORD_FIELDS",
    "NATIVE_TYPED_OPERATIONS",
)


# Factories return fresh containers; Boolean false and integer zero remain distinct types.
ZERO_FACTORIES: Mapping[str, Callable[[], object]] = MappingProxyType(
    {"boolean": bool, "integer": int, "number": float, "string": str, "array": list, "object": dict, "null": lambda: None}
)


# These families describe compiler support, not a second upstream builtin inventory.
# Source-derived effects and result shapes remain in compiler.builtins.
CERTIFICATES = frozenset(
    {"genCA", "genCAWithKey", "genSelfSignedCert", "genSelfSignedCertWithKey", "genSignedCert", "genSignedCertWithKey"}
)
SCALARS = frozenset({"toString", "quote", "squote", "b64enc", "b64dec", "toYaml", "toJson", "trim", "lower", "upper", "sha256sum"})


MIN_INTEGER = -(2**63)
MAX_INTEGER = 2**63 - 1


# Aliases share one handler so their shape and uncertainty rules cannot drift.
FUNCTION_ALIASES: Mapping[str, str] = MappingProxyType(
    {
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
)
COLLECTIONS = frozenset(
    {"list", "concat", "splitList", "split", "splitn", "omit", "pick", "append", "prepend", "first", "last", "reverse", "uniq", "sortAlpha"}
)
SELECTIONS = frozenset({"ternary", "default", "coalesce", "not", "empty", "and", "or", "eq", "ne", "hasKey"})
TEXT_CONVERSIONS = frozenset({"toString", "toYaml", "toJson"})
TEMPLATE_CALLS = frozenset({"include", "template"})
MERGES = frozenset({"merge", "mustMerge", "mergeOverwrite", "mustMergeOverwrite"})
COPIES = frozenset({"deepCopy", "mustDeepCopy"})
# These operations establish an integer Go type, unlike an unconverted YAML number.
INTEGER_RESULTS = frozenset({"int", "int64", "atoi", "add", "add1", "sub", "mul", "min", "max"})
SEMVER_FIELDS = ("Major", "Minor", "Patch", "Prerelease", "Metadata", "Original")
CERTIFICATE_FIELDS = ("Cert", "Key")
# A known return shape alone cannot make context mutation or dynamic execution safe.
CONTEXT_EFFECTS = frozenset({"mutation", "dynamic-code"})


# Public operations and internal replay selectors use the same concrete handlers.
FORMAT_TRANSFORMS = frozenset({"quote", "squote", "indent", "nindent", "print", "toString"})
SELECTION_TRANSFORMS = frozenset({"default", "coalesce", "kindIs", "ternary"})
COLLECTION_TRANSFORMS = frozenset({"splitList", "split", "_field", "_get", "_index", "concat"})
TEXT_TRANSFORMS = frozenset(
    {
        "sha256sum",
        "b64enc",
        "trunc",
        "lower",
        "upper",
        "trim",
        "regexMatch",
        "mustRegexMatch",
        "regexFind",
        "trimAll",
        "trimPrefix",
        "trimSuffix",
        "contains",
        "hasPrefix",
        "hasSuffix",
        "replace",
        "regexReplaceAll",
    }
)
TRANSFORMATIONS = (
    FORMAT_TRANSFORMS | SELECTION_TRANSFORMS | (COLLECTION_TRANSFORMS - {"_field", "_get", "_index"}) | TEXT_TRANSFORMS | INTEGER_RESULTS
)


# These are execution adapters, not purity declarations. The generated builtin
# inventory remains the source of effect classifications.
NATIVE_OPERATIONS: Mapping[str, int] = MappingProxyType(
    {
        # Negative arity denotes a variadic function, still bounded by compiler budgets.
        "print": -1,
        "println": -1,
        "quote": -1,
        "b64dec": 1,
        "regexMatch": 2,
        "mustRegexMatch": 2,
        "regexFind": 2,
        "mustRegexFind": 2,
        "regexReplaceAll": 3,
        "mustRegexReplaceAll": 3,
        "regexReplaceAllLiteral": 3,
        "mustRegexReplaceAllLiteral": 3,
        "toYaml": 1,
        "toJson": 1,
        "fromYaml": 1,
        "fromJson": 1,
    }
)


# Reviewed deterministic calls delegated to the selected Helm binary. Operand
# admission still rejects clock fallbacks, unordered outputs and excessive allocation.
NATIVE_EXTENSIONS = frozenset(
    {
        "abbrev",
        "abbrevboth",
        "add1f",
        "addf",
        "adler32sum",
        "all",
        "any",
        "atoi",
        "b32dec",
        "b32enc",
        "base",
        "biggest",
        "buildCustomCert",
        "camelcase",
        "cat",
        "ceil",
        "chunk",
        "clean",
        "compact",
        "date",
        "dateInZone",
        "dateModify",
        "date_in_zone",
        "date_modify",
        "decryptAES",
        "deepCopy",
        "deepEqual",
        "derivePassword",
        "dig",
        "dir",
        "div",
        "divf",
        "duration",
        "durationDays",
        "durationHours",
        "durationMicroseconds",
        "durationMilliseconds",
        "durationMinutes",
        "durationNanoseconds",
        "durationRound",
        "durationRoundTo",
        "durationSeconds",
        "durationTruncateTo",
        "durationWeeks",
        "ext",
        "float64",
        "floor",
        "fromJsonArray",
        "fromToml",
        "fromYamlArray",
        "hello",
        "html",
        "htmlDate",
        "htmlDateInZone",
        "initial",
        "initials",
        "int",
        "int64",
        "isAbs",
        "join",
        "js",
        "kebabcase",
        "kindIs",
        "kindOf",
        "last",
        "maxf",
        "minf",
        "mod",
        "mulf",
        "mustAppend",
        "mustChunk",
        "mustCompact",
        "mustDateModify",
        "mustDeepCopy",
        "mustFirst",
        "mustFromJson",
        "mustInitial",
        "mustLast",
        "mustPrepend",
        "mustPush",
        "mustRegexFindAll",
        "mustRegexSplit",
        "mustRest",
        "mustReverse",
        "mustSlice",
        "mustToDate",
        "mustToDuration",
        "mustToJson",
        "mustToPrettyJson",
        "mustToRawJson",
        "mustToToml",
        "mustToYaml",
        "mustUniq",
        "mustWithout",
        "must_date_modify",
        "nospace",
        "osBase",
        "osClean",
        "osDir",
        "osExt",
        "osIsAbs",
        "pluck",
        "plural",
        "prepend",
        "printf",
        "push",
        "regexFindAll",
        "regexQuoteMeta",
        "regexSplit",
        "repeat",
        "rest",
        "round",
        "semver",
        "seq",
        "sha1sum",
        "sha512sum",
        "slice",
        "snakecase",
        "splitn",
        "subf",
        "substr",
        "swapcase",
        "title",
        "toDate",
        "toDecimal",
        "toPrettyJson",
        "toRawJson",
        "toStrings",
        "toToml",
        "toYamlPretty",
        "trimall",
        "tuple",
        "typeIs",
        "typeIsLike",
        "typeOf",
        "uniq",
        "unixEpoch",
        "until",
        "untilStep",
        "untitle",
        "urlJoin",
        "urlquery",
        "values",
        "wrap",
        "wrapWith",
    }
)

NATIVE_RECORD_FIELDS = frozenset(
    {*SEMVER_FIELDS, "String", "Cert", "Key", "Year", "Month", "Day", "Hour", "Minute", "Second", "Unix", "UnixNano", "IsZero"}
)

# A typed native intermediate must not pass through Python reflection or scalar
# formatting: JSON erases Go records, named numeric types and concrete slice types.
NATIVE_TYPED_OPERATIONS = (
    NATIVE_EXTENSIONS
    | TRANSFORMATIONS
    | frozenset(
        {
            "eq",
            "ne",
            "lt",
            "le",
            "gt",
            "ge",
            "not",
            "empty",
            "len",
            "typeIs",
            "has",
            "mustHas",
            "get",
            "index",
            "first",
            "reverse",
            "append",
            "without",
        }
    )
)
