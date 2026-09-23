"""
Read CLI evidence from its published artifact location instead of relying on verbose terminal reports.
"""

from pathlib import Path

__all__ = ("result_text",)


def result_text(output: str) -> str:
    """
    Read a test or scan's saved results, or a command's explicitly structured output.

    Args:
        output (str): Captured command output containing the result location.

    Returns:
        str: Full JSON evidence without requiring the terminal to repeat it.
    """
    paths = [line.removeprefix("Results saved: ") for line in output.splitlines() if line.startswith("Results saved: ")]
    return Path(paths[-1]).read_text() if paths else output
