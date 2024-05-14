import json

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.axes import Axes

import pixel_sim


def encode_cyclic_colormap(cmap_name: str, num: int = 101):
    print(f"encoding {cmap_name} ...")  # ['twilight', 'twilight_shifted', 'hsv']
    cyclic_params = pixel_sim.analysis.compute_cyclic_param(cmap_name, num=num)
    print(f"encoding completed")
    r, g, b = pixel_sim.analysis.compute_cyclic_color(cyclic_params)

    fig, axes = plt.subplots(5, sharex="col", height_ratios=(1, 0.25, 0.25, 0.25, 0.25))

    axes: list[Axes]
    t = np.linspace(0.0, 1.0, num=num)
    pixel_sim.plotting.plot_rgb_curve(t, r, g, b, ax=axes[0], show_legend=True)
    axes[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    axes[0].set_title(f"{cmap_name}-decode")
    axes[0].set_ylim((-0.1, 1.1))

    pixel_sim.plotting.plot_color_ribbon(t, r, g, b, ax=axes[1])
    axes[1].set_title(f"decode (target)")
    # axes[1].set_aspect(0.05)

    # screen
    scale = 0.5
    white = np.ones_like(r) * scale
    r_scr = pixel_sim.color.apply_screen(white, r)
    g_scr = pixel_sim.color.apply_screen(white, g)
    b_scr = pixel_sim.color.apply_screen(white, b)
    pixel_sim.plotting.plot_color_ribbon(t, r_scr, g_scr, b_scr, ax=axes[2])
    axes[2].set_title(f"screen")

    # inverse screen
    r_inv = pixel_sim.color.apply_screen_inverse(white, r)
    g_inv = pixel_sim.color.apply_screen_inverse(white, g)
    b_inv = pixel_sim.color.apply_screen_inverse(white, b)
    pixel_sim.plotting.plot_color_ribbon(t, r_inv, g_inv, b_inv, ax=axes[3])
    axes[3].set_title(f"inverse")

    # re-screen
    r_re = pixel_sim.color.apply_screen(white, r_inv)
    g_re = pixel_sim.color.apply_screen(white, g_inv)
    b_re = pixel_sim.color.apply_screen(white, b_inv)
    pixel_sim.plotting.plot_color_ribbon(t, r_re, g_re, b_re, ax=axes[4])
    axes[4].set_title(f"re-screen")

    axes[-1].set_xlim([-0.05, 1.05])

    plt.tight_layout()
    # fig.show()
    plt.show()


if __name__ == "__main__":
    Fire(encode_cyclic_colormap)
