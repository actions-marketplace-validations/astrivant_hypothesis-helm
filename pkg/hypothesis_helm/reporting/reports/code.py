"""
Style literal report inputs without interpreting their contents as markup.
"""

import textwrap
from collections.abc import Callable
from html import escape

from reportlab.pdfbase.pdfmetrics import stringWidth  # type: ignore[import-untyped]
from reportlab.pdfgen.canvas import Canvas  # type: ignore[import-untyped]

__all__ = ("CODE_BACKGROUND", "code_markup", "draw_code_block")

CODE_BACKGROUND = "#f1f3f5"


def code_markup(value: str) -> str:
    """
    Highlight inline code while escaping literal HTML and preserving spaces.

    Args:
        value (str): Literal path, command, or input value without Markdown delimiters.

    Returns:
        str: Safe ReportLab paragraph markup with a gray monospace background.
    """
    literal = escape(value).replace(" ", "&#160;")
    return f'<font name="Courier" backColor="{CODE_BACKGROUND}">{literal}</font>'


def draw_code_block(  # type: ignore[no-any-unimported]
    canvas: Canvas, content: str, top: float, new_page: Callable[[], float], *, left: float = 36, width: float = 540
) -> float:
    """
    Draw a shaded code block, preserving indentation and splitting long blocks across pages.

    Args:
        canvas (Canvas): Report canvas to draw on.
        content (str): Literal fenced text, including blank lines.
        top (float): Upper edge available on the current page.
        new_page (Callable[[], float]): Start a page and return its available upper edge.
        left (float): Left edge of the code box in PDF points.
        width (float): Width of the code box in PDF points.

    Returns:
        float: Baseline available for the next report paragraph.
    """
    padding, size, leading, bottom = 8, 8, 11, 42
    columns = max(1, int((width - 2 * padding) / stringWidth("M", "Courier", size)))
    wrapper = textwrap.TextWrapper(width=columns, replace_whitespace=False, drop_whitespace=False, break_on_hyphens=False)
    # Wrap each source line separately: YAML nesting and intentional empty lines
    # must not be collapsed by the prose renderer. Tabs get fixed-width stops.
    # Escape unsupported glyphs before wrapping so an expanded escape cannot
    # extend past the right edge of the background box.
    content = content.encode("latin-1", "backslashreplace").decode("latin-1")
    lines = [part for line in content.split("\n") for part in wrapper.wrap(line.expandtabs(4)) or [""]]
    total_height = len(lines) * leading + 2 * padding
    if total_height <= 180 and top - total_height < bottom:
        top = new_page()
    offset = 0
    while offset < len(lines):
        count = int((top - bottom - 2 * padding) // leading)
        if count < 1:
            top = new_page()
            continue
        chunk = lines[offset : offset + count]
        height = len(chunk) * leading + 2 * padding
        canvas.saveState()
        canvas.setFillColor(CODE_BACKGROUND)
        canvas.roundRect(left, top - height, width, height, 3, stroke=0, fill=1)
        canvas.setFillColor("#23313d")
        canvas.setFont("Courier", size)
        for index, line in enumerate(chunk):
            canvas.drawString(left + padding, top - padding - size - index * leading, line)
        canvas.restoreState()
        offset += len(chunk)
        top -= height + 8
        if offset < len(lines):
            top = new_page()
    return top - 8
