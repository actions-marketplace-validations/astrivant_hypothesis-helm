"""
Render branded, paginated PDF reports while preserving links and input examples.
"""

import re
from html import escape
from importlib.resources import files
from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib.styles import ParagraphStyle  # type: ignore[import-untyped]
from reportlab.lib.utils import ImageReader  # type: ignore[import-untyped]
from reportlab.pdfgen.canvas import Canvas  # type: ignore[import-untyped]
from reportlab.platypus import Paragraph  # type: ignore[import-untyped]

from hypothesis_helm.reporting.documentation.contents import heading_inventory
from hypothesis_helm.reporting.reports.code import CODE_BACKGROUND, draw_code_block
from hypothesis_helm.reporting.reports.links import linked_prose
from hypothesis_helm.reporting.reports.overview import CellLink

__all__ = ("write_pdf",)

_HYPOTHESIS_REPOSITORY = "https://github.com/HypothesisWorks/hypothesis/"


def _panel_height(paths: list[Path], width: float, maximum: float = 440) -> float:
    """
    Reserve enough space for every image in a shared report row.

    Args:
        paths (list[Path]): Available images in the row.
        width (float): Width allocated to each image in PDF points.
        maximum (float): Height ceiling; full-page overviews can use more space than chart panels.

    Returns:
        float: Largest scaled image height, capped to fit a page.
    """
    heights = []
    for path in paths:
        with Image.open(path) as image:
            heights.append(width * image.height / image.width)
    return min(maximum, max(heights, default=160.0))


def _report_image(path: Path, width: float, height: float) -> BytesIO:
    """
    Embed a print-sized copy while leaving the original study image intact.

    Args:
        path (Path): Original PNG or other raster study image.
        width (float): Available width in PDF points.
        height (float): Available height in PDF points.

    Returns:
        BytesIO: Compressed image at up to 216 dots per inch for a compact report.
    """
    with Image.open(path) as original:
        original.thumbnail((int(width * 3), int(height * 3)), Image.Resampling.LANCZOS)
        # Composite transparency onto paper rather than turning it black in JPEG.
        image = Image.new("RGB", original.size, "white")
        rgba = original.convert("RGBA")
        image.paste(rgba, mask=rgba.getchannel("A"))
        stream = BytesIO()
        image.save(stream, format="JPEG", quality=90, optimize=True)
    stream.seek(0)
    return stream


def _cover(  # type: ignore[no-any-unimported]
    canvas: Canvas, source: str, details: tuple[tuple[str, str], ...], source_url: str | None
) -> None:
    """
    Draw a title page using the scan's recorded provenance, never the publication time.

    Args:
        canvas (Canvas): PDF page with its standard header already drawn.
        source (str): Repository, package source, or directory that was scanned.
        details (tuple[tuple[str, str], ...]): Recorded timestamps, commit, package versions, and command; commit may use a Markdown link.
        source_url (str | None): Public repository or package-source URL, when known.

    Returns:
        None: The current page contains a cover title, source, and execution details.
    """
    y = 618.0
    title = Paragraph(
        "Scan results from<br/>Helm Hypothesis testing",
        ParagraphStyle("cover-title", fontName="Helvetica-Bold", fontSize=28, leading=35, textColor="#23313d"),
    )
    _, height = title.wrap(504, 650)
    title.drawOn(canvas, 54, y - height)
    y -= height + 24
    identity = Paragraph(
        f'<link href="{escape(source_url, quote=True)}" color="#1459a6"><u>{escape(source)}</u></link>' if source_url else escape(source),
        ParagraphStyle("cover-source", fontName="Helvetica", fontSize=17, leading=23, textColor="#23313d"),
    )
    _, height = identity.wrap(504, 650)
    identity.drawOn(canvas, 54, y - height)
    y -= height + 32
    canvas.saveState()
    canvas.setStrokeColorRGB(0.82, 0.85, 0.88)
    canvas.line(54, y, 558, y)
    canvas.restoreState()
    y -= 28
    for label, value in details:
        literal = label in {"Scan command", "Working directory"}
        if literal:
            caption = Paragraph(
                escape(label), ParagraphStyle("cover-code-label", fontName="Helvetica", fontSize=10, leading=15, textColor="#53616b")
            )
            _, height = caption.wrap(504, 650)
            caption.drawOn(canvas, 54, y - height)
            y -= height + 8
        paragraph = Paragraph(
            escape(value).replace("\n", "<br/>")
            if literal
            else f'<font name="Helvetica" color="#53616b" size="10">{escape(label)}</font><br/>' + linked_prose(value),
            ParagraphStyle(
                "cover-detail",
                fontName="Courier" if literal else "Helvetica",
                fontSize=10 if literal else 12,
                leading=15,
                backColor=CODE_BACKGROUND if literal else None,
                borderPadding=8 if literal else 0,
            ),
        )
        _, height = paragraph.wrap(488 if literal else 504, 650)
        paragraph.drawOn(canvas, 62 if literal else 54, y - height)
        y -= height + (20 if literal else 12)


def write_pdf(
    content: str,
    pdf: Path,
    *,
    title: str = "Helm chart scan",
    overview: Path | None = None,
    overview_cells: tuple[CellLink, ...] = (),
    images: dict[str, Path] | None = None,
    caption_targets: dict[str, str] | None = None,
    cover_details: tuple[tuple[str, str], ...] = (),
    cover_source_url: str | None = None,
) -> None:
    """
    Render report Markdown with a reserved header and working PDF hyperlinks.

    Args:
        content (str): Report prose and fenced reproducing values.
        pdf (Path): Destination PDF file.
        title (str): Document metadata title.
        overview (Path | None): Local overview figure to embed, even when Markdown uses public URLs.
        overview_cells (tuple[CellLink, ...]): Chart cells linked to their corresponding detail sections.
        images (dict[str, Path] | None): Additional local images indexed by their Markdown alt labels.
        caption_targets (dict[str, str] | None): Internal appendix anchors indexed by image alt label.
        cover_details (tuple[tuple[str, str], ...]): Recorded timestamps, source commit, versions, and full scan command.
        cover_source_url (str | None): Public URL for the source named on the title page.

    Returns:
        None: The PDF begins with a title page and contains its logo without requiring an external image file.
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
    chart_anchors = {anchor for _, anchor in chart_sections}
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
        canvas.drawCentredString(306, 24, str(canvas.getPageNumber()))
        if canvas.getPageNumber() > 1:
            canvas.setFillColorRGB(0.08, 0.35, 0.65)
            canvas.drawRightString(576, 24, "Hypothesis")
            canvas.linkURL(
                _HYPOTHESIS_REPOSITORY,
                (576 - canvas.stringWidth("Hypothesis", "Helvetica", 8), 22, 576, 34),
                relative=0,
                thickness=0,
            )
            if canvas.getPageNumber() > 2:
                canvas.drawString(36, 24, "Back to contents")
                canvas.linkRect("", contents_anchor, (36, 22, 106, 34), relative=0, thickness=0)
        canvas.restoreState()
        return divider - 20

    canvas.setTitle(title)
    page_header()
    if heading is not None:
        canvas.bookmarkPage(destinations[heading][2])
        canvas.addOutlineEntry("Title page", destinations[heading][2], level=0)
    _cover(canvas, header_title.removeprefix("Scan results: "), cover_details, cover_source_url)
    canvas.showPage()
    y = page_header()
    canvas.bookmarkPage(contents_anchor)
    canvas.addOutlineEntry("Table of contents", contents_anchor, level=0)
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
    code_fence = ""
    code_lines: list[str] = []
    outline_levels: list[int] = []
    figure_page = False

    def code_page() -> float:
        """
        Continue a literal code block beneath the next page's normal header.

        Returns:
            float: Top edge available for the continued code box.
        """
        canvas.showPage()
        return page_header() + 8

    for index, line in enumerate(lines):
        if index == heading:
            continue
        if code_fence:
            if re.fullmatch(r" {0,3}" + re.escape(code_fence[0]) + "{" + str(len(code_fence)) + r",}\s*", line):
                y = draw_code_block(canvas, "\n".join(code_lines), y + 8, code_page)
                code_lines.clear()
                code_fence = ""
            else:
                code_lines.append(line)
            continue
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            code_fence = marker[1]
            continue
        if not line.strip():
            y -= 4
            continue
        if index in destinations:
            level, label, anchor = destinations[index]
            chart_panels = (
                [images[key] for key in (f"Topology: {label}", f"Sensitivity: {label}") if key in images]
                if anchor in chart_anchors and images
                else []
            )
            # Keep the chart heading and both panels together using their
            # actual dimensions, including differently sized sensitivity panels.
            required = _panel_height(chart_panels, 264) + 121 if chart_panels else 120
            if y < required or (figure_page and level <= 2) or (level == 2 and label.startswith("Appendix: ")):
                canvas.showPage()
                y = page_header()
                figure_page = False
            size = 14 if level <= 2 else 12 if level == 3 else 10
            paragraph = Paragraph(
                linked_prose(re.sub(r"^\s*#{1,6}\s+", "", line), document=pdf),
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
        if line in {"| Chart topology | Mutation sensitivity |", "| --- | --- |"}:
            continue
        matches = list(re.finditer(r"!\[([^\]]+)\]\((?:<[^>]+>|[^)]+)\)", line))
        if matches and images and any(match[1] in images for match in matches):
            paired = line.startswith("|")
            width = 264.0 if paired else 540.0
            height = _panel_height([images[match[1]] for match in matches if match[1] in images], width, 440 if paired else 520)
            if y - height - 55 < 42:
                canvas.showPage()
                y = page_header()
            for match in matches:
                path = images.get(match[1])
                if path is None:
                    continue
                column = line[: match.start()].count("|") - 1 if paired else 0
                panel_left = 36 + column * 276
                image = ImageReader(_report_image(path, width, height))
                iw, ih = image.getSize()
                scale = min(width / iw, height / ih)
                canvas.drawImage(
                    image, panel_left + (width - iw * scale) / 2, y - ih * scale, width=iw * scale, height=ih * scale, mask="auto"
                )
                target = (caption_targets or {}).get(match[1])
                caption_text = linked_prose(f"[{match[1]}](#{target})", document=pdf) if target else escape(match[1])
                caption = Paragraph(caption_text, ParagraphStyle("image-label", fontName="Helvetica", fontSize=8, leading=11))
                _, ch = caption.wrap(width, 100)
                caption.drawOn(canvas, panel_left, y - height - ch - 7)
            if paired:
                for column, panel_text in enumerate(line.strip("|").split("|")):
                    if "![" not in panel_text:
                        canvas.setFont("Helvetica", 9)
                        canvas.drawString(36 + column * 276, y - 40, panel_text.strip())
            y -= height + 43
            if any(match[1] in {"Published compiler graph invariants", "Output-space PCA before and after selection"} for match in matches):
                figure_page = True
            continue
        if overview is not None and line.startswith("!["):
            image = ImageReader(str(overview))
            width, height = image.getSize()
            scaled_height = 540 * height / width
            if y - scaled_height < 42:
                canvas.showPage()
                y = page_header()
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
            figure_page = True
            continue
        paragraph = Paragraph(linked_prose(line, document=pdf), ParagraphStyle("body", fontName="Helvetica", fontSize=9, leading=13))
        _, height = paragraph.wrap(540, 708)
        if y - height < 42:
            canvas.showPage()
            y = page_header()
        paragraph.drawOn(canvas, 36, y + 8 - height)
        y -= height
    if code_fence:
        draw_code_block(canvas, "\n".join(code_lines), y + 8, code_page)
    canvas.save()
