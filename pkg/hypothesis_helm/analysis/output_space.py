"""
Encode bounded manifest observations and fit one PCA frame for a repository report.
"""

import hashlib
import json
import math
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

__all__ = ("DIMENSIONS", "ENCODING", "manifest_vector", "project")

DIMENSIONS = 256
ENCODING = "signed-sha256-manifest-features-256-v1"


def manifest_vector(resources: object) -> list[float]:
    """
    Encode output structure and values in a fixed-size vector without storing manifest text.

    Args:
        resources (object): Parsed manifest documents from one successful render.

    Returns:
        list[float]: Signed hashed features; collisions are possible and do not establish equivalence.
    """
    vector = [0.0] * DIMENSIONS

    def add(path: tuple[str | int, ...], kind: str, value: object = None, weight: float = 1.0) -> None:
        """
        Accumulate one typed feature without retaining its original field contents.

        Args:
            path (tuple[str | int, ...]): Manifest field address.
            kind (str): Presence, container, numeric or categorical feature.
            value (object): Category value when applicable.
            weight (float): Numeric feature magnitude.

        Returns:
            None: The fixed feature vector is updated.
        """
        key = json.dumps([path, kind, value], sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        digest = hashlib.sha256(key.encode()).digest()
        index = int.from_bytes(digest[:4], "big") % DIMENSIONS
        vector[index] += weight if digest[4] & 1 else -weight

    def visit(value: object, path: tuple[str | int, ...]) -> None:
        """
        Visit leaves and containers, retaining types and array positions.

        Args:
            value (object): JSON-compatible manifest node.
            path (tuple[str | int, ...]): Stable resource-relative address.

        Returns:
            None: Features enter the bounded vector without a vocabulary-sized matrix.
        """
        add(path, "present")
        if isinstance(value, dict):
            add(path, "object")
            for key, child in sorted(value.items()):
                visit(child, (*path, str(key)))
        elif isinstance(value, list):
            add(path, "array")
            for index, child in enumerate(value):
                visit(child, (*path, index))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            # A signed log retains direction without allowing extreme valid
            # schema numbers to overflow centering or dominate every chart.
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("Nonfinite manifest number cannot enter PCA")
            magnitude = math.log(abs(value)) if abs(value) > 1e300 else math.log1p(abs(value))
            add(path, "number", weight=-magnitude if value < 0 else magnitude)
        else:
            add(path, type(value).__name__, value)

    if not isinstance(resources, list):
        raise ValueError("PCA expects a list of rendered resource objects")
    ordered = sorted(resources, key=lambda value: json.dumps(value, sort_keys=True))
    occurrences: dict[str, int] = {}
    for resource in ordered:
        if not isinstance(resource, dict):
            raise ValueError("PCA expects rendered resource objects")
        metadata = resource.get("metadata", {})
        if not isinstance(metadata, dict):
            raise ValueError("PCA expects resource metadata to be an object")
        identity = json.dumps(
            [resource.get("apiVersion"), resource.get("kind"), metadata.get("namespace"), metadata.get("name")],
            sort_keys=True,
        )
        occurrence = occurrences.get(identity, 0)
        occurrences[identity] = occurrence + 1
        visit(resource, (identity, occurrence))
    return vector


def project(vectors: Sequence[Sequence[float]]) -> tuple[NDArray[np.float64], dict[str, object]]:
    """
    Fit standardized PCA to all reference observations once, before taking the retained subset.

    Args:
        vectors (Sequence[Sequence[float]]): Compatible bounded manifest vectors from every measured chart.

    Returns:
        tuple[NDArray[np.float64], dict[str, object]]: Two-dimensional coordinates and explained-variance metadata.
    """
    if not vectors:
        return np.zeros((0, 2)), {"explained_variance_ratio": [0.0, 0.0], "rank": 0, "encoding": ENCODING}
    matrix = np.asarray(vectors, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[1] != DIMENSIONS or not np.isfinite(matrix).all():
        raise ValueError("PCA observations require compatible, finite manifest vectors")
    center = matrix.mean(axis=0)
    scale = matrix.std(axis=0)
    active = scale > 0
    normalized = (matrix[:, active] - center[active]) / scale[active]
    scores = np.zeros((len(vectors), 2), dtype=np.float64)
    variance = np.zeros(2)
    rank = 0
    if normalized.shape[1]:
        _, singular, basis = np.linalg.svd(normalized, full_matrices=False)
        dimensions = min(2, len(singular))
        components = basis[:dimensions].copy()
        # Axis signs are arbitrary in SVD; fix them for reproducible redraws.
        for component in components:
            if component[np.argmax(np.abs(component))] < 0:
                component *= -1
        scores[:, :dimensions] = normalized @ components.T
        total = float(np.sum(singular**2))
        if total:
            variance[:dimensions] = singular[:dimensions] ** 2 / total
            tolerance = singular[0] * max(normalized.shape) * np.finfo(normalized.dtype).eps
            rank = int(np.sum(singular > tolerance))
    return scores, {
        "encoding": ENCODING,
        "explained_variance_ratio": variance.tolist(),
        "rank": rank,
        "fit": "one standardized frame fitted to the pooled reference sample; retained outputs reuse it",
        "weighting": "one observation per measured reference configuration, including repeated outputs",
    }
