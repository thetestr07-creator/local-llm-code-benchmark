# taskflow

A small in-process task/job engine with retries and exponential backoff.

Register a task, submit a job, and let the engine run it. If the task raises,
the engine retries it according to a **retry policy**: exponential backoff
(`base_delay * factor ** attempt`) bounded above by a configurable `max_delay`
cap, so a single wait never exceeds the ceiling no matter how many times the job
has failed.

```python
from taskflow import Engine, Job, RetryPolicy, register

@register("flaky")
def flaky():
    ...

engine = Engine(policy=RetryPolicy(max_attempts=6, base_delay=1, factor=2, max_delay=30))
engine.submit(Job("flaky", max_attempts=6))
result = engine.run()
```

Package layout:

- `taskflow/core/`    — `engine`, `scheduler`, `executor`, `registry`, `job`, `clock`
- `taskflow/policy/`  — `retry` (facade), `backoff`, `decider`, `jitter`
- `taskflow/queue/`   — in-memory priority queue backends
- `taskflow/observe/` — event bus + middleware
- `taskflow/store/`   — result/attempt store

The engine uses a **virtual clock**, so retries don't really sleep — time jumps
forward to each job's scheduled time, making runs deterministic.

Run the smoke test with `python3 tests/test_smoke.py`.
