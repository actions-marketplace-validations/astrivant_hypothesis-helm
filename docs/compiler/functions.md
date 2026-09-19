# Helm builtin functions

<!-- toc:start -->
**Table of contents**

- [Coverage and limits](#coverage-and-limits)
- [Effects and compiler decisions](#effects-and-compiler-decisions)
- [Findings addressed](#findings-addressed)
- [Function matrix](#function-matrix)
- [Sources and upgrades](#sources-and-upgrades)
<!-- toc:end -->

[Compiler guide](README.md) · [Syntax trees](syntax-trees.md) · [Rejection analysis](analysis.md#explicit-rejection-discovery)

The compiler records what a function can affect before deciding whether it can
analyze the result. For example, `upper` changes text, `set` changes a dictionary
that other variables may also reference, and `randAlphaNum` can change output
between otherwise identical renders.

## Coverage and limits

The inventory covers **251 functions** from Helm 4.3.0, Sprig 3.3.0 and Go 1.26.0.
It includes aliases and Helm overrides, and excludes `env` and `expandenv`, which
Helm removes. The checked-in [source inventory](../../pkg/hypothesis_helm/compiler/builtin_inventory.json)
records upstream versions, source checksums and function names. Tests check that
every name has a classification and ask a matching native Helm parser to resolve
all names without executing them.

Three levels of support are separate:

| Level | What it establishes | What it does not establish |
| --- | --- | --- |
| Effect classification | Whether a function can mutate context, execute code, read external state or change between renders. | The function's concrete output. |
| Discovery model | Possible input dependencies, collection members, scalar arguments and selected result fields. | An accepted input domain or identical manifests. |
| Concrete evaluation or equality proof | A result within a pass's explicitly supported subset. | The behavior of unsupported arguments, functions or renderer modes. |

Every listed function has an effect classification. Only supported operations
have concrete models. A known return shape is insufficient to prove truthiness,
an enum or equivalent manifests. Unsupported expressions retain uncertainty and
remain eligible for Helm testing. A new function absent from this pinned inventory
is also unknown; it is never automatically treated as pure.

`if`, `range`, `with`, `template`, `block`, `define`, `break` and `continue` are
language actions, not function-map entries. `.Capabilities` and `.Files` are
context objects with methods. Their analysis is described in the
[syntax guide](syntax-trees.md) and [renderer-context contract](analysis.md).

## Effects and compiler decisions

| Effect | Examples | Compiler response |
| --- | --- | --- |
| Argument-dependent output | `upper`, `add`, `sha256sum` | Preserve input origins. Evaluate only the supported subset; otherwise let Helm calculate the result. |
| Map mutation | `set`, `unset`, both `merge` variants and their `must` aliases | Invalidate affected map facts, including aliases. Rejection analysis treats writes in conditions as barriers too. |
| Dynamic code | `include`, `tpl`, `call` | Analyze a resolvable helper or available template source. Unresolved code cannot justify pruning. |
| Randomness | `shuffle`, `randInt`, `encryptAES`, `bcrypt`, certificate generators | Preserve dependencies and report the native effect. Do not assign a repeatable concrete result. |
| Clock or timezone | `now`, `ago`, date conversion, certificate validity periods | Keep the environment-dependent result unknown. Explicit fixed arguments may permit a future narrower model. |
| External state | `lookup`, `getHostByName` | Require matching renderer settings before using offline behavior; otherwise keep the result unknown. |
| Unspecified order | `keys`, `values` | Do not assume map enumeration order. A Go template `range` over a string-keyed map itself visits sorted keys. |
| Operating-system behavior | `osBase`, `osClean` and related functions | Do not substitute Python path semantics for Helm's platform. |
| Explicit rejection | `fail`, `required` | Derive supported guarded requirements and verify rejection predictions with Helm. |

These effects can overlap. A generated certificate depends on both randomness
and time. The `must` prefix changes error handling; it does not remove mutation
or make an operation pure. All functions can also fail on invalid arguments.
The matrix is not an assertion that unmarked calls always succeed.

Plain `helm template` has no Kubernetes connection: `lookup` returns an empty map.
With DNS disabled, `getHostByName` returns an empty string. Rejection analysis uses
these results only after the executor attaches those renderer settings. Standalone
discovery, an unconfigured evaluator, and a renderer permitting cluster or DNS
access retain uncertainty. The audit, generation and planning entry points explicitly
select the tool's offline execution mode. No live cluster contents are invented.

## Findings addressed

| Pattern | Analysis behavior |
| --- | --- |
| `range.Values.items`, `if.Values.enabled`, chained `else if.Values.other` | Both syntax trees recognize the compact Go syntax and retain balanced blocks. |
| `split`, `splitn`, `splitList` with literal text | Track exact members. Dictionary keys such as `_10` sort before `_2`; list entries retain position order. |
| `concat` and supported list aliases | Preserve member origins and distinguish exact lists from unknown-length collections. |
| Scalar helper arguments such as `include "label" (printf "%s" .Values.name)` | Analyze scalar dot contexts and preserve the original input path. Invalid field access on a scalar still warns. |
| An odd number of `dict` arguments | Explain that Helm supplies an empty final value. Do not silently assume the intended helper context. |
| Unsupported mutation, dynamic helper output or unavailable `tpl` source | Keep the limitation visible and retain affected tests. |

The Airflow annotation merge calls that pass two maps without wrapping them in
`list` are not parser errors: Sprig accepts the odd dictionary argument list.
They can nevertheless pass a different context and collection than the helper
expects. This requires a chart correction, not suppressing the finding.

Decoding and error behavior also matter. For example, `fromYaml` may return a map
containing an `Error` entry; a successful template invocation alone does not prove
that the intended data survived. Helm remains the authority for rendered output.

## Function matrix

Result families describe possible shapes after a successful call, not exact
values. The operation column groups related functions; the pinned upstream
sources below define their signatures and complete behavior.

<!-- [[[cog
from hypothesis_helm.compiler.builtins import reference
cog.outl(reference())
]]] -->
| Function | Meaning | Result | Effects |
| --- | --- | --- | --- |
| `abbrev` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `abbrevboth` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `add` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `add1` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `add1f` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `addf` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `adler32sum` | Compute a deterministic checksum | scalar | Argument-dependent; no external effects classified |
| `ago` | Format, parse or calculate dates and durations | scalar | clock-or-timezone |
| `all` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `and` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `any` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `append` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `atoi` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `b32dec` | Encode or decode base32/base64 text | scalar | Argument-dependent; no external effects classified |
| `b32enc` | Encode or decode base32/base64 text | scalar | Argument-dependent; no external effects classified |
| `b64dec` | Encode or decode base32/base64 text | scalar | Argument-dependent; no external effects classified |
| `b64enc` | Encode or decode base32/base64 text | scalar | Argument-dependent; no external effects classified |
| `base` | Manipulate slash-separated paths | scalar | Argument-dependent; no external effects classified |
| `bcrypt` | Hash passwords, derive keys or encrypt/decrypt text | scalar | randomness |
| `biggest` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `buildCustomCert` | Decode certificate material | certificate | Argument-dependent; no external effects classified |
| `call` | Invoke a function supplied through context | any | dynamic-code |
| `camelcase` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `cat` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `ceil` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `chunk` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `clean` | Manipulate slash-separated paths | scalar | Argument-dependent; no external effects classified |
| `coalesce` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `compact` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `concat` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `contains` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `date` | Format, parse or calculate dates and durations | scalar | clock-or-timezone |
| `dateInZone` | Format, parse or calculate dates and durations | scalar | clock-or-timezone |
| `dateModify` | Parse, adjust or read a timestamp | timestamp | Argument-dependent; no external effects classified |
| `date_in_zone` | Format, parse or calculate dates and durations | scalar | clock-or-timezone |
| `date_modify` | Parse, adjust or read a timestamp | timestamp | Argument-dependent; no external effects classified |
| `decryptAES` | Hash passwords, derive keys or encrypt/decrypt text | scalar | Argument-dependent; no external effects classified |
| `deepCopy` | Copy a value and its nested containers | any | Argument-dependent; no external effects classified |
| `deepEqual` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `default` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `derivePassword` | Hash passwords, derive keys or encrypt/decrypt text | scalar | Argument-dependent; no external effects classified |
| `dict` | Construct or select dictionary entries | map | Argument-dependent; no external effects classified |
| `dig` | Read dictionary or collection entries | any | Argument-dependent; no external effects classified |
| `dir` | Manipulate slash-separated paths | scalar | Argument-dependent; no external effects classified |
| `div` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `divf` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `duration` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationDays` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationHours` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationMicroseconds` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationMilliseconds` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationMinutes` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationNanoseconds` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationRound` | Format, parse or calculate dates and durations | scalar | clock-or-timezone |
| `durationRoundTo` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationSeconds` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationTruncateTo` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `durationWeeks` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `empty` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `encryptAES` | Hash passwords, derive keys or encrypt/decrypt text | scalar | randomness |
| `eq` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `ext` | Manipulate slash-separated paths | scalar | Argument-dependent; no external effects classified |
| `fail` | Reject the current render explicitly | scalar | rejection |
| `first` | Read a list endpoint | any | Argument-dependent; no external effects classified |
| `float64` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `floor` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `fromJson` | Parse JSON, YAML or TOML text | any | Argument-dependent; no external effects classified |
| `fromJsonArray` | Parse an array document | sequence | Argument-dependent; no external effects classified |
| `fromToml` | Parse JSON, YAML or TOML text | any | Argument-dependent; no external effects classified |
| `fromYaml` | Parse JSON, YAML or TOML text | any | Argument-dependent; no external effects classified |
| `fromYamlArray` | Parse an array document | sequence | Argument-dependent; no external effects classified |
| `ge` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `genCA` | Generate certificate material | certificate | clock-or-timezone, randomness |
| `genCAWithKey` | Generate certificate material | certificate | clock-or-timezone, randomness |
| `genPrivateKey` | Hash passwords, derive keys or encrypt/decrypt text | scalar | randomness |
| `genSelfSignedCert` | Generate certificate material | certificate | clock-or-timezone, randomness |
| `genSelfSignedCertWithKey` | Generate certificate material | certificate | clock-or-timezone, randomness |
| `genSignedCert` | Generate certificate material | certificate | clock-or-timezone, randomness |
| `genSignedCertWithKey` | Generate certificate material | certificate | clock-or-timezone, randomness |
| `get` | Read dictionary or collection entries | any | Argument-dependent; no external effects classified |
| `getHostByName` | Resolve a hostname when Helm DNS access is enabled | scalar | external-state |
| `gt` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `has` | Test list membership | scalar | Argument-dependent; no external effects classified |
| `hasKey` | Test dictionary membership | scalar | Argument-dependent; no external effects classified |
| `hasPrefix` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `hasSuffix` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `hello` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `html` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `htmlDate` | Format, parse or calculate dates and durations | scalar | clock-or-timezone |
| `htmlDateInZone` | Format, parse or calculate dates and durations | scalar | clock-or-timezone |
| `htpasswd` | Hash passwords, derive keys or encrypt/decrypt text | scalar | randomness |
| `include` | Execute a named template or template string | scalar | dynamic-code |
| `indent` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `index` | Read dictionary or collection entries | any | Argument-dependent; no external effects classified |
| `initial` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `initials` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `int` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `int64` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `isAbs` | Manipulate slash-separated paths | scalar | Argument-dependent; no external effects classified |
| `join` | Join a list into text | scalar | Argument-dependent; no external effects classified |
| `js` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `kebabcase` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `keys` | Collect dictionary entries into a list | sequence | unordered |
| `kindIs` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `kindOf` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `last` | Read a list endpoint | any | Argument-dependent; no external effects classified |
| `le` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `len` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `list` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `lookup` | Read Kubernetes resources from renderer context | map | external-state |
| `lower` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `lt` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `max` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `maxf` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `merge` | Construct or select dictionary entries | map | mutation |
| `mergeOverwrite` | Construct or select dictionary entries | map | mutation |
| `min` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `minf` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `mod` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `mul` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `mulf` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `mustAppend` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustChunk` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustCompact` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustDateModify` | Parse, adjust or read a timestamp | timestamp | Argument-dependent; no external effects classified |
| `mustDeepCopy` | Copy a value and its nested containers | any | Argument-dependent; no external effects classified |
| `mustFirst` | Read a list endpoint | any | Argument-dependent; no external effects classified |
| `mustFromJson` | Parse JSON, YAML or TOML text | any | Argument-dependent; no external effects classified |
| `mustHas` | Test list membership | scalar | Argument-dependent; no external effects classified |
| `mustInitial` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustLast` | Read a list endpoint | any | Argument-dependent; no external effects classified |
| `mustMerge` | Construct or select dictionary entries | map | mutation |
| `mustMergeOverwrite` | Construct or select dictionary entries | map | mutation |
| `mustPrepend` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustPush` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustRegexFind` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `mustRegexFindAll` | Extract or split multiple regex matches | sequence | Argument-dependent; no external effects classified |
| `mustRegexMatch` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `mustRegexReplaceAll` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `mustRegexReplaceAllLiteral` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `mustRegexSplit` | Extract or split multiple regex matches | sequence | Argument-dependent; no external effects classified |
| `mustRest` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustReverse` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustSlice` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustToDate` | Parse, adjust or read a timestamp | timestamp | clock-or-timezone |
| `mustToDuration` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `mustToJson` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `mustToPrettyJson` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `mustToRawJson` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `mustToToml` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `mustToYaml` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `mustUniq` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `mustWithout` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `must_date_modify` | Parse, adjust or read a timestamp | timestamp | Argument-dependent; no external effects classified |
| `ne` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `nindent` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `nospace` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `not` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `now` | Parse, adjust or read a timestamp | timestamp | clock-or-timezone |
| `omit` | Construct or select dictionary entries | map | Argument-dependent; no external effects classified |
| `or` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `osBase` | Manipulate operating-system paths | scalar | platform |
| `osClean` | Manipulate operating-system paths | scalar | platform |
| `osDir` | Manipulate operating-system paths | scalar | platform |
| `osExt` | Manipulate operating-system paths | scalar | platform |
| `osIsAbs` | Manipulate operating-system paths | scalar | platform |
| `pick` | Construct or select dictionary entries | map | Argument-dependent; no external effects classified |
| `pluck` | Collect dictionary entries into a list | sequence | Argument-dependent; no external effects classified |
| `plural` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `prepend` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `print` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `printf` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `println` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `push` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `quote` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `randAlpha` | Generate random data or shuffle text | scalar | randomness |
| `randAlphaNum` | Generate random data or shuffle text | scalar | randomness |
| `randAscii` | Generate random data or shuffle text | scalar | randomness |
| `randBytes` | Generate random data or shuffle text | scalar | randomness |
| `randInt` | Generate random data or shuffle text | scalar | randomness |
| `randNumeric` | Generate random data or shuffle text | scalar | randomness |
| `regexFind` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `regexFindAll` | Extract or split multiple regex matches | sequence | Argument-dependent; no external effects classified |
| `regexMatch` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `regexQuoteMeta` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `regexReplaceAll` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `regexReplaceAllLiteral` | Match, extract, quote or replace regular expressions | scalar | Argument-dependent; no external effects classified |
| `regexSplit` | Extract or split multiple regex matches | sequence | Argument-dependent; no external effects classified |
| `repeat` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `replace` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `required` | Choose values by emptiness or a condition | any | rejection |
| `rest` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `reverse` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `round` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `semver` | Parse a semantic version | version | Argument-dependent; no external effects classified |
| `semverCompare` | Compare semantic versions | scalar | Argument-dependent; no external effects classified |
| `seq` | Generate a space-separated integer sequence | scalar | Argument-dependent; no external effects classified |
| `set` | Construct or select dictionary entries | map | mutation |
| `sha1sum` | Compute a deterministic checksum | scalar | Argument-dependent; no external effects classified |
| `sha256sum` | Compute a deterministic checksum | scalar | Argument-dependent; no external effects classified |
| `sha512sum` | Compute a deterministic checksum | scalar | Argument-dependent; no external effects classified |
| `shuffle` | Generate random data or shuffle text | scalar | randomness |
| `slice` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `snakecase` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `sortAlpha` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `split` | Split text into numbered dictionary entries | map | Argument-dependent; no external effects classified |
| `splitList` | Split text into a list | sequence | Argument-dependent; no external effects classified |
| `splitn` | Split text into numbered dictionary entries | map | Argument-dependent; no external effects classified |
| `squote` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `sub` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `subf` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `substr` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `swapcase` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `ternary` | Choose values by emptiness or a condition | any | Argument-dependent; no external effects classified |
| `title` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `toDate` | Parse, adjust or read a timestamp | timestamp | clock-or-timezone |
| `toDecimal` | Convert numbers or calculate arithmetic | scalar | Argument-dependent; no external effects classified |
| `toJson` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `toPrettyJson` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `toRawJson` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `toString` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `toStrings` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `toToml` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `toYaml` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `toYamlPretty` | Serialize a value to JSON, YAML or TOML text | scalar | Argument-dependent; no external effects classified |
| `tpl` | Execute a named template or template string | scalar | dynamic-code |
| `trim` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `trimAll` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `trimPrefix` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `trimSuffix` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `trimall` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `trunc` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `tuple` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `typeIs` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `typeIsLike` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `typeOf` | Compare values or inspect their types | scalar | Argument-dependent; no external effects classified |
| `uniq` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `unixEpoch` | Format, parse or calculate dates and durations | scalar | Argument-dependent; no external effects classified |
| `unset` | Construct or select dictionary entries | map | mutation |
| `until` | Generate an integer sequence | sequence | Argument-dependent; no external effects classified |
| `untilStep` | Generate an integer sequence | sequence | Argument-dependent; no external effects classified |
| `untitle` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `upper` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `urlJoin` | Assemble URL fields into text | scalar | Argument-dependent; no external effects classified |
| `urlParse` | Parse a URL into fields | map | Argument-dependent; no external effects classified |
| `urlquery` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `uuidv4` | Generate random data or shuffle text | scalar | randomness |
| `values` | Collect dictionary entries into a list | sequence | unordered |
| `without` | Construct, select or reorder a list | sequence | Argument-dependent; no external effects classified |
| `wrap` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
| `wrapWith` | Transform, format or escape text | scalar | Argument-dependent; no external effects classified |
<!-- [[[end]]] -->

## Sources and upgrades

- [Helm function map and serialization helpers](https://github.com/helm/helm/blob/v4.3.0/pkg/engine/funcs.go).
- [Helm renderer overrides, offline lookup and DNS behavior](https://github.com/helm/helm/blob/v4.3.0/pkg/engine/engine.go).
- [Sprig function map and aliases](https://github.com/Masterminds/sprig/blob/v3.3.0/functions.go).
- [Go template builtin functions](https://github.com/golang/go/blob/go1.26.0/src/text/template/funcs.go).

When updating the pinned versions, compare the upstream function tables, update
the source inventory and review effects for every added or changed entry. Do not
rely only on Sprig's list of non-hermetic functions: the compiler also accounts
for random password hashing, encryption, certificates and unordered map results.
Regenerate this matrix with `cog -r docs/compiler/functions.md`, then run the
builtin and compiler regression tests.
