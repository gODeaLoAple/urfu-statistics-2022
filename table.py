from typing import Dict, Tuple

import pandas as pd
from matplotlib import pyplot as plt

from variance_collection import VarianceCollection


class Table:
    def __init__(self, x: VarianceCollection, y: VarianceCollection, frequency_table: Dict[Tuple[int, int], int]):
        self.x_intervals = x
        self.y_intervals = y
        self.table = frequency_table

    def get_frequency_at(self, x_index, y_index):
        return self.table.get((x_index, y_index), 0)

    def draw(self):
        columns = [str(list(x)) for x in self.x_intervals.segments()]
        rows = [str(list(y)) for y in self.y_intervals.segments()]

        data = []
        for y in range(len(rows)):
            data.append([])
            data[y].append(rows[y])
            for x in range(len(columns)):
                data[y].append(self.table.get((x, y), ""))

        fig, ax = plt.subplots()

        fig.patch.set_visible(False)
        ax.axis('off')

        df = pd.DataFrame(data, columns=["Y\\X"] + columns)

        ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc="center")

        fig.tight_layout()

        plt.savefig("results/table.png")
        plt.show()
