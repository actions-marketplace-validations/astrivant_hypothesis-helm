"""
Continue an interrupted refresh from its journal while preserving earlier logs and results.
"""

import hashlib
import json
import os
import sys
import time
from pathlib import Path

from hypothesis_helm.environment import env
from hypothesis_helm.execution.runtime.processes import Processes
from hypothesis_helm.execution.runtime.signals import DeferredSignals, Termination
from hypothesis_helm.schemas.contracts import mapping, sequence
from pipeline import Operation, OperationQueue

__all__ = ("remaining", "resume")


def remaining(journal: Path) -> tuple[Operation, ...]:
    """
    Reconstruct unfinished operations and remove only verified completed prerequisites.

    Args:
        journal (Path): Original or continuation operations.json file.

    Returns:
        tuple[Operation, ...]: Remaining queue, including failed operations for retry.
    """
    records = [mapping(item) for item in sequence(mapping(json.loads(journal.read_text()))["operations"])]
    # A journal entry counts as satisfied only after completion, not merely after a process was started.
    completed = {
        str(item["name"])
        for item in records
        if item.get("status") == "completed" and (item.get("exit_code") == 0 or item.get("allow_failure") is True)
    }
    return tuple(
        Operation(
            name=str(item["name"]),
            command=tuple(str(part) for part in sequence(item["command"])),
            requires=tuple(str(name) for name in sequence(item["requires"]) if str(name) not in completed),
            exclusive=bool(item.get("exclusive", False)),
            allow_failure=bool(item.get("allow_failure", False)),
            timeout=float(str(item["timeout"])) if item.get("timeout") is not None else None,
        )
        for item in records
        if str(item["name"]) not in completed
    )


def resume(journal: Path, workers: int, *, dry_run: bool = False) -> None:
    """
    Verify measured sources and resume under the normal refresh ownership contract.

    Args:
        journal (Path): Previous operation journal; no earlier attempt is overwritten.
        workers (int): Maximum concurrent independent operations.
        dry_run (bool): Print the unfinished inventory without creating a new queue.

    Returns:
        None: Completion, or an exception retaining the new journal for another continuation.
    """
    from hypothesis_helm_benchmarking.refresh.cli import RefreshLock

    journal = journal.resolve()
    if journal.is_dir():
        journal /= "operations.json"
    operations = remaining(journal)
    root = next((path for path in journal.parents if (path / "measured-source-hashes.json").is_file()), None)
    if root is None:
        raise ValueError("Resume requires a prepared refresh workspace with measured-source-hashes.json")
    # Resume the measured implementation; mixing newer code into old measurements would invalidate the comparison.
    sources = mapping(json.loads((root / "measured-source-hashes.json").read_text()))
    for name, expected in sources.items():
        if hashlib.sha256((root / "frozen-source" / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Frozen measured source changed: {name}")
    if dry_run:
        print("Remaining operations: " + ", ".join(item.name for item in operations))
        return
    if not operations:
        print("This journal has no unfinished operations")
        return
    with RefreshLock(root.parent / "full-refresh.lock"):
        directory = root / f"resumed-{time.time_ns()}"
        environment = dict(env, MPLBACKEND="Agg")
        environment["PYTHONPATH"] = str(root / "frozen-source/pkg")
        environment["PATH"] = str(Path(sys.executable).parent) + os.pathsep + environment.get("PATH", "")
        queue = OperationQueue(
            operations,
            workers=workers,
            directory=directory,
            cwd=Path.cwd(),
            environment=environment,
            owner_factory=lambda: Processes(interrupt_grace=15.0),
            cancellation_scope=Termination,
            critical_scope=DeferredSignals,
            notify=lambda message: print(message, file=sys.stderr, flush=True),
        )
        print(f"Resume: {directory}; previous journal: {journal}", file=sys.stderr, flush=True)
        queue.run()
