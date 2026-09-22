"""
Publish complete chart audit findings as portable, compressed JSON attachments.
"""

import gzip
import json
from pathlib import Path

from hypothesis_helm.schemas.contracts import mapping

__all__ = ("write_audit_data",)


def write_audit_data(report: dict[str, object], chart: dict[str, object], stem: Path, index: int) -> Path:
    """
    Retain the findings behind a chart's abbreviated report without copying its raw run directory.

    Args:
        report (dict[str, object]): Scan identity and recorded execution timestamps.
        chart (dict[str, object]): Chart with its original audit findings and unresolved accesses.
        stem (Path): Human report filename without its extension.
        index (int): One-based chart number shown in the report overview.

    Returns:
        Path: Compressed JSON attachment containing every reported audit finding and source reference.
    """
    audit = mapping(chart["audit"])
    document = {
        "chart": chart["chart"],
        "run_hash": report["run_hash"],
        "started_at": report["started_at"],
        "finished_at": report["finished_at"],
        "findings": audit.get("findings", []),
        "unresolved": audit.get("unresolved", []),
    }
    # Report numbering avoids interpreting arbitrary chart names as filesystem paths.
    destination = stem.parent / f"{stem.name}-data" / f"{index:04d}.audit.json.gz"
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Source references repeat heavily; gzip keeps these final attachments small.
    # A fixed gzip timestamp makes republishing identical evidence byte-for-byte stable.
    destination.write_bytes(gzip.compress((json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode(), mtime=0))
    return destination
