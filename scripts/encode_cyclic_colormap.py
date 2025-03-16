import json

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.axes import Axes

import pixel_sim
import pixel_sim.colormaps
from PIL import ImageColor


def encode_cyclic_colormap(cmap_name: str, num: int = 101, min_lumi: float = 0.5):
    print(f"encoding {cmap_name} ...")  # ['twilight', 'twilight_shifted', 'hsv']
    t = np.linspace(0.0, 1.0, num=num)

    if cmap_name in pixel_sim.colormaps.COLORMAP_SAMPLES:
        colors = pixel_sim.colormaps.COLORMAP_SAMPLES[cmap_name]
        rgb1 = np.array(ImageColor.getcolor(colors[0], "RGB")) / 255
        rgb2 = np.array(ImageColor.getcolor(colors[1], "RGB")) / 255
        params = pixel_sim.analysis.compute_sine_params_from_colors(rgb1, rgb2)
        r, g, b = [
            p.amp * np.sin(p.angular_freq * t + p.init_phase) + p.offset for p in params
        ]
    else:
        r_cmap, g_cmap, b_cmap = pixel_sim.color.get_color_of_colormap(cmap_name)
        spectrum_params = pixel_sim.analysis.compute_cyclic_param(
            r_cmap, g_cmap, b_cmap
        )

        print(f"encoding completed")
        r, g, b = pixel_sim.analysis.compute_cyclic_color(spectrum_params, num=num)

    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="col",
        sharey="row",
        layout="tight",
        figsize=(600 / 72, 200 / 72),
    )

    axes: list[list[Axes]]

    pixel_sim.plotting.plot_rgb_curve(t, r, g, b, ax=axes[0], show_legend=False)
    axes[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    axes[0].set_title(f"{cmap_name}")
    axes[0].set_ylim((-0.1, 1.1))

    pixel_sim.plotting.plot_color_ribbon(t, r, g, b, ax=axes[1])
    # axes[1].set_title(f"decode (target)")
    plt.tight_layout()
    # fig.show()
    plt.show()


if __name__ == "__main__":
    Fire(encode_cyclic_colormap)
