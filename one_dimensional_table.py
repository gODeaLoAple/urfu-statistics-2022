from collections import Counter
from typing import Dict, Tuple, List

from intervals import Intervals


def _get_middle(pair):
    x, y = pair
    return (x + y) / 2


class OneDimensionalTable:
    def __init__(self, x: Intervals):
        self.intervals = x

    def create_table(self, variances: List[int]) -> Dict[int, int]:
        return dict(Counter(map(self.intervals.get_index, variances)))

    def create_discrete_table(self, variances: List[int]):
        return self.map_to_discrete_table(self.create_table(variances))

    def map_to_tables(self, frequencies):
        return {self.intervals.get_by_index(k): v for k, v in frequencies.items()}

    def map_to_discrete_table(self, frequencies) -> Dict[float, int]:
        return {_get_middle(self.intervals.get_by_index(k)): v for k, v in frequencies.items()}
