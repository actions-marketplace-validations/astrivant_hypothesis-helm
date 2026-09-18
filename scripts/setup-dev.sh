#!/usr/bin/env bash
# Install local build tools and Python dependencies on macOS or Debian/Ubuntu Linux.
set -euo pipefail

##
# Show the supported setup modes.
# -> ret::void
usage() {
    local script_name="${0##*/}"

    echo "Usage: $script_name [--check] [--schemas]"
    echo 'Default: install tools, create .venv, and install development dependencies.'
    echo '--check: report missing tools without installing anything.'
    echo '--schemas: also rebuild the pinned Kubernetes input-domain catalog and schema cache.'
}

##
# Require a command and report how to bootstrap missing dependencies.
# arg1::string -> ret::status
require_command() {
    local command_name="$1"

    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "Missing development dependency: $command_name" >&2
        return 1
    fi
}

##
# Install OS packages used by source checkout and parallel integration tests.
# arg1::string -> ret::void
install_system_packages() {
    local platform="$1"
    local privilege=""

    if [[ "$platform" == darwin ]]; then
        require_command brew
        brew install git git-lfs parallel
    elif command -v apt-get >/dev/null 2>&1; then
        if [[ "$EUID" != 0 ]]; then
            require_command sudo
            privilege=sudo
        fi
        $privilege apt-get update
        $privilege apt-get install -y ca-certificates curl git git-lfs parallel build-essential
    else
        echo 'Install curl, git, git-lfs and GNU Parallel with your Linux package manager, then rerun.' >&2
        require_command curl
        require_command git
        require_command git-lfs
        require_command parallel
    fi
}

##
# Check a downloaded archive against its published SHA-256 digest.
# arg1::path arg2::string -> ret::void
verify_archive() {
    local archive="$1"
    local expected="$2"
    local observed

    if command -v sha256sum >/dev/null 2>&1; then
        observed="$(sha256sum "$archive")"
    else
        observed="$(shasum -a 256 "$archive")"
    fi
    observed="${observed%% *}"
    if [[ "$observed" != "$expected" ]]; then
        echo "Checksum mismatch: $archive" >&2
        exit 1
    fi
}

##
# Install pinned Go and Helm binaries under the project's ignored development cache.
# arg1::string arg2::string arg3::path -> ret::void
install_build_tools() {
    local platform="$1"
    local architecture="$2"
    local tool_root="$3"
    local go_version=1.25.0
    local helm_version=v4.3.0
    local archive expected

    mkdir -p "$tool_root/downloads" "$tool_root/bin"
    if [[ ! -x "$tool_root/go/bin/go" ]]; then
        archive="$tool_root/downloads/go${go_version}.${platform}-${architecture}.tar.gz"
        curl -fsSL 'https://go.dev/dl/?mode=json&include=all' -o "$tool_root/downloads/go-releases.json"
        expected="$(
            .venv/bin/python - "$tool_root/downloads/go-releases.json" "${archive##*/}" <<'PY'
import json
import sys
from pathlib import Path
releases = json.loads(Path(sys.argv[1]).read_text())
print(next(file['sha256'] for release in releases for file in release['files'] if file['filename'] == sys.argv[2]))
PY
        )"
        curl -fsSL "https://go.dev/dl/${archive##*/}" -o "$archive"
        verify_archive "$archive" "$expected"
        tar -xzf "$archive" -C "$tool_root"
    fi
    if [[ ! -x "$tool_root/bin/helm" ]]; then
        archive="$tool_root/downloads/helm-${helm_version}-${platform}-${architecture}.tar.gz"
        curl -fsSL "https://get.helm.sh/${archive##*/}.sha256sum" -o "$archive.sha256sum"
        read -r expected _ <"$archive.sha256sum"
        curl -fsSL "https://get.helm.sh/${archive##*/}" -o "$archive"
        verify_archive "$archive" "$expected"
        tar -xzf "$archive" -C "$tool_root/downloads" "${platform}-${architecture}/helm"
        install "$tool_root/downloads/${platform}-${architecture}/helm" "$tool_root/bin/helm"
    fi
}

##
# Bootstrap Python and Poetry locally, then install all project development extras.
# arg1::path -> ret::void
install_python_tools() {
    local tool_root="$1"
    local uv_version=0.8.17

    mkdir -p "$tool_root/bin"
    if [[ ! -x "$tool_root/bin/uv" ]]; then
        curl -fsSL "https://astral.sh/uv/${uv_version}/install.sh" -o "$tool_root/uv-install.sh"
        UV_INSTALL_DIR="$tool_root/bin" UV_NO_MODIFY_PATH=1 sh "$tool_root/uv-install.sh"
    fi
    export UV_PYTHON_INSTALL_DIR="$tool_root/python"
    export UV_TOOL_DIR="$tool_root/python-tools"
    export UV_TOOL_BIN_DIR="$tool_root/bin"
    "$tool_root/bin/uv" python install 3.13
    "$tool_root/bin/uv" tool install --python 3.13 poetry==2.1.3
    if [[ ! -x .venv/bin/python ]]; then
        "$tool_root/bin/uv" venv --python 3.13 .venv
    fi
    unset VIRTUAL_ENV PYENV_VERSION PYENV_VIRTUAL_ENV
    POETRY_VIRTUALENVS_IN_PROJECT=true "$tool_root/bin/poetry" install --extras benchmarking --with dev
}

##
# Configure the checkout and optionally rebuild its ignored schema cache.
# arg1::string[] -> ret::void
main() {
    local check_only=false
    local build_schemas=false
    local platform architecture project_root tool_root argument

    for argument in "$@"; do
        case "$argument" in
            --check) check_only=true ;;
            --schemas) build_schemas=true ;;
            --help | -h)
                usage
                return
                ;;
            *)
                usage >&2
                exit 2
                ;;
        esac
    done
    project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    cd "$project_root"
    tool_root="$project_root/.cache/dev-tools"
    export PATH="$project_root/.venv/bin:$tool_root/bin:$tool_root/go/bin:$PATH"
    if [[ "$check_only" == true ]]; then
        for argument in git git-lfs parallel go helm poetry pre-commit shfmt python; do
            require_command "$argument"
        done
        python -c 'import sys; assert sys.version_info >= (3, 13), "Python 3.13+ is required"'
        go version
        helm version --short
        return
    fi
    platform="$(uname -s | tr '[:upper:]' '[:lower:]')"
    case "$platform" in darwin | linux) ;; *)
        echo 'Supported platforms: macOS and Linux' >&2
        exit 2
        ;;
    esac
    case "$(uname -m)" in arm64 | aarch64) architecture=arm64 ;; x86_64) architecture=amd64 ;; *)
        echo 'Unsupported CPU architecture' >&2
        exit 2
        ;;
    esac
    install_system_packages "$platform"
    install_python_tools "$tool_root"
    install_build_tools "$platform" "$architecture" "$tool_root"
    pre-commit install
    if ! helm hypothesis --help >/dev/null 2>&1; then
        PYTHON="$project_root/.venv/bin/python" helm plugin install .
    fi
    if [[ "$build_schemas" == true ]]; then
        hypothesis-helm-catalog --cache-dir schemas
    fi
    printf 'Development environment ready. In your current shell, run:\n  export PATH="%s/.venv/bin:%s/bin:%s/go/bin:$PATH"\n' \
        "$project_root" "$tool_root" "$tool_root"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
