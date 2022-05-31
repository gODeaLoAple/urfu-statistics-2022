from typing import List

from interval import Interval, BaseInterval
from intervals_range import IntervalsRange


def _create_interval(values, left, right):
    interval = BaseInterval(left, right)
    return Interval(left, right, [v for v in values if v in interval])


class VarianceCollection:
    def __init__(self, values: List[float], settings: IntervalsRange):
        self.values = values
        self.intervals = [_create_interval(values, left, right) for left, right in settings.range()]

    def get_interval(self, index):
        return self.intervals[index]

    def get_index(self, value):
        for i, interval in enumerate(self.intervals):
            if value in interval:
                return i
        raise IndexError

    def middles(self):
        return [x.middle for x in self.intervals]

    def count(self):
        return len(self.values)

    def segments(self):
        return list((x.left, x.right) for x in self.intervals)
