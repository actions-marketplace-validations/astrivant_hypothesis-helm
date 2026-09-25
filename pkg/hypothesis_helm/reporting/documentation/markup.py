"""
Protect literal report paths and values from Markdown interpretation.
"""

import re

__all__ = ("code_block", "inline_code")


def inline_code(value: str) -> str:
    """
    Enclose literal text with a backtick delimiter longer than any backticks it contains.

    Args:
        value (str): Literal path, input value, or command.

    Returns:
        str: Markdown code span preserving embedded punctuation and delimiters.
    """
    fence = "`" * (max((len(match[0]) for match in re.finditer(r"`+", value)), default=0) + 1)
    # Markdown removes one padding space at both ends. Padding keeps literal
    # boundary backticks separate from the delimiter and retains paired spaces.
    padding = (
        " " if value.startswith("`") or value.endswith("`") or (value.startswith(" ") and value.endswith(" ") and value.strip()) else ""
    )
    return f"{fence}{padding}{value}{padding}{fence}"


def code_block(value: str) -> list[str]:
    """
    Fence multiline literals without letting their contents close the block early.

    Args:
        value (str): Literal text whose indentation and line breaks must remain intact.

    Returns:
        list[str]: Opening fence, unchanged source lines, and matching closing fence.
    """
    fence = "`" * max(3, 1 + max((len(match[0]) for match in re.finditer(r"`+", value)), default=0))
    return [fence + "text", *value.split("\n"), fence]
