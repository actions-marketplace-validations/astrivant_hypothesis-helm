"""
Share schema models and paths across configuration, generation, and Kubernetes validation.

Keep common JSON boundaries, the values model, and path inspection at this level.
Use configuration for user policy, generation for candidate inputs, and kubernetes
for downstream resource schemas and manifest validation.
"""

__all__ = ()
