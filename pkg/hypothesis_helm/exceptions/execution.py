"""
Stop work at execution boundaries without treating cancellation as a test failure.
"""


class TimeLimitReached(BaseException):
    """
    Stop execution without turning a budget deadline into a shrinking counterexample.
    """
