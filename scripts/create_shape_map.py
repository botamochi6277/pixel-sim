import math

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.collections import PolyCollection

from pixel_sim import shapes


def create_shape_map(is_reversed: bool = False, name: str = "heat"):
    # https://matplotlib.org/stable/gallery/mplot3d/polys3d.html#sphx-glr-gallery-mplot3d-polys3d-py
    x = np.linspace(0, 1.0, num=51)
    t = np.linspace(-1.0, 1.0, num=21)

    ax = plt.figure().add_subplot(projection="3d")
    colormap = plt.colormaps["coolwarm"]

    if name == "pulse":
        f = lambda x, t: shapes.pulse(x, t)
    elif name == "wipe":
        f = lambda x, t: shapes.wipe(x, t)
    elif name == "wipe_quad":
        f = lambda x, t: shapes.wipe(x, t, "quad")
    elif name == "heat":
        f = lambda x, t: np.ones_like(x) * t
    elif name == "saw":
        f = lambda x, t: shapes.wave(x, t, "saw")
    elif name == "sin":
        f = lambda x, t: shapes.wave(x, t, "sin")
    else:
        print(f"ERROR! {name} is invalid")
        return

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
