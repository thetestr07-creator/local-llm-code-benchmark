"""Simple configuration holder for a Gateway deployment."""


class Config:
    def __init__(self, **kwargs):
        self._values = dict(kwargs)

    def get(self, key, default=None):
        return self._values.get(key, default)

    def set(self, key, value):
        self._values[key] = value
        return self

    def as_dict(self):
        return dict(self._values)
