# Development

This document is for contributors modifying the framework. End-user chart testing
is entirely through [Helm commands](usage.md).

## Environment

The project follows Astrivant's Python 3.13, Poetry and package-local test layout.
`.python-version` selects the interpreter and `poetry.toml` keeps the virtualenv
inside the checkout. Preserve an older environment elsewhere before recreating it
when upgrading from Python 3.10.

```sh
python3.13 -m venv .venv
env -u VIRTUAL_ENV -u PYENV_VERSION -u PYENV_VIRTUAL_ENV poetry install
bash scripts/project-python.sh -m pre_commit install
```

`scripts/project-python.sh` uses this checkout's interpreter even when another
virtual environment is active. Pytest is a runtime dependency because Helm runs
generated suites inside the plugin environment; linting tools remain development
dependencies. The Poetry lock pins contributor/CI dependencies. Plugin installation
resolves the package's runtime constraints.

## Checks

```sh
bash scripts/check.sh
poetry build
```

The validation command runs Ruff lint/format, strict mypy, pydocstyle, pydoclint,
and the package's pytest suite. Source and test docstrings follow Astrivant's
Google-style convention. No type-checking exclusions weaken the source checks.

Unit and integration tests live under `src/hypothesis_helm/tests`. Helm must be
available for render tests; the neighboring Astrivant audit skips when absent.
`ASTRIVANT_CHART=<path>` opts into the full whole-chart Astrivant integration gate.
Fixture schemas deliberately containing documentation gaps are not processed by
a Helm README/schema generator.

## Plugin verification

```sh
PYTHON=python3.13 helm plugin install .
helm hypothesis test examples/workload --max-examples 5
helm hypothesis generate examples/workload --output /tmp/generated-workload
helm hypothesis run /tmp/generated-workload
```

CircleCI checks the framework and the end-user plugin workflow, then builds the
wheel and source distribution. Generated-suite execution uses the plugin's
interpreter, with unrelated pytest configuration and auto-loaded plugins disabled.
The saved suite's own code and conftest remain editable.

Publishing and remote repository-setting changes are not automated by local checks.
