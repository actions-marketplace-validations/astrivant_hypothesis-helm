"""
Verify readable PDF tables preserve their cell content and links across pages.
"""

import base64
import re
import zlib
from pathlib import Path

from hypothesis_helm.reporting.reports.pdf import write_pdf
from hypothesis_helm.reporting.reports.tables import read_table


def test_parse_table_preserves_literal_pipes_and_alignment() -> None:
    """
    Distinguish column boundaries from code and keep chart image panels separate.

    Returns:
        None: Parsed tables retain escaped pipes, inline code, and column alignment.
    """
    table = read_table(["| Number | Chart | Counts |", "| :---: | :--- | ---: |", r"| 01 | `a|b` and c\|d | 2 / 1 |", "after"], 0)
    assert table is not None
    assert table.rows[1] == ("01", "`a|b` and c|d", "2 / 1")
    assert table.alignments == (1, 0, 2) and table.end == 3
    assert read_table(["| Chart |", "| --- |", "| ![Topology](topology.png) |"], 0) is None
    assert read_table(["| Not | a table |", "ordinary text"], 0) is None


def test_pdf_table_repeats_headers_and_preserves_links(tmp_path: Path) -> None:
    """
    Split a large color key into styled pages without losing chart destinations or the last row.

    Args:
        tmp_path (Path): Table PDF destination.

    Returns:
        None: Headers repeat, pipe separators disappear, and every cell link reaches the correct chart.
    """
    rows = ["| Color number | Chart | Measured / retained |", "| :---: | :--- | ---: |"]
    rows.extend(f"| {index:03d} | [chart-{index:03d}](#target-chart) | {index} / 1 |" for index in range(1, 116))
    content = "# Table report\n\n## Charts\n\n### Target chart\n\nPassed.\n\n## Color key\n\n" + "\n".join(rows)
    pdf = tmp_path / "table.pdf"
    write_pdf(content, pdf)
    objects = dict(re.findall(rb"(\d+) 0 obj\s*(.*?)\s*endobj", pdf.read_bytes(), re.DOTALL))
    outline = next(body for body in objects.values() if b"/Title (Target chart)" in body)
    destination = re.search(rb"/Dest \[ ([^]]+)\]", outline)
    assert destination is not None
    links = [body for body in objects.values() if b"/Subtype /Link" in body and b"/Dest [ " + destination[1] + b"]" in body]
    assert len(links) == 115
    streams = []
    for body in objects.values():
        if b"/Subtype /Image" in body:
            continue
        if b"/Filter [ /ASCII85Decode /FlateDecode ]" in body and (match := re.search(rb"stream\s*\n(.*?)endstream", body, re.DOTALL)):
            streams.append(zlib.decompress(base64.a85decode(match[1].strip(), adobe=True)))
    drawn = b"\n".join(streams)
    assert drawn.count(b"(Color number)") >= 3
    assert b"(chart-115)" in drawn and b"(115 / 1)" in drawn
    assert b"|" not in drawn  # PDF tables use drawn cells, not Markdown punctuation.
    assert b".898039 .917647 .941176 rg" in drawn  # Header background.
    assert b".960784 .968627 .976471 rg" in drawn  # Alternating body rows.
