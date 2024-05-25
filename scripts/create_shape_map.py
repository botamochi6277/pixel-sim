import math

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.collections import PolyCollection

from pixel_sim import shapes


def polygon_under_graph(x, y):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (x, y) line graph. This assumes x is in ascending order.
    """
    return [(x[0], 0.0), *zip(x, y), (x[-1], 0.0)]


def create_shape_map(is_reversed: bool = False, name: str = "wipe"):
    # https://matplotlib.org/stable/gallery/mplot3d/polys3d.html#sphx-glr-gallery-mplot3d-polys3d-py
    x = np.linspace(0, 1.0, num=51)
    t = np.linspace(-1.0, 1.0, num=21)

    ax = plt.figure().add_subplot(projection="3d")
    colormap = plt.colormaps["twilight"]
    # facecolors = plt.colormaps["viridis_r"](np.linspace(0, 1, len(verts)))

    # poly = PolyCollection(verts, facecolors=facecolors, alpha=0.7)
    # ax.add_collection3d(poly, zs=t, zdir="y")

    if name == "pulse":
        f = lambda x, t: shapes.pulse(x, t)
    elif name == "quad":
        f = lambda x, t: shapes.wipe(x, t, "quad")
    else:
        f = lambda x, t: shapes.wipe(x, t)

    for t_i in t:
        if is_reversed:
            z = f(1.0 - x, t_i)
        else:
            z = f(x, t_i)
        ax.plot(x, t_i * np.ones_like(x), z, color=colormap(t_i / 2 + 0.5))

    ax.set(
        xlim=(0, 1.0),
        ylim=(-1.0, 1.0),
        zlim=(-1.0, 1.0),
        xlabel="x",
        ylabel="t",
        zlabel="intensity",
        title=name,
    )

    plt.show()


if __name__ == "__main__":
    Fire(create_shape_map)
