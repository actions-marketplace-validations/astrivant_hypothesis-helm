"""
Identify schema domains that cannot be safely enumerated.
"""


class NonFiniteSchema(ValueError):
    """
    The schema cannot be safely enumerated within the requested limit.
    """
