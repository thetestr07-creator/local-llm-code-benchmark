Users of this configuration library report that when a higher-priority source
overrides only *part* of a nested section, the sibling keys from lower-priority
sources vanish.

For example, with defaults `{"db": {"host": "localhost", "port": 5432}}` and an
environment override that sets only `db.port`, the resolved config should be
`{"db": {"host": "localhost", "port": 6000}}` — `db.host` must survive. Instead,
the whole `db` section is being replaced by the override, so `db.host`
disappears. Deeper nesting (e.g. `db.pool.size`) is affected the same way.

Top-level scalar overrides work fine; only nested sections are dropped.

Find where configuration layers are combined and fix the logic so that nested
mappings are merged recursively (override values win at each leaf, but keys only
present in a lower-priority layer are preserved). Do not change any public
function or class signatures, and keep the library importable.
