"""HELD-OUT verification for tooluse-01. The model never sees this."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from textkit.normalize import slugify

cases = {
    "Hello,  World!": "hello-world",
    "  A  B  ": "a-b",
    "Python 3.12 rocks": "python-3-12-rocks",
    "Multiple---dashes__here": "multiple-dashes-here",
    "Hello World": "hello-world",
    "Trailing punctuation!!!": "trailing-punctuation",
}
for src, want in cases.items():
    got = slugify(src)
    assert got == want, "slugify(%r) -> %r, expected %r" % (src, got, want)
print("HELDOUT_OK")
