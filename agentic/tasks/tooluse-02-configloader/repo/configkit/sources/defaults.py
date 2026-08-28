"""Lowest-priority source: built-in defaults supplied by the application."""


class DefaultsSource:
    priority = 0

    def __init__(self, data):
        self._data = dict(data)

    def load(self):
        # Defaults are returned as-is; they form the base layer everything
        # else merges on top of.
        return dict(self._data)
