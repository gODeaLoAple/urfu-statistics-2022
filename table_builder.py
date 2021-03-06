from collections import Counter
from typing import List, Tuple, Dict

from data.variance_collection import VarianceCollection
from covariance_table import CovarianceTable


class CovarianceTableBuilder:
    def __init__(self, x: VarianceCollection, y: VarianceCollection):
        self.x_intervals = x
        self.y_intervals = y

    def build(self, pairs: List[Tuple[int, int]]) -> CovarianceTable:
        return CovarianceTable(self.x_intervals, self.y_intervals, self._create_table(pairs))

    def _create_table(self, pairs: List[Tuple[int, int]]) -> Dict[Tuple[int, int], int]:
        return dict(Counter(map(self._map_to_indexes, pairs)))

    def _map_to_indexes(self, pair):
        x, y = pair
        return self.x_intervals.get_index(x), self.y_intervals.get_index(y)
