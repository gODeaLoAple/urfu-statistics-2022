from collections import Counter
from typing import List, Tuple

from intervals import Intervals
from table import Table


class TableBuilder:
    def __init__(self, x: Intervals, y: Intervals):
        self.x_intervals = x
        self.y_intervals = y

    def build(self, pairs: List[Tuple[int, int]]) -> Table:
        return Table(self.x_intervals, self.y_intervals, self._map_to_tables(self._create_table(pairs)))

    def _create_table(self, pairs: List[Tuple[int, int]]):
        return dict(Counter(map(self._map_to_indexes, pairs)))

    def _map_to_tables(self, frequencies):
        return {self._map_coords(c): frequencies[c] for c in frequencies.keys()}

    def _map_to_indexes(self, pair):
        x, y = pair
        return self.x_intervals.get_index(x), self.y_intervals.get_index(y)

    def _map_coords(self, pair):
        x, y = pair
        return self.x_intervals.get_by_index(x), self.y_intervals.get_by_index(y)