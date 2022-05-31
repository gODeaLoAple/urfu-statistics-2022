from typing import Optional

import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import laplace

from statistics_data import StatisticsData
from table_helper import draw_table
from variance_collection import VarianceCollection


class NormReportOptions:
    def __init__(self, alpha: float, xi_expected: Optional[float] = None, q: Optional[float] = None):
        self.xi_expected = xi_expected
        self.q = q
        self.alpha = alpha


def calculate_laplace(a, sigma, left, right):
    return laplace.cdf((right - a) / sigma) - laplace.cdf((left - a) / sigma)


class ReportBuilder:
    def __init__(self, intervals: VarianceCollection, stat: StatisticsData, name,
                 options: NormReportOptions):
        self.name = name
        self.collection = intervals
        self.options = options
        self.stat = stat

    def report_distribution(self):
        values = {x.middle: x.count for x in self.collection.intervals}
        columns = [self.name] + list(map(str, values.keys()))
        data = [["N"] + list(map(str, values.values()))]
        draw_table(columns, data, filename=f"results/Distribution {self.name}.png")

    def report_hist(self):
        frequencies = {x.middle: x.count for x in self.collection.intervals}
        values = list(frequencies.values())
        indexes = list(map(lambda x: str(x).replace(".0", ""), frequencies.keys()))

        df = pd.DataFrame(dict(data=values), index=indexes)
        fig, ax = plt.subplots()
        df["data"].plot(kind='bar', edgecolor='black', grid=True, width=1.0)
        df["data"].plot(kind='line', marker='*', color='black', ms=10, grid=True)
        plt.title(f"Гистограмма и полигоны варианты {self.name}")
        plt.xlabel(self.name)
        plt.ylabel("n")

        step = 10
        ticks = list(range(step, max(values) + step, step)) + values
        major_tick = list(sorted(ticks))
        ax.set_yticks(major_tick)

        plt.savefig(f"results/Hist {self.name}.png")
        plt.show()

    def report_stat(self):
        t_gamma = 1 - self.options.alpha
        stat = self.stat
        n = self.collection.count()
        k = t_gamma * stat.sigma_2 / (n ** 0.5)
        a = stat.sample_mean
        sigma = stat.sigma_2
        if self.options.q is None:
            q = float(input(f"Значение в таблице q=q({t_gamma}, {n}): "))
        else:
            q = self.options.q
        p = self.pirson(a, sigma)
        columns = [f"Числовые характеристики", self.name]
        data = [
            ["Выборочное среднее", f"{stat.sample_mean:0.5f}"],
            ["Выборочная дисперсия", f"{stat.sample_variance:0.5f}"],
            ["Выборочное СКО", f"{stat.sigma:0.5f}"],
            ["Испавленное СКО", f"{stat.sigma_2:0.5f}"],
            ["Мода", f"{stat.mode:0.5f}"],
            ["Медиана", f"{stat.median:0.5f}"],
            [r"Точечная оценка $a$", f"{a:0.5f}"],
            [r"Интервальная оценка $a$", f"({a - k:0.5f}; {a + k:0.5f})"],
            [r"Точечная оценка $\sigma$", f"{sigma:0.5f}"],
            [r"Интервальная оценка $\sigma$", f"({stat.sigma_2 * (1 - q):0.5f}; {stat.sigma_2 * (1 + q):0.5f})"],
            [r"Критерий Пирсона", p]
        ]
        draw_table(columns, data, filename=f"results/Characteristics {self.name}.png")

    def report_norm(self):
        a = self.stat.sample_mean
        sigma = self.stat.sigma_2
        self.create_norm_hist(a, sigma)

    def create_norm_hist(self, a, sigma):
        frequencies = {x.middle: x.count for x in self.collection.intervals}
        values = list(frequencies.values())
        indexes = list(frequencies.keys())

        n = self.collection.count()
        good_values = [calculate_laplace(a, sigma, x.left, x.right) * n for x in self.collection.intervals]

        plt.figure(figsize=(10, 10))
        plt.plot(indexes, values, label=r'Эмпирические данные')
        plt.plot(indexes, good_values, label=fr'Ожидаемые данные')
        plt.xlabel(r'$x$', fontsize=7)
        plt.ylabel(r'$f(x)$', fontsize=7)
        plt.grid(True)
        plt.legend(loc='best', fontsize=7)

        plt.savefig(f"results/Hist_Norm_{self.name}.png")
        plt.show()

    def pirson(self, a, sigma):
        n = self.collection.count()
        s = 0
        for interval in self.collection.intervals:
            p1_i = interval.count
            p2_i = calculate_laplace(a, sigma, interval.left, interval.right) * n
            s += (p2_i - p1_i) ** 2 / p2_i
        xi_empirical = s
        k = len([v for v in self.collection.intervals if v.count >= 4]) - 3
        if self.options.xi_expected is not None:
            xi_expected = self.options.xi_expected
        else:
            xi_expected = float(input(f"Значение в таблице Пирсона Xi = Xi({self.options.alpha}, {k}): "))
        return xi_empirical < xi_expected
