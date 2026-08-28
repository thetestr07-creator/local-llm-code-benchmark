"""RetryPolicy facade.

Bundles the retry knobs and delegates the two sub-decisions:
    * eligibility  -> decider.should_retry
    * delay        -> backoff.compute_delay (optionally jittered)

The engine holds one RetryPolicy and asks it, after each failure, whether to
retry and (if so) how long to wait. The policy does not itself sleep or requeue.
"""
from .decider import should_retry
from .backoff import compute_delay
from .jitter import apply_jitter, deterministic_rng


class RetryPolicy:
    def __init__(self, max_attempts=3, base_delay=1.0, factor=2.0,
                 max_delay=60.0, permanent=(), jitter=0.0, seed=None):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.factor = factor
        self.max_delay = max_delay
        self.permanent = tuple(permanent)
        self.jitter = jitter
        self._rng = deterministic_rng(seed) if seed is not None else None

    def should_retry(self, attempt, error=None):
        return should_retry(attempt, self.max_attempts, error, self.permanent)

    def next_delay(self, attempt):
        """Seconds to wait before the retry numbered `attempt` (0-based)."""
        delay = compute_delay(attempt, self.base_delay, self.factor, self.max_delay)
        if self.jitter:
            delay = apply_jitter(delay, self.jitter, self._rng)
        return delay
