import math

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.collections import PolyCollection


def wipe(x: np.ndarray, t: float):
    # https://numpy.org/doc/stable/reference/generated/numpy.heaviside.html

    d = t / abs(t) if abs(t) > 1e-3 else 1.0

    return d * np.heaviside(x - 1.0 + abs(t), 1.0)


def polygon_under_graph(x, y):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (x, y) line graph. This assumes x is in ascending order.
    """
    return [(x[0], 0.0), *zip(x, y), (x[-1], 0.0)]


def create_shape_map():
    # https://matplotlib.org/stable/gallery/mplot3d/polys3d.html#sphx-glr-gallery-mplot3d-polys3d-py
    x = np.linspace(0, 1.0, num=51)
    t = np.linspace(-1.0, 1.0, num=21)

    # verts = [
    #     polygon_under_graph(x, np.sin(2.0 * np.pi * 1.0 * t_i - np.pi * x)) for t_i in t
    # ]

    # verts = [polygon_under_graph(x, wipe(x, t_i)) for t_i in t]

    ax = plt.figure().add_subplot(projection="3d")
    colormap = plt.colormaps["Spectral"]
    # facecolors = plt.colormaps["viridis_r"](np.linspace(0, 1, len(verts)))

    # poly = PolyCollection(verts, facecolors=facecolors, alpha=0.7)
    # ax.add_collection3d(poly, zs=t, zdir="y")

    for t_i in t:
        z = wipe(x, t_i)
        ax.plot(x, t_i * np.ones_like(x), z, color=colormap(t_i / 2 + 0.5))

    ax.set(
        xlim=(0, 1.0),
        ylim=(-1.0, 1.0),
        zlim=(-1.0, 1.0),
        xlabel="x",
        ylabel="t",
        zlabel="intensity",
    )

    plt.show()


if __name__ == "__main__":
    Fire(create_shape_map)
