"""
Verify progress output preserves the manifest channel.
"""

import pytest

from hypothesis_helm.display import start_progress


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
