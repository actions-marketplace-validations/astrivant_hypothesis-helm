#!/usr/bin/env bash
# Run the same Python checks locally and in CircleCI.
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/project-python.sh -m ruff check src scripts examples/generated-workload
bash scripts/project-python.sh -m ruff format --check src scripts examples/generated-workload
bash scripts/project-python.sh -m mypy
bash scripts/project-python.sh -m pydocstyle --config=pyproject.toml src scripts
bash scripts/project-python.sh -m pydoclint.main --config=pyproject.toml src scripts
bash scripts/project-python.sh -m pytest "$@"
