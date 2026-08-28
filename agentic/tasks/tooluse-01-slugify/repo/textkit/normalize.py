"""Text normalization helpers."""


def slugify(s):
    """Turn a human title into a URL slug (lowercase, words joined by hyphens)."""
    return s.lower().replace(" ", "-")


def titlecase(s):
    return " ".join(w.capitalize() for w in s.split())
