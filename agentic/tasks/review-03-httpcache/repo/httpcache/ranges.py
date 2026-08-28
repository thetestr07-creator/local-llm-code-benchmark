"""Parse a `Range: bytes=...` header into structured byte ranges.

This module only PARSES the syntax; it does not know the representation length,
so it cannot decide satisfiability. Resolving/clamping against the actual body
length happens in `content.py`.
"""


class ByteRange:
    """A single requested range.

    Exactly one of two forms:
      - explicit:   first is an int >= 0; last is an int >= first, or None for
                    an open-ended `first-` range.
      - suffix:     first is None; suffix_length is a positive int for a
                    `-N` (last N bytes) range.
    """

    def __init__(self, first=None, last=None, suffix_length=None):
        self.first = first
        self.last = last
        self.suffix_length = suffix_length

    def is_suffix(self):
        return self.first is None and self.suffix_length is not None

    def __repr__(self):
        if self.is_suffix():
            return "ByteRange(suffix=%d)" % self.suffix_length
        return "ByteRange(first=%r, last=%r)" % (self.first, self.last)


def parse_range_header(value):
    """Parse a `Range` header value into a list of ByteRange, or None.

    Returns None when the header is absent, does not use the `bytes` unit, or is
    syntactically malformed (the caller then ignores it and serves 200). An
    empty list is never returned: a syntactically valid header has >= 1 range.
    """
    if not value:
        return None
    value = value.strip()
    if "=" not in value:
        return None
    unit, _, spec = value.partition("=")
    if unit.strip().lower() != "bytes":
        return None

    ranges = []
    for part in spec.split(","):
        part = part.strip()
        if not part or "-" not in part:
            return None
        start_txt, _, end_txt = part.partition("-")
        start_txt, end_txt = start_txt.strip(), end_txt.strip()

        if start_txt == "":
            # suffix range: -N
            if not end_txt.isdigit():
                return None
            n = int(end_txt)
            if n == 0:
                return None
            ranges.append(ByteRange(suffix_length=n))
            continue

        if not start_txt.isdigit():
            return None
        first = int(start_txt)

        if end_txt == "":
            ranges.append(ByteRange(first=first, last=None))
        else:
            if not end_txt.isdigit():
                return None
            last = int(end_txt)
            if last < first:
                return None
            ranges.append(ByteRange(first=first, last=last))

    return ranges or None
