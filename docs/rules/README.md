# Chart findings and ignored checks

<!-- toc:start -->
<details>
<summary>Table of contents</summary>

- [Stop on findings](#stop-on-findings)
- [Controls for individual values paths](#controls-for-individual-values-paths)
- [Export suppressions from a run](#export-suppressions-from-a-run)
- [What ignoring changes](#what-ignoring-changes)
- [Shared finding library](#shared-finding-library)
- [Finding catalog](#finding-catalog)
- [Reserved code ranges](#reserved-code-ranges)
  - [HH1001: Unclassified template failure](#hh1001-unclassified-template-failure)
  - [HH1201: Render invocation timed out](#hh1201-render-invocation-timed-out)
  - [HH1101: Invalid YAML in rendered output](#hh1101-invalid-yaml-in-rendered-output)
  - [HH1102: Manifest document is not an object](#hh1102-manifest-document-is-not-an-object)
  - [HH1103: Missing resource API version or kind](#hh1103-missing-resource-api-version-or-kind)
  - [HH1104: Invalid resource list](#hh1104-invalid-resource-list)
  - [HH1105: Missing resource name](#hh1105-missing-resource-name)
  - [HH1106: Duplicate resource identity](#hh1106-duplicate-resource-identity)
  - [HH1107: Empty resource bundle](#hh1107-empty-resource-bundle)
  - [HH1108: Kubernetes schema validation failed](#hh1108-kubernetes-schema-validation-failed)
  - [HH1011: Rendered output cannot be encoded as JSON](#hh1011-rendered-output-cannot-be-encoded-as-json)
  - [HH1012: Unclassified baseline lint failure](#hh1012-unclassified-baseline-lint-failure)
  - [HH2001: Undocumented values path](#hh2001-undocumented-values-path)
  - [HH2002: Unspecified values type](#hh2002-unspecified-values-type)
  - [HH2003: Missing values description](#hh2003-missing-values-description)
  - [HH2004: No supplied default for a values path](#hh2004-no-supplied-default-for-a-values-path)
  - [HH2005: Unresolved template value access](#hh2005-unresolved-template-value-access)
  - [HH2006: Opaque object schema](#hh2006-opaque-object-schema)
  - [HH3001: Template accesses a missing object](#hh3001-template-accesses-a-missing-object)
  - [HH3002: Incompatible value type in template](#hh3002-incompatible-value-type-in-template)
  - [HH3003: Undefined named template](#hh3003-undefined-named-template)

</details>
<!-- toc:end -->

[Project](../../README.md) · [CLI reference](../cli/README.md)

Codes describe observed conditions across runs, independently of Python exceptions.
The catalog distinguishes **violations** (an input or output fails a checked contract), **warnings**
(missing values documentation or defaults), and **diagnostics** (execution or analysis could not establish a result).
A timeout, unresolved dynamic access or an unclassified Helm failure does not by itself establish a chart defect.
Even a violation can be intentional: a chart designed to render nothing can disable the nonempty-output check.
The report's `E001`, `E002`, etc. identify groups within one report and cannot be used to disable checks.

Generate [the repository configuration](../../.hypothesis-helm.yaml) in your working directory:

```bash
helm hypothesis --generate-config > .hypothesis-helm.yaml
```

The output matches the checked-in template, including code descriptions and commented input-domain settings.
It ignores `HH2006` (opaque-object warnings); other codes are commented out and remain enabled.
Remove or comment out the `HH2006` entry to enable those warnings. Uncomment other checks to disable them:

```yaml
ignored:
  - HH1106  # Duplicate resource identities
  - HH2003  # Missing schema descriptions
```

```bash
helm hypothesis rules
helm hypothesis rules --format config  # Also prints the complete default template
helm hypothesis rules --format json > finding-catalog.json
helm hypothesis test ./charts --config .hypothesis-helm.yaml
helm hypothesis scan https://github.com/example/charts.git --ignore HH2003
helm hypothesis test ./charts --report --disable-codes HH2006,HH2003
```

`audit`, `generate`, `test`, `scan`, and `run` read `.hypothesis-helm.yaml` from the working directory by default.
`--config FILE` selects another file. Use `--disable-codes HH2006,HH2003` for a comma-delimited list,
or repeat `--ignore CODE` for individual codes. These options can be repeated and combine with the file's list;
duplicates are removed. Surrounding whitespace is accepted; quote lists containing spaces. Empty entries and unknown codes are errors.
Run generated suites through `helm hypothesis run` to apply this file; plain `pytest` does not load CLI configuration.
An empty or fully commented `ignored` list disables nothing. Unknown codes and configuration keys are errors.
Without a config file or CLI exclusions, all checks remain enabled.
Remote repositories cannot supply their own ignore policy: the policy is loaded locally before fetching charts.

## Stop on findings

Add `--fail` to stop on the first unsuppressed finding and exit `1`. This includes audit warnings such as
`HH2001` (a values path missing from the schema), `HH2004` (a path missing from `values.yaml`), and `HH2006` (an opaque object).
It applies to `audit`, `generate`, `test`, `scan`, and `run`. The former `--strict` option has been removed.

Without `--fail`, repository scans record audit findings as warnings and continue testing the chart and subsequent charts.
Render and test failures remain failures; they can produce exit `1` after the scan finishes. Audit warnings alone do not.
Ignored findings neither stop execution nor change its exit status, and audits retain them under `ignored_findings`.
Parallel execution stops scheduling work and joins active workers when a failed property is reported.

```bash
helm hypothesis test ./charts --fail
helm hypothesis audit ./chart --fail
```

## Controls for individual values paths

Use `ignored` and `enabled` inside `input_constraints` to override checks for one chart's input branches:

```yaml
ignored:
  - HH2006
input_constraints:
  - charts: [example]
    path: $.credentials
    ignored: [HH2001]
  - charts: [example]
    path: $.credentials.token
    enabled: [HH2001]
  - charts: [example]
    path: $.extraConfig
    enabled: [HH2006]
```

The first rule suppresses undocumented-schema findings beneath `credentials`; the second restores them for `credentials.token`.
The third enables opaque-object findings for `extraConfig` despite the global exclusion. These rules affect findings, not generated types.
A code-only rule needs no `profile` or `schema` and may target a missing path. A rule can also combine code controls with a generation constraint.

`charts` accepts `Chart.yaml` names, glob patterns, and [source/name matrices](../input-domains/README.md#source-and-chart-matrices). A path includes its descendants; `$.items[*].name` matches array items,
and `$` applies to the whole chart. More specific paths override broader paths and global exclusions, including CLI exclusions.
If separate rules for the same path disagree, enabling wins, independent of their order. A single rule cannot both enable and ignore a code.

Audit controls match the finding's path. For rendered candidates, controls match **all fields changed from the baseline**, including
changes needed to satisfy dependent inputs. A failure is suppressed only if every changed path permits it. This prevents an exception
for one field from hiding a failure when another field changes alongside it. These paths identify the input context, not a proven cause.
Baseline checks and diagnostics without a known input path use only global and `$` controls.

For narrower generated values while keeping checks enabled, configure [input domains](../input-domains/README.md).
Disabling HH2006 only suppresses warnings about objects lacking a declared field structure or typed map-value schema.
It does not skip those inputs or disable validation of structured fields.

## Export suppressions from a run

Add `--export-suppressions` to write an editable `suppressions.yaml` after each chart finishes:

```bash
helm hypothesis test ./charts --filter --export-suppressions --report
helm hypothesis scan https://github.com/example/charts.git --export-suppressions --report
helm hypothesis audit ./chart --export-suppressions
helm hypothesis run ./generated-tests --export-suppressions
```

Each file lives in that chart's artifact directory; the terminal prints its location and scan reports link to it.
Recursive scans export before starting the next chart. Fail-fast, timed-out, and interrupted runs export the observations
collected so far. Generated-suite shards write separate drafts in their respective artifact directories.
No export is made for charts that were never started. Audits use `.cache/hypothesis-helm/audits/` unless `--artifact-dir` overrides it.

The file contains ordinary `input_constraints`, grouped by finding category, with each code's title and classification:

```yaml
input_constraints:
  # Manifest
  # HH1101: Invalid YAML in rendered output (violation)
  - charts:
      - sources: [https://github.com/example/charts.git]
        names: [external-dns]
    path: $.txtEncrypt.secretName
    ignored: [HH1101]
```

**These are suggestions, not active suppressions.** Remove the codes or entries you want to keep detecting, then copy the remaining
entries into your existing configuration's `input_constraints` list. This preserves your generation settings and existing controls.
More specific `enabled` rules still take precedence. Sources and chart names match the original run; same-named charts within that
source also match. Adjust those selectors if you test the chart through a different repository URL or directory.

The exporter covers all recorded finding codes, including intermediate failures during shrinking, and removes duplicate rules.
It removes descendant rules already covered by an observed parent, but does not invent broader parent rules to shorten the file.
Failures involving several changed fields require rules for **all** those fields, including changes to dependent inputs.
These paths describe the tested input context, not a proven cause of the error.

Rules suppress a code for any value beneath their paths, not just one failing value or one exact combination.
Failures on unchanged defaults need a chart-wide `$` rule. Array indices become `[*]`; keys unsupported by the path syntax use their
nearest supported parent. Those broader rules are labelled explicitly. Tool/setup errors without a catalog code are counted as
uncovered rather than assigned an invented code. A later run may reveal additional findings after these checks are suppressed.

The original findings and exit status remain unchanged. Requesting this export bypasses completed-chart reuse so the draft reflects
a fresh run; saved suites still honor their selected, cached, and sharded property sets.

## What ignoring changes

Disabled manifest checks allow the remaining checks to continue when the parsed output permits it.
Kubernetes schema checking is skipped where `HH1108` is disabled. Schema preparation still runs if a path rule can enable it elsewhere.
Each code selects an individual condition. For example, ignoring `HH3001`
(missing object access) does not ignore `HH3002` (incompatible type). `HH1001` covers only unclassified template failures;
it does not suppress these specific findings or baseline lint (`HH1012`).
If Helm fails or produces unreadable output, ignoring that failure cannot create valid manifests: the affected candidate is excluded,
or the baseline/property is marked `ignored`/skipped when further checks cannot run. These cases do not become successful validation witnesses.
A generated Python property blocked by such a failure is skipped, including its remaining examples.
Audits keep ignored findings separately. Reports list disabled checks, and candidate reports count ignored blocking failures by code.
Passing means the enabled checks passed; it does not certify the disabled checks.

The resolved policy is inherited by workers and included in cache identities. Re-enabling a check forces fresh validation.
All shards must use the same policy. Ignore codes do not suppress configuration errors, missing executables, dependency preparation failures,
whole-run deadlines, interrupts, or assertions in user-written Python tests.
External tools such as kubesec retain their own rule systems; `DL` and `SC` codes are not hypothesis-helm codes.

## Shared finding library

[`findings/catalog.py`](../../pkg/hypothesis_helm/findings/catalog.py) stores each code's category, evidence criterion,
example and suggested action. [`FindingGenerator`](../../pkg/hypothesis_helm/findings/generator.py) creates structured
findings and generates the CLI listing, JSON catalog, commented configuration and reference below from those definitions.
Add a definition and a detector with regression tests when implementing a new check; a catalog entry alone does not detect anything.

Audits attach structured findings to values paths and template references. Test reports retain the classification,
diagnostic, triggering paths and values, and suggested action. Exceptions carry these findings where execution needs to stop;
they do not define the taxonomy. A template error, a manifest check and an audit can report findings through the same interface.

Specific Helm classifications require a recognized diagnostic. Unrecognized messages stay unclassified.
User-authored `fail`/`required` messages do not become type or missing-object findings just because they contain similar wording.
The existing input-rejection verification still decides which explicit configuration constraints can be filtered.
For an invalid manifest, the catalog describes the observed failure and lists quoting
as one possible cause to investigate.

## Finding catalog

## Reserved code ranges

Unclassified findings occupy `HH1000`-`HH1099`, manifest findings `HH1100`-`HH1199`, and execution findings
`HH1200`-`HH1299`. Each group has a 100-code range for future classifications. Unallocated codes are reserved,
not valid ignore entries. Existing values/analysis codes (`HH200x`) and template codes (`HH300x`) are unchanged.

This renumbers existing findings. Update ignore/enable lists when upgrading:

| Previous code | Current code | Finding |
| --- | --- | --- |
| HH1002 | HH1201 | Render timeout |
| HH1003 | HH1101 | Invalid rendered YAML |
| HH1004 | HH1102 | Non-object document |
| HH1005 | HH1103 | Missing API version or kind |
| HH1006 | HH1104 | Invalid resource list |
| HH1007 | HH1105 | Missing resource name |
| HH1008 | HH1106 | Duplicate resource identity |
| HH1009 | HH1107 | Empty resource bundle |
| HH1010 | HH1108 | Kubernetes schema validation |

Unclassified codes `HH1001`, `HH1011` and `HH1012` retain their meanings. Published report snapshots retain the codes
used when they were produced. Old codes are not aliases in new configurations.

<!-- [[[cog
import cog
from hypothesis_helm.findings.generator import FindingGenerator
cog.out(FindingGenerator.render("markdown"))
]]] -->
| Code | Finding | Category | Kind |
| --- | --- | --- | --- |
| `HH1001` | Unclassified template failure | unclassified | diagnostic |
| `HH1201` | Render invocation timed out | execution | diagnostic |
| `HH1101` | Invalid YAML in rendered output | manifest | violation |
| `HH1102` | Manifest document is not an object | manifest | violation |
| `HH1103` | Missing resource API version or kind | manifest | violation |
| `HH1104` | Invalid resource list | manifest | violation |
| `HH1105` | Missing resource name | manifest | violation |
| `HH1106` | Duplicate resource identity | manifest | violation |
| `HH1107` | Empty resource bundle | manifest | violation |
| `HH1108` | Kubernetes schema validation failed | manifest | violation |
| `HH1011` | Rendered output cannot be encoded as JSON | unclassified | diagnostic |
| `HH1012` | Unclassified baseline lint failure | unclassified | diagnostic |
| `HH2001` | Undocumented values path | values | warning |
| `HH2002` | Unspecified values type | values | warning |
| `HH2003` | Missing values description | values | warning |
| `HH2004` | No supplied default for a values path | values | warning |
| `HH2005` | Unresolved template value access | analysis | diagnostic |
| `HH2006` | Opaque object schema | values | warning |
| `HH3001` | Template accesses a missing object | template | violation |
| `HH3002` | Incompatible value type in template | template | violation |
| `HH3003` | Undefined named template | template | violation |

### HH1001: Unclassified template failure

Detected when: Helm template exits unsuccessfully without a recognized diagnostic.

Example: A chart-specific fail message that has not been verified as an input constraint.

Suggested action: Inspect the Helm diagnostic and reproducer; the exit alone does not establish a chart defect.

### HH1201: Render invocation timed out

Detected when: The Helm subprocess exceeds its invocation deadline.

Example: A render takes longer than the configured timeout.

Suggested action: Check runner load and render cost, then adjust the timeout if appropriate. This is incomplete validation, not proof of a bug.

### HH1101: Invalid YAML in rendered output

Detected when: The YAML parser rejects rendered output, or Helm reports a YAML parse error.

Example: A substituted value breaks YAML indentation.

Suggested action: Inspect the failing YAML and template interpolation, including quoting and indentation.

### HH1102: Manifest document is not an object

Detected when: A nonempty rendered document is a scalar or sequence instead of a mapping.

Example: A template emits a bare string document.

Suggested action: Emit a resource mapping or remove the stray document.

### HH1103: Missing resource API version or kind

Detected when: A resource has no nonempty string apiVersion or kind.

Example: kind: null

Suggested action: Supply both resource identifiers in every branch that emits a resource.

### HH1104: Invalid resource list

Detected when: A resource with kind List has no array-valued items field.

Example: kind: List with items: null

Suggested action: Emit an items array, including an empty array when appropriate.

### HH1105: Missing resource name

Detected when: The resource fails the tool's nonempty metadata.name contract.

Example: metadata: {name: ""}

Suggested action: Provide a name in each resource branch; ignore this check if your workflow intentionally uses generated names.

### HH1106: Duplicate resource identity

Detected when: Two resources in the checked bundle share apiVersion, kind, namespace and name.

Example: Enabling an optional component emits a second ConfigMap with the same identity.

Suggested action: Give the resources distinct names or make their activation conditions exclusive.

### HH1107: Empty resource bundle

Detected when: The active test requires resources but this configuration renders none.

Example: All resource-producing branches are disabled.

Suggested action: Check resource activation; ignore this contract if an empty chart is intentional.

### HH1108: Kubernetes schema validation failed

Detected when: The configured Kubernetes validator rejects the output.

Example: An unquoted boolean becomes a non-string ConfigMap data value.

Suggested action: Use the validator's field path and expected type to check the template and input schema.

### HH1011: Rendered output cannot be encoded as JSON

Detected when: Manifest processing reports a JSON representation failure.

Example: A YAML tag produces an unsupported Python scalar object.

Suggested action: Inspect YAML tags and parser support to determine whether the failure comes from an unsupported value or a chart defect.

### HH1012: Unclassified baseline lint failure

Detected when: Helm lint fails on the supplied chart defaults.

Example: Lint reports an error before generated inputs are tested.

Suggested action: Read the lint diagnostic; distinguish chart errors from missing dependencies or environment requirements.

### HH2001: Undocumented values path

Detected when: The audit finds a values path with no matching schema declaration.

Example: Templates read service.mode but its schema entry is absent.

Suggested action: Document the path in values.schema.json, including its accepted values.

### HH2002: Unspecified values type

Detected when: A schema path declares no type, enum or const.

Example: service.mode has only a description: "Service mode".

Suggested action: Declare the accepted type or a finite set of values.

### HH2003: Missing values description

Detected when: A typed schema path has no description.

Example: A boolean gate is declared without explaining which component it enables.

Suggested action: Describe the field's behavior and any requirements shared with other fields.

### HH2004: No supplied default for a values path

Detected when: A discovered path is absent from the original values file.

Example: A conditional branch reads credentials.token, which defaults omit.

Suggested action: Supply a default or document when users must provide the field. Render the relevant configurations to check its requirements.

### HH2005: Unresolved template value access

Detected when: Static analysis cannot resolve a template's values access.

Example: An index expression selects a key computed at runtime.

Suggested action: Review the dynamic access and coverage report. Exercise the affected inputs to establish their rendering behavior.

### HH2006: Opaque object schema

Detected when: An object permits unspecified entries without named fields, patterned fields or a typed map-value schema.

Example: extraConfig: {"type": "object"} permits unspecified keys and values.

Suggested action: Describe fields with properties, patternProperties or typed additionalProperties. Ignore HH2006 for intentional free-form configuration; tests still sample those values.

### HH3001: Template accesses a missing object

Detected when: Helm reports a nil pointer while evaluating a template field.

Example: A template reads .Values.service.port when service is absent.

Suggested action: Guard or default the parent object, or require it in the values schema.

### HH3002: Incompatible value type in template

Detected when: Helm reports a wrong value type, a field unavailable on a type, or an unsupported range operand.

Example: A string-only template function receives a boolean allowed by the input schema.

Suggested action: Align the template operation with the accepted input types, or narrow the schema.

### HH3003: Undefined named template

Detected when: Helm reports that a called named template is not defined.

Example: include "service.name" . refers to an absent helper.

Suggested action: Check the helper name, its definition and dependency availability.
<!-- [[[end]]] -->
