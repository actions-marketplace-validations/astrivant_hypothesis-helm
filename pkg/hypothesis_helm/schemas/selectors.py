"""
Match local chart policies against stable source locations and chart-name matrices.
"""

import os
from fnmatch import fnmatchcase
from pathlib import Path
from types import TracebackType

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.schemas.contracts import mapping, sequence

SOURCE_ENVIRONMENT = "HYPOTHESIS_HELM_CHART_SOURCE"


def chart_identity(chart: Path) -> str:
    """
    Read the exact chart name used by policy selectors, without log-preview truncation.

    Args:
        chart (Path): Chart directory, including an isolated working copy.

    Returns:
        str: Metadata name, or the directory name if no metadata is available.
    """
    metadata = chart / "Chart.yaml"
    return str(mapping(yamlio.load(metadata.read_text())).get("name")) if metadata.is_file() else chart.name


def source_identity(chart: Path) -> str:
    """
    Identify the original source rather than a disposable working copy.

    Args:
        chart (Path): Original chart directory for direct commands.

    Returns:
        str: Scan source inherited by workers, or the resolved chart directory.
    """
    return os.environ.get(SOURCE_ENVIRONMENT, str(chart.resolve()))


def selectors(value: object, root: Path) -> list[object]:
    """
    Validate plain chart names or matrix rows of source and name patterns.

    Args:
        value (object): The charts entry from a local configuration.
        root (Path): Configuration directory used to resolve local source paths.

    Returns:
        list[object]: Serializable names and normalized matrix rows.
    """
    if not isinstance(value, list) or not value:
        raise ValueError("charts must be a nonempty list of names or {sources: [...], names: [...]} selectors")
    result: list[object] = []
    for item in value:
        if isinstance(item, str) and item:
            result.append(item)
            continue
        if not isinstance(item, dict) or set(item) != {"sources", "names"}:
            raise ValueError("Chart matrix rows require only 'sources' and 'names' lists")
        for key in ("sources", "names"):
            entries = item[key]
            if not isinstance(entries, list) or not entries or any(not isinstance(entry, str) or not entry for entry in entries):
                raise ValueError(f"Chart selector {key} must be a nonempty list of strings")
        sources = []
        for raw in sequence(item["sources"]):
            source = str(raw)
            if source.startswith((".", "/", "~")):
                source = str((root / Path(source).expanduser()).resolve())
            sources.append(source)
        result.append({"sources": sorted(set(sources)), "names": sorted(set(str(name) for name in sequence(item["names"])))})
    return result


def matching_rules(chart: Path) -> list[dict[str, object]]:
    """
    Select policy rows by chart metadata and the original repository or local source.

    Args:
        chart (Path): Chart directory, including temporary copies.

    Returns:
        list[dict[str, object]]: Rules whose source/name product includes this chart.
    """
    from hypothesis_helm.schemas.policy import inherited_policy

    rules = sequence(inherited_policy().get("input_constraints", []))
    if not rules:
        return []
    name = chart_identity(chart)
    source = source_identity(chart)
    result = []
    for raw in rules:
        rule = mapping(raw)
        for selector in sequence(rule["charts"]):
            if isinstance(selector, str):
                matched = fnmatchcase(name, selector)
            else:
                row = mapping(selector)
                matched = any(fnmatchcase(source, str(pattern)) for pattern in sequence(row["sources"])) and any(
                    fnmatchcase(name, str(pattern)) for pattern in sequence(row["names"])
                )
            if matched:
                result.append(rule)
                break
    return result


class SourceScope:
    """
    Preserve original source identity through subprocess inheritance and nested scans.
    """

    def __init__(self, source: str) -> None:
        """
        Retain the source to expose while the scope is active.

        Args:
            source (str): Original repository URL, Helm reference, or local directory.
        """
        self.source = source
        self.previous: str | None = None

    def __enter__(self) -> None:
        """
        Publish source identity to this process and its workers.

        Returns:
            None: The previous identity is retained for restoration.
        """
        self.previous = os.environ.get(SOURCE_ENVIRONMENT)
        os.environ[SOURCE_ENVIRONMENT] = self.source

    def __exit__(self, kind: type[BaseException] | None, error: BaseException | None, traceback: TracebackType | None) -> None:
        """
        Restore the caller's source even when cancellation interrupts a scan.

        Args:
            kind (type[BaseException] | None): Propagating exception type.
            error (BaseException | None): Original exception.
            traceback (TracebackType | None): Original traceback.

        Returns:
            None: Exceptions continue after source restoration.
        """
        if self.previous is None:
            os.environ.pop(SOURCE_ENVIRONMENT, None)
        else:
            os.environ[SOURCE_ENVIRONMENT] = self.previous
