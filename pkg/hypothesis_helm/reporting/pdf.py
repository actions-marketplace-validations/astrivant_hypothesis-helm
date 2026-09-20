"""
Render branded, paginated PDF reports while preserving links and input examples.
"""

import re
import textwrap
from html import escape
from importlib.resources import files
from io import BytesIO
from pathlib import Path

from reportlab.lib.styles import ParagraphStyle  # type: ignore[import-untyped]
from reportlab.lib.utils import ImageReader  # type: ignore[import-untyped]
from reportlab.pdfgen.canvas import Canvas  # type: ignore[import-untyped]
from reportlab.platypus import Paragraph  # type: ignore[import-untyped]

from hypothesis_helm.reporting.contents import heading_inventory
from hypothesis_helm.reporting.links import LINK, linked_prose
from hypothesis_helm.reporting.overview import CellLink
from hypothesis_helm.reporting.references import APPENDIX_TITLE


def write_pdf(
    content: str,
    pdf: Path,
    *,
    title: str = "Helm chart scan",
    overview: Path | None = None,
    overview_cells: tuple[CellLink, ...] = (),
) -> None:
    """
    Render report Markdown with a reserved header and working PDF hyperlinks.

    Args:
        content (str): Report prose and fenced reproducing values.
        pdf (Path): Destination PDF file.
        title (str): Document metadata title.
        overview (Path | None): Local overview figure to embed, even when Markdown uses public URLs.
        overview_cells (tuple[CellLink, ...]): Chart cells linked to their corresponding detail sections.

    Returns:
        None: The PDF contains its logo without requiring an external image file.
    """
    canvas = Canvas(str(pdf), pagesize=(612, 792))
    logo = ImageReader(BytesIO(files("hypothesis_helm.reporting").joinpath("assets", "logo.png").read_bytes()))

    lines = content.splitlines()
    headings = heading_inventory(content)
    chart_sections = []
    in_charts = False
    for _, level, label, anchor in headings:
        if level <= 2:
            in_charts = level == 2 and label == "Charts"
        elif in_charts and level == 3:
            chart_sections.append((label, anchor))
    destinations = {index: (level, label, anchor) for index, level, label, anchor in headings}
    contents_anchor = "report-contents"
    while contents_anchor in {anchor for _, _, _, anchor in headings}:
        contents_anchor += "-contents"
    heading = next((index for index, line in enumerate(lines) if line.strip()), None)
    header_title = title
    if heading is not None and lines[heading].startswith("# "):
        header_title = lines[heading][2:].strip()
    else:
        heading = None

    def page_header() -> float:
        """
        Align the report title and compact logo within one shared header.

        Returns:
            float: Body baseline below the header divider, accounting for wrapped titles.
        """
        canvas.saveState()
        paragraph = Paragraph(escape(header_title), ParagraphStyle("header", fontName="Helvetica-Bold", fontSize=14, leading=18))
        _, height = paragraph.wrap(486, 708)
        paragraph.drawOn(canvas, 36, 766 - height)
        # The packaged square asset includes transparent padding around the mark.
        # Its visible right edge aligns with the body's 576-point right margin.
        canvas.drawImage(logo, 543, 734, width=44, height=44, mask="auto", preserveAspectRatio=True)
        divider = min(736.0, 756 - float(height))
        canvas.setStrokeColorRGB(0.82, 0.85, 0.88)
        canvas.setLineWidth(0.5)
        canvas.line(36, divider, 576, divider)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColorRGB(0.4, 0.44, 0.48)
        canvas.drawRightString(576, 24, str(canvas.getPageNumber()))
        if canvas.getPageNumber() > 1:
            canvas.setFillColorRGB(0.08, 0.35, 0.65)
            canvas.drawString(36, 24, "Back to contents")
            canvas.linkRect("", contents_anchor, (36, 22, 106, 34), relative=0, thickness=0)
        canvas.restoreState()
        return divider - 20

    canvas.setTitle(title)
    y = page_header()
    canvas.bookmarkPage(contents_anchor)
    canvas.addOutlineEntry("Table of contents", contents_anchor, level=0)
    if heading is not None:
        canvas.bookmarkPage(destinations[heading][2])
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(36, y, "Table of contents")
    y -= 38
    for index, level, label, anchor in headings:
        if index == heading or level > 2:
            continue
        paragraph = Paragraph(
            f'<link href="#{escape(anchor, quote=True)}" color="#1459a6"><u>{escape(label)}</u></link>',
            ParagraphStyle("contents", fontName="Helvetica", fontSize=12, leading=18),
        )
        _, height = paragraph.wrap(540, 708)
        if y - height < 90:
            canvas.showPage()
            y = page_header()
        paragraph.drawOn(canvas, 36, y - height)
        y -= height + 14
    note = Paragraph(
        "Click a section to jump to it. The PDF bookmarks also link to individual charts and diagnostics.",
        ParagraphStyle("navigation", fontName="Helvetica", fontSize=10, leading=15, textColor="#53616b"),
    )
    _, height = note.wrap(440, 708)
    note.drawOn(canvas, 36, y - height - 12)
    canvas.showPage()
    y = page_header()
    canvas.setFont("Courier", 8)
    code_fence = ""
    outline_levels: list[int] = []
    overview_page = False
    for index, line in enumerate(lines):
        if index == heading:
            continue
        if not line.strip():
            y -= 4
            continue
        marker = re.match(r"^(`{3,})(.*)$", line)
        if not code_fence and marker:
            code_fence = marker[1]
            continue
        if code_fence and re.fullmatch(re.escape(code_fence) + r"`*\s*", line):
            code_fence = ""
            continue
        if index in destinations:
            level, label, anchor = destinations[index]
            if y < 120 or (overview_page and level <= 2) or (level == 2 and label == APPENDIX_TITLE):
                canvas.showPage()
                y = page_header()
                overview_page = False
            size = 14 if level <= 2 else 12 if level == 3 else 10
            paragraph = Paragraph(
                linked_prose(re.sub(r"^\s*#{1,6}\s+", "", line)),
                ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=size, leading=size + 4),
            )
            _, height = paragraph.wrap(540, 708)
            if y - height < 90:
                canvas.showPage()
                y = page_header()
            canvas.bookmarkHorizontalAbsolute(anchor, y + 12)
            while outline_levels and outline_levels[-1] >= level:
                outline_levels.pop()
            canvas.addOutlineEntry(label, anchor, level=len(outline_levels), closed=level >= 2)
            outline_levels.append(level)
            paragraph.drawOn(canvas, 36, y + 11 - height)
            y -= height + 8
            continue
        if not code_fence and overview is not None and line.startswith("!["):
            image = ImageReader(str(overview))
            width, height = image.getSize()
            scaled_height = 540 * height / width
            canvas.drawImage(image, 36, y - scaled_height, width=540, height=scaled_height, mask="auto")
            for cell in overview_cells:
                label, anchor = chart_sections[cell.chart]
                left, bottom, right, top = cell.bounds
                canvas.linkRect(
                    f"Chart {cell.chart + 1:02d}: {label}",
                    anchor,
                    (
                        36 + left * 540,
                        y - scaled_height + bottom * scaled_height,
                        36 + right * 540,
                        y - scaled_height + top * scaled_height,
                    ),
                    relative=0,
                    thickness=0,
                )
            y -= scaled_height + 16
            overview_page = True
            continue
        if not code_fence and LINK.search(line):
            paragraph = Paragraph(linked_prose(line), ParagraphStyle("links", fontName="Courier", fontSize=8, leading=12))
            _, height = paragraph.wrap(540, 708)
            if y - height < 42:
                canvas.showPage()
                y = page_header()
            paragraph.drawOn(canvas, 36, y + 8 - height)
            y -= height
            continue
        if not code_fence:
            line = re.sub(r"\[([^\]]+)\]\(<\1>\)", r"\1", line)
            line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", line)
            line = line.replace("**", "").replace("`", "")
        for wrapped in textwrap.wrap(line, width=100) or [""]:
            if y < 42:
                canvas.showPage()
                y = page_header()
            canvas.setFont("Courier", 8)
            canvas.drawString(36, y, wrapped.encode("latin-1", "backslashreplace").decode("latin-1"))
            y -= 12
    canvas.save()
