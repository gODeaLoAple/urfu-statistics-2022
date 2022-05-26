from statistics_data import StatisticsData
from table import Table
from variance_collection import VarianceCollection


def get_middle(interval: VarianceCollection, index: int):
    return interval.get_interval(index).middle


class Correlation:
    def __init__(self, table: Table, x_stat: StatisticsData, y_stat: StatisticsData):
        self.table = table
        self.x_stat = x_stat
        self.y_stat = y_stat

    def coefficient(self):
        frequencies = self.table.table
        x_intervals = self.table.x_intervals
        y_intervals = self.table.y_intervals
        n = sum(frequencies.values())

        xy = sum(v * get_middle(x_intervals, x) * get_middle(y_intervals, y) for (x, y), v in frequencies.items()) / n
        kxy = xy - self.x_stat.sample_mean * self.y_stat.sample_mean
        return kxy / (self.x_stat.sigma_2 * self.y_stat.sigma_2)
