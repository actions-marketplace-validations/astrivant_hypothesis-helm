"""
Classify every function exposed by the pinned Helm, Sprig and Go template engines.

Effects describe analysis barriers, not a promise to evaluate every function in Python.
Unknown future functions remain opaque. Concrete semantics belong to individual passes.
"""

import json
from pathlib import Path

from attrs import frozen

from hypothesis_helm.schemas.contracts import mapping


@frozen
class Builtin:
    """
    Describe a function's output family and effects independently of exact evaluation.

    Attributes:
        name (str): Template function identifier.
        provider (str): Pinned source that supplies or overrides the function.
        meaning (str): Operation family, expanded in the generated reference.
        shape (str): Scalar, sequence, map, certificate, version or unconstrained result.
        effects (frozenset[str]): Reasons analysis must retain uncertainty or invalidate state.
    """

    name: str
    provider: str
    meaning: str
    shape: str
    effects: frozenset[str]


# Every name is assigned explicitly. New upstream entries must be reviewed, not presumed pure.
FAMILIES = (
    (
        "Transform, format or escape text",
        "scalar",
        "abbrev abbrevboth camelcase cat contains hasPrefix hasSuffix hello html indent initials js kebabcase lower nindent "
        "nospace plural print printf println quote repeat replace snakecase squote substr swapcase title toString trim trimAll "
        "trimPrefix trimSuffix trimall trunc untitle upper urlquery wrap wrapWith",
    ),
    (
        "Convert numbers or calculate arithmetic",
        "scalar",
        "add add1 add1f addf atoi biggest ceil div divf float64 floor int int64 max maxf min minf mod mul mulf round sub subf toDecimal",
    ),
    ("Compare values or inspect their types", "scalar", "deepEqual eq ge gt kindIs kindOf le len lt ne typeIs typeIsLike typeOf"),
    ("Choose values by emptiness or a condition", "any", "all and any coalesce default empty not or ternary required"),
    ("Construct or select dictionary entries", "map", "dict omit pick set unset merge mergeOverwrite mustMerge mustMergeOverwrite"),
    ("Read dictionary or collection entries", "any", "dig get index"),
    ("Test dictionary membership", "scalar", "hasKey"),
    ("Collect dictionary entries into a list", "sequence", "keys pluck values"),
    (
        "Construct, select or reorder a list",
        "sequence",
        "append chunk compact concat initial list mustAppend mustChunk mustCompact mustInitial mustPrepend mustPush mustRest "
        "mustReverse mustSlice mustUniq mustWithout prepend push rest reverse slice sortAlpha toStrings tuple uniq without",
    ),
    ("Read a list endpoint", "any", "first last mustFirst mustLast"),
    ("Test list membership", "scalar", "has mustHas"),
    ("Join a list into text", "scalar", "join"),
    ("Split text into numbered dictionary entries", "map", "split splitn"),
    ("Split text into a list", "sequence", "splitList"),
    ("Generate an integer sequence", "sequence", "until untilStep"),
    ("Generate a space-separated integer sequence", "scalar", "seq"),
    ("Copy a value and its nested containers", "any", "deepCopy mustDeepCopy"),
    (
        "Serialize a value to JSON, YAML or TOML text",
        "scalar",
        "mustToJson mustToPrettyJson mustToRawJson mustToToml mustToYaml toJson toPrettyJson toRawJson toToml toYaml toYamlPretty",
    ),
    ("Parse JSON, YAML or TOML text", "any", "fromJson fromToml fromYaml mustFromJson"),
    ("Parse an array document", "sequence", "fromJsonArray fromYamlArray"),
    (
        "Format, parse or calculate dates and durations",
        "scalar",
        "ago date dateInZone date_in_zone duration durationDays durationHours durationMicroseconds "
        "durationMilliseconds durationMinutes durationNanoseconds durationRound durationRoundTo durationSeconds durationTruncateTo "
        "durationWeeks htmlDate htmlDateInZone mustToDuration unixEpoch",
    ),
    ("Parse, adjust or read a timestamp", "timestamp", "dateModify date_modify mustDateModify must_date_modify mustToDate now toDate"),
    ("Manipulate slash-separated paths", "scalar", "base clean dir ext isAbs"),
    ("Manipulate operating-system paths", "scalar", "osBase osClean osDir osExt osIsAbs"),
    ("Encode or decode base32/base64 text", "scalar", "b32dec b32enc b64dec b64enc"),
    ("Compute a deterministic checksum", "scalar", "adler32sum sha1sum sha256sum sha512sum"),
    ("Hash passwords, derive keys or encrypt/decrypt text", "scalar", "bcrypt decryptAES derivePassword encryptAES genPrivateKey htpasswd"),
    ("Decode certificate material", "certificate", "buildCustomCert"),
    (
        "Generate certificate material",
        "certificate",
        "genCA genCAWithKey genSelfSignedCert genSelfSignedCertWithKey genSignedCert genSignedCertWithKey",
    ),
    ("Generate random data or shuffle text", "scalar", "randAlpha randAlphaNum randAscii randBytes randInt randNumeric shuffle uuidv4"),
    ("Parse a semantic version", "version", "semver"),
    ("Compare semantic versions", "scalar", "semverCompare"),
    (
        "Match, extract, quote or replace regular expressions",
        "scalar",
        "mustRegexFind mustRegexMatch mustRegexReplaceAll mustRegexReplaceAllLiteral regexFind regexMatch regexQuoteMeta "
        "regexReplaceAll regexReplaceAllLiteral",
    ),
    ("Extract or split multiple regex matches", "sequence", "mustRegexFindAll mustRegexSplit regexFindAll regexSplit"),
    ("Parse a URL into fields", "map", "urlParse"),
    ("Assemble URL fields into text", "scalar", "urlJoin"),
    ("Read Kubernetes resources from renderer context", "map", "lookup"),
    ("Resolve a hostname when Helm DNS access is enabled", "scalar", "getHostByName"),
    ("Execute a named template or template string", "scalar", "include tpl"),
    ("Invoke a function supplied through context", "any", "call"),
    ("Reject the current render explicitly", "scalar", "fail"),
)

EFFECTS = {
    "mutation": frozenset("set unset merge mergeOverwrite mustMerge mustMergeOverwrite".split()),
    "dynamic-code": frozenset({"include", "tpl", "call"}),
    "randomness": frozenset(
        "bcrypt htpasswd encryptAES genPrivateKey genCA genCAWithKey genSelfSignedCert genSelfSignedCertWithKey "
        "genSignedCert genSignedCertWithKey randAlpha randAlphaNum randAscii randBytes randInt randNumeric shuffle uuidv4".split()
    ),
    "clock-or-timezone": frozenset(
        "ago now date dateInZone date_in_zone htmlDate htmlDateInZone toDate mustToDate durationRound "
        "genCA genCAWithKey genSelfSignedCert genSelfSignedCertWithKey genSignedCert genSignedCertWithKey".split()
    ),
    "external-state": frozenset({"lookup", "getHostByName"}),
    "platform": frozenset("osBase osClean osDir osExt osIsAbs".split()),
    "unordered": frozenset({"keys", "values"}),
    "rejection": frozenset({"fail", "required"}),
}


def inventory() -> dict[str, Builtin]:
    """
    Load the reviewed source inventory, rejecting missing or duplicate classifications.

    Returns:
        dict[str, Builtin]: Complete pinned function registry.

    Raises:
        ValueError: A source function has no classification, or classifications disagree with sources.
    """
    providers = mapping(json.loads(Path(__file__).with_name("builtin_inventory.json").read_text())["functions"])
    result: dict[str, Builtin] = {}
    for meaning, shape, names in FAMILIES:
        for name in names.split():
            if name in result or name not in providers:
                raise ValueError(f"invalid builtin classification: {name}")
            effects = frozenset(effect for effect, members in EFFECTS.items() if name in members)
            result[name] = Builtin(name, str(providers[name]), meaning, shape, effects)
    if result.keys() != providers.keys():
        raise ValueError(f"unclassified Helm builtins: {sorted(providers.keys() - result.keys())}")
    return result


BUILTINS = inventory()
MUTATIONS = EFFECTS["mutation"]
NATIVE_STATE = frozenset.union(*(members for effect, members in EFFECTS.items() if effect not in {"mutation", "rejection", "dynamic-code"}))


def reference() -> str:
    """
    Generate the reviewed builtin matrix for documentation without inferring evaluator support.

    Returns:
        str: Markdown table of every exposed function, operation family, shape and effects.
    """
    lines = ["| Function | Meaning | Result | Effects |", "| --- | --- | --- | --- |"]
    for name, spec in sorted(BUILTINS.items()):
        effects = ", ".join(sorted(spec.effects)) or "Argument-dependent; no external effects classified"
        lines.append(f"| `{name}` | {spec.meaning} | {spec.shape} | {effects} |")
    return "\n".join(lines)
