"""
Render test progress on stderr without capturing the manifest stream.
"""

from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def start_progress(total: int, workers: int) -> tuple[Progress, TaskID]:
    """
    Start a terminal progress bar, or a final-only summary for redirected output.

    Args:
        total (int): Number of selected properties.
        workers (int): Initial worker target.

    Returns:
        tuple[Progress, TaskID]: Live display and its test task identifier.
    """
    progress = Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("workers={task.fields[workers]}"),
        TimeElapsedColumn(),
        TextColumn("ETA"),
        TimeRemainingColumn(),
        console=Console(stderr=True),
        auto_refresh=False,
        redirect_stdout=False,
        redirect_stderr=False,
    )
    task = progress.add_task("Tests", total=total, workers=workers)
    progress.start()
    return progress, task
