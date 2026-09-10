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

## Distributed sharding

Both `test` and `run` default to `--shard auto`, detecting CI node coordinates.
Use `--shard none` to disable detection or `--shard INDEX/TOTAL` to choose a
one-based partition explicitly. See [CI integration](ci.md) for provider mappings
and the GitHub Action.
Each independently launched instance executes only its assigned properties,
with its own fixed or PID-controlled worker pool:

```sh
# Separate runners, using the same chart revision and command options:
helm hypothesis test ./chart --shard 1/3 --jobs auto --seed 42
helm hypothesis test ./chart --shard 2/3 --jobs auto --seed 42
helm hypothesis test ./chart --shard 3/3 --jobs auto --seed 42

# Inspect one partition without rendering:
helm hypothesis test ./chart --shard 1/3 --match image --collect-only

# Partition an existing suite, with reports in a separate location:
helm hypothesis run generated-tests --shard 1/3 --artifact-dir reports/distributed
```

The partition algorithm (`sha256-nodeid-v1`) hashes the UTF-8 pytest node ID
relative to the suite root, then takes the result modulo TOTAL. It is independent
of absolute checkout location, Python hash randomization, collection order, and
worker scheduling. It runs after keyword selection. Different totals repartition
the suite; identical totals and node IDs preserve ownership when unrelated tests
are added. Hash partitioning does not promise equal counts or equal execution
time, and a long property is not split across shards.

Run every index from 1 through TOTAL using the same chart/suite revision, plugin
version, `--match`, generation options, and seed. Each property then belongs to
exactly one instance, without a coordinator or shared queue. Repeating a shard
intentionally repeats its properties; no distributed deduplication service is
involved. A partition with no assigned properties succeeds with zero workers.
An empty overall selection, including a mistyped `--match`, still exits with
pytest's no-tests status (5). Sharding is unavailable in the explicit
`--whole-chart` and `--exhaustive` modes.

`test` writes its generated suite and reports beneath
`ARTIFACT_DIR/shards/INDEX-of-TOTAL/`. `run` reads the saved suite in place and
writes reports beneath `SUITE/shards/INDEX-of-TOTAL/`, or under the supplied
`--artifact-dir`. Each directory includes `shard.json` with the algorithm,
matched count, assigned count, and exact node IDs, plus the usual JUnit and run
reports and, when workers execute, concurrency history. Distinct shards do not
overwrite one another's artifacts. Do not run the same shard twice concurrently
against the same artifact directory.

Progress bars, stdout manifest streams, exit statuses, and Ctrl-C shutdown are
local to each instance. Keep each shard's JSON stream separate; independent
instances do not share the manifest-write lock. Collect the shard JUnit files in
CI and require every instance to succeed. Cancelling one instance does not stop
the others; the CI orchestrator controls cancellation across runners.

Auto concurrency uses each instance's available CPU count. Separate machines or
CPU-limited containers provide independent resource budgets. On a shared host,
set `--jobs N` per instance to avoid multiplying the automatic CPU budget.
Custom fixtures must also avoid mutating shared files or external resources.

## Persistent path results

`helm hypothesis test` and `helm hypothesis run` cache completed path outcomes under
`<artifact-dir>/cache/` (inside the shard directory when sharding). With a valid
cache, local runs retry failed, skipped, and incomplete paths; previously passing
paths are deselected. If every selected path already passed, the command succeeds
without rendering new manifests. First runs and changed inputs run the full selection.
`--collect-only` lists the full selection and leaves the result cache unchanged.

```bash
helm hypothesis test ./chart                         # local failed-path rerun
helm hypothesis test ./chart --rerun all             # force every selected path
helm hypothesis test ./chart --cache-dir .cache/helm # choose a persistent cache
helm hypothesis test ./chart --no-cache              # neither read nor write results
CI=true helm hypothesis test ./chart --rerun failed  # explicitly retry in CI
```

`--rerun auto` is the default. CI runs execute every selected path while recording
results. `$CI` is case-insensitive: empty, `0`, `false`, `no`, and `off` mean local;
other nonempty values mean CI. If `$CI` is absent, `GITHUB_ACTIONS`, `GITLAB_CI`, and
`CIRCLECI` provide fallback detection. An explicit `$CI` takes precedence.

Cache keys include the suite source, coalesced values, schema, original chart files
(including dependencies), framework source, Python version, seed, keyword selection,
and shard. Changes invalidate prior results. Shards have independent cache entries;
thread workers record separate outcome files, which the parent merges atomically.
Interrupted runs retain completed results; incomplete paths remain eligible for retry.
Malformed cache files are treated as cold caches. Cache entries record pytest node IDs
and outcomes, not rendered manifests or Hypothesis examples. Use `--rerun all` after
changing external tools or environment-dependent behavior, or to resample passing paths.

## Kubernetes API conformity

Enable strict [kubeconform](https://github.com/yannh/kubeconform) validation for each
rendered YAML stream. Install Git and kubeconform first (`brew install git kubeconform`
on macOS), then use the Helm command:

```bash
helm hypothesis test ./chart --kubeconform
helm hypothesis test ./chart --kubeconform --schema-version 1.35.0
helm hypothesis run ./generated-tests --kubeconform --schema-version 1.35.0
```

`--schema-version latest` is the default: it selects the highest stable `X.Y.Z`
version published in [Kubernetes JSON Schema](https://github.com/yannh/kubernetes-json-schema),
not Kubernetes development HEAD. Pin an exact version for reproducible CI runs.
`--kube-version` remains the separate Helm capabilities option; set both options to
the same version when testing a specific cluster target.

The tool fetches Git metadata with `--depth=1 --filter=blob:none` and sparsely checks
out only the selected `vX.Y.Z-standalone-strict` directory. The cache defaults to
`.cache/hypothesis-helm/schemas`; override it with `--schema-cache-dir PATH`. A file
lock serializes checkout updates, and immutable snapshots let threads and shards
validate against the same schema content even while another run updates the checkout.
Online runs refresh the catalog. To use only previously downloaded schemas:

```bash
helm hypothesis test ./chart --kubeconform --schema-version 1.35.0 \
  --schema-cache-dir .cache/hypothesis-helm/schemas --schema-offline
```

Offline mode fails clearly if the requested schemas are absent. Restore/save the
entire schema cache directory in CI, including its Git metadata. This cache is
separate from path-result caching; `--no-cache` disables cached test outcomes, while
schema caching remains active. `--collect-only` does not fetch schemas or run the validator.

Validation uses local schema files, strict mode, and one kubeconform worker per
property worker to avoid nested concurrency. Invalid resources, unsupported API
versions, and missing schemas fail the property and participate in Hypothesis shrinking.
Custom resources require schemas beyond the upstream Kubernetes catalog and currently
fail as missing schemas. This checks API structure, not admission policies or live
cluster behavior. Manifests still stream through `--output json` before validation,
including failing examples. Use `--kubeconform-binary PATH` for a specific executable.

Path-result cache keys include the schema content identity, resolved Kubernetes
version, and validator binary digest. Enabling validation or changing any of these
requires a fresh property run. Use `--rerun all` to validate fresh manifests again
when an unchanged local suite previously passed.


### Preparing schemas independently

`helm hypothesis schemas --schema-version latest --schema-cache-dir
.cache/hypothesis-helm/schemas` fetches the remote catalog, sparsely checks out the
selected strict schema version, and prints the resolved configuration as JSON.
Use it before a CI cache-save step when schema downloads must survive a later
failing test. It accepts `--schema-offline` and `--kubeconform-binary` as well.

### Timing estimates

The progress bar's ETA uses measured property completion rates and stays unknown
until enough observations exist. JUnit durations measure individual properties,
including generation, rendering, validation, and shrinking. Neither is a reliable
prediction based solely on schema types: input rejection, branch-dependent output,
shrinking, and changing parallelism affect elapsed time. The ETA excludes schema
preparation and collection, which happen before the progress bar starts.

## Cache-aware dry runs

Preview work without executing property examples, rendering charts, validating
manifests, or downloading schemas:

```bash
helm hypothesis test ./chart --dry-run
helm hypothesis test ./chart --dry-run --rerun all --kubeconform \
  --schema-version latest --schema-cache-dir .cache/hypothesis-helm/schemas
helm hypothesis run generated-tests --dry-run --match replicas
```

The command emits a JSON plan to stdout (`-o json` also works). It applies the
same keyword filter, shard, seed, cache fingerprint, and local/CI rerun policy as
execution. `selected_properties` counts properties after filtering and sharding;
`scheduled_properties` counts those that need to run; `reused_properties` counts
cached successes omitted by the rerun policy. Each property includes its prior
outcome, planned action, and literal `max_examples` setting when known.

`successful_example_budget` sums those settings for scheduled properties. It is
not an exact render count or an exhaustive count of the value domain: Hypothesis
may stop early or do additional work for rejection, replay, and shrinking. If a
hand-edited test has an unknown budget, the aggregate is `null`. All cached
successes produce zero scheduled properties and a zero budget locally; CI or
`--rerun all` still schedules the full selected suite. Cache files do not contain
reliable timing histories, so `estimated_seconds` remains `null` when work exists.

With `--kubeconform`, the dry run inspects locally available schemas using offline
preparation. Missing schemas or a missing validator are reported without downloading
anything, and cached successes are not reused when validation identity cannot be
established. An online execution can refresh schema content and invalidate the
estimated cache hit; `schema_cache.note` makes this uncertainty explicit. Use
`--schema-offline` to plan against the cached schema snapshot alone.

Chart tests are generated in temporary storage at their intended logical location,
so their fingerprint matches a real run. Existing generated files, reports, and
result caches are preserved. Pytest collection imports suite modules and conftest
files, so custom import-time side effects still apply. `--dry-run` is for per-path
suites and cannot be combined with `--collect-only`, `--whole-chart`, or `--exhaustive`.
