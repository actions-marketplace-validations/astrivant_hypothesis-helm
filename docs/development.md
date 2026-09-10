# Development and CLI reference

Generate Python property tests for the configuration paths in a Helm chart.
The generator loads `values.yaml` with `ruamel.yaml`, merges in undocumented
levers discovered in templates, enumerates paths from `values.schema.json`, and
emits a named Hypothesis test for each path. GPL-3.0-only.

## Install and generate tests

Requires Python 3.13+, Poetry, and Helm 3 (tested with 3.18.0-rc.2). Helm 4 has
not been verified. No cluster is required.

```sh
git clone https://github.com/astrivant/hypothesis-helm.git
cd hypothesis-helm
python3.13 -m venv .venv
env -u VIRTUAL_ENV -u PYENV_VERSION -u PYENV_VIRTUAL_ENV poetry install

VIRTUAL_ENV="$PWD/.venv" poetry run hypothesis-helm generate examples/workload \
  --output generated-tests/workload --max-examples 50
VIRTUAL_ENV="$PWD/.venv" poetry run pytest generated-tests/workload
```

Or install the Helm plugin and generate through Helm:

```sh
helm plugin install .
helm hypothesis generate examples/workload --output generated-tests/workload
# Run the emitted Python tests in the Poetry environment above.
VIRTUAL_ENV="$PWD/.venv" poetry run pytest generated-tests/workload
```

The plugin hook installs the package in an isolated `.plugin-venv`. Set
`PYTHON=/path/to/python3` when installing to select the interpreter. The Python
CLI is also available through `pipx install .` or `pip install .` in a virtual
environment. Running generated tests requires `pytest`, included in the Poetry
development dependencies. `poetry.lock` pins development dependencies; plugin
installation resolves runtime constraints from `pyproject.toml`.

## What is generated

A complete generated example is checked in at
[`examples/generated-workload/test_chart_values.py`](../examples/generated-workload/test_chart_values.py).

Each output directory contains:

| File | Purpose |
| --- | --- |
| `test_chart_values.py` | Editable pytest functions, one per enumerated path |
| `values.coalesced.yaml` | Round-trip YAML snapshot with discovered levers merged in |
| `values.inferred.schema.json` | Original schema extended with inferred undocumented paths |
| `paths.json` | Paths, schema fragments, strategy expressions, inference origins and diagnostics |

For example, `replicas` declared as an integer between zero and five produces:

```python
@settings(max_examples=50, deadline=None,
          suppress_health_check=[HealthCheck.too_slow])
@given(value=st.integers(min_value=0, max_value=5), data=st.data())
def test_replicas_6b8f1e2a90(chart, value, data):
    check_path(chart, ("replicas",), value, data)
```

Function names use a stable hash suffix to avoid path-name collisions. `chart` is a generated
module-scoped fixture. It prepares a temporary chart containing the coalesced YAML
and inferred schema, leaving the source chart untouched. Each test changes its
path in the baseline values and renders with Helm. If sibling/schema constraints
make that context invalid, it draws a schema-valid context constrained to the
selected path value. Hypothesis reports and shrinks counterexamples normally;
the failing path and values override are included as notes.

Generation overwrites these four files in the chosen output directory. Regenerate
after changing values, templates or schemas. Chart paths in the emitted module
are relative to its location; keep the generated directory and chart together
when moving the repository. The temporary chart includes dependencies already
present under `charts/`; run `helm dependency build <chart>` separately if needed.

## Coalescing and type inference

`ruamel.yaml` handles values parsing, round-trip serialization, and manifest
parsing. The coalescer merges missing keys into an independent round-trip copy of its
mapping, preserving comments, quotes, anchors and existing values. It does not
rewrite the input chart's `values.yaml` or schema.

A missing template-referenced key takes an unambiguous schema default or literal
`default`/`dig` fallback when available. Parent objects are created as needed.
Existing defaults always win. Inferred schemas derive types from existing YAML
values and recovered fallback values; they do not invent numeric bounds or turn
a single observed value into an enum. Unknown or conflicting defaults become null
placeholders with diagnostics; without schema/type evidence their strategy is
unconstrained JSON, not a claim that only null is valid. Review these entries.
Dynamic wildcard paths do not cause invented keys or list elements in the saved
YAML; their schema-driven tests construct concrete paths at runtime.

For undocumented levers, the **temporary testing contract is extended** with the
inferred properties, including when the original schema forbids additional keys.
This lets the tests exercise hidden template levers rather than reject every case
at the original schema boundary. Existing documented constraints are retained.
The inferred contract and generated tests are reviewable artifacts, not an
assertion that the original schema documented those values. The `audit` command
still reports gaps against the original chart.

## Path enumeration and Hypothesis strategies

The inventory includes object/array containers and their leaves, local references,
composition branches, positional arrays, and wildcard paths for array items and
schema-defined maps. Containers get tests too, so array lengths, empty maps and
optional fields are exercised alongside individual leaf values. A wildcard picks
a concrete entry during a test; recursive schemas are rejected during enumeration
rather than reported as fully covered.

| Schema evidence | Emitted strategy |
| --- | --- |
| Boolean | `st.booleans()` |
| Integer with inclusive/exclusive bounds | `st.integers(...)` |
| Number with inclusive bounds | `st.floats(..., allow_nan=False, allow_infinity=False)` |
| String with length constraints | `st.text(...)` |
| Enum / constant | `st.sampled_from(...)` / `st.just(...)` |
| Array with item and length constraints | `st.lists(item_strategy, ...)` |
| Regex, multiples, unique arrays, objects, unions and other compound constraints | `hypothesis_jsonschema.from_schema(...)` |

The complete schema is checked in addition to each path's strategy. Impossible
combinations or excessive rejection fail with Hypothesis diagnostics rather than
silently count as successful coverage. JSON null follows Helm's deletion semantics;
values supplied as overrides still undergo Helm's default coalescing.

The dependencies are [Hypothesis](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html),
[hypothesis-jsonschema](https://github.com/python-jsonschema/hypothesis-jsonschema),
and [ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/api/).

## Template discovery and the test contract

The `attrs` action/block AST resolves direct `.Values` and `$.Values` paths,
simple aliases, `with`/`range` scopes, and literal `index`, `get`, and `dig`
lookups. Quoted delimiters and comments are handled. The
[existing Tree-sitter grammar](https://github.com/ngalaiko/tree-sitter-go-template)
was evaluated; the checked Python parser bundle did not include it, so this
package supplies a focused analyzer.

Computed keys, named-template caller contexts, `tpl`, mutations and unresolved
aliases produce diagnostics. Dependency templates and template strings inside
values or `.Files` are not recursively audited. Generate tests separately for
subcharts. Static paths are not control-flow paths: generating a test for a lever
does not prove that all guards around it were activated, that it affects the
output, or that every template execution branch was reached.

Rendering must finish within 30 seconds per case and produce nonempty, parseable
YAML with resource `apiVersion`, `kind`, and `metadata.name` fields; resource
identity duplicates are rejected and Kubernetes `List` items checked recursively.
Edit generated assertions or call `check_path(..., timeout=..., allow_empty=True)`
to customize this contract. It does not validate Kubernetes admission or runtime
behavior. Schema-driven sampling, including per-path sampling, is not a formal
proof of totality.

## Local examples and Astrivant

```sh
# Four tests: image container, repository, tag, replicas.
helm hypothesis generate examples/workload --output generated-tests/workload
# Coalesces secretSwitch and other-switch from template fallbacks.
helm hypothesis generate examples/hidden-levers --output generated-tests/hidden
# Generates a test that discovers the unsupported replicas=0 case.
helm hypothesis generate examples/broken --output generated-tests/broken
# Real neighboring chart; does not modify that checkout.
helm hypothesis generate ../astrivant/helm/astrivant --output generated-tests/astrivant
VIRTUAL_ENV="$PWD/.venv" poetry run pytest generated-tests/astrivant
```

`examples/configmap` additionally exercises a constrained string and boolean.
Astrivant has incomplete schema entries, computed lookups, and caller-dependent
helpers: review its generated inventory and inferred contract before treating the
suite as a CI gate. Generated tests may expose real chart failures.

The earlier whole-chart runner remains available for interaction sampling and
finite-domain enumeration:

```sh
helm hypothesis audit ./chart --strict
helm hypothesis test examples/workload --exhaustive --max-cases 1000
helm hypothesis test ./chart --max-examples 100 --seed 42 --artifact-dir reports/chart
```

Whole-chart failures save `values.json` and `report.json` for replay with
`helm template hypothesis ./chart --values reports/chart/values.json`. Generated
Python tests instead use pytest/Hypothesis reporting and its example database.

Run the project's own suite with `VIRTUAL_ENV="$PWD/.venv" poetry run pytest`.
It tests generation, coalescing, strategy constraints and emitted tests against
real Helm. Neighboring Astrivant audit coverage skips when absent; the full
whole-chart Astrivant gate is opt-in with `ASTRIVANT_CHART=<path>`.

## Repository tooling

Python is pinned by `.python-version`; `poetry.toml` keeps the virtualenv in this
checkout. Use `scripts/project-python.sh` to avoid running checks in an unrelated
activated environment. Tests are colocated in `src/hypothesis_helm/tests`.

```sh
bash scripts/project-python.sh -m pre_commit install
bash scripts/check.sh
bash scripts/project-python.sh -m pytest examples/generated-workload
poetry build
```

The checks enforce strict mypy, Ruff lint/format, pydocstyle, and pydoclint using
the same Python configuration as Astrivant. `scripts/check.sh` and CircleCI use
the same commands. The Helm README generator is not applied to deliberately
incomplete test fixture schemas: those fixtures are test inputs.

When upgrading an older Python 3.10 checkout, recreate its `.venv` using Python
3.13 before `poetry install`, and reinstall the Helm plugin with a Python 3.13
interpreter. The package now requires Python 3.13 or newer.
