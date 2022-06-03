import pandas as pd
from matplotlib import pyplot as plt


def draw_table(columns, data, filename=None):
    fig, ax = plt.subplots(figsize=(10, 20))

    fig.patch.set_visible(False)
    ax.axis('off')

    df = pd.DataFrame(data, columns=columns)

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc="center")

    plt.tight_layout()
    table.scale(1, 2)

    if filename:
        plt.savefig(filename)
    plt.show()
