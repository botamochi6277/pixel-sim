import math

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.collections import PolyCollection

from pixel_sim import shapes
from pathlib import Path


def create_shape_map(
    name: str = "heat",
    width: float = 0.1,
    is_reversed: bool = False,
):
    # https://matplotlib.org/stable/gallery/mplot3d/polys3d.html#sphx-glr-gallery-mplot3d-polys3d-py
    position = np.linspace(0, 1.0, num=101)
    t = np.linspace(0.0, 1.0, num=5)

    if name == "pulse":
        f = lambda t, x: shapes.pulse(t, x, width=width)
    elif name == "wipe":
        f = lambda t, x: shapes.wipe(t, x)
    elif name == "wipe_quad":
        f = lambda t, x: shapes.wipe(t, x, "quad")
    elif name == "heat":
        f = lambda t, x: np.ones_like(x) * t
    elif name == "saw":
        f = lambda t, x: shapes.saw_wave(t, x)
    elif name == "sin":
        f = lambda t, x: shapes.sin_wave(t, x)
    else:
        print(f"ERROR! {name} is invalid")
        return

    fig, axes = plt.subplots(nrows=len(t), layout="tight", sharex=True)

    for t_i, ax in zip(t, axes):
        if is_reversed:
            z = f(1.0 - t_i, position)
        else:
            z = f(t_i, position)

        ax.plot(position, z, label=f"t={t_i:0.2f}")

        ax.legend(loc="upper right")
        ax.set_ylim((-0.1, 1.1))

    # ax.set(
    #     xlim=(-0.1, 1.1),
    #     ylim=(-0.1, 1.1),
    #     xlabel="position",
    #     ylabel="intensity",
    #     title=name,
    # )
    axes[0].set_title(name)
    axes[-1].set_xlim((-0.1, 1.1))
    # axes[-1].set_ylabel("intensity")
    axes[-1].set_xlabel("position")

    plt.show()

    dst_path = Path(__file__).parent.joinpath(f"../assets/shapes/{name}.svg")
    fig.savefig(dst_path)


if __name__ == "__main__":
    Fire(create_shape_map)
