"""
Carry classified Helm rendering and manifest validation failures.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("RenderFailure",)


if TYPE_CHECKING:
    from hypothesis_helm.findings.generator import Finding


class RenderFailure(AssertionError):
    """
    Attach a stable check identifier to a reproducible render failure.

    Attributes:
        code (str): Stable identifier, independent of report grouping order.
        finding (Finding): Structured observation carried by this exception.
        controls (dict[str, object]): Frozen severity and failure decision from the detecting scope.
        resources (list[object] | None): Parsed output available before validation failed.
    """

    code: str
    finding: Finding
    controls: dict[str, object]
    resources: list[object] | None = None

    def __init__(self, message: str, code: str = "HH1001") -> None:
        """
        Retain the diagnostic and its explicit rule identity.

        Args:
            message (str): Original renderer or validator diagnostic.
            code (str): Explicit detected condition, or an unclassified template failure.
        """
        from hypothesis_helm.findings.generator import FindingGenerator
        from hypothesis_helm.findings.severity import attributes

        self.finding = FindingGenerator.create(code, message)
        self.code = self.finding.rule.code
        self.controls = attributes(self.code)
        super().__init__(f"[{self.code}] {message}")
