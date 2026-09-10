# Helm command reference

Install with Helm 3 and Python 3.13+ available:

```sh
PYTHON=python3.13 helm plugin install https://github.com/astrivant/hypothesis-helm
```

For a checkout, use `helm plugin install .`. The install hook bundles the package,
Hypothesis, ruamel.yaml, and pytest into the plugin's private virtualenv. End users
need neither Poetry nor a separately installed test runner. Helm 4 is unverified.

## Test a chart

```sh
helm hypothesis test ./chart
helm hypothesis test ./chart --max-examples 50 --seed 42
helm hypothesis test ./chart --match replicas
helm hypothesis test ./chart --collect-only
```

Inside a chart directory, `helm hypothesis test` uses the current directory.

`test` loads the chart, coalesces its undocumented template levers, generates one
Python property per value path, and runs the resulting suite. `--max-examples`
is a budget **per property**, not a total across the chart. `--match` selects
Python test names with a pytest keyword expression; path segments are included in
those names. `--collect-only` generates and lists the tests without rendering.
An empty selection returns a nonzero status rather than reporting success.

Progress is logged for each path as it is coalesced, assigned a generated test,
and tested. Generation messages go to stderr so `generate` keeps its JSON output
on stdout. Test progress appears live, once per selected property rather than once
per Hypothesis example:

```text
[INFO] Coalescing path $.image.tag
[INFO] Generating test for path $.image.tag (schema)
[INFO] Testing path $.image.tag
```

`audit` similarly logs each audited path. Wildcard items appear as `[*]`; unusual
keys use quoted bracket notation.
`--match` limits test execution logs to selected properties. `--collect-only`
logs generation and lists tests without claiming to execute them.

The plugin invokes pytest with its own Python interpreter, pins the invocation's
Hypothesis seed, and streams failures and progress to the Helm console. Ambient
pytest configuration, `PYTEST_ADDOPTS`, and auto-loaded third-party pytest plugins
are excluded. Saved-suite Python and suite-local `conftest.py` remain executable
and editable.

Use a dedicated artifact directory for each chart/run:

```sh
helm hypothesis test ./chart --artifact-dir reports/my-chart \
  --release example --namespace testing --kube-version 1.31.0 --timeout 30
```

`--helm` selects the renderer executable. `--timeout` bounds each Helm invocation,
not the complete suite; use your CI job timeout for an overall budget. Pass
`--allow-empty` when the chart legitimately renders no resources. Dependencies
must already be present; `helm dependency build ./chart` prepares them.
No release is installed and no cluster is required.

## Inspect and rerun generated suites

```sh
helm hypothesis generate ./chart --output generated-tests
helm hypothesis run generated-tests
helm hypothesis run generated-tests --seed 42 --match replicas
helm hypothesis run generated-tests --collect-only
```

`generate` only exports the suite for review or customization. `run` executes its
saved Python without regenerating it, preserving edits. It accepts seed, selection
and collection options. Rendering settings and per-property example budgets are
embedded in the generated source; configure them through `test` when creating a
suite or edit the saved Python. Both commands use the plugin's bundled dependencies.

| Artifact | Meaning |
| --- | --- |
| `test_chart_values.py` | Editable, named Hypothesis properties and embedded render settings |
| `values.coalesced.yaml` | Round-trip YAML snapshot with discovered levers merged in |
| `values.inferred.schema.json` | Original schema extended with inferred undocumented properties |
| `paths.json` | Schema fragments, strategies, provenance and unresolved constructs |
| `junit.xml` | Test outcomes and failure details, including Hypothesis counterexamples |
| `report.json` | Run status, pytest exit code, seed, selection and result location |
| `hypothesis-helm.pytest.ini` | Dedicated pytest configuration for the plugin invocation |

`test` writes these beneath `--artifact-dir` (default `reports/hypothesis-helm`).
`run` writes results beside the saved suite. Reusing a directory overwrites its
artifacts; regenerate after chart changes. Generated chart paths are relative to
the suite directory. Keep that relationship when moving the repository.

Passing tests return 0 and failing properties return 1. Pytest collection, usage,
internal-error and empty-selection exit codes propagate through Helm. Invalid
chart paths, schemas and command setup return 2. Counterexamples appear in the
console and JUnit failure details; no Python command is needed to rerun the suite.

## Coalescing, paths, and strategies

The coalescer loads `values.yaml` with `ruamel.yaml`, preserving comments, quotes,
anchors, merge keys, and existing values in an independent round-trip copy.
Source chart files are not rewritten. A missing template-referenced key takes an
unambiguous schema default or literal `default`/`dig` fallback when available.
Parent objects are created as needed. Unknown or conflicting defaults become null
placeholders with diagnostics; they are not assumed to accept only null.

Undocumented types are inferred from existing YAML and recovered literal fallback
values. No arbitrary numeric bounds or enums are invented. The temporary testing
schema is extended for those discovered properties, including when the original
schema forbids additional keys. Existing documented constraints are retained.
Review `paths.json` and the inferred schema before adopting them as a contract.

The inventory includes containers, leaves, local schema references, composition
branches, array items, and schema-defined map entries. Containers receive tests
for lengths, empty collections and optional fields. Wildcards select concrete
entries at runtime; missing required siblings are drawn from their schema.
Each test first uses baseline values, then draws a dependent context if necessary.
The complete schema is validated in addition to each path's strategy.

| Schema evidence | Strategy |
| --- | --- |
| Boolean | `st.booleans()` |
| Bounded integer | `st.integers(...)` |
| Number | Finite `st.floats(...)` |
| String length bounds | `st.text(...)` |
| Enum / constant | `st.sampled_from(...)` / `st.just(...)` |
| Array items and lengths | `st.lists(...)` |
| Objects, regex, multiples, unique arrays and compound constraints | `hypothesis_jsonschema.from_schema(...)` |

The runtime dependencies are [Hypothesis](https://hypothesis.readthedocs.io/en/latest/),
[hypothesis-jsonschema](https://github.com/python-jsonschema/hypothesis-jsonschema),
[ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/api/), and pytest.
A [generated example](../examples/generated-workload/test_chart_values.py) is
checked in for review. Edit assertions or rendering options in saved Python,
then use `helm hypothesis run` to execute it.

## Audit and rendering limits

```sh
helm hypothesis audit ./chart
helm hypothesis audit ./chart --strict
```

The template AST resolves direct values, root access, simple aliases, lexical
scopes, and literal lookups. Computed keys, named-template caller contexts,
`tpl`, mutations and unresolved aliases produce diagnostics. Dependency templates
and `.Files` content are not recursively audited; inspect subcharts separately.
Recursive schema paths are rejected instead of reported as covered.

Rendered YAML must contain resource envelopes with nonempty `apiVersion`, `kind`
and `metadata.name`; duplicate identities are rejected and `List` items checked
recursively. This is not Kubernetes admission or application behavior validation.
JSON null follows Helm's deletion semantics. Path coverage does not prove that
all template guards were activated or every execution branch was reached.

## Whole-chart modes

```sh
helm hypothesis test ./chart --whole-chart --max-examples 100 --seed 42
helm hypothesis test examples/workload --exhaustive --max-cases 1000
```

These explicit modes retain the earlier whole-chart runner against the original
schema. Sampling tests complete override objects; exhaustive mode enumerates
supported finite domains and refuses oversized or unsupported domains. They do
not generate a per-path suite and do not accept `--match` or `--collect-only`.
Failures save `values.json` and `report.json` for replay:

```sh
helm template hypothesis ./chart --values reports/hypothesis-helm/values.json
```

Sampling is evidence from tested inputs, not a proof of totality. Exhaustive
coverage is limited to the declared finite input domain and rendering environment.

## Examples and Astrivant

```sh
helm hypothesis test examples/workload
helm hypothesis test examples/configmap
helm hypothesis test examples/broken
helm hypothesis test examples/hidden-levers
helm hypothesis test ../astrivant/helm/astrivant --collect-only \
  --artifact-dir reports/astrivant
helm hypothesis run reports/astrivant --match networkPolicy
```

The broken chart intentionally fails on `replicas: 0`. The hidden-lever chart
exercises recovered template fallbacks. Astrivant has incomplete schema entries
and dynamic references; its generated tests may expose real chart failures.

## Stream rendered manifests

Use `helm hypothesis test ./chart --output json` (or `-o json`) to emit
newline-delimited JSON: one compact Kubernetes resource per line, flushed as
each Helm render completes. The same flag works with `helm hypothesis run
reports/hypothesis-helm`, `--whole-chart`, and `--exhaustive`. Progress,
pytest output, reports, and errors go to stderr; stdout contains only manifests.
Collection-only runs emit no manifests.

Every rendered example is included, including repeated examples during shrinking.
Documents are emitted before resource-envelope checks, so a JSON-serializable
resource that fails those checks still reaches the validator. Failed Helm
invocations and unparseable YAML cannot produce JSON manifests. Empty renders
emit no lines. This is a JSON Lines stream, not one JSON array.

To validate each manifest with both tools as it arrives, use this Bash pipeline.
Each validator receives the original resource separately, and either failure
makes the pipeline fail:

```bash
set -o pipefail
helm hypothesis test ./chart -o json |
  (
    status=0
    while IFS= read -r manifest; do
      printf '%s\n' "$manifest" | kubeconform -strict || status=1
      printf '%s\n' "$manifest" | kubesec scan /dev/stdin || status=1
    done
    exit "$status"
  )
```

The per-line loop avoids requiring validators to understand JSON Lines.
[Kubeconform](https://github.com/yannh/kubeconform) validates Kubernetes resource
schemas; [Kubesec](https://github.com/controlplaneio/kubesec) analyzes security
configuration. Their exit statuses determine pipeline success; external validator
findings are not fed back into Hypothesis for shrinking or recorded as pytest
assertions. Configure any score threshold separately from Kubesec's scan exit
status. In `generate`, `--output` continues to specify the suite directory.

## Adaptive parallel test execution

`helm hypothesis test` and `helm hypothesis run` default to `--jobs auto`.
Auto mode starts with the available logical CPU count and uses PID feedback
to adjust active worker concurrency as individual tests finish. Its ceiling is
four times the available CPU count, capped by the number of selected tests.
Use `--jobs N` / `-j N` for fixed concurrency, or `--jobs 1` for serial execution:

```sh
helm hypothesis test ./chart
helm hypothesis test ./chart --jobs auto -o json
helm hypothesis run reports/hypothesis-helm --jobs 4
helm hypothesis run reports/hypothesis-helm -j 1
```

The controller measures completed tests per second, including interpreter startup,
rendering, shrinking, and manifest-output backpressure. Each completion updates
the measurement window. To reduce timing noise, control adjustments wait for at
least one target-sized group of completions (minimum two) and 100 milliseconds.
Startup, concurrency drain, and the final partially occupied queue do not count
as evidence that higher concurrency reduces throughput.

Since the maximum throughput is unknown, the controller probes nearby concurrency
levels and estimates the marginal throughput change per worker. A PID controller
uses that gradient to approach zero marginal gain, with a filtered derivative,
integral anti-windup, and a one-worker adjustment limit per measurement window.
Periodic probes allow further exploration; flat throughput favors fewer workers.
This seeks a local throughput maximum within the bounds, rather than guaranteeing
an optimum for heterogeneous tests or changing host load. Short suites may finish
before enough measurements exist to adjust concurrency.

A thread pool dispatches one selected property at a time into an isolated pytest
interpreter. Lowering concurrency lets active tests finish before replacing them;
it never cancels a property's Hypothesis generation or shrinking.
[Pytest is not generally thread-safe](https://docs.pytest.org/en/stable/explanation/flaky.html#thread-safety),
so pytest state stays isolated. With concurrent execution, module and session
fixtures run separately for each property. Interpreter and fixture startup costs
can dominate very small tests; `--jobs 1` uses a single pytest invocation.

Workers preserve live path logs and JSON manifest streaming. Manifest order
depends on scheduling; writes are synchronized so even large JSON lines remain
intact. Results are merged into `junit.xml`. `report.json` records the jobs mode,
peak scheduled worker count, and aggregate exit status. `concurrency.json`
records each completed test, elapsed time, exit code, active count, target count,
and latest measured throughput. Target changes also appear in progress logs.
Any failed worker fails the command.

Collection-only runs stay serial. The explicit `--whole-chart` and
`--exhaustive` modes remain serial; `auto` does not change their execution and
they reject numeric `--jobs` values above one.
The pre-commit hook inherits `--jobs auto` without configuration changes.

## Progress and interruption

A Rich progress bar shows completed/selected tests, the worker target, and elapsed
time on stderr. It updates after each property finishes; redirected output keeps
a final summary without terminal animations. Serial runs show the same progress
through the bundled pytest plugin. Collection-only runs do not show a test bar.

Press Ctrl-C to stop submitting tests and interrupt active pytest process groups,
including their Helm children. Workers receive two seconds to finish cleanup,
followed by SIGTERM and a further one-second grace period before SIGKILL. The
command exits with status 130. Generated-suite runs retain the partial JUnit and
run reports; unfinished parallel tests are marked skipped, and concurrency
history records the interruption. The bar keeps its partial completion count.
JSON stdout remains reserved for manifests emitted before shutdown.
