import math
import typing
from collections import Counter

from matplotlib import pyplot as plt

from correlation_options import CorrelationOptions
from statistics_data import StatisticsData
from table import Table
from table_helper import draw_table
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
        return self.covaration() / (self.x_stat.sigma_2 * self.y_stat.sigma_2)

    def covaration(self):
        frequencies = self.table.table
        x_intervals = self.table.x_intervals
        x_middles = x_intervals.middles()
        y_intervals = self.table.y_intervals
        y_middles = y_intervals.middles()
        n = self.count

        s = sum(v * x_middles[x] * y_middles[y] for (x, y), v in frequencies.items())
        kxy = (s - n * self.x_stat.sample_mean * self.y_stat.sample_mean) / (n - 1)
        return kxy

    def student_coefficient(self):
        n = self.count
        rxy = self.coefficient()
        t = rxy * math.sqrt((n - 2) / (1 - rxy ** 2))
        return t

    def significance(self):
        n = self.count
        if self.options.critical_t is None:
            critical_t = float(input(f"Значение в таблице Стьюдента t=t({self.options.alpha}, {n - 2}): "))
        else:
            critical_t = self.options.critical_t
        return abs(self.student_coefficient()) < critical_t

    def report(self):
        r = self.coefficient()
        y0 = self.y_stat.sample_mean
        x0 = self.x_stat.sample_mean
        ky = r * self.y_stat.sigma_2 / self.x_stat.sigma_2
        kx = r * self.x_stat.sigma_2 / self.y_stat.sigma_2

        def y_regression(x):
            return y0 + ky * (x - x0)

        def x_regression(y):
            return x0 + kx * (y - y0)

        # Y = Y(X)
        xs, ys = list(map(list, zip(*self.get_x_to_y())))
        self.draw_regression(xs, ys, y_regression, f"results/Regression Y on X.png")

        # X = X(Y)
        xs, ys = list(map(list, zip(*self.get_y_to_x())))
        self.draw_regression(xs, ys, x_regression, f"results/Regression X on Y.png")

        columns = ["Величина", "Значение"]
        data = [
            ["Ковариация", f"{self.covaration():0.4f}"],
            ["Коэффициент корреляции", f"{self.coefficient():0.4f}"],
            ["Наблюдаемое значение критерия Стюдента", f"{self.student_coefficient():0.4f}"],
            ["Уравнение теоретической регрессии Y на X", f"$y = ({ky:0.2f}) * x + ({(y0 - ky * x0):0.2f})$"],
            ["Уравнение теоретической регрессии X на Y", f"$x = ({kx:0.2f}) * y + ({(x0 - kx * y0):0.2f})$"],
        ]
        draw_table(columns, data, filename="results/Correlation.png")

    @staticmethod
    def draw_regression(xs, ys, f, name):
        plt.figure(figsize=(10, 10))
        plt.plot(xs, ys, label=r'Эмпирические данные')
        plt.plot(xs, list(map(f, xs)), label=r'Теоретические данные')
        plt.grid(True)
        plt.legend(loc='best', fontsize=7)

        plt.savefig(name)
        plt.show()

    def get_x_to_y(self):
        return self.get_conditional_coords([(x, y) for x, y in self.get_middles()])

    def get_y_to_x(self):
        return self.get_conditional_coords([(y, x) for x, y in self.get_middles()])

    @staticmethod
    def get_conditional_coords(pairs):
        result = {}
        for x, y in pairs:
            if x not in result:
                result[x] = []
            result[x].append(y)
        result = [(xm, Counter(yms)) for xm, yms in result.items()]
        result = [(xm, sum(y * n for y, n in c.items()) / sum(c.values())) for xm, c in result]
        return list(sorted(result, key=lambda t: t[0]))

    def get_middles(self):
        x_intervals = self.table.x_intervals
        y_intervals = self.table.y_intervals
        for x, y in self.table.table.keys():
            xm = get_middle(x_intervals, x)
            ym = get_middle(y_intervals, y)
            yield xm, ym
