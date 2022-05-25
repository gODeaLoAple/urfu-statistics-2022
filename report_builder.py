from typing import List, Dict

import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import laplace

from intervals import Intervals
from statistics_calculator import StatisticsCalculator
from statistics_data import StatisticsData
from table_helper import draw_table


class NormReportOptions:
    def __init__(self, alpha: float, xi_expected: float | None = None, q: float | None = None):
        self.xi_expected = xi_expected
        self.q = q
        self.alpha = alpha


def calculate_laplace(a, sigma, left, right):
    return laplace.cdf((right - a) / sigma) - laplace.cdf((left - a) / sigma)


class ReportBuilder:
    def __init__(self, variances: List[int], frequencies: Dict[float, int], intervals: Intervals, name,
                 options: NormReportOptions):
        self.frequencies = frequencies
        self.variances = variances
        self.name = name
        self.intervals = intervals
        self.options = options
        self.stat = StatisticsCalculator(self.frequencies, self.variances).calculate()

    def print_table(self):
        columns = [self.name] + list(map(str, self.frequencies.keys()))
        data = [["N"] + list(map(str, self.frequencies.values()))]
        draw_table(columns, data, filename=f"distribution {self.name}.png")

    def create_hist(self):
        values = list(self.frequencies.values())
        indexes = list(map(lambda x: str(x).replace(".0", ""), self.frequencies.keys()))

        df = pd.DataFrame(dict(data=values), index=indexes)
        fig, ax = plt.subplots()
        df["data"].plot(kind='bar', edgecolor='black', grid=True, width=1.0)
        df["data"].plot(kind='line', marker='*', color='black', ms=10, grid=True)
        plt.title(f"Гистограмма и полигоны варианты {self.name}")
        plt.xlabel(self.name)
        plt.ylabel("n")

        val = self.frequencies.values()
        step = 10
        ticks = list(range(step, max(val) + step, step)) + list(self.frequencies.values())
        major_tick = list(sorted(ticks))
        ax.set_yticks(major_tick)

        plt.savefig(f"Hist_{self.name}.png")
        plt.show()

    def create_norm_hist(self, a, sigma):
        values = list(self.frequencies.values())
        indexes = list(self.frequencies.keys())

        n = sum(self.frequencies.values())
        good_values = [calculate_laplace(a, sigma, left, right) * n for left, right in self.intervals.intervals]

        plt.figure(figsize=(10, 10))
        plt.plot(indexes, values, label=r'Эмпирические данные')
        plt.plot(indexes, good_values, label=fr'Ожидаемые данные')
        plt.xlabel(r'$x$', fontsize=7)
        plt.ylabel(r'$f(x)$', fontsize=7)
        plt.grid(True)
        plt.legend(loc='best', fontsize=7)

        plt.savefig(f"Hist_Norm_{self.name}.png")
        plt.show()

    def print_stat(self):
        stat = self.stat
        columns = ["Числовые хар-ки", self.name]
        data = [
            ["Выборочное среднее", stat.sample_mean],
            ["Выборочная дисперсия", stat.sample_variance],
            ["Выборочное СКО", stat.sigma],
            ["\"Испавленное\" СКО", stat.sigma_2],
            ["Мода", stat.mode],
            ["Медиана", stat.median],
        ]

        draw_table(columns, data, filename=f"Characteristics {self.name}.png")

    def report_norm(self):
        t_gamma = 1 - self.options.alpha
        stat = self.stat
        n = len(self.variances)
        k = t_gamma * stat.sigma_2 / (n ** 0.5)
        a = stat.sample_mean
        sigma = stat.sigma_2
        columns = ["Числовые хар-ки", self.name]
        if self.options.q is None:
            q = float(input(f"Значение в таблице q=q({t_gamma}, {n}): "))
        else:
            q = self.options.q
        p = self.pirson(a, sigma)
        data = [
            [r"Точечная оценка $a$", a],
            [r"Точечнкая оценка $\sigma$", sigma],
            [r"Интервальная оценка $a$", f"({stat.sample_mean - k}; {stat.sample_mean + k})"],
            [r"Интервальная оценка $\sigma$", f"({stat.sigma_2 * (1 - q)}; {stat.sigma_2 * (1 + q)})"],
            [r"Критерий Пирсона", p]
        ]
        draw_table(columns, data, filename=f"Characteristics Normal {self.name}.png")
        if not p:
            self.create_norm_hist(a, sigma)

    def pirson(self, a, sigma):
        n = sum(self.frequencies.values())
        s = 0
        for left, right in self.intervals.intervals:
            p1_i = self.frequencies[(left + right) / 2]
            p2_i = calculate_laplace(a, sigma, left, right) * n
            s += (p2_i - p1_i) ** 2 / p2_i
        xi_empirical = s
        k = len([v for v in self.frequencies.values() if v >= 4]) - 3
        if self.options.xi_expected is not None:
            xi_expected = self.options.xi_expected
        else:
            xi_expected = float(input(f"Значение в таблице Xi = Xi({self.options.alpha}, {k}): ")) ** 2
        print(xi_empirical)
        print(xi_expected)
        return xi_empirical < xi_expected
