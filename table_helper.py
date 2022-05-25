import pandas as pd
from matplotlib import pyplot as plt


def draw_table(columns, data, filename=None):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')

    df = pd.DataFrame(data, columns=columns)

    ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc="center")

    fig.tight_layout()

    if filename:
        plt.savefig(filename)
    plt.show()
