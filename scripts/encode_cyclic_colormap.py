import json

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.axes import Axes

import pixel_sim
from pixel_sim.colormaps import COLORMAP_SAMPLES
from PIL import ImageColor

from pathlib import Path


def encode_cyclic_colormap(cmap_name: str, num: int = 101, show: bool = False):
    print(f"encoding {cmap_name} ...")  # ['twilight', 'twilight_shifted', 'hsv']
    t = np.linspace(0.0, 1.0, num=num)

    if cmap_name in COLORMAP_SAMPLES:
        colors = COLORMAP_SAMPLES[cmap_name]
        rgb1 = np.array(ImageColor.getcolor(colors[0], "RGB")) / 255
        rgb2 = np.array(ImageColor.getcolor(colors[1], "RGB")) / 255
        params = pixel_sim.analysis.compute_sine_params_from_colors(rgb1, rgb2)

    else:
        r_cmap, g_cmap, b_cmap = pixel_sim.color.get_color_of_colormap(cmap_name)
        spectrum_params = pixel_sim.analysis.compute_cyclic_param(
            r_cmap, g_cmap, b_cmap
        )

        params = [
            pixel_sim.analysis.SineWaveParam.from_spectrum(p) for p in spectrum_params
        ]

    r, g, b = pixel_sim.analysis.compute_sine_color(params, num=num)

    # print(f"encoding completed")
    # r, g, b = pixel_sim.analysis.compute_cyclic_color(spectrum_params, num=num)

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
    axes[0].set_xlim([-0.05, 1.05])

    pixel_sim.plotting.plot_color_ribbon(t, r, g, b, ax=axes[1])
    # axes[1].set_title(f"decode (target)")
    plt.tight_layout()

    img_path = Path(__file__).parent.joinpath(f"../assets/{cmap_name}.png")
    fig.savefig(img_path)
    # fig.show()
    if show:
        plt.show()

    dst_path = Path(__file__).parent.joinpath(f"../assets/{cmap_name}.json")
    with open(dst_path, "w") as f:
        json.dump(
            dict(
                red=params[0].to_dict(),
                green=params[1].to_dict(),
                blue=params[2].to_dict(),
            ),
            f,
            indent=4,
        )


def encode_cyclic_colormaps(cmap_names: str, num: int = 101, show: bool = False):

    if cmap_names == "all":

        targets = ["twilight", "twilight_shifted", "hsv"] + list(
            COLORMAP_SAMPLES.keys()
        )

        for cmap_name in targets:
            encode_cyclic_colormap(cmap_name, num, show)
        return

    for cmap_name in cmap_names.split(","):
        encode_cyclic_colormap(cmap_name, num, show)


if __name__ == "__main__":
    Fire(encode_cyclic_colormaps)
