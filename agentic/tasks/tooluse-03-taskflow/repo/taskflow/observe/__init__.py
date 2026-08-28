"""Observability: an event bus and lightweight middleware hooks the engine
emits to. Purely for logging/metrics; never influences scheduling decisions."""
from .events import EventBus

__all__ = ["EventBus"]
