"""
Stop work at execution boundaries without treating cancellation as a test failure.
"""

__all__ = ("ChartUnavailable", "TimeLimitReached")


class ChartUnavailable(BaseException):
    """
    Abort testing when its source disappears, without shrinking an infrastructure failure.
    """


class TimeLimitReached(BaseException):
    """
    Stop execution without turning a budget deadline into a shrinking counterexample.
    """
