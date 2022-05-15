import pandas as pd
from matplotlib import pyplot as plt


def draw_table(columns, data):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    df = pd.DataFrame(data, columns=columns)

    ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc="center")

    fig.tight_layout()

    plt.show()