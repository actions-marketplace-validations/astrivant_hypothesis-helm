"""
Present live findings and relay structured worker logs through the coordinator.
"""

import json
import logging
import re
from pathlib import Path

from attrs import define, field
from ruamel.yaml.error import YAMLError

from hypothesis_helm.charts.values import yamlio
from hypothesis_helm.findings.catalog import CATALOG
from hypothesis_helm.findings.severity import level
from hypothesis_helm.reporting.progress import format_path
from hypothesis_helm.reporting.reproductions import changed_values

LOGGER = logging.getLogger(__name__)
WORKER_PREFIX = "HYPOTHESIS_HELM_LOG "


class LogFormatter(logging.Formatter):
    """
    Optionally color only the severity label, preserving plain worker and manifest streams.
    """

    def __init__(self, *, color: bool = False) -> None:
        """
        Select explicit ANSI coloring for the terminal-facing handler.

        Args:
            color (bool): Whether the destination should receive ANSI escape sequences.
        """
        super().__init__("[%(levelname)s] %(message)s")
        self.color = color

    def format(self, record: logging.LogRecord) -> str:
        """
        Format one message without changing the shared log record.

        Args:
            record (logging.LogRecord): Original local or relayed worker record.

        Returns:
            str: Plain text or a colored severity label followed by the unchanged message.
        """
        rendered = super().format(record)
        if not self.color:
            return rendered
        color = "31" if record.levelno >= logging.ERROR else "33" if record.levelno >= logging.WARNING else "36"
        label = f"[{record.levelname}]"
        return f"\033[{color}m{label}\033[0m" + rendered[len(label) :]


def compact(value: str, limit: int = 320) -> str:
    """
    Bound terminal previews and remove control characters from untrusted diagnostics.

    Args:
        value (str): Diagnostic, chart name, path or rendered input preview.
        limit (int): Maximum displayed characters before an omission marker.

    Returns:
        str: One printable line, with full evidence retained in artifacts.
    """
    text = " ".join("".join(char if char.isprintable() else " " for char in value).split())
    return text if len(text) <= limit else text[:limit] + "..."


def diagnostic_line(message: str) -> str:
    """
    Prefer Helm's error over preceding merge warnings while keeping multiline evidence in artifacts.

    Args:
        message (str): Complete diagnostic, possibly prefixed with a finding code.

    Returns:
        str: First explicit error line, or the original first nonempty line as a fallback.
    """
    lines = [re.sub(r"^\[HH\d+\]\s*", "", line.strip()) for line in message.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if line.lower().startswith(("error:", "fatal:")) or re.search(r"\blevel=ERROR\b", line):
            if "execution error at (" in line and line.endswith(":"):
                return " ".join(item for item in lines[index : index + 4] if not item.startswith("Use --debug"))
            return line
    return lines[0] if lines else ""


def chart_name(directory: Path) -> str:
    """
    Identify an isolated chart by its metadata rather than its temporary directory name.

    Args:
        directory (Path): Chart source or isolated dependency-build copy.

    Returns:
        str: Readable chart name with a directory fallback.
    """
    try:
        metadata = yamlio.load((directory / "Chart.yaml").read_text())
        if isinstance(metadata, dict) and isinstance(metadata.get("name"), str):
            return compact(metadata["name"], 100)
    except (OSError, ValueError, YAMLError):
        pass
    return compact(directory.name, 100)


def input_baseline(directory: Path, fields: int) -> None:
    """
    Announce the compiler inventory at the boundary of one chart run.

    Args:
        directory (Path): Chart owned by the coordinator or standalone runner.
        fields (int): Number of statically named fields in its shared inventory.

    Returns:
        None: One INFO record identifies the chart and its discovered input surface.
    """
    name = chart_name(directory)
    LOGGER.info("Compiler input baseline: %d statically named fields; chart=%s", fields, name, extra={"chart": name})


@define
class FindingLog:
    """
    Announce the first observed condition per code, then its final reproducing input.

    Attributes:
        chart (str): Human-readable chart name.
        defaults (dict[str, object]): Baseline used to identify changed overrides.
        paths (tuple[tuple[str | int, ...], ...]): Paths selected for the current property.
        artifacts (Path | None): Full reproducer destination, if enabled.
        seen (set[str]): Codes already announced during this property, including shrinking.
    """

    chart: str
    defaults: dict[str, object]
    paths: tuple[tuple[str | int, ...], ...] = ()
    artifacts: Path | None = None
    seen: set[str] = field(factory=set)

    def observed(self, code: str, message: str, values: dict[str, object]) -> None:
        """
        Log a detected condition once without repeating every shrink attempt.

        Args:
            code (str): Observed finding code, or a custom property identifier.
            message (str): Diagnostic from the failing check.
            values (dict[str, object]): Actual overrides submitted to the failing check.

        Returns:
            None: A bounded WARNING record is emitted immediately for each new code.
        """
        from hypothesis_helm.findings.suppressions import observe

        observe(code, self.defaults, values)
        if code not in self.seen:
            self.seen.add(code)
            self.emit("Finding observed", code, message, values)

    def emit(self, stage: str, code: str, message: str, values: dict[str, object] | None = None, *, severity: str | None = None) -> None:
        """
        Render a concise finding with input context and a link to retained evidence.

        Args:
            stage (str): Observation, final counterexample, or execution diagnostic.
            code (str): Finding code or diagnostic category.
            message (str): Original diagnostic, shortened for console output.
            values (dict[str, object] | None): Overrides when available; None means no input was recorded.
            severity (str | None): Recorded severity when the detecting scope has already exited.

        Returns:
            None: Logging does not change the check's outcome or its reproducing input.
        """
        if not LOGGER.isEnabledFor(logging.WARNING):
            return
        severity = level(code) if severity is None else severity
        title = CATALOG[code].title if code in CATALOG else code
        diagnostic = diagnostic_line(message)
        selected = ", ".join(format_path(path) for path in self.paths) or "chart"
        preview = "input not recorded"
        if values is not None:
            try:
                changes = changed_values(values, self.defaults)
                preview = "; ".join(
                    f"{compact(path, 100)} = {compact(json.dumps(value, ensure_ascii=True), 120)}"
                    for path, value in list(changes.items())[:4]
                )
                if not changes:
                    preview = "no changed overrides (chart defaults)"
                elif len(changes) > 4:
                    preview += f"; {len(changes) - 4} more changed paths"
            except (TypeError, ValueError):
                preview = "input preview unavailable; see artifacts"
        LOGGER.warning(
            "%s: chart=%s; path=%s; [%s] %s; severity=%s; %s; %s%s",
            stage,
            self.chart,
            compact(selected, 200),
            code,
            title,
            severity,
            compact(diagnostic),
            preview,
            f"; artifacts={self.artifacts}" if self.artifacts is not None else "",
            extra={
                "chart": self.chart,
                "finding_code": code,
                "finding_severity": severity,
                "value_paths": [list(path) for path in self.paths],
            },
        )


class WorkerLogFormatter(logging.Formatter):
    """
    Mark logging records so coordinators can distinguish them from raw child diagnostics.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Encode one complete record on one physical line for incremental reading.

        Args:
            record (logging.LogRecord): Worker event with optional finding context.

        Returns:
            str: Tagged JSON; embedded newlines never split the event.
        """
        return WORKER_PREFIX + json.dumps(
            {
                "name": record.name,
                "level": record.levelno,
                "message": record.getMessage(),
                **{
                    key: record.__dict__[key]
                    for key in ("chart", "finding_code", "value_paths", "diagnostic_key")
                    if key in record.__dict__
                },
            }
        )


@define
class WorkerLogs:
    """
    Forward new worker records exactly once without buffering complete logs in memory.

    Attributes:
        directory (Path): Queue directory containing per-worker diagnostic logs.
        workers (int): Number of worker log files to inspect.
        offsets (dict[int, int]): Byte position after the last complete line from each worker.
        diagnostics (set[str]): Compiler diagnostics already forwarded for this chart queue.
    """

    directory: Path
    workers: int
    offsets: dict[int, int] = field(factory=dict)
    diagnostics: set[str] = field(factory=set)

    def drain(self) -> None:
        """
        Relay complete INFO-or-higher records, retaining partial lines for the next poll.

        Returns:
            None: The coordinator's configured handlers receive live worker events.
        """
        for slot in range(self.workers):
            path = self.directory / f"worker-{slot}.log"
            if not path.is_file():
                continue
            with path.open("rb") as stream:
                stream.seek(self.offsets.get(slot, 0))
                while line := stream.readline():
                    if not line.endswith(b"\n"):
                        break
                    self.offsets[slot] = stream.tell()
                    if not line.startswith(WORKER_PREFIX.encode()):
                        continue
                    try:
                        record = json.loads(line[len(WORKER_PREFIX) :])
                    except (ValueError, UnicodeError):
                        continue
                    if not isinstance(record, dict) or not isinstance(record.get("message"), str):
                        continue
                    level = record.get("level")
                    if not isinstance(level, int) or not logging.INFO <= level <= logging.CRITICAL:
                        continue
                    diagnostic = record.get("diagnostic_key")
                    if isinstance(diagnostic, str):
                        if diagnostic in self.diagnostics:
                            continue
                        self.diagnostics.add(diagnostic)
                    name = str(record.get("name", ""))
                    logger = logging.getLogger(name if name.startswith("hypothesis_helm.") else "hypothesis_helm.workers")
                    logger.log(
                        level,
                        "%s",
                        record["message"],
                        extra={key: record[key] for key in ("chart", "finding_code", "value_paths", "diagnostic_key") if key in record},
                    )
