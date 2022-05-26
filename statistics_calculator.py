import math
from collections import Counter

from variance_collection import VarianceCollection
from statistics_data import StatisticsData


def calculate_median(numbers):
    if len(numbers) == 1:
        return numbers[0]

    sorted_list = list(sorted(numbers, key=lambda x: x))
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
        variances = self.collection.values
        sample_mean = sum(interval.middle * interval.count for interval in intervals) / n

        s = sum((interval.middle ** 2) * interval.count for interval in intervals)
        sample_variance = s / n - (sample_mean ** 2)

        sigma = math.sqrt(sample_variance)
        s_2 = (n / (n - 1)) * sample_variance if n > 1 else 0
        sigma_2 = math.sqrt(s_2)

        mode = Counter(variances).most_common(1)[0][0]

        median = calculate_median(variances)

        return StatisticsData(
            sample_mean,
            sample_variance,
            sigma,
            s_2,
            mode,
            median,
            sigma_2)
