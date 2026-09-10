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
