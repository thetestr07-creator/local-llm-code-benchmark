"""HELD-OUT verification for multiedit-02. The model under test never sees this."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gwlib.clock import ManualClock
from gwlib.ratelimit import TokenBucket, RateLimiter
from gwlib.gateway import Gateway
from gwlib.router import Router
from gwlib.request import Request
from gwlib.handlers import ping

# ---- TokenBucket: starts full, drains, refuses when empty ----
clk = ManualClock(0.0)
b = TokenBucket(capacity=2, refill_per_sec=1.0, clock=clk)
assert b.tokens == 2, b.tokens
assert b.allow() is True          # 2 -> 1
assert b.allow() is True          # 1 -> 0
assert b.allow() is False         # empty, stays empty
assert abs(b.tokens - 0.0) < 1e-9, b.tokens

# ---- refill is time-based and capped at capacity ----
clk.advance(1)                    # +1 token
assert b.allow() is True          # 1 -> 0
assert b.allow() is False
clk.advance(10)                   # would be +10 but capped at capacity(2)
assert abs(b.tokens - 0.0) < 1e-9
assert b.allow() is True          # refill to 2, then 2 -> 1
assert abs(b.tokens - 1.0) < 1e-9, b.tokens

# ---- cost parameter ----
clk2 = ManualClock(0.0)
b2 = TokenBucket(capacity=5, refill_per_sec=0.0, clock=clk2)
assert b2.allow(cost=3) is True   # 5 -> 2
assert b2.allow(cost=3) is False  # only 2 left, unchanged
assert abs(b2.tokens - 2.0) < 1e-9, b2.tokens

# ---- validation ----
for bad_cap in (0, -1):
    try:
        TokenBucket(capacity=bad_cap, refill_per_sec=1.0, clock=ManualClock())
        raise AssertionError("TokenBucket accepted capacity=%r" % bad_cap)
    except ValueError:
        pass
try:
    TokenBucket(capacity=1, refill_per_sec=-0.5, clock=ManualClock())
    raise AssertionError("TokenBucket accepted negative refill")
except ValueError:
    pass
try:
    TokenBucket(capacity=1, refill_per_sec=1.0, clock=ManualClock()).allow(cost=0)
    raise AssertionError("allow accepted cost=0")
except ValueError:
    pass

# ---- RateLimiter: independent bucket per client ----
clk3 = ManualClock(0.0)
rl = RateLimiter(capacity=1, refill_per_sec=0.0, clock=clk3)
assert rl.check("alice") is True    # alice: 1 -> 0
assert rl.check("alice") is False   # alice empty
assert rl.check("bob") is True      # bob has his own full bucket

# ---- wired into Gateway.dispatch ----
clk4 = ManualClock(0.0)
router = Router()
router.register("ping", ping)
limiter = RateLimiter(capacity=1, refill_per_sec=0.0, clock=clk4)
gw = Gateway(router=router, clock=clk4, limiter=limiter)

r1 = gw.dispatch(Request("ping", client="c1"))
assert r1.status == 200 and r1.body == "pong", r1
r2 = gw.dispatch(Request("ping", client="c1"))   # c1 out of tokens
assert r2.status == 429, r2
assert r2.body == "rate limited", r2
# a different client is unaffected
r3 = gw.dispatch(Request("ping", client="c2"))
assert r3.status == 200, r3

# metrics: two calls for c1's route plus c2's -> 3 total "ping.calls";
# one ok is c1's first, plus c2's -> but count via explicit metrics
assert gw.metrics.get("route.ping.calls") == 3, gw.metrics.snapshot()
assert gw.metrics.get("route.limited") == 1, gw.metrics.snapshot()
assert gw.metrics.get("route.ok") == 2, gw.metrics.snapshot()

# ---- no limiter -> unchanged behaviour (backwards compatible) ----
gw2 = Gateway()
gw2.register("ping", ping)
assert gw2.limiter is None
for _ in range(5):
    assert gw2.dispatch(Request("ping", client="anyone")).status == 200
assert gw2.metrics.get("route.ok") == 5

print("HELDOUT_OK")
