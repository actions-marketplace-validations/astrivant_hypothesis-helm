# Helm builtin functions

<!-- toc:start -->
**Table of contents**

- [Testing random outputs](#testing-random-outputs)
- [Coverage and limits](#coverage-and-limits)
- [Effects and compiler decisions](#effects-and-compiler-decisions)
- [Findings addressed](#findings-addressed)
- [Function matrix](#function-matrix)
- [Sources and upgrades](#sources-and-upgrades)
  - [What comes from source, and what still needs a contract](#what-comes-from-source-and-what-still-needs-a-contract)
<!-- toc:end -->

[Compiler guide](README.md) · [Syntax trees](syntax-trees.md) · [Rejection analysis](analysis.md#explicit-rejection-discovery)

The compiler records what a function can affect before deciding whether it can
analyze the result. For example, `upper` changes text, `set` changes a dictionary
that other variables may also reference, and `randAlphaNum` can change output
between otherwise identical renders.

## Testing random outputs

`--renderer-policy auto` is the default. For charts with possible runtime effects, it lets Hypothesis generate and shrink
supported random outputs separately from the chart's values. For example, `randAlphaNum 8` becomes an input with exactly
eight ASCII letters or digits, including uppercase and digit-only strings.

| Policy | Execution | When control is unavailable |
| --- | --- | --- |
| `auto` (default) | Use the prepared, compatible renderer for potential runtime effects; ordinary charts use Helm. | Log the reason and rerender the whole case with native Helm. |
| `native` | Always use the configured Helm executable during testing. | Random outputs remain native and cannot be replayed from a draw tape. |
| `strict` | Require the pinned renderer and control every effect reached during that render. | Stop with an unavailable result, not a chart-defect finding. |

Prepare the controlled renderer once, then test or scan normally:

```sh
hypothesis-helm-renderer --build
helm hypothesis test ./chart --filter --max-examples 10
helm hypothesis test ./chart --renderer-policy strict
helm hypothesis test ./chart --renderer-policy native
```

The build requires Go and downloads the pinned Go 1.26 toolchain and Helm 4.3.0 SDK when needed. Its source-addressed executable
lives under `.cache/random-renderer/`; `--go /path/to/go` selects the compiler. Repository refresh builds it automatically.
Automatic testing does not download or compile tools inside a chart's execution budget. An absent build causes a visible native
fallback. Strict chart testing prepares its required build before the test budget starts.

The selected Helm executable must report version 4.3.0, matching the reviewed SDK. A different version, including a prerelease,
causes automatic fallback or strict rejection. This checks version compatibility; it does not certify custom Helm builds.
Version probes are cached per executable identity. Changing source, values, release settings or the renderer invalidates replay.

Configure the policy globally or for a chart selected by an `input_constraints` entry with `path: $`:

```yaml
hypothesis:
  renderer_policy: auto
```

This replaces the earlier `--random-inputs` testing switch and `hypothesis.random_inputs` Boolean. The replay command below
still uses `--random-inputs FILE` to select its saved tape.

The native Go parser assigns identities to random calls in a loaded, in-memory chart. Helm's function hook supplies the test
values; chart files and `values.yaml` remain unchanged. Each executed call receives an independent draw, including loop and
helper invocations. Reusing a variable reuses its value. Calls inside dynamically generated `tpl` code are recorded under an
explicit dynamic-call identity. Helm still checks argument types, coalesces dependencies, validates the values schema, and
executes the templates.

Each case starts **one renderer process**. A JSON stream requests a draw when execution reaches a random call, and Hypothesis
replies while that same Helm render waits. Previous prefixes are not rendered again. The process exits after that case; it is
not a persistent service shared between tests. Stdout and stderr are drained together, and timeouts or interruptions stop and
join the owned process group.

Hypothesis owns the draws during sampled tests, so the existing seed and shrinking settings apply. Defaults and finite plans
use a fixed all-zero alphanumeric representative. Their counts cover values configurations, not every possible random string.
**Sampled outputs never justify rejection or exact-equivalence pruning.** Static analysis can still report `HH2007` at a random
call because a sampled value is not a proven constant.

An executed clock, lookup, or unsupported random function makes that case unavailable for controlled replay. Automatic mode
discards its partial draw tape and rerenders the original input entirely with native Helm, using the remaining execution budget.
The output and any resulting finding carry `replayable: false` and the fallback reason. Reports show the limitation, and run
coverage records observed controlled renders and native fallback reasons. Native failures remain findings. Unreached unsupported
branches do not prevent replay of the executed path.

Malformed tapes, changed replay context, actual chart failures and expired execution budgets never trigger automatic fallback.
Explicit replay always requires full control, regardless of the chart's automatic policy.

Path scans and saved suites include a root property for renderer inputs, so charts with an empty values file still exercise
random outputs. Reports show the synthetic call paths and strings alongside ordinary changed values.

Failure artifacts include `random-inputs.json` beside `values.json`. The tape retains call paths, lengths, exact strings, and
hashes of the chart, values and renderer. Replay rejects changed inputs, missing or unused draws, and strings outside the
function's domain:

```sh
hypothesis-helm-renderer ./chart --values artifacts/values.json --random-inputs artifacts/random-inputs.json
```

Supply the same Helm executable (`--helm`), release, namespace and Kubernetes version when those options were used originally. The original chart must
still have its dependencies prepared. Replays restore the renderer inputs; custom Python assertions still require the original
test. `compiler.max_string_chars`, `compiler.max_steps`, and the render timeout bound generated lengths, call counts and the
total time spent completing a draw tape. One streamed render completes a tape. An automatic native fallback shares that same timeout.

## Coverage and limits

<!-- [[[cog
import json
from importlib.resources import files
from hypothesis_helm.compiler import builtins
snapshot = json.loads(files("hypothesis_helm.compiler.assets").joinpath("builtin_inventory.json").read_text(encoding="utf-8"))
versions = ", ".join(source["version"] for source in snapshot["sources"])
cog.outl(f"The inventory covers **{len(builtins.BUILTINS)} functions** from {versions}.")
]]] -->
The inventory covers **251 functions** from Go 1.26.0, Sprig 3.3.0, Helm 4.3.0.
<!-- [[[end]]] -->
A Go AST extractor reads their function maps, aliases, removals and renderer
assignments. The compiler loads its generated JSON instead of maintaining a
second list of function families.

The [source lock](../../pkg/hypothesis_helm_catalog/data/builtin-sources.json)
pins artifact checksums. The [generated inventory](../../pkg/hypothesis_helm/compiler/assets/builtin_inventory.json)
records package file hashes, implementations, signatures, return shapes,
call relationships, effect evidence and unresolved operations. No upstream Go
function is executed during extraction. A changed registration syntax fails the
rebuild instead of silently losing entries.

Three levels of support are separate:

| Level | What it establishes | What it does not establish |
| --- | --- | --- |
| Effect classification | Whether a function can mutate context, execute code, read external state or change between renders. | The function's concrete output. |
| Discovery model | Possible input dependencies, collection members, scalar arguments and selected result fields. | An accepted input domain or identical manifests. |
| Concrete evaluation or equality proof | A result within a pass's explicitly supported subset. | The behavior of unsupported arguments, functions or renderer modes. |

Every listed function has a generated source record. Only supported operations
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
| Map mutation | `set`, `unset`, both `merge` variants and their `must` aliases | Invalidate affected map facts, including aliases. Rejection analysis supports [owned local writes and flat-map merges](analysis.md#transformed-input-domains); shared writes and nested merges remain barriers. |
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
values. The implementation column identifies the upstream code; the source inventory
contains signatures and evidence. An unresolved count includes imported calls,
method dispatch and writes the extractor cannot resolve. Zero detected effects
is not a purity proof, even when no unresolved calls were recorded.

<!-- [[[cog
from hypothesis_helm.compiler.builtins import reference
cog.outl(reference())
]]] -->
| Function | Upstream implementation | Result | Detected effects | Unresolved calls/writes |
| --- | --- | --- | --- | ---: |
| `abbrev` | `abbrev` | scalar | None detected (not a purity proof) | 1 |
| `abbrevboth` | `abbrevboth` | scalar | None detected (not a purity proof) | 1 |
| `add` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `add1` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `add1f` | `closure` | scalar | None detected (not a purity proof) | 5 |
| `addf` | `closure` | scalar | None detected (not a purity proof) | 6 |
| `adler32sum` | `adler32sum` | scalar | None detected (not a purity proof) | 3 |
| `ago` | `dateAgo` | scalar | clock-or-timezone | 5 |
| `all` | `all` | scalar | None detected (not a purity proof) | 10 |
| `and` | `and` | any | None detected (not a purity proof) | 0 |
| `any` | `any` | scalar | None detected (not a purity proof) | 10 |
| `append` | `push` | sequence | None detected (not a purity proof) | 8 |
| `atoi` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `b32dec` | `base32decode` | scalar | None detected (not a purity proof) | 2 |
| `b32enc` | `base32encode` | scalar | None detected (not a purity proof) | 2 |
| `b64dec` | `base64decode` | scalar | None detected (not a purity proof) | 2 |
| `b64enc` | `base64encode` | scalar | None detected (not a purity proof) | 2 |
| `base` | `path.Base` | any | None detected (not a purity proof) | 1 |
| `bcrypt` | `bcrypt` | scalar | randomness | 3 |
| `biggest` | `max` | scalar | None detected (not a purity proof) | 1 |
| `buildCustomCert` | `buildCustomCertificate` | record | None detected (not a purity proof) | 13 |
| `call` | `emptyCall` | any | dynamic-code | 0 |
| `camelcase` | `xstrings.ToPascalCase` | any | None detected (not a purity proof) | 1 |
| `cat` | `cat` | scalar | None detected (not a purity proof) | 3 |
| `ceil` | `ceil` | scalar | None detected (not a purity proof) | 2 |
| `chunk` | `chunk` | sequence | None detected (not a purity proof) | 11 |
| `clean` | `path.Clean` | any | None detected (not a purity proof) | 1 |
| `coalesce` | `coalesce` | any | None detected (not a purity proof) | 10 |
| `compact` | `compact` | sequence | None detected (not a purity proof) | 16 |
| `concat` | `concat` | any | None detected (not a purity proof) | 7 |
| `contains` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `date` | `date` | scalar | clock-or-timezone | 5 |
| `dateInZone` | `dateInZone` | scalar | clock-or-timezone | 5 |
| `dateModify` | `dateModify` | any | None detected (not a purity proof) | 2 |
| `date_in_zone` | `dateInZone` | scalar | clock-or-timezone | 5 |
| `date_modify` | `dateModify` | any | None detected (not a purity proof) | 2 |
| `decryptAES` | `decryptAES` | scalar | None detected (not a purity proof) | 5 |
| `deepCopy` | `deepCopy` | any | None detected (not a purity proof) | 2 |
| `deepEqual` | `reflect.DeepEqual` | any | None detected (not a purity proof) | 1 |
| `default` | `dfault` | any | None detected (not a purity proof) | 10 |
| `derivePassword` | `derivePassword` | scalar | None detected (not a purity proof) | 12 |
| `dict` | `dict` | map | None detected (not a purity proof) | 4 |
| `dig` | `dig` | any | None detected (not a purity proof) | 1 |
| `dir` | `path.Dir` | any | None detected (not a purity proof) | 1 |
| `div` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `divf` | `closure` | scalar | None detected (not a purity proof) | 5 |
| `duration` | `duration` | scalar | None detected (not a purity proof) | 3 |
| `durationDays` | `durationDays` | scalar | None detected (not a purity proof) | 14 |
| `durationHours` | `durationHours` | scalar | None detected (not a purity proof) | 14 |
| `durationMicroseconds` | `durationMicroseconds` | scalar | None detected (not a purity proof) | 14 |
| `durationMilliseconds` | `durationMilliseconds` | scalar | None detected (not a purity proof) | 14 |
| `durationMinutes` | `durationMinutes` | scalar | None detected (not a purity proof) | 14 |
| `durationNanoseconds` | `durationNanoseconds` | scalar | None detected (not a purity proof) | 14 |
| `durationRound` | `durationRound` | scalar | clock-or-timezone | 4 |
| `durationRoundTo` | `durationRoundTo` | any | None detected (not a purity proof) | 14 |
| `durationSeconds` | `durationSeconds` | scalar | None detected (not a purity proof) | 14 |
| `durationTruncateTo` | `durationTruncateTo` | any | None detected (not a purity proof) | 14 |
| `durationWeeks` | `durationWeeks` | scalar | None detected (not a purity proof) | 14 |
| `empty` | `empty` | scalar | None detected (not a purity proof) | 10 |
| `encryptAES` | `encryptAES` | scalar | randomness | 8 |
| `eq` | `eq` | scalar | None detected (not a purity proof) | 26 |
| `ext` | `path.Ext` | any | None detected (not a purity proof) | 1 |
| `fail` | `closure` | scalar | rejection | 2 |
| `first` | `first` | any | None detected (not a purity proof) | 7 |
| `float64` | `toFloat64` | scalar | None detected (not a purity proof) | 1 |
| `floor` | `floor` | scalar | None detected (not a purity proof) | 2 |
| `fromJson` | `fromJSON` | any | None detected (not a purity proof) | 4 |
| `fromJsonArray` | `fromJSONArray` | sequence | None detected (not a purity proof) | 3 |
| `fromToml` | `fromTOML` | map | None detected (not a purity proof) | 4 |
| `fromYaml` | `fromYAML` | map | None detected (not a purity proof) | 4 |
| `fromYamlArray` | `fromYAMLArray` | sequence | None detected (not a purity proof) | 3 |
| `ge` | `ge` | scalar | None detected (not a purity proof) | 13 |
| `genCA` | `generateCertificateAuthority` | record | clock-or-timezone, external-state, randomness | 24 |
| `genCAWithKey` | `generateCertificateAuthorityWithPEMKey` | record | clock-or-timezone, external-state, randomness | 31 |
| `genPrivateKey` | `generatePrivateKey` | scalar | randomness | 12 |
| `genSelfSignedCert` | `generateSelfSignedCertificate` | record | clock-or-timezone, external-state, randomness | 22 |
| `genSelfSignedCertWithKey` | `generateSelfSignedCertificateWithPEMKey` | record | clock-or-timezone, external-state, randomness | 29 |
| `genSignedCert` | `generateSignedCertificate` | record | clock-or-timezone, external-state, randomness | 31 |
| `genSignedCertWithKey` | `generateSignedCertificateWithPEMKey` | record | clock-or-timezone, external-state, randomness | 30 |
| `get` | `get` | any | None detected (not a purity proof) | 0 |
| `getHostByName` | `closure` | scalar | external-state, randomness | 2 |
| `gt` | `gt` | scalar | None detected (not a purity proof) | 31 |
| `has` | `has` | scalar | None detected (not a purity proof) | 8 |
| `hasKey` | `hasKey` | scalar | None detected (not a purity proof) | 0 |
| `hasPrefix` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `hasSuffix` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `hello` | `closure` | scalar | None detected (not a purity proof) | 0 |
| `html` | `HTMLEscaper` | scalar | mutation | 7 |
| `htmlDate` | `htmlDate` | scalar | clock-or-timezone | 5 |
| `htmlDateInZone` | `htmlDateInZone` | scalar | clock-or-timezone | 5 |
| `htpasswd` | `htpasswd` | scalar | randomness | 4 |
| `include` | `includeFun` | scalar | dynamic-code | 5 |
| `indent` | `indent` | scalar | None detected (not a purity proof) | 2 |
| `index` | `index` | any | None detected (not a purity proof) | 25 |
| `initial` | `initial` | sequence | None detected (not a purity proof) | 8 |
| `initials` | `initials` | scalar | None detected (not a purity proof) | 1 |
| `int` | `toInt` | scalar | None detected (not a purity proof) | 1 |
| `int64` | `toInt64` | scalar | None detected (not a purity proof) | 1 |
| `isAbs` | `path.IsAbs` | any | None detected (not a purity proof) | 1 |
| `join` | `join` | scalar | None detected (not a purity proof) | 9 |
| `js` | `JSEscaper` | scalar | mutation | 10 |
| `kebabcase` | `xstrings.ToKebabCase` | any | None detected (not a purity proof) | 1 |
| `keys` | `keys` | sequence | unordered | 0 |
| `kindIs` | `kindIs` | scalar | None detected (not a purity proof) | 3 |
| `kindOf` | `kindOf` | scalar | None detected (not a purity proof) | 3 |
| `last` | `last` | any | None detected (not a purity proof) | 7 |
| `le` | `le` | scalar | None detected (not a purity proof) | 31 |
| `len` | `length` | scalar | None detected (not a purity proof) | 5 |
| `list` | `list` | sequence | None detected (not a purity proof) | 0 |
| `lookup` | `newLookupFunction(ctx, *e.clientProvider)` | any | external-state | 1 |
| `lower` | `strings.ToLower` | any | None detected (not a purity proof) | 1 |
| `lt` | `lt` | scalar | None detected (not a purity proof) | 13 |
| `max` | `max` | scalar | None detected (not a purity proof) | 1 |
| `maxf` | `maxf` | scalar | None detected (not a purity proof) | 2 |
| `merge` | `merge` | any | mutation | 1 |
| `mergeOverwrite` | `mergeOverwrite` | any | mutation | 1 |
| `min` | `min` | scalar | None detected (not a purity proof) | 1 |
| `minf` | `minf` | scalar | None detected (not a purity proof) | 2 |
| `mod` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `mul` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `mulf` | `closure` | scalar | None detected (not a purity proof) | 5 |
| `mustAppend` | `mustPush` | sequence | None detected (not a purity proof) | 8 |
| `mustChunk` | `mustChunk` | sequence | None detected (not a purity proof) | 11 |
| `mustCompact` | `mustCompact` | sequence | None detected (not a purity proof) | 16 |
| `mustDateModify` | `mustDateModify` | any | None detected (not a purity proof) | 2 |
| `mustDeepCopy` | `mustDeepCopy` | any | None detected (not a purity proof) | 1 |
| `mustFirst` | `mustFirst` | any | None detected (not a purity proof) | 7 |
| `mustFromJson` | `mustFromJson` | any | None detected (not a purity proof) | 2 |
| `mustHas` | `mustHas` | scalar | None detected (not a purity proof) | 8 |
| `mustInitial` | `mustInitial` | sequence | None detected (not a purity proof) | 8 |
| `mustLast` | `mustLast` | any | None detected (not a purity proof) | 7 |
| `mustMerge` | `mustMerge` | any | mutation | 1 |
| `mustMergeOverwrite` | `mustMergeOverwrite` | any | mutation | 1 |
| `mustPrepend` | `mustPrepend` | sequence | None detected (not a purity proof) | 8 |
| `mustPush` | `mustPush` | sequence | None detected (not a purity proof) | 8 |
| `mustRegexFind` | `mustRegexFind` | scalar | None detected (not a purity proof) | 2 |
| `mustRegexFindAll` | `mustRegexFindAll` | sequence | None detected (not a purity proof) | 2 |
| `mustRegexMatch` | `mustRegexMatch` | scalar | None detected (not a purity proof) | 1 |
| `mustRegexReplaceAll` | `mustRegexReplaceAll` | scalar | None detected (not a purity proof) | 2 |
| `mustRegexReplaceAllLiteral` | `mustRegexReplaceAllLiteral` | scalar | None detected (not a purity proof) | 2 |
| `mustRegexSplit` | `mustRegexSplit` | sequence | None detected (not a purity proof) | 2 |
| `mustRest` | `mustRest` | sequence | None detected (not a purity proof) | 8 |
| `mustReverse` | `mustReverse` | sequence | None detected (not a purity proof) | 8 |
| `mustSlice` | `mustSlice` | any | None detected (not a purity proof) | 8 |
| `mustToDate` | `mustToDate` | any | clock-or-timezone | 1 |
| `mustToDuration` | `mustToDuration` | any | None detected (not a purity proof) | 13 |
| `mustToJson` | `mustToJSON` | scalar | None detected (not a purity proof) | 1 |
| `mustToPrettyJson` | `mustToPrettyJson` | scalar | None detected (not a purity proof) | 1 |
| `mustToRawJson` | `mustToRawJson` | scalar | None detected (not a purity proof) | 5 |
| `mustToToml` | `mustToTOML` | scalar | None detected (not a purity proof) | 4 |
| `mustToYaml` | `mustToYAML` | scalar | None detected (not a purity proof) | 2 |
| `mustUniq` | `mustUniq` | sequence | None detected (not a purity proof) | 8 |
| `mustWithout` | `mustWithout` | sequence | None detected (not a purity proof) | 8 |
| `must_date_modify` | `mustDateModify` | any | None detected (not a purity proof) | 2 |
| `ne` | `ne` | scalar | None detected (not a purity proof) | 26 |
| `nindent` | `nindent` | scalar | None detected (not a purity proof) | 2 |
| `nospace` | `util.DeleteWhiteSpace` | any | None detected (not a purity proof) | 1 |
| `not` | `not` | scalar | None detected (not a purity proof) | 2 |
| `now` | `time.Now` | any | clock-or-timezone | 1 |
| `omit` | `omit` | map | None detected (not a purity proof) | 2 |
| `or` | `or` | any | None detected (not a purity proof) | 0 |
| `osBase` | `filepath.Base` | any | platform | 1 |
| `osClean` | `filepath.Clean` | any | platform | 1 |
| `osDir` | `filepath.Dir` | any | platform | 1 |
| `osExt` | `filepath.Ext` | any | platform | 1 |
| `osIsAbs` | `filepath.IsAbs` | any | platform | 1 |
| `pick` | `pick` | map | None detected (not a purity proof) | 1 |
| `pluck` | `pluck` | sequence | None detected (not a purity proof) | 0 |
| `plural` | `plural` | scalar | None detected (not a purity proof) | 0 |
| `prepend` | `prepend` | sequence | None detected (not a purity proof) | 8 |
| `print` | `fmt.Sprint` | any | None detected (not a purity proof) | 1 |
| `printf` | `fmt.Sprintf` | any | None detected (not a purity proof) | 1 |
| `println` | `fmt.Sprintln` | any | None detected (not a purity proof) | 1 |
| `push` | `push` | sequence | None detected (not a purity proof) | 8 |
| `quote` | `quote` | scalar | None detected (not a purity proof) | 4 |
| `randAlpha` | `randAlpha` | scalar | randomness | 1 |
| `randAlphaNum` | `randAlphaNumeric` | scalar | randomness | 1 |
| `randAscii` | `randAscii` | scalar | randomness | 1 |
| `randBytes` | `randBytes` | scalar | randomness | 2 |
| `randInt` | `closure` | scalar | randomness | 1 |
| `randNumeric` | `randNumeric` | scalar | randomness | 1 |
| `regexFind` | `regexFind` | scalar | None detected (not a purity proof) | 2 |
| `regexFindAll` | `regexFindAll` | sequence | None detected (not a purity proof) | 2 |
| `regexMatch` | `regexMatch` | scalar | None detected (not a purity proof) | 1 |
| `regexQuoteMeta` | `regexQuoteMeta` | scalar | None detected (not a purity proof) | 1 |
| `regexReplaceAll` | `regexReplaceAll` | scalar | None detected (not a purity proof) | 2 |
| `regexReplaceAllLiteral` | `regexReplaceAllLiteral` | scalar | None detected (not a purity proof) | 2 |
| `regexSplit` | `regexSplit` | sequence | None detected (not a purity proof) | 2 |
| `repeat` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `replace` | `replace` | scalar | None detected (not a purity proof) | 1 |
| `required` | `closure` | any | rejection | 2 |
| `rest` | `rest` | sequence | None detected (not a purity proof) | 8 |
| `reverse` | `reverse` | sequence | None detected (not a purity proof) | 8 |
| `round` | `round` | scalar | None detected (not a purity proof) | 5 |
| `semver` | `semver` | any | None detected (not a purity proof) | 1 |
| `semverCompare` | `semverCompare` | scalar | None detected (not a purity proof) | 3 |
| `seq` | `seq` | scalar | None detected (not a purity proof) | 4 |
| `set` | `set` | map | mutation | 0 |
| `sha1sum` | `sha1sum` | scalar | None detected (not a purity proof) | 3 |
| `sha256sum` | `sha256sum` | scalar | None detected (not a purity proof) | 3 |
| `sha512sum` | `sha512sum` | scalar | None detected (not a purity proof) | 3 |
| `shuffle` | `xstrings.Shuffle` | any | randomness | 1 |
| `slice` | `slice` | any | None detected (not a purity proof) | 22 |
| `snakecase` | `xstrings.ToSnakeCase` | any | None detected (not a purity proof) | 1 |
| `sortAlpha` | `sortAlpha` | sequence | None detected (not a purity proof) | 12 |
| `split` | `split` | map | None detected (not a purity proof) | 3 |
| `splitList` | `closure` | sequence | None detected (not a purity proof) | 1 |
| `splitn` | `splitn` | map | None detected (not a purity proof) | 3 |
| `squote` | `squote` | scalar | None detected (not a purity proof) | 2 |
| `sub` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `subf` | `closure` | scalar | None detected (not a purity proof) | 5 |
| `substr` | `substring` | scalar | None detected (not a purity proof) | 0 |
| `swapcase` | `util.SwapCase` | any | None detected (not a purity proof) | 1 |
| `ternary` | `ternary` | any | None detected (not a purity proof) | 0 |
| `title` | `strings.Title` | any | None detected (not a purity proof) | 1 |
| `toDate` | `toDate` | any | clock-or-timezone | 1 |
| `toDecimal` | `toDecimal` | scalar | None detected (not a purity proof) | 2 |
| `toJson` | `toJSON` | scalar | None detected (not a purity proof) | 1 |
| `toPrettyJson` | `toPrettyJson` | scalar | None detected (not a purity proof) | 1 |
| `toRawJson` | `toRawJson` | scalar | None detected (not a purity proof) | 5 |
| `toString` | `strval` | scalar | None detected (not a purity proof) | 3 |
| `toStrings` | `strslice` | sequence | None detected (not a purity proof) | 8 |
| `toToml` | `toTOML` | scalar | None detected (not a purity proof) | 5 |
| `toYaml` | `toYAML` | scalar | None detected (not a purity proof) | 2 |
| `toYamlPretty` | `toYAMLPretty` | scalar | None detected (not a purity proof) | 5 |
| `tpl` | `tplFun` | any | dynamic-code | 12 |
| `trim` | `strings.TrimSpace` | any | None detected (not a purity proof) | 1 |
| `trimAll` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `trimPrefix` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `trimSuffix` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `trimall` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `trunc` | `trunc` | scalar | None detected (not a purity proof) | 0 |
| `tuple` | `list` | sequence | None detected (not a purity proof) | 0 |
| `typeIs` | `typeIs` | scalar | None detected (not a purity proof) | 1 |
| `typeIsLike` | `typeIsLike` | scalar | None detected (not a purity proof) | 1 |
| `typeOf` | `typeOf` | scalar | None detected (not a purity proof) | 1 |
| `uniq` | `uniq` | sequence | None detected (not a purity proof) | 8 |
| `unixEpoch` | `unixEpoch` | scalar | None detected (not a purity proof) | 2 |
| `unset` | `unset` | map | mutation | 0 |
| `until` | `until` | sequence | None detected (not a purity proof) | 0 |
| `untilStep` | `untilStep` | sequence | None detected (not a purity proof) | 0 |
| `untitle` | `untitle` | scalar | None detected (not a purity proof) | 1 |
| `upper` | `strings.ToUpper` | any | None detected (not a purity proof) | 1 |
| `urlJoin` | `urlJoin` | scalar | None detected (not a purity proof) | 9 |
| `urlParse` | `urlParse` | map | None detected (not a purity proof) | 12 |
| `urlquery` | `URLQueryEscaper` | scalar | mutation | 4 |
| `uuidv4` | `uuidv4` | scalar | randomness | 2 |
| `values` | `values` | sequence | unordered | 0 |
| `without` | `without` | sequence | None detected (not a purity proof) | 8 |
| `wrap` | `closure` | scalar | None detected (not a purity proof) | 1 |
| `wrapWith` | `closure` | scalar | None detected (not a purity proof) | 1 |
<!-- [[[end]]] -->

## Sources and upgrades

Start with [dependency maintenance](../dependencies.md#helm-sprig-and-go) when upgrading these sources. It also identifies the
separate native renderer module, replay metadata, CLI versions and CI pins that a Helm upgrade must account for.

- [Helm function map and serialization helpers](https://github.com/helm/helm/blob/v4.3.0/pkg/engine/funcs.go).
- [Helm renderer overrides, offline lookup and DNS behavior](https://github.com/helm/helm/blob/v4.3.0/pkg/engine/engine.go).
- [Sprig function map and aliases](https://github.com/Masterminds/sprig/blob/v3.3.0/functions.go).
- [Go template builtin functions](https://github.com/golang/go/blob/go1.26.0/src/text/template/funcs.go).

Rebuild the inventory and its reference before releasing:

```bash
poetry install --only-root
poetry run hypothesis-helm-builtins
poetry run cog -r docs/compiler/functions.md
```

Use `hypothesis-helm-builtins --check` to regenerate and compare without writing.
Use `--offline` after the sources are cached, `--go /path/to/go` to select the
Go executable, and `--source-lock path.json` to test a reviewed upstream upgrade.
The source downloads and Go build cache live under `.cache/compiler-builtins/`
by default. Ordinary chart tests load the bundled JSON and need neither Go nor
network access. Tagged release builds verify the inventory before packaging.

Both catalog commands build the same Go package under
[`hypothesis_helm_catalog/upstream`](../../pkg/hypothesis_helm_catalog/upstream/):
`main.go` handles command dispatch and shared utilities, `helm.go` analyzes Helm,
Sprig and Go template functions, and `kubernetes.go` extracts API constraints and
checks their boundary cases against Kubernetes validators. The first build caches
the pinned Go dependencies; subsequent `--offline` builds require those dependencies
and the upstream source downloads in the selected cache directory. The extractor
fingerprint includes all three Go files and both dependency manifests.

### What comes from source, and what still needs a contract

```mermaid
flowchart LR
    A[Checksum-locked upstream sources] --> B[Go syntax trees]
    B --> C[Function registrations and runtime overrides]
    B --> D[Signatures, return shapes and local calls]
    D --> E[Detected effects and unresolved boundaries]
    C --> F[Generated compiler inventory]
    E --> F
    F --> G[Symbolic result shapes and effect barriers]
    G --> H[Supported evaluator or native Helm]
```

Local-call traversal propagates detected effects through wrappers and aliases,
including recursive call graphs. Primitive API contracts identify randomness,
clock access, network access and map merging; Helm's rejection and renderer
intrinsics need explicit contracts too. These are small semantic boundaries,
not a classification of every exposed function name. Imported implementations
and unresolved method calls remain recorded as analysis gaps.

This is a conservative source-fact extractor, not a complete Go effect system.
It does not prove purity, infer arbitrary interface behavior, invert functions,
or synthesize exact evaluators. Its reported effects can include internal helper
work; their presence is conservative, and their absence is not evidence that a
call has no effects. Conditional renderer replacements retain effects from both
implementations, so an offline placeholder cannot hide a live-cluster operation.
Compiler passes retain their reviewed argument-level semantics; generated facts
alone cannot prove a rejection, accepted input domain or equivalent manifests.

Return declarations can improve the symbolic IR automatically: for example, a
new slice-returning function yields a collection of unknown length, retaining its
input dependencies. A known scalar return does not supply a value or truthiness.
Imported or interface-valued return types remain unconstrained until a supported
model establishes more.

The extractor uses Go's [syntax-tree parser](https://pkg.go.dev/go/parser).
A future inter-package analysis could use [Go SSA](https://pkg.go.dev/golang.org/x/tools/go/ssa)
for typed call and memory-flow analysis; reflection, callbacks and renderer state
would still require explicit conservative boundaries. No runtime speedup from
using Go is claimed here: this command runs during release preparation.
