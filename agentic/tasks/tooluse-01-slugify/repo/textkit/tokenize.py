"""Tokenization helpers (unrelated to the slug issue)."""


def tokens(s):
    return s.split()


def ngrams(s, n=2):
    ws = tokens(s)
    return [tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)]
