import json

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.axes import Axes

import pixel_sim


def encode_cyclic_colormap(cmap_name: str, num: int = 101, min_lumi: float = 0.5):
    print(f"encoding {cmap_name} ...")  # ['twilight', 'twilight_shifted', 'hsv']
    r_cmap, g_cmap, b_cmap = pixel_sim.color.get_color_of_colormap(cmap_name)
    cyclic_params = pixel_sim.analysis.compute_cyclic_param(r_cmap, g_cmap, b_cmap)

    print(f"encoding completed")
    r, g, b = pixel_sim.analysis.compute_cyclic_color(cyclic_params)

    fig, axes = plt.subplots(
        nrows=3, ncols=2, sharex="col", sharey="row", height_ratios=(1, 0.25, 0.25)
    )

    axes: list[list[Axes]]
    t = np.linspace(0.0, 1.0, num=num)
    pixel_sim.plotting.plot_rgb_curve(t, r, g, b, ax=axes[0][0], show_legend=False)
    # axes[0][0].legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    axes[0][0].set_title(f"{cmap_name}-decode")
    axes[0][0].set_ylim((-0.1, 1.1))

    pixel_sim.plotting.plot_color_ribbon(t, r, g, b, ax=axes[1][0])
    axes[1][0].set_title(f"decode (target)")
    # axes[1].set_aspect(0.05)

    # screen
    scale = 0.5
    white = np.ones_like(r) * scale
    r_scr = pixel_sim.color.apply_screen(white, r)
    g_scr = pixel_sim.color.apply_screen(white, g)
    b_scr = pixel_sim.color.apply_screen(white, b)
    pixel_sim.plotting.plot_color_ribbon(t, r_scr, g_scr, b_scr, ax=axes[2][0])
    axes[2][0].set_title(f"screen")

    # rescale?
    luminance_cmap = pixel_sim.color.compute_luminance(r_cmap, g_cmap, b_cmap)
    scale = (1.0 - min_lumi) / (1.0 - luminance_cmap.min())
    r2 = (r_cmap - 1.0) * scale + 1.0
    g2 = (g_cmap - 1.0) * scale + 1.0
    b2 = (b_cmap - 1.0) * scale + 1.0
    pixel_sim.plotting.plot_rgb_curve(t, r2, g2, b2, ax=axes[0][1], show_legend=True)
    axes[0][1].set_title(f"tuned")

    pixel_sim.plotting.plot_color_ribbon(t, r2, g2, b2, ax=axes[1][1])
    axes[1][1].set_title(f"tuned")

    # re-screen
    r_re = pixel_sim.color.apply_screen(white, r2)
    g_re = pixel_sim.color.apply_screen(white, g2)
    b_re = pixel_sim.color.apply_screen(white, b2)
    pixel_sim.plotting.plot_color_ribbon(t, r_re, g_re, b_re, ax=axes[2][1])
    axes[2][1].set_title(f"tuned-screen")

    axes[-1][0].set_xlim([-0.05, 1.05])
    axes[-1][1].set_xlim([-0.05, 1.05])

    plt.tight_layout()
    # fig.show()
    plt.show()


if __name__ == "__main__":
    Fire(encode_cyclic_colormap)
