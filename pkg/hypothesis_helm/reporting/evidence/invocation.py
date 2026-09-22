"""
Capture the interpreter's installed versions and replayable CLI invocation at scan start.
"""

import shlex
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from hypothesis_helm.environment import env

__all__ = ("record_invocation",)


def record_invocation(arguments: list[str] | None = None) -> dict[str, object]:
    """
    Record execution provenance without borrowing a caller's unrelated process arguments.

    Args:
        arguments (list[str] | None): Original CLI arguments before normalization; absent for library callers.

    Returns:
        dict[str, object]: Installed versions, working directory, and an optional shell-quoted command with its argument vector.
    """
    versions: dict[str, str | None] = {}
    for package in ("hypothesis", "hypothesis-helm"):
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = None
    # The plugin execs the Python entry point; retain the public Helm invocation when it supplied the environment.
    prefix = ["helm", "hypothesis"] if env.get("HELM_PLUGIN_DIR") else ["hypothesis-helm"]
    argv = [*prefix, *arguments] if arguments is not None else None
    return {
        "versions": versions,
        "working_directory": str(Path.cwd()),
        "argv": argv,
        "command": shlex.join(argv) if argv is not None else None,
    }
