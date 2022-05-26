import math

from correlation_options import CorrelationOptions
from statistics_data import StatisticsData
from table import Table
from variance_collection import VarianceCollection


def get_middle(interval: VarianceCollection, index: int):
    return interval.get_interval(index).middle


class Correlation:
    def __init__(self, table: Table, x_stat: StatisticsData, y_stat: StatisticsData, options: CorrelationOptions):
        self.table = table
        self.x_stat = x_stat
        self.y_stat = y_stat
        self.count = sum(self.table.table.values())
        self.options = options

    def coefficient(self):
        frequencies = self.table.table
        x_intervals = self.table.x_intervals
        y_intervals = self.table.y_intervals
        n = self.count

        s = sum(v * get_middle(x_intervals, x) * get_middle(y_intervals, y) for (x, y), v in frequencies.items())
        kxy = (s - n * self.x_stat.sample_mean * self.y_stat.sample_mean) / (n - 1)
        return kxy / (self.x_stat.sigma_2 * self.y_stat.sigma_2)

    def significance(self):
        n = self.count
        rxy = self.coefficient()
        t = rxy * math.sqrt((n - 2) / (1 - rxy ** 2))
        if self.options.critical_t is None:
            critical_t = float(input(f"Значение в таблице Стьюдента t=t({self.options.alpha}, {n - 2}): "))
        else:
            critical_t = self.options.critical_t
        return abs(t) < critical_t
