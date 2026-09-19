"""
Fingerprint application and harness sources for reproducible measurements.
"""

import hashlib
from pathlib import Path

import hypothesis_helm
import hypothesis_helm_catalog
import pipeline


def code_digest() -> str:
    """
    Identify measured application and harness code, including uncommitted changes.

    Returns:
        str: SHA-256 fingerprint of execution and harness Python sources.
    """
    digest = hashlib.sha256()
    roots = [
        Path(__file__).resolve().parents[1],
        *(Path(str(module.__file__)).parent for module in (hypothesis_helm, hypothesis_helm_catalog, pipeline)),
    ]
    for base in roots:
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in {".py", ".json"} and "tests" not in path.parts:
                digest.update(f"{base.name}/{path.relative_to(base)}".encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()
