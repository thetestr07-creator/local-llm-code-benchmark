"""taskflow — a small in-process task/job engine.

A job is registered with a name, submitted to the engine, and executed by a
worker. If it raises, the engine consults a retry policy to decide whether and
when to run it again, using exponential backoff bounded by a configurable cap.

Public surface:
    Engine, Job, JobResult          (core)
    RetryPolicy                     (policy)
    register, get_task              (core.registry)
"""
from .core.engine import Engine
from .core.job import Job, JobResult
from .core.registry import register, get_task
from .policy.retry import RetryPolicy

__all__ = ["Engine", "Job", "JobResult", "register", "get_task", "RetryPolicy"]
