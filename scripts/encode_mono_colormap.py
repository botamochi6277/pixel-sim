import json

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.axes import Axes

import pixel_sim
from pixel_sim.colormaps import COLORMAP_DIVERGING
from pathlib import Path
from PIL import ImageColor
from matplotlib.colors import LinearSegmentedColormap


def encode_mono_colormap(
    cmap_name: str,
    num: int = 101,
    order: int = 4,
    show: bool = False,
):
    print(f"encoding {cmap_name} ...")  # ['Spectral', 'coolwarm', 'bwr']
    t = np.linspace(0.0, 1.0, num=num)
    if cmap_name in COLORMAP_DIVERGING:
        colors = COLORMAP_DIVERGING[cmap_name]
        rgb1 = np.array(ImageColor.getcolor(colors[0], "RGB")) / 255
        rgb2 = np.array(ImageColor.getcolor(colors[1], "RGB")) / 255
        rgb3 = np.array(ImageColor.getcolor(colors[2], "RGB")) / 255
        cdict = {
            "red": [
                (0.0, rgb1[0], rgb1[0]),
                (0.5, rgb2[0], rgb2[0]),
                (1.0, rgb3[0], rgb3[0]),
            ],
            "green": [
                (0.0, rgb1[1], rgb1[1]),
                (0.5, rgb2[1], rgb2[1]),
                (1.0, rgb3[1], rgb3[1]),
            ],
            "blue": [
                (0.0, rgb1[2], rgb1[2]),
                (0.5, rgb2[2], rgb2[2]),
                (1.0, rgb3[2], rgb3[2]),
            ],
        }
        cmap = LinearSegmentedColormap(cmap_name, cdict)
        rgba = cmap(t)
        poly_params = pixel_sim.analysis.compute_poly_param(
            rgba[:, 0], rgba[:, 1], rgba[:, 2], order=order
        )

    else:
        r_cmap, g_cmap, b_cmap = pixel_sim.color.get_color_of_colormap(
            cmap_name, num=num
        )
        poly_params = pixel_sim.analysis.compute_poly_param(
            r_cmap, g_cmap, b_cmap, order
        )

    print(f"encoding completed")

    dst_data = {
        "name": cmap_name,
        "type": "poly",
        "red": poly_params[0].tolist(),
        "green": poly_params[1].tolist(),
        "blue": poly_params[2].tolist(),
    }

    r, g, b = pixel_sim.analysis.compute_poly_color(poly_params, num=num)

    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        sharex="col",
        sharey="row",
        layout="tight",
        figsize=(600 / 72, 200 / 72),
    )

    axes: list[list[Axes]]
    t = np.linspace(0.0, 1.0, num=num)
    pixel_sim.plotting.plot_rgb_curve(t, r, g, b, ax=axes[0], show_legend=False)
    axes[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    axes[0].set_title(f"{cmap_name}")
    axes[0].set_ylim((-0.1, 1.1))
    axes[0].set_xlim([-0.05, 1.05])

    pixel_sim.plotting.plot_color_ribbon(t, r, g, b, ax=axes[1])

    img_path = Path(__file__).parent.joinpath(f"../assets/{cmap_name}.png")
    fig.savefig(img_path)
    # fig.show()
    if show:
        plt.show()

    dst_path = Path(__file__).parent.joinpath(f"../assets/{cmap_name}.json")
    with open(dst_path, "w") as f:
        json.dump(
            dst_data,
            f,
            indent=4,
        )


if __name__ == "__main__":
    Fire(encode_mono_colormap)
