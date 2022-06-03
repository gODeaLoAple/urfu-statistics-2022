import itertools
import math
from typing import List

from data.interval import Interval
from data.variance_collection import VarianceCollection
from data.statistics_data import StatisticsData


def calculate_sample_mean(intervals: List[Interval], n: int):
    return sum(x.middle * x.count for x in intervals) / n


def calculate_sample_variance(intervals: List[Interval], sample_mean: float, n: int):
    return sum((x.middle ** 2) * x.count for x in intervals) / n - (sample_mean ** 2)


def calculate_sigma(sample_variance: float):
    return math.sqrt(sample_variance)


def calculate_s_2(sample_variance: float, n: int):
    assert n > 1
    return n / (n - 1) * sample_variance


def calculate_sigma_2(s_2: float):
    return math.sqrt(s_2)


def calculate_mode(intervals: List[Interval]):
    return list(sorted(intervals, key=lambda x: x.count))[-1].middle


def calculate_median(intervals: List[Interval]):
    numbers = itertools.chain(*([x.middle] * x.count for x in intervals))
    sorted_list = list(sorted(numbers))

    length = len(sorted_list)
    index = (length - 1) // 2

    if length % 2 != 0:
        return sorted_list[index]
    else:
        return (sorted_list[index] + sorted_list[index + 1]) / 2


class StatisticsCalculator:
    def __init__(self, collection: VarianceCollection):
        self.collection = collection

    def calculate(self) -> StatisticsData:
        n = self.collection.count()
        intervals = self.collection.intervals

        sample_mean = calculate_sample_mean(intervals, n)
        sample_variance = calculate_sample_variance(intervals, sample_mean, n)
        sigma = calculate_sigma(sample_variance)
        s_2 = calculate_s_2(sample_variance, n)
        sigma_2 = calculate_sigma_2(s_2)
        mode = calculate_mode(intervals)
        median = calculate_median(intervals)

        return StatisticsData(
            sample_mean,
            sample_variance,
            sigma,
            s_2,
            mode,
            median,
            sigma_2)
