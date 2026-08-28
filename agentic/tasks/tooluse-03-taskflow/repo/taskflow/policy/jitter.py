"""Optional jitter for backoff delays.

Deterministic, seedable jitter so retries don't stampede. Off by default; the
engine only applies it when a RetryPolicy is constructed with jitter enabled.
This module never changes the *magnitude ceiling* of a delay — it only nudges a
delay that has already been computed (and capped) elsewhere.
"""
import random


def apply_jitter(delay, ratio=0.1, rng=None):
    """Return `delay` perturbed by up to +/- ratio, clamped to be non-negative."""
    if ratio <= 0:
        return delay
    r = rng or random
    span = delay * ratio
    out = delay + r.uniform(-span, span)
    return out if out > 0 else 0.0


def deterministic_rng(seed):
    return random.Random(seed)
