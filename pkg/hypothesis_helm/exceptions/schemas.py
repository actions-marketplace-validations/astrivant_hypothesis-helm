"""
Identify schema domains that cannot be safely enumerated.
"""

__all__ = ("NonFiniteSchema",)


class NonFiniteSchema(ValueError):
    """
    The schema cannot be safely enumerated within the requested limit.
    """
