"""
Run a small heartbeat pipeline and export each dependency-graph rewrite.
"""

import argparse
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from threading import Event

from pipeline import BreadthFirst, Control, Outcome, Scheduler, ShutdownContract, Statistics, Work
from pipeline.gates import AND, NOT, OR, Signal

__all__ = ("Heartbeat", "main")


@dataclass
class Heartbeat:
    """
    Do no useful computation while reporting one healthy tick each second.

    Attributes:
        work (Work): Identity and prerequisites.
        after_tick (Callable[[], None] | None): Optional rewrite callback after the heartbeat.
    """

    work: Work
    after_tick: Callable[[], None] | None = None

    def run(self, control: Control, checkpoint: dict[str, object] | None) -> Outcome:
        """
        Wait cooperatively for one second and publish one healthy tick.

        Args:
            control (Control): Cancellation and progress channel.
            checkpoint (dict[str, object] | None): Unused because this example finishes each tick.

        Returns:
            Outcome: Completion after reporting health.
        """
        if control.cancel.wait(1):
            raise InterruptedError("heartbeat cancelled")
        print(f"{self.work.name}: healthy (1s)", flush=True)
        control.report(Statistics(1, 1))
        if self.after_tick is not None:
            self.after_tick()
        return Outcome()


def main() -> int:
    """
    Run the example in a fresh output directory.

    Returns:
        int: Zero after the pipeline completes.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(f".cache/pipeline/example-{time.time_ns()}"))
    options = parser.parse_args()
    healthy = Event()
    scheduler: Scheduler

    def rewrite() -> None:
        """
        Expand a chain to a fork-join graph while its root is active.

        Returns:
            None: Each acknowledged rewrite has a plot and an event.
        """
        healthy.set()
        scheduler.submit(
            [
                Heartbeat(Work("left", "v1", requires=("root",))),
                Heartbeat(Work("right", "v1", requires=("root",))),
                Heartbeat(Work("join", "v1", requires=("left",))),
                Heartbeat(Work("disabled", "v1", requires=("root",))),
            ]
        ).result(timeout=30)
        scheduler.dependencies("join", ("left", "right")).result(timeout=30)

    scheduler = Scheduler(
        [Heartbeat(Work("root", "v1"), rewrite)],
        slots=2,
        directory=options.output,
        policy=BreadthFirst(),
        diagrams=True,
        plots=True,
        routes={
            "left": AND(Signal("healthy"), NOT(Signal("maintenance"))),
            "right": OR(Signal("healthy"), Signal("override")),
            "disabled": Signal("maintenance"),
        },
        facts=lambda: {"healthy": healthy.is_set(), "maintenance": False, "override": False},
        shutdown=ShutdownContract(after_seconds=30, grace_seconds=2),
    )
    print(scheduler.run())
    print(f"Plots and rewrite journal: {options.output}")
    return 0
