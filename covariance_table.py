from typing import Dict, Tuple

import pandas as pd
from matplotlib import pyplot as plt

from data.variance_collection import VarianceCollection


class CovarianceTable:
    def __init__(self, x: VarianceCollection, y: VarianceCollection, frequency_table: Dict[Tuple[int, int], int]):
        self.x_intervals = x
        self.y_intervals = y
        self.table = frequency_table

    def draw(self):
        columns = [f"[{x[0]}, {x[1]})" for x in self.x_intervals.segments()]
        rows = [f"[{y[0]}, {y[1]})" for y in self.y_intervals.segments()]

        data = []
        for y in range(len(rows)):
            data.append([])
            data[y].append(rows[y])
            for x in range(len(columns)):
                data[y].append(self.table.get((x, y), ""))

        fig, ax = plt.subplots(figsize=(10, 10))

        fig.patch.set_visible(False)
        ax.axis('off')

        df = pd.DataFrame(data, columns=["Y\\X"] + columns)

        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc="center")
        table.scale(1, 2)
        fig.tight_layout()

        plt.savefig("results/Ковариационная таблица.png")
        plt.show()
