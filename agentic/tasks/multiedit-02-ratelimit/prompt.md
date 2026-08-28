Add per-client **rate limiting** to `gwlib`, using a token-bucket algorithm.

## 1. New module `gwlib/ratelimit.py`

Create a class `TokenBucket` with this exact behaviour:

- `TokenBucket(capacity, refill_per_sec, clock)`
  - `capacity`: the maximum number of tokens the bucket can hold (a positive number).
  - `refill_per_sec`: how many tokens are added per second (a non-negative number).
  - `clock`: an object with a `now()` method returning seconds (as in `gwlib/clock.py`).
  - The bucket starts **full** (`capacity` tokens).
  - Raise `ValueError` if `capacity <= 0` or `refill_per_sec < 0`.

- `TokenBucket.allow(cost=1)`
  - First, refill: add `refill_per_sec * elapsed` tokens, where `elapsed` is the time
    since the last refill according to `clock.now()`; cap the total at `capacity`.
  - Then, if the bucket holds **at least** `cost` tokens, subtract `cost` and return `True`.
    Otherwise leave the tokens unchanged and return `False`.
  - `cost` defaults to 1 and must be a positive number; raise `ValueError` if `cost <= 0`.
  - `tokens` (a float attribute) must reflect the current token count after each call.

Also create a class `RateLimiter` that manages **one bucket per client**:

- `RateLimiter(capacity, refill_per_sec, clock)` — stores the config and clock; buckets are
  created lazily.
- `RateLimiter.check(client, cost=1)` — returns the result of `allow(cost)` on that client's
  bucket, creating the bucket (full) on first use. Each distinct `client` string gets its own
  independent bucket.

## 2. Wire it into `gwlib/gateway.py`

- `Gateway.__init__` gains a new **optional** keyword argument `limiter=None`. Keep all existing
  arguments (`router`, `metrics`, `clock`) and their order/defaults unchanged. Store it as
  `self.limiter`.
- In `Gateway.dispatch`, **after** counting the call (`route.<name>.calls`) but **before**
  resolving the route, if `self.limiter` is not `None`, call
  `self.limiter.check(request.client)`. If it returns `False`, do **not** run the handler;
  increment the metric `"route.limited"` and return `Response(429, "rate limited")`.
  If it returns `True` (or there is no limiter), proceed exactly as before.

Order of metrics for one dispatch that is rate-limited: `route.<name>.calls` then `route.limited`
(and no `route.ok`/`route.error`/`route.unknown`).

## Constraints

- Do not change existing public signatures of `Router`, `Metrics`, `Request`, `Response`, or the
  existing behaviour of `dispatch` when no limiter is configured.
- Keep the library importable and `python3 tests/test_smoke.py` passing.
- Pure standard library only.
