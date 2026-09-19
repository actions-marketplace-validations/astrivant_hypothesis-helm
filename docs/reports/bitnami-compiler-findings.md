# First three Bitnami charts: compiler review

<!-- toc:start -->
**Table of contents**

- [Run and coverage](#run-and-coverage)
- [Findings and priorities](#findings-and-priorities)
  - [1. Preserve failures before shrinking finishes](#1-preserve-failures-before-shrinking-finishes)
  - [2. Normalize YAML containers before evaluating transformations](#2-normalize-yaml-containers-before-evaluating-transformations)
  - [3. Complete deterministic context and basic expression support](#3-complete-deterministic-context-and-basic-expression-support)
  - [4. Recover destination constraints](#4-recover-destination-constraints)
  - [5. Recognize explicit input rejection](#5-recognize-explicit-input-rejection)
  - [6. Correct diagnostics and worker summaries](#6-correct-diagnostics-and-worker-summaries)
- [Chart defects confirmed with follow-up renders](#chart-defects-confirmed-with-follow-up-renders)
  - [Apache: valid numeric-looking Secret name becomes a number](#apache-valid-numeric-looking-secret-name-becomes-a-number)
  - [Airflow: malformed helper dictionary silently loses annotations](#airflow-malformed-helper-dictionary-silently-loses-annotations)
- [Recommended fix order](#recommended-fix-order)
- [Fixes implemented after this scan](#fixes-implemented-after-this-scan)
- [Validation](#validation)
<!-- toc:end -->

The scan found actionable compiler gaps and a reporting defect that loses observed failures when shrinking reaches the time limit.
Follow-up Helm renders also reproduced two chart defects using ordinary, valid-looking configuration values.

## Run and coverage

Tested Airflow 25.1.0, Apache 11.4.30 and APISIX 6.0.2, in discovery order, from Bitnami revision
[`6a8cccf3c29a`](https://github.com/bitnami/charts/tree/6a8cccf3c29a1faabf0c34c8276a09ed14f3c5b3/bitnami).
Helm 4.3 rendered the charts with prepared dependencies. Each chart had a five-minute execution budget, six local path workers,
`--filter`, `--max-examples 10`, random traversal and seed `0`. Cached successes were disabled; `HH2006` was suppressed.
Dependency preparation happened before the scan and did not consume its testing budget.

| Chart | Visited / discovered paths | Completed paths | Render attempts | Recorded failed properties | Execution seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Airflow | 25 / 2,816 | 19 | 341 | 0* | 304.4 |
| Apache | 276 / 276 | 276 | 3,916 | 54 | 130.6 |
| APISIX | 17 / 1,212 | 11 | 261 | 2* | 303.4 |

These are path properties, not distinct bugs or exhaustive input coverage. Attempts include shrinking. Airflow and APISIX stopped at
their deadlines; the few extra seconds include worker shutdown. Apache completed its selected path properties, not every possible input.
The full scan took 778.49 seconds after dependency preparation.

*Airflow logged failures in five unfinished properties; APISIX logged failures in three. Their timeout records omitted these failures.
Consequently, the generated report's 56 recorded failure occurrences and 31 distinct diagnostics undercount what was observed.

The scan used structural manifest checks without full Kubernetes schema validation. The Apache reproduction below was additionally
checked against the cached Kubernetes 1.35.0 Deployment schema.

See the [scan report](bitnami-compiler-review.md) and [PDF](bitnami-compiler-review.pdf). Raw worker logs, prepared charts and reproduction
outputs remain locally under `.cache/bitnami-compiler-review-1789844100/`.

## Findings and priorities

These findings describe the original scan. Follow-up fixes are recorded below; the original measurements remain unchanged.

### 1. Preserve failures before shrinking finishes

Airflow's `redis.metrics.containerPorts`, `redis.sentinel.service.headless`, `redis.metrics.livenessProbe.periodSeconds`,
`redis.sysctl.image.pullPolicy` and `worker.extraEnvVarsSecrets` properties logged native Helm failures. None retained an error code,
message or counterexample in its final timeout record. APISIX showed the same loss for three properties beneath `etcd`.

The runner stores the last failure in memory, but `stopped_report()` writes only incomplete coverage and measurements.
It does not persist that failure as `save_failure()` does.
See [runner.py](../../pkg/hypothesis_helm/charts/testing/runner.py) and
[candidates.py](../../pkg/hypothesis_helm/charts/testing/candidates.py).

Persist a verified counterexample immediately, then replace it if shrinking finds a smaller one. On timeout, retain the unminimized
failure and separately mark coverage and minimization incomplete. This should be fixed before another large scan.

Ten examples per property does not cap shrinking at ten renders. Long shrinking sessions and expensive dependency renders occupied
workers while most Airflow and APISIX paths remained unvisited. A separate shrink budget would improve breadth within the chart deadline.

### 2. Normalize YAML containers before evaluating transformations

Redis PDB templates use `coalesce .Values.pdb .Values.master.pdb`. Both values are ordinary YAML mappings, represented by ruamel's
`CommentedMap`. The evaluator rejects them with `unknown emptiness semantics` because it checks exact Python types.

A direct probe reproduced this: both original mappings fail, while converting them to plain dictionaries produces the expected PDB map.
The current `native()` conversion normalizes string and integer subclasses but leaves these mapping subclasses unchanged.
See [contract_values.py](../../pkg/hypothesis_helm/compiler/asts/contract_values.py) and
[transformations.py](../../pkg/hypothesis_helm/compiler/asts/transformations.py).

Normalize supported YAML containers at the analysis boundary while preserving input provenance, or accept compatible container types
in the transfer functions. This is a concrete implementation defect, not a need for a larger inspection budget.

### 3. Complete deterministic context and basic expression support

The rejection evaluator supplies Values, Capabilities, Files and Release, but not Chart or Template. Common helpers access
`.Chart.Name` and `.Chart.Annotations.images`; checksum includes use `$.Template.BasePath`. These missing contexts block otherwise
deterministic reasoning, including image-policy rejection checks.

The scan also exposed zero-argument `dict`, `trunc`, `splitList`, integer conversion, formatting and serialization gaps. In particular,
the evaluator recognizes bare `list` but not bare `dict`. Some existing `printf` support does not cover the `%d` use in Airflow.
See [contracts.py](../../pkg/hypothesis_helm/compiler/asts/contracts.py).

Supply chart-scoped metadata and source-specific template context, then add bounded transfer functions with Helm comparison tests.
A builtin's presence in the effects registry does not establish that its value semantics are implemented.
Continue treating external lookups, randomness and genuinely dynamic code as unknown; these require different evidence.

### 4. Recover destination constraints

Apache received **zero** destination-derived rules and 14 projection diagnostics; APISIX received **zero** and 47 diagnostics.
Airflow received ten reviewed bindings but still had 51 projection diagnostics. Unsupported helper arguments and control flow cause
the projection pass to abandon whole template files.

The resulting examples included:

| Intended field | Generated example | Missing domain information |
| --- | --- | --- |
| Apache Secret / ConfigMap references | `"'"` | Kubernetes name constraints |
| Apache node ports | `"'"` | Port type and range, with chart-specific fallback values |
| Apache image-pull Secret entries | Nested arrays and maps | Element structure and name constraints |
| Apache annotations | `{"": []}` | String-valued annotation map |
| APISIX's etcd PDB | `maxUnavailable: "-"` | Nonnegative count or percentage, plus supported empty fallback |

See [domains.py](../../pkg/hypothesis_helm/compiler/passes/domains.py) and
[domain_helpers.py](../../pkg/hypothesis_helm/compiler/passes/domain_helpers.py).

Analyze independently justified output fragments with their guards and scope intact. Expand supported helper contexts and collection
element shapes. Do not infer a domain merely from a field's name, or drop an unknown fragment in a way that changes surrounding YAML.
Retain conflicts with authored schemas as findings.

Filtering was enabled throughout. For these open input spaces it used known-path generation; it did not obtain a finite exhaustive plan.
Larger compiler limits would not resolve these unsupported semantics.

### 5. Recognize explicit input rejection

Apache's `cloneHtdocsFromGit.enabled=true` triggers an explicit validation message requiring repository and branch values.
Changing an image repository triggers Bitnami's deliberate image allowlist rejection. These currently appear as `HH1001` failures.

The scan recorded zero predicted or filtered rejections for all three charts, despite these native rejection messages.
Missing chart metadata and helper semantics explain part of that gap. Recognize guarded requirements and generate their related values
together, while verifying rejection predictions with Helm and retaining contradictions with an authored schema.

Keep genuine dependency failures distinct: Apache's `tags.bitnami-common=false` removes a library whose helpers remain unconditionally
referenced, producing `HH3003`. That is different from a chart deliberately rejecting an unsupported configuration.

### 6. Correct diagnostics and worker summaries

The scan emitted 733 `HH2007` lines for 131 distinct messages; many repeated once per worker. Deduplicate by chart, source location and
reason at the coordinator. Audit messages also used the temporary directory name `chart` instead of the actual chart name.

Each chart's top-level rejection summary reported `incomplete_evaluations: 0`, although its worker summaries contained nonzero counts.
The aggregation in [paths.py](../../pkg/hypothesis_helm/charts/testing/paths.py) sums several counters but omits this one.
Some reported worker policy settings also reflect the coordinator rather than the worker that performed the analysis.

Airflow's audit includes `HH2001` and `HH2004` for unresolved wildcard paths such as `$[*][*]`. A dynamic access is not by itself proof
that a specific required field is undocumented or missing. Keep that uncertainty separate from findings about concrete named fields.

## Chart defects confirmed with follow-up renders

### Apache: valid numeric-looking Secret name becomes a number

Render Apache with `--set-string extraEnvVarsSecret=0`. Helm exits successfully, but the unquoted reference in
`templates/deployment.yaml` produces:

```yaml
envFrom:
  - secretRef:
      name: 0
```

The input is the string `"0"`, which satisfies the Secret-name character rules. The output is a number. Validation against the cached
Kubernetes 1.35.0 Deployment schema rejects `spec.template.spec.containers[0].envFrom[0].secretRef.name`:
`0 is not of type 'string', 'null'`.

This is an example tighter generation should preserve. Quoting the rendered name is the likely template correction.

### Airflow: malformed helper dictionary silently loses annotations

Render Airflow with:

```yaml
executor: KubernetesExecutor
worker:
  ephemeral:
    enabled: true
    annotations:
      example: value
```

`templates/config/configmap-pod-template.yaml:247` passes an odd number of arguments to `dict` when calling `common.tplvalues.merge`.
It supplies two annotation maps separately where the helper expects its `values` entry to be a list.

Helm exits successfully. In the generated ConfigMap's embedded `pod_template.yaml`, the ephemeral volume claim's annotations contain
an `Error` entry with a decoding error instead of `example: value`.

This is a semantic defect that outer YAML parsing does not catch. The embedded error is itself valid YAML and a string annotation,
so validating the embedded Pod's schema alone would not prove the intended annotation was preserved. Track malformed helper arguments
and parser-error results through data flow, then verify a reachable configuration with Helm. Do not treat every user-defined `Error`
key as a failure.

## Recommended fix order

1. Persist failures before shrinking and correct worker counter aggregation.
2. Fix YAML container normalization and empty-container expressions.
3. Supply deterministic Chart and Template context; extend bounded helper transfer functions.
4. Recover independently provable destination constraints and guarded requirements.
5. Classify malformed helper calls and parser-error propagation; deduplicate diagnostics.

The conservative fallback remains appropriate: unsupported analysis must keep candidates available for Helm. These changes would
improve useful coverage and the reliability of reports without claiming equivalence or rejection where neither has been established.

## Fixes implemented after this scan

- Failed candidates are atomically checkpointed before shrinking. A deadline preserves the failure while marking minimization and coverage
  incomplete. The coordinator can recover a checkpoint if a worker never writes its final queue record.
- Worker totals sum every property's counter delta, including incomplete evaluations and authored-schema conflicts. Duplicate compiler
  diagnostics are shown once per chart queue; multiline rejection logs include the chart's reason.
- `default` and `coalesce` accept YAML container subclasses. Empty `dict`, bounded string operations and typed integer formatting gained
  native Helm comparison tests.
- Fixed Chart metadata and Template context now respect dependency aliases and archived charts. Filename includes assembled from a known
  Template base path can resolve to parsed template bodies. Unmodeled metadata fields remain unknown.
- Dynamic wildcard references remain in audit evidence without being treated as proof that a concrete field is missing.
- Anchor tests exposed an additional generation bug: changing one path could change a sibling alias. Path replacement now detaches the
  selected occurrence; native Helm tests cover mapping aliases, sequence aliases and merge-key override precedence.

A follow-up scan used the same three prepared charts with a 30-second chart execution budget, six workers and two generated examples per
property. Apache retained four failing inputs at the deadline, with matching checkpoint and final-report values. Its 451 incomplete-analysis
evaluations matched the sum of its property records. All 154 emitted `HH2007` messages were distinct after coordinator deduplication.
This was a functional check under concurrent test-suite load, not a comparable performance measurement.

Whole-template destination projection still needs further work. Opaque helper outputs, mutation, serialization and joint validation rules
must retain conservative handling. The fixes above do not establish complete helper semantics or fix the upstream chart defects.

## Validation

The broad core-suite run passed 1,834 tests and skipped 23. Its 14 failures were subsequently resolved: seven required implementation or
expectation corrections, three required normal terminal-color settings, and four required permission to bind temporary localhost ports.
All affected cases passed in the 185-test focused rerun. Subsequent checks passed 128 execution/reporting tests and 172 compiler/domain
tests after the final changes. Ruff, mypy, docstring checks and generated-reference checks passed.

No scan is left running. The full original Bitnami report was not overwritten, and these changes do not modify the upstream charts.
