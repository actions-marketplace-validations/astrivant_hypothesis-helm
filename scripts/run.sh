#!/bin/sh
set -eu
: "${HELM_PLUGIN_DIR:?Helm must set HELM_PLUGIN_DIR}"
exec "$HELM_PLUGIN_DIR/.plugin-venv/bin/hypothesis-helm" "$@"
