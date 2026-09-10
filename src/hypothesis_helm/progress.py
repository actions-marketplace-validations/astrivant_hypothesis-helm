"""
Display readable value paths during generation and pytest execution.
"""

import json
import logging
from typing import cast

import pytest

LOGGER = logging.getLogger(__name__)


def format_path(path: tuple[str | int, ...]) -> str:
    """
    Format a value path without losing literal dots, indices, or wildcard segments.

    Args:
        path (tuple[str | int, ...]): Schema path being processed.

    Returns:
        str: Dollar-rooted path with unusual keys escaped in bracket notation.
    """
    result = "$"
    for segment in path:
        if segment == "*":
            result += "[*]"
        elif isinstance(segment, int):
            result += f"[{segment}]"
        elif segment.isidentifier():
            result += f".{segment}"
        else:
            result += f"[{json.dumps(segment, ensure_ascii=True)}]"
    return result


def pytest_configure(config: pytest.Config) -> None:
    """
    Register the generated test marker used to identify each values path.

    Args:
        config (pytest.Config): Configuration for the bundled pytest invocation.

    Returns:
        None: Pytest recognizes generated path metadata without marker warnings.
    """
    config.addinivalue_line(
        "markers", "hypothesis_helm_path(path): schema path exercised by a test"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    """
    Log the selected path once before its property examples and fixture setup.

    Args:
        item (pytest.Item): Selected property about to execute.

    Returns:
        None: The path is emitted through pytest's live logging output.
    """
    marker = item.get_closest_marker("hypothesis_helm_path")
    if marker is not None:
        path = cast(tuple[str | int, ...], marker.args[0])
        LOGGER.info("Testing path %s", format_path(path))
    else:
        # Older or hand-edited suites may not carry generated path metadata.
        LOGGER.info("Testing %s", item.name)
