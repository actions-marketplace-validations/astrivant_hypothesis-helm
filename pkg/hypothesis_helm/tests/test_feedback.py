"""
Verify adaptive throughput control against deterministic capacity curves.
"""

import pytest

from hypothesis_helm.execution.feedback import PID, ThroughputController


@pytest.mark.parametrize("initial", [1, 12])
def test_finds_and_tracks_throughput_peak(initial: int) -> None:
    """
    Approach an unknown throughput peak from either side and track a capacity change.

    Args:
        initial (int): Initial concurrency below or above the optimum.

    Returns:
        None: The controller settles around the current capacity optimum.
    """
    controller = ThroughputController(initial, 16, 0)
    for optimum in (4, 2):
        history = []
        for _ in range(100):
            workers = controller.limit
            history.append(workers)
            controller.sample(10 * workers / (1 + (workers / optimum) ** 2), 2)
        assert all(optimum - 1 <= workers <= optimum + 1 for workers in history[-20:])


def test_pid_bounds_and_reversal() -> None:
    """
    Avoid integral windup and reverse control when additional workers hurt throughput.

    Returns:
        None: Saturated feedback remains bounded and responds to a reversed gradient.
    """
    controller = PID()
    for _ in range(100):
        assert controller.step(1.0, 10) == 1
    assert abs(controller.integral) <= 1
    assert controller.step(-1.0, 10) < 0


def test_completion_windows_and_draining() -> None:
    """
    Ignore drain periods and simultaneous completions as evidence of capacity loss.

    Returns:
        None: Only populated windows at the target concurrency update throughput.
    """
    controller = ThroughputController(2, 8, 0)
    assert controller.completed(0, 2, True) == 2
    assert controller.completed(0, 2, True) == 2
    assert controller.throughput == 0
    assert controller.completed(1, 2, True) == 3
    rate = controller.throughput
    assert controller.completed(2, 2, True) == 3
    assert controller.completed(3, 3, False) == 3
    assert controller.throughput == rate


def test_boundaries_and_single_worker() -> None:
    """
    Respect actuator bounds even when throughput keeps increasing.

    Returns:
        None: Exploration stays within configured limits.
    """
    controller = ThroughputController(1, 4, 0)
    history = []
    for _ in range(40):
        history.append(controller.limit)
        controller.sample(float(controller.limit), 1)
    assert max(history) == 4
    assert min(history) >= 1
    single = ThroughputController(1, 1, 0)
    for _ in range(10):
        assert single.sample(1.0, 1) == 1
