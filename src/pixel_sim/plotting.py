import matplotlib.pyplot as plt

# import seaborn as sns
import numpy as np
from matplotlib.axes import Axes

from . import color


def plot_rgb_curve(
    t: np.ndarray,
    red: np.ndarray,
    green: np.ndarray,
    blue: np.ndarray,
    ax: Axes | None = None,
):
    if ax is None:
        ax = plt.gca()
    luminance = color.compute_luminance(red, green, blue)
    ax.plot(t, red, label="red", color="#e2431e")
    ax.plot(t, green, label="green", color="#6f9654")
    ax.plot(t, blue, label="blue", color="#43459d")
    ax.plot(t, luminance, label="luminance", linestyle="dotted", color="#a0a0a0")
    # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    # ax.set_ylabel("intensity")

    return ax


def plot_color_ribbon(
    t: np.ndarray,
    red: np.ndarray,
    green: np.ndarray,
    blue: np.ndarray,
    ax: Axes | None = None,
):
    if ax is None:
        ax = plt.gca()
    for i in range(0, len(t), 1):
        ax.barh(
            0,
            width=1.1 / len(t),
            height=0.2,
            left=t[i] - 0.5 / len(t),
            color=(red[i], green[i], blue[i]),
        )
    # ax.set_xlim([-0.05, 1.05])
    return ax
