from typing import Dict, Tuple

import pandas as pd
from matplotlib import pyplot as plt

from intervals import Intervals


class Table:
    def __init__(self, x: Intervals, y: Intervals, table: Dict[Tuple[int, int], int]):
        self.x_intervals = x
        self.y_intervals = y
        self.table = table

    def draw(self):
        columns = [str(list(x)) for x in self.x_intervals.intervals]
        rows = [str(list(y)) for y in self.y_intervals.intervals]
        data = []
        for y in range(len(rows)):
            data.append([])
            data[y].append(rows[y])
            for x in range(len(columns)):
                c = self.x_intervals.get_by_index(x), self.y_intervals.get_by_index(y)
                data[y].append(self.table.get(c, ""))

        fig, ax = plt.subplots()

        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')

        df = pd.DataFrame(data, columns=["Y\\X"] + columns)

        ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc="center")

        fig.tight_layout()

        plt.show()
