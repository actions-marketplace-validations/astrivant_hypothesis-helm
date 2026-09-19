"""
Collect discovery trees and uniquely defined helpers from installed chart sources.
"""

from __future__ import annotations

import io
import json
import tarfile
from pathlib import Path

from attrs import define, field

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.compiler.asts.actions import Action, parse
from hypothesis_helm.compiler.asts.renderer import archive_files
from hypothesis_helm.compiler.limits import active_limits


def signature(nodes: list[Action]) -> tuple[object, ...]:
    """
    Compare helper action structure independently of filenames and source line offsets.

    Args:
        nodes (list[Action]): Helper body in lexical order.

    Returns:
        tuple[object, ...]: Statements and their branch structure; literal output is irrelevant to discovery.
    """
    return tuple((node.text, signature(node.children), signature(node.otherwise)) for node in nodes)


@define
class DiscoverySources:
    """
    Keep render roots separate from callable helper definitions.

    Attributes:
        roots (dict[str, list[Action]]): Root-chart templates eligible for direct execution.
        helpers (dict[str, tuple[str, list[Action]]]): Unique helper bodies with source filenames.
        templates (dict[str, tuple[str, list[Action]]]): Root-chart files addressable by Helm template name.
        base_path (str): Helm's chart-qualified template directory for root invocations.
        ambiguous (set[str]): Helper names whose installed definitions disagree.
        diagnostics (list[tuple[str, int, str]]): Source loading or parsing failures.
    """

    roots: dict[str, list[Action]] = field(factory=dict)
    helpers: dict[str, tuple[str, list[Action]]] = field(factory=dict)
    templates: dict[str, tuple[str, list[Action]]] = field(factory=dict)
    base_path: str = ""
    ambiguous: set[str] = field(factory=set)
    diagnostics: list[tuple[str, int, str]] = field(factory=list)

    def add(self, source: str, content: str, *, root: bool) -> None:
        """
        Parse one source and register its statically named definitions.

        Args:
            source (str): Chart-relative source filename, including archive members when needed.
            content (str): Original Go template text.
            root (bool): Whether this file belongs to the chart being inspected.

        Returns:
            None: Trees or diagnostics are retained in this source registry.
        """
        try:
            nodes = parse(content)
        except ValueError as exc:
            self.diagnostics.append((source, 1, str(exc)))
            return
        if root and not Path(source).name.startswith("_"):
            self.roots[source] = nodes
        if root:
            self.templates[f"{self.base_path}/{source.removeprefix('templates/')}"] = (source, nodes)

        def register(items: list[Action]) -> None:
            """
            Collect named definitions without treating their bodies as root executions.

            Args:
                items (list[Action]): Current action subtree.

            Returns:
                None: Literal helper names are registered or marked ambiguous.
            """
            for node in items:
                if node.tokens[0] in ("define", "block") and len(node.tokens) >= 2:
                    token = node.tokens[1]
                    if token.startswith(('"', "`")):
                        name = token[1:-1] if token.startswith("`") else str(json.loads(token))
                        previous = self.helpers.get(name)
                        if previous is not None and signature(previous[1]) != signature(node.children):
                            self.ambiguous.add(name)
                        self.helpers[name] = (source, node.children)
                register(node.children)
                register(node.otherwise)

        register(nodes)

    @classmethod
    def build(cls, chart: Path, *, limits: dict[str, int] | None = None) -> DiscoverySources:
        """
        Read local templates and dependency helpers, including bounded nested chart archives.

        Args:
            chart (Path): Prepared chart directory.
            limits (dict[str, int] | None): Captured parent budgets, or settings resolved for this chart.

        Returns:
            DiscoverySources: Root trees, callable helpers, and explicit failures to inspect sources.
        """
        result = cls()
        limits = active_limits(chart) if limits is None else limits
        metadata = yamlio.load((chart / "Chart.yaml").read_text()) if (chart / "Chart.yaml").is_file() else {}
        name = metadata.get("name", chart.name) if isinstance(metadata, dict) else chart.name
        result.base_path = f"{name}/templates"

        def archive(data: bytes, source: str, depth: int) -> None:
            """
            Read dependency templates from an archive without extracting its members.

            Args:
                data (bytes): Installed chart archive bytes.
                source (str): Logical archive location for diagnostics.
                depth (int): Current dependency archive nesting depth.

            Returns:
                None: Helper definitions and bounded-loading diagnostics are recorded.
            """
            if depth >= limits["max_dependency_depth"]:
                result.diagnostics.append(
                    (source, 1, f"dependency helper inspection exceeds compiler.max_dependency_depth={limits['max_dependency_depth']}")
                )
                return
            for name, content in archive_files(io.BytesIO(data), limits=limits).items():
                parts = Path(name).parts
                if parts[0] == "templates" or (parts[0] == "charts" and "templates" in parts):
                    result.add(f"{source}/{name}", content.decode(), root=False)
                elif parts[0] == "charts" and name.endswith(".tgz"):
                    archive(content, f"{source}/{name}", depth + 1)

        for directory in (chart / "templates", chart / "charts"):
            for file in sorted(directory.rglob("*")):
                if not file.is_file():
                    continue
                source = file.relative_to(chart).as_posix()
                root = directory.name == "templates"
                try:
                    if not root and file.suffix == ".tgz":
                        if file.stat().st_size > limits["max_context_bytes"]:
                            raise ValueError(f"dependency archive exceeds compiler.max_context_bytes={limits['max_context_bytes']}")
                        archive(file.read_bytes(), source, 0)
                    elif root or "templates" in file.relative_to(directory).parts:
                        result.add(source, file.read_text(), root=root)
                except (OSError, UnicodeError, ValueError, tarfile.TarError) as exc:
                    result.diagnostics.append((source, 1, str(exc)))
        for name in result.ambiguous:
            result.helpers.pop(name, None)
        return result
