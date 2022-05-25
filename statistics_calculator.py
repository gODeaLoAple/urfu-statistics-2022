import math
from collections import Counter
from typing import Dict, List

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
    def __init__(self, data: Dict[float, int], variances: List[float]):
        self.data = data
        self.variances = variances

    def calculate(self) -> StatisticsData:
        n = sum(self.data.values())

        sample_mean = sum(x * k for x, k in self.data.items()) / n

        sample_variance = sum(x ** 2 * k for x, k in self.data.items()) / n - (sample_mean ** 2)

        sigma = math.sqrt(sample_variance)
        s_2 = (n / (n - 1)) * sample_variance if n > 1 else 0
        sigma_2 = math.sqrt(s_2)

        mode = Counter(self.variances).most_common(1)[0][0]

        median = calculate_median(self.variances)

        return StatisticsData(
            sample_mean,
            sample_variance,
            sigma,
            s_2,
            mode,
            median,
            sigma_2)
