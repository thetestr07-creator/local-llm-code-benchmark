"""Persistence of job state/results. Distinct from queueing and retry logic."""
from .memory import InMemoryStore

__all__ = ["InMemoryStore"]
