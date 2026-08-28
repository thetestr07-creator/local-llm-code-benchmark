# Byte-range rules (subset of RFC 7233)

A representation has a length `L` (the number of bytes in the body). Byte
positions are zero-based, so the last valid byte offset is `L - 1`.

A single range request `bytes=first-last` is interpreted as follows:

- `first-last`  : bytes `first` through `last` inclusive.
- `first-`      : bytes `first` through the end (`L - 1`).
- `-suffix`     : the final `suffix` bytes, i.e. `L - suffix` through `L - 1`.

## Satisfiability

A range is **satisfiable** only if `first` refers to a byte that actually
exists in the representation. Because the last valid offset is `L - 1`, a range
is satisfiable iff:

    first <= last  AND  first < L

If `last` is greater than `L - 1`, it is clamped down to `L - 1` (the range is
still satisfiable as long as `first < L`).

A request for `bytes=L-...` (a `first` equal to the length, i.e. one past the
final byte) is **not satisfiable** and must yield HTTP 416, never an empty or
partial body.
