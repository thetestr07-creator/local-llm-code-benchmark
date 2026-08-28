"""Smoke test — passes on the current code.

Exercises registration, execution, event flow, the queue, the store, and a
retry sequence whose delays all stay comfortably *below* max_delay (so the cap
never has to engage). It does NOT probe what happens once the exponential curve
would exceed the configured maximum.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from taskflow import Engine, Job, RetryPolicy, register, get_task
from taskflow.core import registry
from taskflow.queue import InMemoryQueue
from taskflow.store import InMemoryStore
from taskflow.observe import EventBus
from taskflow.policy.decider import should_retry
from taskflow.policy.backoff import compute_delay

registry.clear()


@register("adder")
def _adder(a, b):
    return a + b

assert get_task("adder")(2, 3) == 5

# A job that fails twice then succeeds; delays 1, 2 stay under the 60s cap.
attempts = {"n": 0}

@register("flaky")
def _flaky():
    attempts["n"] += 1
    if attempts["n"] < 3:
        raise RuntimeError("transient")
    return "done"

eng = Engine(policy=RetryPolicy(max_attempts=5, base_delay=1.0, factor=2.0, max_delay=60.0))
eng.submit(Job("flaky", max_attempts=5))
res = eng.run()
assert res.ok and res.value == "done", res
assert res.attempts == 3, res.attempts
assert eng.events.count("job.retry") == 2

# Plain success path.
registry.clear()
@register("ok")
def _ok():
    return 42
eng2 = Engine()
eng2.submit(Job("ok"))
assert eng2.run().value == 42

# Distractor helpers behave.
assert should_retry(0, 3) is True
assert should_retry(3, 3) is False
# Small-attempt delays (uncapped region) are correct regardless of the bug.
assert compute_delay(0, base_delay=1.0, factor=2.0, max_delay=60.0) == 1.0
assert compute_delay(2, base_delay=1.0, factor=2.0, max_delay=60.0) == 4.0

q = InMemoryQueue()
j = Job("ok"); j.scheduled_at = 5.0
q.push(j)
assert len(q) == 1 and q.pop() is j

s = InMemoryStore()
s.record_attempt("x")
assert s.attempts("x") == 1

bus = EventBus()
seen = []
bus.subscribe("e", lambda p: seen.append(p))
bus.publish("e", {"v": 1})
assert seen == [{"v": 1}]

print("smoke OK")
