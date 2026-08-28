"""Mid-priority source: a config document already parsed into a dict.

Real deployments would read TOML/JSON from disk; to stay stdlib-only and
deterministic this source just wraps an in-memory mapping (as the parser
module would produce) and hands back a deep copy so callers can't mutate it.
"""
import copy


class DictFileSource:
    priority = 10

    def __init__(self, data):
        self._data = copy.deepcopy(data)

    def load(self):
        return copy.deepcopy(self._data)
