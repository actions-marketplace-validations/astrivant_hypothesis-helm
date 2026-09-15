"""
Balance cooperative workloads without releasing resources before checkpoint completion.
"""

import json
import re
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from queue import Empty, SimpleQueue
from threading import Event, Lock
from typing import cast

from workgraph.gates import Gate
from workgraph.shutdown import ShutdownContract, ShutdownState
from workgraph.workloads import Control, Estimate, Outcome, Statistics, Work, Workload

from workbalance import checkpoints
from workbalance.policy import ShortestRemaining


@dataclass
class State:
    """
    Keep coordinator-owned progress and lifecycle state separate from workload code.

    Attributes:
        unit (Workload): Cooperative implementation.
        work (Work): Immutable scheduling description.
        statistics (Statistics): Latest cumulative progress.
        waiting_since (float): Monotonic time the current wait began.
        status (str): Pending, running, pausing, paused, completed, failed or cancelled.
        checkpoint (dict[str, object] | None): Verified resume payload.
        rate (float | None): Smoothed completed units per second.
        observed_at (float): Time of previous progress observation.
        observed_completed (int): Units at previous observation.
    """

    unit: Workload
    work: Work
    statistics: Statistics
    waiting_since: float
    status: str = "pending"
    checkpoint: dict[str, object] | None = None
    rate: float | None = None
    observed_at: float = 0
    observed_completed: int = 0


class Scheduler:
    """
    Own a single resource pool, mutable dependency graph, event log and cooperative workers.
    """

    def __init__(
        self,
        units: Sequence[Workload],
        *,
        slots: int,
        directory: Path,
        memory_bytes: int | None = None,
        policy: ShortestRemaining | None = None,
        diagrams: bool = False,
        plots: bool = False,
        routes: Mapping[str, Gate] | None = None,
        facts: Callable[[], Mapping[str, bool]] | None = None,
        restore: bool = False,
        shutdown: ShutdownContract | None = None,
        notify: Callable[[str], None] = print,
    ) -> None:
        """
        Validate initial work before creating any workers.

        Args:
            units (Sequence[Workload]): Initial dependency graph.
            slots (int): Total resource slots, including nested workload parallelism.
            directory (Path): Exclusive scheduler journal and checkpoint directory.
            memory_bytes (int | None): Optional memory reservation budget.
            policy (ShortestRemaining | None): Ready-work ordering and preemption policy.
            diagrams (bool): Write Mermaid snapshots when graph or lifecycle state changes.
            plots (bool): Save matplotlib PNG snapshots on graph creation and rewrites.
            routes (Mapping[str, Gate] | None): Boolean admission rules keyed by workload name.
            facts (Callable[[], Mapping[str, bool]] | None): Coordinator callback supplying current Boolean observations.
            restore (bool): Restore compatible paused checkpoints from a previous scheduler.
            shutdown (ShutdownContract | None): Conditions and grace period for cooperative graph shutdown.
            notify (Callable[[str], None]): Human-readable coordinator event sink.
        """
        if slots < 1 or (memory_bytes is not None and memory_bytes < 0):
            raise ValueError("invalid resource capacity")
        self.slots, self.memory_bytes = slots, memory_bytes
        self.directory, self.policy = directory, policy or ShortestRemaining()
        self.diagrams, self.restore, self.notify = diagrams, restore, notify
        self.plots, self.routes, self.facts = plots, dict(routes or {}), facts or dict
        self.states: dict[str, State] = {}
        self.active: dict[str, tuple[Future[Outcome], Control, float]] = {}
        self.messages: SimpleQueue[tuple[str, object]] = SimpleQueue()
        self.events: SimpleQueue[tuple[str, Statistics, float]] = SimpleQueue()
        self.cancelled = Event()
        self.shutdown_contract = shutdown or ShutdownContract()
        self.shutdown_reason: str | None = None
        self.shutdown_started: float | None = None
        self.inbox_lock = Lock()
        self.closed = False
        self.sequence = 0
        self.parent_control: Control | None = None
        self._insert(units)

    def _validate(self, works: dict[str, Work]) -> None:
        """
        Validate resource bounds, names and acyclic dependencies.

        Args:
            works (dict[str, Work]): Proposed complete graph.

        Returns:
            None: Invalid graphs raise before mutation.
        """
        resolved: set[str] = set()
        for work in works.values():
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", work.name) or not work.fingerprint:
                raise ValueError("work requires a safe name and input fingerprint")
            if work.slots < 1 or work.slots > self.slots or work.memory_bytes < 0:
                raise ValueError(f"invalid resource reservation: {work.name}")
            if self.memory_bytes is not None and work.memory_bytes > self.memory_bytes:
                raise ValueError(f"work exceeds memory capacity: {work.name}")
            if set(work.requires) - works.keys():
                raise ValueError(f"unknown prerequisite: {work.name}")
        while len(resolved) < len(works):
            ready = {name for name, work in works.items() if set(work.requires) <= resolved} - resolved
            if not ready:
                raise ValueError("work dependencies contain a cycle")
            resolved.update(ready)

    def _insert(self, units: Sequence[Workload]) -> None:
        """
        Commit a validated batch without partially mutating the graph on rejection.

        Args:
            units (Sequence[Workload]): New workload implementations.

        Returns:
            None: All validated additions become visible together.
        """
        works = {name: state.work for name, state in self.states.items()}
        for unit in units:
            if unit.work.name in works:
                raise ValueError(f"duplicate work: {unit.work.name}")
            works[unit.work.name] = unit.work
        self._validate(works)
        additions = {}
        for unit in units:
            work = unit.work
            restored = checkpoints.load(self.directory / "checkpoints", work) if self.restore and work.resumable else None
            payload, stats = restored if restored else (None, work.statistics)
            additions[work.name] = State(unit, work, stats, time.monotonic(), checkpoint=payload)
        self.states.update(additions)

    def submit(self, units: Sequence[Workload]) -> Future[None]:
        """
        Request an atomic graph extension from any thread.

        Args:
            units (Sequence[Workload]): New work, whose dependencies may refer to this batch or existing work.

        Returns:
            Future[None]: Coordinator acknowledgement, or the validation error.
        """
        acknowledgement: Future[None] = Future()
        with self.inbox_lock:
            if self.closed:
                acknowledgement.set_exception(RuntimeError("scheduler stopped"))
            else:
                self.messages.put(("add", (tuple(units), acknowledgement)))
        return acknowledgement

    def dependencies(self, name: str, requires: tuple[str, ...]) -> Future[None]:
        """
        Request dependency changes for work that has not started.

        Args:
            name (str): Pending workload to rewire.
            requires (tuple[str, ...]): New prerequisites.

        Returns:
            Future[None]: Coordinator acknowledgement after cycle and lifecycle validation.
        """
        acknowledgement: Future[None] = Future()
        with self.inbox_lock:
            if self.closed:
                acknowledgement.set_exception(RuntimeError("scheduler stopped"))
            else:
                self.messages.put(("dependencies", (name, requires, acknowledgement)))
        return acknowledgement

    def cancel(self) -> None:
        """
        Request cancellation; workers must cooperate and release their owned resources.

        Returns:
            None: The cancellation event wakes the coordinator.
        """
        self.cancelled.set()

    def _emit(self, kind: str, **detail: object) -> None:
        """
        Write ordered events and optional diagrams from the coordinator only.

        Args:
            kind (str): Event category.
            **detail (object): JSON-compatible event attributes.

        Returns:
            None: Journal and optional graph snapshots are updated.
        """
        self.sequence += 1
        event = {"sequence": self.sequence, "epoch": time.time(), "event": kind, **detail}
        with (self.directory / "events.jsonl").open("a") as stream:
            stream.write(json.dumps(event, allow_nan=False) + "\n")
        if kind != "statistics":
            self.notify(f"[workbalance] {kind}: {json.dumps(detail)}")
        records = {
            name: {"status": state.status, "work": asdict(state.work), "statistics": asdict(state.statistics)}
            for name, state in self.states.items()
        }
        temporary = self.directory / "state.json.pending"
        temporary.write_text(json.dumps(records, indent=2) + "\n")
        temporary.replace(self.directory / "state.json")
        if self.parent_control is not None:
            unfinished = [state for state in self.states.values() if state.status not in {"completed", "skipped"}]
            estimates = [state.statistics.estimate for state in unfinished]
            remaining = [estimate.remaining_seconds for estimate in estimates]
            self.parent_control.report(
                Statistics(
                    len(self.states) - len(unfinished),
                    len(self.states),
                    Estimate(
                        remaining_seconds=sum(value for value in remaining if value is not None)
                        if all(value is not None for value in remaining)
                        else None,
                        uncertainty_seconds=sum(estimate.uncertainty_seconds for estimate in estimates),
                    ),
                )
            )
        if self.diagrams and kind != "statistics":
            nodes = {name: f"n{index}" for index, name in enumerate(self.states)}
            lines = ["flowchart TD"]
            for name, state in self.states.items():
                lines.append(f'    {nodes[name]}["{name}: {state.status}"]')
                lines.extend(f"    {nodes[parent]} --> {nodes[name]}" for parent in state.work.requires)
            (self.directory / f"graph-{self.sequence:06d}.mmd").write_text("\n".join(lines) + "\n")

        if self.plots and kind in {"graph_created", "graph_changed"}:
            from workbalance.plotting import plot_graph

            plot_graph(
                {name: state.work for name, state in self.states.items()},
                self.directory / f"graph-{self.sequence:06d}.png",
                title=f"{kind}: revision {self.sequence}",
            )

    def _route(self, ready: list[str]) -> list[str]:
        """
        Decide admission once prerequisites have completed.

        Args:
            ready (list[str]): Otherwise eligible units.

        Returns:
            list[str]: Units with satisfied or absent routing conditions.
        """
        facts = dict(self.facts())
        admitted = []
        for name in ready:
            gate = self.routes.get(name)
            decision = True if gate is None or self.states[name].status == "paused" else gate.evaluate(facts)
            if decision is True:
                admitted.append(name)
            elif decision is False:
                self.states[name].status = "skipped"
                self._emit("route_skipped", work=name, rule=asdict(gate) if gate is not None else None, facts=facts)
        return admitted

    def _messages(self) -> None:
        """
        Process graph requests atomically and resolve every acknowledgement.

        Returns:
            None: Requests receive success or their validation error.
        """
        while True:
            try:
                kind, payload = self.messages.get_nowait()
            except Empty:
                break
            if kind == "add":
                units, acknowledgement = cast(tuple[tuple[Workload, ...], Future[None]], payload)
                try:
                    self._insert(units)
                    self._emit("graph_changed", added=[unit.work.name for unit in units])
                except Exception as error:
                    acknowledgement.set_exception(error)
                else:
                    acknowledgement.set_result(None)
            else:
                name, requires, acknowledgement = cast(tuple[str, tuple[str, ...], Future[None]], payload)
                try:
                    state = self.states[name]
                    if state.status != "pending" or state.checkpoint is not None:
                        raise ValueError("only unstarted work can change prerequisites")
                    work = replace(state.work, requires=requires)
                    self._validate({key: work if key == name else item.work for key, item in self.states.items()})
                    old = state.work.requires
                    state.work = work
                    self._emit("graph_changed", work=name, removed_edges=list(old), added_edges=list(requires))
                except Exception as error:
                    acknowledgement.set_exception(error)
                else:
                    acknowledgement.set_result(None)

    def _progress(self) -> None:
        """
        Update smoothed throughput and remaining-time estimates from worker observations.

        Returns:
            None: Latest progress and estimates are journaled.
        """
        while True:
            try:
                name, stats, now = self.events.get_nowait()
            except Empty:
                break
            state = self.states[name]
            if stats.completed < state.statistics.completed:
                raise ValueError(f"progress moved backwards: {name}")
            elapsed, completed = now - state.observed_at, stats.completed - state.observed_completed
            if elapsed > 0 and completed > 0:
                rate = completed / elapsed
                state.rate = rate if state.rate is None else 0.3 * rate + 0.7 * state.rate
            estimate = stats.estimate
            if state.rate and stats.total is not None and estimate.remaining_seconds is None:
                estimate = replace(estimate, remaining_seconds=(stats.total - stats.completed) / state.rate)
            state.statistics = replace(stats, estimate=estimate)
            if completed > 0:
                state.observed_at, state.observed_completed = now, stats.completed
            self._emit("statistics", work=name, progress=asdict(state.statistics))

    def _control(self, name: str) -> Control:
        """
        Bind progress events to a stable workload identity.

        Args:
            name (str): Workload identity.

        Returns:
            Control: Cooperative events and a bound progress sink.
        """

        def report(stats: Statistics) -> None:
            """
            Queue an immutable progress observation.

            Args:
                stats (Statistics): New cumulative progress.

            Returns:
                None: Observation enters the coordinator queue.
            """
            self.events.put((name, stats, time.monotonic()))

        return Control(Event(), Event(), report)

    def _fits(self, work: Work) -> bool:
        """
        Count running and pausing reservations until their workers actually return.

        Args:
            work (Work): Candidate reservation.

        Returns:
            bool: Whether the remaining capacity can host this workload.
        """
        used = [self.states[name].work for name in self.active]
        return sum(item.slots for item in used) + work.slots <= self.slots and (
            self.memory_bytes is None or sum(item.memory_bytes for item in used) + work.memory_bytes <= self.memory_bytes
        )

    def _finalize(self, activated: float) -> None:
        """
        Hold the graph boundary until every named finalizer acknowledges durable cleanup.

        Args:
            activated (float): Monotonic activation timestamp for finalizer observations.

        Returns:
            None: All finalizers have acknowledged completion; failures remain pending and are retried.
        """
        pending = list(self.shutdown_contract.finalizers)
        for finalizer in pending:
            self._emit("finalizer_pending", finalizer=finalizer.name)
        while pending:
            observation = ShutdownState(
                time.monotonic() - activated,
                sum(state.status == "completed" for state in self.states.values()),
                len(self.states),
                sum(state.statistics.completed for state in self.states.values()),
            )
            for finalizer in tuple(pending):
                try:
                    complete = finalizer.finish(observation)
                except Exception as error:
                    self._emit("finalizer_failed", finalizer=finalizer.name, error=str(error))
                    continue
                if complete:
                    pending.remove(finalizer)
                    self._emit("finalizer_completed", finalizer=finalizer.name)
            if pending:
                time.sleep(self.shutdown_contract.finalizer_retry_seconds)

    def run(self, control: Control | None = None) -> dict[str, str]:
        """
        Run the graph to completion or a parent-requested quiescent checkpoint boundary.

        Args:
            control (Control | None): Parent graph pause, cancellation and progress channel.

        Returns:
            dict[str, str]: Final per-workload statuses.

        Raises:
            RuntimeError: A workload violates its checkpoint contract.
            InterruptedError: Cancellation was requested.
        """
        self.parent_control = control
        self.directory.mkdir(parents=True, exist_ok=True)
        lock = self.directory / "scheduler.lock"
        lock.mkdir()
        pool: ThreadPoolExecutor | None = None
        activated = time.monotonic()
        paused_by_parent = False
        finalized = True
        try:
            events_path = self.directory / "events.jsonl"
            if events_path.exists():
                if not self.restore:
                    raise ValueError("scheduler directory already has history; use restore=True or a new directory")
                for line in events_path.read_text().splitlines():
                    self.sequence = max(self.sequence, int(json.loads(line)["sequence"]))
            pool = ThreadPoolExecutor(max_workers=self.slots, thread_name_prefix="workbalance")
            self._emit("graph_created", nodes=list(self.states))
            last_order: list[str] = []
            activated = time.monotonic()
            while True:
                self._messages()
                self._progress()
                for name, (future, control, _started) in tuple(self.active.items()):
                    if not future.done():
                        continue
                    state = self.states[name]
                    try:
                        outcome = future.result()
                        self._progress()
                        if outcome.checkpoint is not None:
                            if not state.work.resumable or not control.pause.is_set():
                                raise RuntimeError("unexpected checkpoint without a cooperative pause request")
                            checkpoints.save(self.directory / "checkpoints", state.work, outcome.checkpoint, state.statistics)
                            state.checkpoint = outcome.checkpoint
                            state.status, state.waiting_since = "paused", time.monotonic()
                            self._emit("checkpoint_committed", work=name)
                        else:
                            state.status = "cancelled" if control.cancel.is_set() else "completed"
                            if state.status == "completed":
                                (self.directory / "checkpoints" / f"{name}.json").unlink(missing_ok=True)
                            self._emit(state.status, work=name)
                    except InterruptedError:
                        if self.shutdown_started is None:
                            raise
                        state.status = "cancelled"
                        self._emit("cancelled", work=name, reason=self.shutdown_reason)
                    except BaseException:
                        state.status = "failed"
                        self._emit("failed", work=name)
                        raise
                    del self.active[name]
                if self.parent_control is not None and self.parent_control.cancel.is_set():
                    raise InterruptedError("parent graph cancelled")
                observation = ShutdownState(
                    time.monotonic() - activated,
                    sum(state.status == "completed" for state in self.states.values()),
                    len(self.states),
                    sum(state.statistics.completed for state in self.states.values()),
                )
                reason = self.shutdown_contract.reason(observation, self.cancelled.is_set())
                if self.shutdown_started is None and reason is not None:
                    self.shutdown_started, self.shutdown_reason = time.monotonic(), reason
                    self._emit("shutdown_started", reason=reason, grace_seconds=self.shutdown_contract.grace_seconds)
                if self.shutdown_started is not None:
                    expired = time.monotonic() - self.shutdown_started >= self.shutdown_contract.grace_seconds
                    for name, (_, child_control, _) in self.active.items():
                        if self.shutdown_contract.checkpoint and self.states[name].work.resumable and not child_control.pause.is_set():
                            child_control.pause.set()
                            self.states[name].status = "pausing"
                            self._emit("pause_requested", work=name, reason="shutdown contract")
                        if expired and not child_control.cancel.is_set():
                            child_control.cancel.set()
                            self._emit("cancellation_requested", work=name, reason="shutdown grace period expired")
                    if not self.active:
                        for state in self.states.values():
                            if state.status == "pending":
                                state.status = "blocked"
                        break
                    time.sleep(0.02)
                    continue
                if self.parent_control is not None and self.parent_control.pause.is_set():
                    for name, (_, child_control, _) in self.active.items():
                        if self.states[name].work.resumable and not child_control.pause.is_set():
                            child_control.pause.set()
                            self.states[name].status = "pausing"
                            self._emit("pause_requested", work=name, reason="parent graph requested pause")
                    if not self.active:
                        paused_by_parent = True
                        self._emit("graph_paused")
                        break
                    self.cancelled.wait(0.02)
                    continue
                completed = {name for name, state in self.states.items() if state.status == "completed"}
                now = time.monotonic()
                ready = [
                    name
                    for name, state in self.states.items()
                    if state.status in {"pending", "paused"} and set(state.work.requires) <= completed
                ]
                for name, state in self.states.items():
                    if state.status == "pending" and any(self.states[parent].status == "skipped" for parent in state.work.requires):
                        state.status = "skipped"
                        self._emit("route_skipped", work=name, reason="prerequisite skipped")
                ready = self._route(ready)
                order = self.policy.priorities({name: state.work for name, state in self.states.items()})
                ready.sort(
                    key=lambda name: self.policy.rank(
                        self.states[name].statistics.estimate, now - self.states[name].waiting_since, order[name]
                    )
                )
                if ready != last_order:
                    self._emit("schedule_changed", previous=last_order, ready=ready)
                    last_order = list(ready)
                for name in ready:
                    state = self.states[name]
                    if self._fits(state.work):
                        control = self._control(name)
                        state.observed_at, state.observed_completed = now, state.statistics.completed
                        resumed = state.checkpoint is not None
                        state.status = "running"
                        future = pool.submit(state.unit.run, control, state.checkpoint)
                        self.active[name] = (future, control, now)
                        self._emit("resumed" if resumed else "started", work=name, estimate=asdict(state.statistics.estimate))
                    else:
                        for other, (_, control, started) in self.active.items():
                            victim = self.states[other]
                            if (
                                victim.work.resumable
                                and not control.pause.is_set()
                                and self.policy.preempt(
                                    victim.statistics.estimate, state.statistics.estimate, now - started, now - state.waiting_since
                                )
                            ):
                                control.pause.set()
                                victim.status = "pausing"
                                self._emit("pause_requested", work=other, waiting_for=name)
                                break
                if not self.active and all(state.status in {"completed", "skipped"} for state in self.states.values()):
                    with self.inbox_lock:
                        if self.messages.empty():
                            self.closed = True
                            break
                self.cancelled.wait(0.02)
            return {name: state.status for name, state in self.states.items()}
        finally:
            with self.inbox_lock:
                self.closed = True
                while not self.messages.empty():
                    _, payload = self.messages.get_nowait()
                    acknowledgement = cast(tuple[object, ...], payload)[-1]
                    cast(Future[None], acknowledgement).set_exception(RuntimeError("scheduler stopped"))
            for _, control, _ in self.active.values():
                control.cancel.set()
            if pool is not None:
                pool.shutdown(wait=True, cancel_futures=True)
            for name in self.active:
                if self.states[name].status != "failed":
                    self.states[name].status = "cancelled"
            try:
                if pool is not None:
                    if not paused_by_parent:
                        finalized = False
                        self._finalize(activated)
                        finalized = True
                    if self.shutdown_started is not None:
                        self._emit("shutdown_completed", reason=self.shutdown_reason)
                    self._emit("scheduler_stopped")
            finally:
                if finalized:
                    lock.rmdir()
