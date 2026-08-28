Operators report that when a job keeps failing, the wait between retries grows
without bound instead of leveling off at the configured maximum.

The retry system is meant to use exponential backoff that is *capped*: the delay
before an attempt should be `base_delay * factor ** attempt`, but never more than
`max_delay`. For example, with `base_delay=1`, `factor=2`, `max_delay=30`, the
per-attempt delays should be `1, 2, 4, 8, 16, 30, 30, 30, ...` — flattening once
they hit the cap. Instead they keep doubling (`1, 2, 4, 8, 16, 32, 64, ...`),
which after enough failures schedules absurdly long waits.

Retries that stay below the cap already behave correctly, so short retry
sequences look fine; the problem only shows once the exponential value would
exceed `max_delay`.

Trace how a retry delay is produced when a job fails and fix the computation so
the cap is honored. Do not change any public function or method signatures
(callers pass `max_delay` today and expect it to be respected), and keep the
package importable.
