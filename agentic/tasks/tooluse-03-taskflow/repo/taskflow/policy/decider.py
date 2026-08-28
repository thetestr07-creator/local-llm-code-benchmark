"""Decide whether a failed job is *eligible* for another attempt.

This answers the yes/no question ("should we retry?"), which is separate from
the how-long question (backoff.py). Eligibility is based on the attempt count
and an optional set of exception types considered permanent (never retried).
"""


def should_retry(attempt, max_attempts, error=None, permanent=()):
    """True if another attempt is allowed.

    `attempt` is the number of attempts already completed. A job may run at most
    `max_attempts` times total, so a retry is allowed while attempt < max_attempts.
    Errors whose type is in `permanent` are never retried.
    """
    if error is not None and isinstance(error, tuple(permanent)) and permanent:
        return False
    return attempt < max_attempts


def attempts_remaining(attempt, max_attempts):
    return max(0, max_attempts - attempt)
