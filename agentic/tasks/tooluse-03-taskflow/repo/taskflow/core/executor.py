"""Execute a single job attempt.

The executor looks the task up in the registry, runs it with the job's args,
and reports back an outcome tuple (ok, value_or_error). It does NOT decide
whether to retry or how long to wait — that is the scheduler's job, informed by
the retry policy. Keeping execution and retry policy separate is deliberate.
"""
from .registry import get_task


class Outcome:
    __slots__ = ("ok", "value", "error")

    def __init__(self, ok, value=None, error=None):
        self.ok = ok
        self.value = value
        self.error = error


class Executor:
    def __init__(self, middlewares=None):
        self._middlewares = list(middlewares or [])

    def run_once(self, job):
        fn = get_task(job.name)
        call = fn
        for mw in reversed(self._middlewares):
            call = mw(call)
        try:
            value = call(*job.args, **job.kwargs)
            return Outcome(True, value=value)
        except Exception as e:  # noqa: BLE001 - report all failures to scheduler
            return Outcome(False, error=e)
