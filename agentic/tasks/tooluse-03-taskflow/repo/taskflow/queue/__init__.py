"""Queue backends used by the scheduler to hold pending jobs."""
from .memory import InMemoryQueue

__all__ = ["InMemoryQueue"]
