"""
Keep one process-local environment snapshot for configuration and child-process setup.
"""

import os

__all__ = ("env", "refresh_env", "set_env")

# Keep this object stable: callers import the dictionary itself, not a getter.
env: dict[str, str] = dict(os.environ)


def refresh_env() -> dict[str, str]:
    """
    Reload the process environment in place before starting a command or its workers.

    Direct changes made by another library become visible only after this call.
    Refresh at execution boundaries, rather than while workers consume configuration.

    Returns:
        dict[str, str]: The existing shared dictionary, with additions, updates and removals applied.
    """
    snapshot = dict(os.environ)
    # Update first so readers never encounter a temporarily empty dictionary.
    env.update(snapshot)
    for name in env.keys() - snapshot.keys():
        del env[name]
    return env


def set_env(name: str, value: str | None) -> str | None:
    """
    Publish a setting to both package readers and newly started child processes.

    Args:
        name (str): Process environment variable name.
        value (str | None): New value, or None to remove the variable.

    Returns:
        str | None: Previous cached value, suitable for restoring a temporary scope.
    """
    previous = env.get(name)
    if value is None:
        os.environ.pop(name, None)
        env.pop(name, None)
    else:
        os.environ[name] = value
        env[name] = value
    return previous
