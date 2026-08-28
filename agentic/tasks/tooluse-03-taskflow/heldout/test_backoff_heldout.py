"""HELD-OUT verification for tooluse-03. The model never sees this."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from taskflow import Engine, Job, RetryPolicy, register
from taskflow.core import registry
from taskflow.policy.backoff import compute_delay, schedule

# --- direct: the exponential curve must flatten at max_delay ---
delays = [compute_delay(a, base_delay=1.0, factor=2.0, max_delay=30.0) for a in range(9)]
assert delays == [1, 2, 4, 8, 16, 30, 30, 30, 30], "backoff not capped: %r" % (delays,)

# below-cap region unchanged
assert compute_delay(0, 1.0, 2.0, 30.0) == 1.0
assert compute_delay(3, 1.0, 2.0, 30.0) == 8.0

# a tiny cap engages immediately
assert compute_delay(5, base_delay=1.0, factor=2.0, max_delay=3.0) == 3.0

# schedule() reflects the cap too
assert schedule(7, base_delay=1.0, factor=2.0, max_delay=10.0) == [1, 2, 4, 8, 10, 10, 10]

# --- through the policy facade ---
pol = RetryPolicy(max_attempts=10, base_delay=1.0, factor=2.0, max_delay=30.0)
assert [pol.next_delay(a) for a in range(9)] == [1, 2, 4, 8, 16, 30, 30, 30, 30]

# --- end-to-end: the engine's scheduled timeline must respect the cap ---
registry.clear()

@register("always_fails")
def _always():
    raise RuntimeError("boom")

eng = Engine(policy=RetryPolicy(max_attempts=8, base_delay=1.0, factor=2.0, max_delay=30.0))
eng.submit(Job("always_fails", max_attempts=8))
result = eng.run()

# It ultimately fails after exhausting attempts. With max_attempts=8 the job
# runs once, then is retried while attempt < 8, i.e. 8 retries -> 9 executions.
assert result is not None and result.ok is False
assert result.attempts == 9, result.attempts

# scheduled_at is cumulative virtual time; consecutive diffs are the delays
# actually scheduled between the 9 executions, and none may exceed max_delay.
times = [t for (_name, _attempt, t) in eng.timeline]
assert times[0] == 0.0
diffs = [round(times[i + 1] - times[i], 6) for i in range(len(times) - 1)]
assert diffs == [1, 2, 4, 8, 16, 30, 30, 30], "engine scheduled uncapped delays: %r" % (diffs,)
assert max(diffs) <= 30.0

print("HELDOUT_OK")
