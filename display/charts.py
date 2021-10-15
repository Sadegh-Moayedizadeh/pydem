import matplotlib.pyplot as plt
from typing import List, Dict


def show_plot(data: Dict[List[float]], title: str) -> None:
    labels = list(data.keys())
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.title(title)
    x_values = data[labels[0]]
    y_values = data[labels[1]]
    plt.plot(x_values, y_values)
    plt.show()