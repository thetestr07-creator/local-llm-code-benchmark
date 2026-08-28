"""Wires normalization + tokenization into a simple processing step."""
from .normalize import slugify, titlecase
from .tokenize import tokens


def process(title):
    return {"slug": slugify(title), "title": titlecase(title), "tokens": tokens(title)}
