from typing import List

import pandas as pd
from matplotlib import pyplot as plt

from intervals import Intervals
from one_dimensional_table import OneDimensionalTable
from statistics_calculator import StatisticsCalculator
from table_helper import draw_table


class ReportBuilder:
    def __init__(self, variances: List[int], intervals: Intervals, name):
        table = OneDimensionalTable(intervals)
        self.frequencies = table.map_to_discrete_table(table.create_table(variances))
        self.variances = variances
        self.name = name

    def print_table(self):
        columns = [self.name] + list(map(str, self.frequencies.keys()))
        data = [["N"] + list(map(str, self.frequencies.values()))]
        draw_table(columns, data)

    def create_hist(self):
        values = list(self.frequencies.values())
        indexes = list(map(lambda x: str(x).replace(".0", ""), self.frequencies.keys()))

        df = pd.DataFrame(dict(data=values), index=indexes)
        fig, ax = plt.subplots()
        df["data"].plot(kind='bar', edgecolor='black', grid=True, width=1.0)
        df["data"].plot(kind='line', marker='*', color='black', ms=10, grid=True)
        plt.title(f"Гистограмма и полигоны новой варианты {self.name}")
        plt.xlabel(self.name)
        plt.ylabel("n")

        major_tick = list(self.frequencies.values()) + [5, 10, 15, 20, 25, 30, 35, 40]
        ax.set_yticks(major_tick)

        plt.show()

    def print_stat(self):
        stat = StatisticsCalculator(self.frequencies, self.variances).calculate()

        columns = ["Числовые хар-ки", self.name]
        data = [
            ["Выборочное среднее", stat.sample_mean],
            ["Выборочная дисперсия", stat.sample_variance],
            ["Выборочное СКО", stat.sigma],
            ["\"Испавленное\" СКО", stat.sigma_2],
            ["Мода", stat.mode],
            ["Медиана", stat.median],
        ]

        draw_table(columns, data)
