"""
Verify progress output preserves the manifest channel.
"""

import pytest

from hypothesis_helm.reporting.display import start_progress


def test_progress_summary_uses_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Preserve partial counts and avoid terminal escape sequences in redirected output.

    Args:
        capsys (pytest.CaptureFixture[str]): Captured standard output and error streams.

    Returns:
        None: Progress is readable on stderr and stdout remains untouched.
    """
    progress, task = start_progress(3, 2)
    progress.update(task, advance=2, workers=1)
    progress.update(task, description="Interrupted")
    progress.stop()
    output = capsys.readouterr()
    assert output.out == ""
    assert "Interrupted" in output.err
    assert "2/3" in output.err
    assert "workers=1" in output.err
    assert "\x1b" not in output.err


def test_eta_uses_measured_completions(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Keep estimates unknown until timed completions establish a measured rate.

    Args:
        monkeypatch (pytest.MonkeyPatch): Substitute a deterministic progress clock.

    Returns:
        None: Remaining time is derived from completed work, not schema assumptions.
    """
    from functools import partial

    from rich.progress import Progress

    from hypothesis_helm.reporting import display

    clock = [0.0]
    monkeypatch.setattr(display, "Progress", partial(Progress, get_time=lambda: clock[0]))
    progress, task = start_progress(4, 1)
    try:
        assert progress.tasks[task].time_remaining is None
        clock[0] = 5.0
        progress.update(task, advance=1)
        clock[0] = 10.0
        progress.update(task, advance=1)
        assert progress.tasks[task].time_remaining == 10
    finally:
        progress.stop()
