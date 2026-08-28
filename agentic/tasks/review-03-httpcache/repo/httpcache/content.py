"""Apply a parsed byte range to a representation body.

The parser in `ranges.py` produces ByteRange objects but knows nothing about the
actual body length. This module resolves each range against the real length,
decides satisfiability, clamps the end, and slices out the bytes.

See docs/SPEC.md: for a body of length L the last valid offset is L-1, so a
range is satisfiable iff `first <= last` and `first < L`. A `first` equal to L
(one past the end) is NOT satisfiable and must raise RangeNotSatisfiable.
"""


class RangeNotSatisfiable(Exception):
    """Raised when a requested range cannot be served (HTTP 416)."""


def _resolve(byte_range, length):
    """Turn a ByteRange into concrete (first, last) offsets given `length`.

    `last` is inclusive. Returns a (first, last) tuple. Raises
    RangeNotSatisfiable when the range does not overlap the body.
    """
    if byte_range.is_suffix():
        n = byte_range.suffix_length
        if n >= length:
            # asking for more (or exactly as many) suffix bytes than exist:
            # serve the whole body.
            return 0, length - 1
        return length - n, length - 1

    first = byte_range.first
    last = byte_range.last

    # Satisfiability: the start must point at a byte that actually exists.
    # The last valid offset is length-1, so `first` must be strictly below
    # `length`; a `first` equal to `length` is one past the end (see SPEC).
    if first > length:
        raise RangeNotSatisfiable("range %r not satisfiable for length %d" % (byte_range, length))

    # Clamp an open-ended or over-long end down to the final byte.
    if last is None or last > length - 1:
        last = length - 1

    return first, last


def apply_range(body, byte_range):
    """Return the bytes of `body` selected by `byte_range`.

    `body` is a bytes-like object. Raises RangeNotSatisfiable (HTTP 416) when
    the range does not overlap the body.
    """
    length = len(body)
    if length == 0:
        raise RangeNotSatisfiable("empty representation")
    first, last = _resolve(byte_range, length)
    return body[first:last + 1]
