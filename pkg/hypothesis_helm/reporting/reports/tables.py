"""
Render generated Markdown tables as paginated PDF tables with live cell links.
"""

import re
from collections.abc import Callable
from pathlib import Path

from attrs import frozen
from reportlab.lib.styles import ParagraphStyle  # type: ignore[import-untyped]
from reportlab.pdfbase.pdfmetrics import stringWidth  # type: ignore[import-untyped]
from reportlab.pdfgen.canvas import Canvas  # type: ignore[import-untyped]
from reportlab.platypus import LongTable, Paragraph, TableStyle  # type: ignore[import-untyped]

from hypothesis_helm.reporting.reports.links import CODE, LINK, linked_prose

__all__ = ("ReportTable", "draw_table", "read_table")


@frozen
class ReportTable:
    """
    Keep a table's Markdown cells and alignment separate from its PDF layout.

    Attributes:
        rows (tuple[tuple[str, ...], ...]): Header followed by data rows.
        alignments (tuple[int, ...]): ReportLab left, center, or right paragraph alignment per column.
        end (int): First source line after this table.
    """

    rows: tuple[tuple[str, ...], ...]
    alignments: tuple[int, ...]
    end: int


def _cells(line: str) -> tuple[str, ...]:
    """
    Split generated pipe-delimited rows without splitting literal pipes inside code.

    Args:
        line (str): One Markdown row, including its outer pipes.

    Returns:
        tuple[str, ...]: Trimmed cells retaining their inline markup.
    """
    line = line.strip()
    spans = [match.span() for match in CODE.finditer(line)]
    boundaries = [
        match.start() for match in re.finditer(r"(?<!\\)\|", line) if not any(start <= match.start() < end for start, end in spans)
    ]
    return tuple(line[start + 1 : end].strip().replace(r"\|", "|") for start, end in zip(boundaries, boundaries[1:], strict=False))


def read_table(lines: list[str], start: int) -> ReportTable | None:
    """
    Recognize a generated Markdown table while leaving chart-image panels to their renderer.

    Args:
        lines (list[str]): Complete report source lines.
        start (int): Candidate header line.

    Returns:
        ReportTable | None: Parsed cells and the next source position, or no table at this line.
    """
    if start + 1 >= len(lines) or not lines[start].strip().startswith("|"):
        return None
    header, separators = _cells(lines[start]), _cells(lines[start + 1])
    if not header or len(header) != len(separators) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separators):
        return None
    rows = [header]
    end = start + 2
    while end < len(lines) and lines[end].strip().startswith("|"):
        cells = _cells(lines[end])
        if len(cells) != len(header):
            break
        rows.append(cells)
        end += 1
    if any("![" in cell for row in rows for cell in row):
        return None
    alignments = tuple(1 if cell.startswith(":") and cell.endswith(":") else 2 if cell.endswith(":") else 0 for cell in separators)
    return ReportTable(tuple(rows), alignments, end)


def _widths(table: ReportTable, width: float) -> list[float]:
    """
    Reserve space for short identifiers and counts, leaving chart names room to wrap.

    Args:
        table (ReportTable): Parsed table with its header and cells.
        width (float): Available PDF width.

    Returns:
        list[float]: Column widths summing to the available width.
    """
    header = table.rows[0]
    if "Chart" not in header:
        return [width / len(header)] * len(header)
    sizes = []
    for column in range(len(header)):
        labels = [LINK.sub(r"\1", row[column]).replace("`", "") for row in table.rows]
        measured = max(stringWidth(label[:32], "Helvetica-Bold" if row == 0 else "Helvetica", 9) for row, label in enumerate(labels))
        sizes.append(min(160.0, max(64.0, measured + 20)))
    chart = header.index("Chart")
    remaining = width - sum(size for index, size in enumerate(sizes) if index != chart)
    if remaining < width / len(header):
        return [width / len(header)] * len(header)
    sizes[chart] = remaining
    return sizes


def draw_table(  # type: ignore[no-any-unimported]
    canvas: Canvas, table: ReportTable, top: float, new_page: Callable[[], float], document: Path
) -> float:
    """
    Draw padded, striped rows and repeat the shaded header on each continuation page.

    Args:
        canvas (Canvas): Report canvas.
        table (ReportTable): Source cells and alignments.
        top (float): Upper edge available on the current page.
        new_page (Callable[[], float]): Start a page and return its upper content edge.
        document (Path): PDF location for resolving links.

    Returns:
        float: Baseline for the paragraph following the completed table.
    """
    cells = [
        [
            Paragraph(
                linked_prose(cell, document=document),
                ParagraphStyle(
                    "table-cell",
                    fontName="Helvetica-Bold" if row == 0 else "Helvetica",
                    fontSize=9,
                    leading=12,
                    textColor="#23313d",
                    alignment=table.alignments[column],
                ),
            )
            for column, cell in enumerate(values)
        ]
        for row, values in enumerate(table.rows)
    ]
    remaining = LongTable(cells, colWidths=_widths(table, 540), repeatRows=1, splitInRow=1, hAlign="LEFT")
    remaining.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), "#e5eaf0"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), ["#ffffff", "#f5f7f9"]),
                ("LINEBELOW", (0, 0), (-1, 0), 0.7, "#bdc6ce"),
                ("LINEBELOW", (0, 1), (-1, -1), 0.25, "#e5eaf0"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    while True:
        # Split before drawing, so cell links inherit the final page coordinates.
        pieces = remaining.split(540, max(0, top - 42))
        if not pieces:
            top = new_page()
            pieces = remaining.split(540, top - 42)
            if not pieces:
                raise ValueError("Report table header and first row cannot fit on a page")
        first = pieces[0]
        _, height = first.wrap(540, top - 42)
        first.drawOn(canvas, 36, top - height)
        if len(pieces) == 1:
            return float(top - height - 12)
        remaining = pieces[1]
        top = new_page()
