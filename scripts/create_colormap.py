import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.colors import LinearSegmentedColormap
from PIL import ImageColor

import pixel_sim


# https://pystyle.info/matplotlib-master-of-colormap/
def create_colormap(color1: str, color2: str, color3: str):
    rgb1 = np.array(ImageColor.getcolor(color1, "RGB")) / 255
    rgb2 = np.array(ImageColor.getcolor(color2, "RGB")) / 255
    rgb3 = np.array(ImageColor.getcolor(color3, "RGB")) / 255

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
    cmap = LinearSegmentedColormap("custom", cdict)

    num = 101
    t = np.linspace(0.0, 1.0, num=num)

    rgba = cmap(t)

    t2 = np.linspace(-1.0, 1.0, num=num)

    # print(f"rgba: {rgba}")

    fig, axes = plt.subplots(
        nrows=2,
        sharex="col",
        #  ncols=2, sharex="col", sharey="row", height_ratios=(1, 0.25, 0.25)
    )

    pixel_sim.plotting.plot_rgb_curve(
        t2, rgba[:, 0], rgba[:, 1], rgba[:, 2], ax=axes[0], show_legend=True
    )

    pixel_sim.plotting.plot_color_ribbon(
        t2, rgba[:, 0], rgba[:, 1], rgba[:, 2], ax=axes[1]
    )

    axes[0].set_xlim(([-1.1, 1.1]))

    plt.show()


if __name__ == "__main__":
    Fire(create_colormap)
