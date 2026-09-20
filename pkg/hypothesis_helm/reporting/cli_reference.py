"""
Render the argument parser consistently in the README and command reference.
"""

import argparse
import os

__all__ = ("help_markdown",)


def help_markdown(*, headings: bool = True) -> str:
    """
    Generate complete, collapsible help for every public core command.

    Args:
        headings (bool): Include command headings in the dedicated CLI reference.

    Returns:
        str: Deterministic Markdown at a fixed terminal width.
    """
    from hypothesis_helm.cli import argument_parser

    previous = os.environ.get("COLUMNS")
    os.environ["COLUMNS"] = "88"
    try:
        parser = argument_parser(prog="helm hypothesis")
        parsers = [("helm hypothesis", parser)]
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                parsers.extend((f"helm hypothesis {name}", child) for name, child in action.choices.items())
        sections = []
        for title, command in parsers:
            heading = f"## {title}\n\n" if headings else ""
            sections.append(f"{heading}<details>\n<summary>{title}</summary>\n\n~~~text\n{command.format_help()}~~~\n\n</details>\n")
        return "\n".join(sections)
    finally:
        if previous is None:
            os.environ.pop("COLUMNS", None)
        else:
            os.environ["COLUMNS"] = previous
