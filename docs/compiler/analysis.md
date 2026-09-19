# Analysis passes

<!-- toc:start -->
**Table of contents**

- [Branch knowledge](#branch-knowledge)
- [Input inventory](#input-inventory)
- [Dependency discovery and activation](#dependency-discovery-and-activation)
- [Explicit rejection discovery](#explicit-rejection-discovery)
  - [Fixed Helm context and concrete templates](#fixed-helm-context-and-concrete-templates)
  - [Incomplete-analysis warnings](#incomplete-analysis-warnings)
  - [Transformed input domains](#transformed-input-domains)
- [Maximum output complexity](#maximum-output-complexity)
- [Sampling profile](#sampling-profile)
<!-- toc:end -->

[Compiler](README.md) · [Syntax trees](syntax-trees.md) · [Selection passes](selection.md)

These passes describe what the chart can consume or produce. Their results guide
testing and populate audits. Test results come from executing the selected checks.

## Branch knowledge

[`branches.py`](../../pkg/hypothesis_helm/compiler/passes/branches.py) narrows possible values inside supported conditions,
removes contradictory nested branches, and merges the surviving alternatives before analyzing later statements.
It runs after literal folding in the exact-equivalence compiler, which is also used by maximum-output analysis.
The [branch knowledge lattice](lattice.md) defines the operations, supported conditions and uncertainty rules.
Audits expose source-level decisions under `complexity.branch_analysis`; test reports include them under `pruning.branch_analysis`.

## Input inventory

[`inputs.py`](../../pkg/hypothesis_helm/compiler/passes/inputs.py) compares three
sources: supplied values, declared schema fields, and references found in
templates. `InputInventory.build` binds these paths to the shared values model
and records their source locations.

The result separates referenced fields missing from values or schema from supplied
fields with no known reference. Dynamic map access, unresolved helper contexts,
and dependency forwarding remain explicit uncertainties. An unmatched field is
not automatically unused.

`known_fields` retains the most specific named references: a parent container is
not counted again when a referenced descendant is known. This supplies a lower
bound for input coverage, not proof that every possible input path was discovered.
`FieldCoverage` records which of those paths changed during testing.<sup>[\[1\]](../inputs/README.md)

## Dependency discovery and activation

[`dependencies.py`](../../pkg/hypothesis_helm/compiler/passes/dependencies.py)
reads chart metadata and installed child charts, including archives. It records
child inputs under their dependency name or alias, ordered Boolean conditions,
shared tag controls, and the parent dependencies that must also be enabled.
The data records live in
[`asts/dependencies.py`](../../pkg/hypothesis_helm/compiler/asts/dependencies.py).

This catches enablement settings that appear only in `Chart.yaml`. For a selected
child field, generation can propose a context that enables the child while
preserving that field's chosen value and the parent schema. The original context
also remains eligible because parent templates can read child values even when
the child is disabled. Finite planning proposes corresponding interaction groups
within its existing group-size budgets.

Missing child sources, ambiguous imports, and unsupported forwarding are reported.
Activation states are predictions checked through Helm execution. They do not
authorize skipping renders: charts with dependencies are outside the current
exact-equivalence and topology proof contract.<sup>[\[2\]](../scanning/README.md#discovery-and-testing)

## Explicit rejection discovery

[`Contracts.build`](../../pkg/hypothesis_helm/compiler/asts/contracts.py) locates
calls to `fail` and `required` in parsed expressions. It follows supported named
helper calls and evaluates the branches that lead to those calls for a candidate.
It does not classify failures by searching comments or error-message keywords.

A prediction identifies the requirement, its location, the input values read,
and any literal choices inspected on the rejecting branch. Installed dependencies
are included, with aliases mapped back to the parent's values paths. Disabled or
unresolved dependencies cannot establish a child rejection.

For example, a helper may accept `(dict "type" .Values.resourcesPreset)` and test
`hasKey $presets .type` before calling `fail`. If `$presets` was constructed with
literal keys, the compiler retains those keys and traces `.type` back to
`$.resourcesPreset`. It does not extract choices from the error message or infer
them from successful renders. A caller can still bypass that helper when the
preset is `none`, custom resources are supplied, or the resource is disabled.
Those branches keep their existing input domains.

These are **candidate-specific choices**, not an unconditional enum added to
`values.schema.json`. The [rejection policy](selection.md#rejection-guided-generation)
confirms each enum rejection with Helm before proposing a replacement. Reports
retain the source, conditions, original inputs, and choices under
`configuration_rejections.requirements`.

| Template construct | Analysis support |
| --- | --- |
| `if`, `else if`, `else`; `and`, `or`, `not`, `empty` | Follow supported conditions for this candidate; preserve short-circuit evaluation. |
| Named `include` with `.`, `$`, or nested `dict` arguments | Follow helper calls and local `:=` aliases; retain the original values path across context changes. |
| `with`, `else with`; declarations and `=` assignments | Change dot within the selected block, retain the invocation's `$`, and update the nearest enclosing declaration without leaking shadowed variables. |
| `range` over lists or string-key maps; `else`, `break`, `continue` | Follow concrete elements and sorted map keys. Keep loop variables scoped and preserve surrounding assignments. |
| Statically named `template` and `block` | Bind a fresh helper scope to the argument pipeline; an omitted argument supplies nil. Conflicting definitions remain unresolved. |
| Literal `dict` + `hasKey`; literal string `list` + `has` / `mustHas` | Retain source-authored choices when membership fails on a rejecting branch. |
| String-key `index` / `get` | Follow map lookups whose input path can be represented unambiguously. |
| `keys`, `sortAlpha`, `join`, `printf` with string `%s` arguments | Construct rejection messages. Unsorted keys may occur in any order, but native verification requires every key exactly once. |
| `eq`, `ne`, `lt`, `le`, `gt`, `ge` | Compare compatible strings, Booleans, or integers; ordered Boolean comparisons are unsupported. |
| `required`, `fail`, `list`, `append`, `without` | Recognize explicit rejection and supported message assembly. |
| `len` on strings, lists and maps | Evaluate collection lengths and UTF-8 byte lengths for strings. |
| `default`, `coalesce` | Evaluate fallback selection, including empty strings, false, zero and empty collections; evaluate arguments eagerly. |
| `lower`, `upper`, `trim` | Model ASCII case conversion and surrounding whitespace removal. |
| `trimAll`, `trimPrefix`, `trimSuffix`, `replace`, `contains`, `hasPrefix`, `hasSuffix` | Model literal string operations in their Helm argument order. |
| `add`, `add1`, `sub`, `mul`, `min`, `max` | Model signed 64-bit integer operands when no intermediate result overflows. |
| `atoi`, `toString` | Model decimal string conversion and string/integer/Boolean formatting; ambiguous conversions remain unresolved. |
| `regexMatch`, `mustRegexMatch` | Evaluate the bounded ASCII regex subset described below. |

These scope rules follow [Go's template language](https://pkg.go.dev/text/template#hdr-Variables)
and are checked against native Helm. The compiler analyzes up to 16 nested helper
calls by default, counting the first call as level 1. This is our analysis budget,
not a Helm rendering restriction. Override it for a run with
`helm hypothesis test ./chart --filter --compiler-call-depth 64`, or configure:

```yaml
compiler:
  max_call_depth: 64
```

`--compiler-call-depth` takes precedence over the config on `audit`, `generate`,
`test`, `scan` and `run`. Both rejection analysis and helper-aware destination
typing use it; workers inherit it, and changing it invalidates cached results.
When the budget is exhausted, analysis leaves the affected code unresolved and
Helm tests continue normally. Raising it permits deeper analysis, but does not
make unsupported expressions or cyclic destination helpers safe to interpret.
Helm has its own [repeated-include recursion guard](https://github.com/helm/helm/blob/v4.3.0/pkg/engine/engine.go),
which this setting does not change.

Other analysis safeguards remain in place, including Python's recursion limit.
Rejection analysis stops after 10,000 statements and
iterations per root template; a range containing more than 4,096 elements remains
unresolved. List-member evidence retains its containing values path and does not
invent an editable scalar enum for the whole list.

Unknown expressions remain ordinary Helm tests. The remaining boundaries are:

| Construct | Why it remains unresolved |
| --- | --- |
| `lookup`, clock and random functions | External or changing state is not injected or predicted. Helm executes these normally. |
| Unsupported operations inside `tpl`, template-local definitions and recursive expansion beyond the call budget | The compiler cannot establish the generated program's behavior within its supported subset. |
| `.Files.Glob`, `.Files.GetBytes`, binary files and file contexts exceeding the inspection budget | These file operations remain native Helm work. |
| Integer/channel ranges; ranges over unsorted `keys` results | Iterator semantics or iteration order are outside the supported deterministic subset. |
| `set`, `unset`, `merge`, `mergeOverwrite` | Can change the context used by later conditions. A direct mutation before a rejection blocks prediction. |
| Unicode case conversion, floating-point arithmetic, implicit numeric coercion, integer overflow | These operations need additional Go-specific semantics; Python's behavior is not assumed to match. |
| Regex groups, alternation, flags, character-class shortcuts and multiple variable repetitions | These expressions exceed the deliberately restricted regex evaluator. |
| Candidate-supplied maps/lists | Their observed members do not prove a fixed enum. Membership can still establish a supported rejection. |
| Ambiguous helper definitions, unresolved globals/imports | The compiler cannot reliably identify the input origin or execution context. |
| Helper calls exceeding `compiler.max_call_depth` (default: 16) | The configured analysis budget has been exhausted; increase it to analyze deeper call chains. |

### Fixed Helm context and concrete templates

Rejection analysis can now follow guards that depend on the renderer's capabilities,
chart files, or a concrete `tpl` string:

| Input to the guard | How analysis obtains it |
| --- | --- |
| `.Capabilities.KubeVersion` and `.Capabilities.APIVersions.Has` | A small probe using the same Helm binary and `--kube-version` as the real render. Results are cached per process. |
| `semverCompare` | Helm evaluates the concrete constraint and version; the compiler does not substitute Python version-comparison rules. |
| `.Files.Get` and `.Files.Lines` | Helm packages a temporary snapshot, applying its own loader and `.helmignore` rules. Analysis reads each chart's accessible files, including dependencies and aliases. |
| `tpl` | The compiler parses the current candidate's actual string, including file-backed text, and evaluates supported expressions with a fresh helper scope. |

Schema availability does not establish cluster API availability. These capabilities describe
the current offline `helm template` invocation, not a live cluster. The context probes do not
execute the chart's original templates or modify its files. File snapshots are bounded to
64 MiB and 10,000 archive entries; individual `tpl` strings are bounded to 1 MiB and share
the configured helper call-depth limit.

Every rejection involving capabilities, file contents or `tpl` requires a native Helm
verification render, even after earlier candidates matched. Authored-schema contradictions
remain findings. This support guides rejection filtering; it does not extend the separate
[exact-equivalence proof contract](selection.md#exact-equivalence-pruning).

The implementation follows Helm's [file access methods](https://github.com/helm/helm/blob/v4.3.0/pkg/engine/files.go),
[chart loader](https://github.com/helm/helm/blob/v4.3.0/pkg/chart/v2/loader/load.go), and
[`tpl` execution scope](https://github.com/helm/helm/blob/v4.3.0/pkg/engine/engine.go).

### Incomplete-analysis warnings

`HH2007` warns before native rendering when an attempted analysis cannot establish a result.
It includes the template location and reason, and avoids repeating the same warning within
an analysis instance. Workers retain their own diagnostics. An unknown expression never
justifies discarding a candidate. A separate, explicit rejection may still exclude it after
Helm verifies that rejection. Exact-equivalence analysis also emits this code when a candidate
must fall back to rendering.

Clock, randomness and cluster lookups keep their normal Helm behavior; this change does not
inject a clock, seed Helm's random functions or simulate a Kubernetes cluster.
The rejection report records `analysis_fallbacks` and `incomplete_evaluations`; the
pruning report records `fallback_reasons`. The evaluation count includes repeated inputs and
proposed repairs, so it is not a count of distinct rendered inputs. These are analysis limits,
not confirmed chart defects.

Silence the warning without removing any tests:

```sh
helm hypothesis test ./chart --filter --disable-codes HH2007
```

Or use global `ignored: [HH2007]` or a targeted rule:

```yaml
input_constraints:
  - charts: [my-chart]
    path: $.extraConfig
    ignored: [HH2007]
```

`enabled: [HH2007]` enables it under a branch despite global suppression.
With `--fail`, an unsuppressed warning stops the chart run; without it, testing continues.

### Transformed input domains

[`transformations.py`](../../pkg/hypothesis_helm/compiler/asts/transformations.py)
retains a transformation tree alongside each evaluated value. Its leaves point
back to the original values paths. For example:

```gotemplate
{{ $mode := .Values.mode | trim | lower | default "small" }}
{{ if not (has $mode (list "small" "large")) }}
  {{ fail "unsupported mode" }}
{{ end }}
```

The allowed **outputs** are `small` and `large`. The original inputs also include
`SMALL`, ` Large ` and the empty string, because those transformations produce
an allowed output. The compiler therefore retains the condition "the transformed
value belongs to this allowlist" instead of replacing the input schema with those
two strings. Mathematically, this is the **preimage** of the output allowlist under
the transformation, restricted to the branch being tested.

For sampled generation, the compiler works backwards through supported operations
to propose a few input values. For instance, an output of `"8"` from
`toString (add .Values.count 3)` suggests `count: 5`. Every proposal is evaluated
forwards through the complete expression, then checked against the chart's schema,
remaining requirements and native Helm rendering. These witnesses do not enumerate
the whole preimage; a missing witness does not establish that the domain is empty.
Finite assignments stay fixed, valid aliases remain eligible, and authored-schema
conflicts remain findings. Reports retain the expression and allowed outputs under
`configuration_rejections.requirements[].transformed_domains`.

The model follows the supported [Sprig string and arithmetic functions](https://github.com/Masterminds/sprig/blob/v3.3.0/functions.go)
and [fallback semantics](https://github.com/Masterminds/sprig/blob/v3.3.0/defaults.go).
In particular, fallback arguments are evaluated eagerly even when not selected.
All rejection predictions involving these transformations require native Helm
confirmation before exclusion.

Regex evaluation supports ASCII literals, dot, simple character classes, `^`/`$`
anchors and at most one variable repetition, such as `[a-z0-9-]+`. Fixed counted
repetitions are also supported. Patterns are limited to 256 characters, subjects
to 4,096, and repeat counts to 1,000. The end anchor is translated to require the
actual end of the string, including when the input ends in a newline. Other Go
regex constructs remain ordinary Helm tests; Python-only regex features are never
accepted as Helm semantics. See the [Go regex syntax](https://pkg.go.dev/regexp/syntax).
Other string transformations have a 16,384-character analysis budget; preimage
search visits at most 128 proposal nodes per observed allowlist.

This support belongs to rejection analysis. Projecting arbitrary transformed
manifest fields back into destination schemas, or proving output equivalence
through those transformations, remains outside this pass.

## Maximum output complexity

[`complexity.py`](../../pkg/hypothesis_helm/compiler/passes/complexity.py) searches
for the largest supported manifest structure that allowed values can produce.
Its score is **breadth × depth**: breadth counts the largest number of nodes on
any one level of the output tree; depth counts the longest path from the bundle
root. Resources, field values, and array entries contribute nodes. Longer scalar
text does not increase the score.<sup>[\[3\]](../inputs/README.md)

The deterministic search proceeds as follows:

1. Split a supported finite input domain into factors, each with allowed choices.
2. Identify the factors each template reads and evaluate that template's local
   assignments. Store the resulting output shapes in a component table.
3. Assign factors in a stable order that prioritizes shared uses and conditions.
   For each partial assignment, compute an upper bound from compatible table rows.
4. Skip a subtree when its bound cannot improve the best valid complete output
   already found. Validate complete assignments and their assembled resource
   bundles before accepting a new best result.

This is **branch-and-bound**: a bound can rule out many assignments without
visiting each one. It does not assume that enabling every Boolean independently
produces the largest valid chart.

Complete component tables and a completed search establish `compiled-maximum`
within the supported model. Unsupported operations or an exhausted budget produce
`unknown`; any retained lower bound comes from a checked complete configuration.
The analysis uses compiled output, without invoking Helm or Kubernetes API schema
validation. It measures potential output structure, not bug count or runtime.
[`compiler/complexity.py`](../../pkg/hypothesis_helm/compiler/complexity.py) supplies
the tree metric and size-based theoretical ceiling.

## Sampling profile

[`sampling.py`](../../pkg/hypothesis_helm/compiler/passes/sampling.py) combines a
fresh complexity result with input domain sizes, scalar kinds, conditional nesting
depth, and the largest number of distinct direct values references in a template.
The latter is reported as `interaction_order`, describing the template's input
references. Measuring causal interactions requires testing their effects on output.

A **gate** in these records means a conditional decision. Gate depth counts how
many such decisions can enclose a template statement. A source fingerprint binds
the profile to the analyzed chart. Unknown complexity or changing source bytes
prevents a supported profile.

The adaptive sampling policy uses this profile to seek applicable benchmark
calibration. `sampling.py` describes the chart; it does not choose a sample size
by itself. Unsupported or unmatched profiles retain ordinary filtering instead
of assuming a bug-discovery rate.<sup>[\[4\]](../adaptive-filtering/README.md)
