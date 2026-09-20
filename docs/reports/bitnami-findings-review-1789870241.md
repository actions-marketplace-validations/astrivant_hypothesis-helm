# Bitnami compiler and diagnostic review

<!-- toc:start -->
**Table of contents**

- [Scope and evidence](#scope-and-evidence)
- [Findings by family](#findings-by-family)
- [Compiler changes completed](#compiler-changes-completed)
- [Schema shims completed](#schema-shims-completed)
- [Priority follow-up work](#priority-follow-up-work)
- [Tooling and setup failures](#tooling-and-setup-failures)
- [Findings that should remain](#findings-that-should-remain)
- [Verification and limits](#verification-and-limits)
<!-- toc:end -->

The completed scan contains substantial input-generation noise, alongside useful chart failures.
A render failure is real evidence that the supplied configuration failed; it is **not automatically evidence of a chart defect**.
A malformed candidate, an expected validation rejection, missing validation setup and a failure on a valid input need different treatment.

## Scope and evidence

Reviewed [the completed report](bitnami.md): **605 distinct diagnostic IDs, 637 chart/error sections, 934 recorded occurrences**.
Every published section is listed in the [diagnostic index](bitnami-findings-index-1789870241.md), with its trigger, assessment and saved diagnostic.
All **751 distinct linked diagnostic files** were read. Targeted native Helm checks investigated representative cases;
this was not a replay of all 934 occurrences. Family assignments identify the next investigation, not a proven false-positive rate.

- Run: `bitnami-charts_1789870241`; finished **2026-09-20 13:14:59.619 UTC**.
- Run fingerprint: `b8b9cd5915b50a4485d0a39dff3399f3b51066808ccf7dc2a32f63c4e2d2dae6`.
- Reviewed Markdown SHA-256: `0d8bcdf20176db38b39bfdd06bbefd5d05171ca4ea17a7652b66a46547ab94cf`.
- **42 linked diagnostics had unfinished shrinking.** Their changed fields are not established minimal causes.
- Native checks used local chart sources with dependencies prepared from the repository. A missing dependency was not treated as a compiler gap.

## Findings by family

Counts below are chart/error sections, adding to 637. The same diagnostic ID may occur under several charts.
A section with several changed fields has one primary investigation category; this does not establish causal attribution.

| Investigation area | Sections | Interpretation |
| --- | ---: | --- |
| Names and resource references | 115 | Invalid-looking names are admitted by weak destination domains or unresolved mappings. Establish the exact API field before narrowing. |
| Composed image references | 88 | Registry, repository, tag and digest interact. Trace their assembled value and fallback conditions. |
| Explicit chart rejection | 85 | Expected rejection or disagreement with the authored schema; not necessarily a broken renderer. |
| Collection element shapes | 71 | Nested arrays, missing object fields and other invalid reference elements survive helper/loop transformations. |
| Destination enums | 53 | Some mappings work, but the catalog contains only a string type. Others still require better provenance. |
| Text serialization and application strings | 52 | Quotes and line breaks may be valid. These require a contract check, not blanket character suppression. |
| Other collection and operand types | 48 | Null elements, arrays in scalar fields, and incorrectly shaped injected resources. |
| Map keys and values | 38 | Annotation/label values, Secret keys and merged dictionaries need independent key/value constraints. |
| Numeric fields and IntOrString | 28 | Preserve optional empty fallbacks; constrain active numeric or percentage branches. |
| Disabled required library | 27 | Disabling `common` leaves live helper calls. Dependency-provider requirements need modeling. |
| Valid string loses its YAML type | 12 | Mostly names such as `"0"` rendered without quotes. These should remain tested. |
| Missing custom resource schema | 9 | Validation prerequisites are missing; resource invalidity is not established. |
| Independently reproduced chart defects | 5 | Ordinary feature switches or a valid LDAP URI reproduce the defect. |
| Generated schema errors | 3 | Tooling errors before useful chart testing, involving JSON Schema dialects. |
| CRD-only rendering | 1 | The invocation omits `--include-crds` and incorrectly reports an empty chart. |
| YAML parser disagreement | 1 | Round-trip parsing rejects Zipkin defaults accepted by Helm and the safe parser. |
| Lost chart source | 1 | A temporary chart vanished during execution; not a chart defect. |

## Compiler changes completed

The [collection projection pass](../../pkg/hypothesis_helm/compiler/passes/domain_collections.py) follows element origins through
helper arguments, nested loops, append-only accumulators and `uniq`. A conditional such as “if this element is a map, use its name”
becomes a condition on **each item**, not on the whole array. Valid mixed string/object representations therefore remain allowed.

On the prepared Bitnami `aspnet-core` chart, generated domains now reject `[[{}]]` at all four affected paths:

- `$.global.imagePullSecrets`
- `$.image.pullSecrets`
- `$.appFromExternalRepo.clone.image.pullSecrets`
- `$.appFromExternalRepo.publish.image.pullSecrets`

Generic regression charts also cover mixed valid references, duplicate names, missing `name`, wrong-shaped elements,
disabled resource guards, unrelated nested arrays, explicit source-type conflicts and quoted conversions.
The tests use renamed helpers, with no Bitnami-specific matching. Native Helm confirms the supported forms and the original malformed case.

This addresses the common collection pattern, **not every one of the 71 sections**. For example, E076 additionally parses helper output
with `fromYaml` and indexes it; the new append analysis alone does not prove that wrapper's contract. Unknown loop replacements,
multiple nested wildcard bindings and unsupported conversions remain explicit limitations.

## Schema shims completed

The compiler already mapped ASP.NET's `service.type` correctly, but the bundled destination was only `type: [string, null]`.
The same limitation existed for `ServiceSpec.sessionAffinity`. The
[reviewed catalog supplements](../../pkg/hypothesis_helm_catalog/data/reviewed-domains.json) now supply their missing enums,
using pinned Kubernetes validation and defaulting sources. Empty and null inputs remain allowed for API defaulting.

The catalog was rebuilt offline and checked for reproducibility. Exact API type/field references carry the shims into both
Service and ServiceList destinations; unrelated strings and custom resources do not acquire these rules.
The prepared ASP.NET chart now excludes `service.type: "'"` while preserving valid Service types and the empty fallback.
The [README inventory](../../README.md#upstream-schema-shims) documents these and the existing supplements for upstream follow-up.

Other gaps remain. The current image-reference and pull-secret-name destinations still provide little more than string types.
Annotation values remain nullable in the schema catalog. These are not all fixed by better traversal: the upstream contract must
supply the missing rule, or an explicitly reviewed, context-specific shim must do so. Do not apply a name regex to every string or
assume every API type called `LocalObjectReference` has an identical contract.

## Priority follow-up work

1. **Complete API destination domains.** Review remaining enums, resource-reference names, annotation keys/values and image grammar.
   Keep versioned source evidence and explicit shim records. Inspect existing bounds before adding another supplement.
2. **Carry structured and transformed origins.** Extend collection reasoning to map entries, supported serialization round trips,
   merged dictionaries and dependent namespaces. Constrain assembled image references through their actual transformation.
3. **Generate jointly valid guarded inputs.** Examples include equal-length MongoDB username/database arrays (E025-E026),
   JetStream/persistence/resource type (E039), and password-update requirements. Preserve authored-schema contradictions separately.
4. **Separate expected rejection from defects.** E021 and E064 record `schema_conflicts=3`: their rejection analysis was not wholly absent.
   Reporting them as missed enum inference would be misleading. A schema conflict can deserve a finding without repeating an expected
   `fail` as a new renderer defect on every sample.
5. **Model required helper providers.** The 27 disabled-library sections need a dependency constraint for live callers.
   Do not globally prohibit disabling dependencies; optional application charts must remain testable.
6. **Correct execution/validation classifications.** Address the CRD-only invocation, generated-schema dialect mismatch and parser
   compatibility below. Missing CRD schemas should report validation unavailable, not assert that the chart generated an invalid resource.

## Tooling and setup failures

| IDs | Evidence | Required treatment |
| --- | --- | --- |
| E527 | `kube-prometheus-crds` contains static `crds/`; native Helm emits zero documents normally and ten with `--include-crds`. | Include static CRDs in the tested bundle or explicitly account for them before declaring the chart empty. Confirmed harness false positive. |
| E511 | Zipkin's default block scalar has a whitespace-only line before its script. Helm and ruamel's safe parser accept it; the round-trip parser rejects it. A tiny chart-independent YAML example reproduces this disagreement. | Align manifest parsing with supported YAML semantics, retaining duplicate-key and type checks. Not a confirmed chart defect. |
| E603-E605 | Generated schemas contain tuple-form `items: [...]`, rejected by a 2020-12 metaschema. | Normalize schema dialects at generation boundaries and check the generated schema before Hypothesis runs. These are generation errors, not failed chart renders. |
| E006 | Temporary `Chart.yaml` is absent during execution. | Retain an execution/incomplete result and stop/join affected children. The source-lifecycle fix is already staged. |
| E528-E534 | Custom kinds lack supplied JSON schemas, including monitoring resources, Grafana and RayCluster. | Provide the corresponding CRD schema. Do not infer resource invalidity from unavailable validation. |

The Zipkin parser disagreement is separate from duplicate mapping keys. Accepting valid blank-line indentation must not disable
checks that catch duplicate keys, such as the kube-arangodb case below.

## Findings that should remain

These targeted checks establish that blanket suppression of YAML, template, or missing-name errors would hide useful results.

| ID / chart | Input | Reproduction |
| --- | --- | --- |
| E002 / PyTorch | `volumePermissions.enabled=true` | Calls undefined `mxnet.volumePermissions.image`; its own helper is named `pytorch.volumePermissions.image`. |
| E601 / Valkey | `serviceBindings.enabled=true` | Calls undefined `valkey.password`. |
| E222 / KeyDB | `replica.networkPolicy.allowExternalEgress=false` | Helm rejects malformed network-policy YAML. |
| E512 / kube-arangodb | `autoscaling.hpa.enabled=true` | Render contains duplicate `namespace` keys; strict YAML parsing rejects it although Helm exits successfully. |
| E079 / Grafana | `ldap.enabled=true`, `ldap.uri="ldap://directory.example"` | Indexing the absent port fails before the documented port fallback can apply. |
| E525 / cloudnative-pg | `operator.serviceAccount.name="0"` | Helm succeeds, but the unquoted name parses as integer `0`, not a string. |

Other E525 sections show the same numeric-looking-name pattern, but only the cloudnative-pg example was independently rerendered here.
RabbitMQ's E525 has a different trigger: an empty Secret key and null value. The index distinguishes it despite the shared diagnostic ID.

Single quotes, newlines, shell fragments and numeric-looking strings are not uniformly invalid user inputs. In particular, multiline
configuration and valid string names must remain in scope. Tighten domains where a contract establishes validity, not merely where
removing a character makes the failure disappear.

## Verification and limits

- The combined collection/compiler/catalog regression group passed **250 tests**; mypy passed across **380 source files**.
- Ruff, formatting, docstring checks, generated CLI references and the offline catalog reproducibility check passed.
- The prepared ASP.NET chart confirms the collection and Service enum behavior described above.
- The catalog rebuild uses cached pinned sources and records reviewed-rule provenance; it does not require runtime source rebuilding by users.
- This review does not erase or relabel the historical scan. A fresh scan is needed to measure the reduction after these changes.
- Family totals are investigation counts, not a statistical estimate of false positives, bug recall or exhaustiveness.
