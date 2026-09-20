"""
Keep complete property manifest streams available when successful tests are reused.
"""

import hashlib
import json
import re
import shutil
from pathlib import Path
from uuid import uuid4

from attrs import frozen

from hypothesis_helm.reporting.output import emit_manifest

__all__ = ("ManifestStore",)


@frozen
class ManifestStore:
    """
    Store immutable manifest bundles beneath one suite fingerprint.

    Attributes:
        root (Path): Directory beside the matching cached property outcomes.
    """

    root: Path

    def index(self, node: str) -> Path:
        """
        Locate a property pointer without treating its pytest ID as a filename.

        Args:
            node (str): Suite-relative pytest property ID.

        Returns:
            Path: Property metadata filename.
        """
        return self.root / (hashlib.sha256(node.encode()).hexdigest() + ".json")

    def publish(self, node: str, capture: Path) -> None:
        """
        Publish a complete stream before atomically replacing its property pointer.

        Args:
            node (str): Property whose call and teardown both succeeded.
            capture (Path): Private JSON Lines file containing every emitted resource.

        Returns:
            None: Concurrent readers see either complete generation of the stream.
        """
        with capture.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        self.root.mkdir(parents=True, exist_ok=True)
        blob = self.root / f"{digest}.jsonl"
        temporary = self.root / f"{uuid4().hex}.tmp"
        try:
            # The configured cache may live on a different filesystem from the run artifacts.
            shutil.copyfile(capture, temporary)
            temporary.replace(blob)
            temporary.write_text(json.dumps({"version": 1, "node": node, "sha256": digest}) + "\n")
            temporary.replace(self.index(node))
        finally:
            temporary.unlink(missing_ok=True)

    def verified(self, node: str) -> Path | None:
        """
        Reject incomplete, corrupt or mismatched streams before skipping a property.

        Args:
            node (str): Property eligible for cached success reuse.

        Returns:
            Path | None: Verified immutable blob, or none to require fresh testing.
        """
        try:
            metadata = json.loads(self.index(node).read_text())
            if not isinstance(metadata, dict) or metadata.get("version") != 1 or metadata.get("node") != node:
                return None
            digest = metadata.get("sha256")
            if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
                return None
            blob = self.root / f"{digest}.jsonl"
            with blob.open("rb") as stream:
                if hashlib.file_digest(stream, "sha256").hexdigest() != digest:
                    return None
                stream.seek(0)
                for line in stream:
                    json.loads(line)
            return blob
        except (OSError, ValueError):
            return None

    def replay(self, node: str) -> int:
        """
        Stream cached resources through the currently selected JSON or YAML output.

        Args:
            node (str): Property skipped after its cached stream was verified.

        Returns:
            int: Number of resources replayed for downstream validation.

        Raises:
            ValueError: Previously verified data became unavailable or corrupt.
        """
        blob = self.verified(node)
        if blob is None:
            raise ValueError(f"Cached manifests became unavailable for {node}; rerun with --rerun all")
        count = 0
        with blob.open() as stream:
            for line in stream:
                emit_manifest(json.loads(line))
                count += 1
        return count
