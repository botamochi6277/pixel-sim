import json

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire
from matplotlib.colors import LinearSegmentedColormap
from PIL import ImageColor

import pixel_sim


# https://pystyle.info/matplotlib-master-of-colormap/
def create_colormap(
    color1: str,
    color2: str,
    color3: str,
    name="custom",
    is_encode: bool = False,
    is_cyclic: bool = False,
    order: int = 4,
):
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
    cmap = LinearSegmentedColormap(name, cdict)

    num = 101
    t = np.linspace(0.0, 1.0, num=num)

    rgba = cmap(t)

    t2 = np.linspace(-1.0, 1.0, num=num)

    # print(f"rgba: {rgba}")

    ncols = 2 if is_encode else 1
    fig, axes = plt.subplots(
        nrows=3,
        ncols=ncols,
        sharex="col",
        sharey="row",
        height_ratios=(1, 0.25, 0.25),
    )

    ax = axes[0] if not is_encode else axes[0][0]
    pixel_sim.plotting.plot_rgb_curve(
        t2, rgba[:, 0], rgba[:, 1], rgba[:, 2], ax=ax, show_legend=(not is_encode)
    )
    ax = axes[1] if not is_encode else axes[1][0]
    pixel_sim.plotting.plot_color_ribbon(t2, rgba[:, 0], rgba[:, 1], rgba[:, 2], ax=ax)

    rgb_screen = np.vstack(
        (
            pixel_sim.color.apply_screen(np.ones_like(rgba[:, 0]) * 0.5, rgba[:, 0]),
            pixel_sim.color.apply_screen(np.ones_like(rgba[:, 0]) * 0.5, rgba[:, 1]),
            pixel_sim.color.apply_screen(np.ones_like(rgba[:, 0]) * 0.5, rgba[:, 2]),
        )
    ).T

    ax = axes[2] if not is_encode else axes[2][0]
    pixel_sim.plotting.plot_color_ribbon(
        t2, rgb_screen[:, 0], rgb_screen[:, 1], rgb_screen[:, 2], ax=ax
    )

    ax.set_xlim(([-1.1, 1.1]))

    if is_encode:
        if is_cyclic:
            cyclic_params = pixel_sim.analysis.compute_cyclic_param(
                rgba[:, 0], rgba[:, 1], rgba[:, 2], order=order
            )
            rgb_fit = np.vstack(
                pixel_sim.analysis.compute_cyclic_color(cyclic_params)
            ).T

            data = {
                "name": name,
                "type": "cyclic",
                "red": {"f": cyclic_params[0].f, "z": cyclic_params[0].z},
                "green": {"f": cyclic_params[1].f, "z": cyclic_params[1].z},
                "blue": {"f": cyclic_params[2].f, "z": cyclic_params[2].z},
            }
        else:
            poly_params = pixel_sim.analysis.compute_poly_param(
                rgba[:, 0], rgba[:, 1], rgba[:, 2], order=order
            )
            rgb_fit = np.vstack(
                pixel_sim.analysis.compute_poly_color(poly_params, num=num)
            ).T

            data = {
                "name": name,
                "type": "poly",
                "red": poly_params[0].tolist(),
                "green": poly_params[1].tolist(),
                "blue": poly_params[2].tolist(),
            }

        json_name = f"{name}.json"
        with open(json_name, "w") as fp:
            json.dump(data, fp)
        print(f"{json_name} was written")
        ax = axes[0][1]

        pixel_sim.plotting.plot_rgb_curve(
            t2,
            rgb_fit[:, 0],
            rgb_fit[:, 1],
            rgb_fit[:, 2],
            ax=ax,
            show_legend=is_encode,
        )

        ax = axes[1][1]
        pixel_sim.plotting.plot_color_ribbon(
            t2,
            rgb_fit[:, 0],
            rgb_fit[:, 1],
            rgb_fit[:, 2],
            ax=ax,
        )

        rgb_screen2 = np.vstack(
            (
                pixel_sim.color.apply_screen(
                    np.ones_like(rgb_fit[:, 0]) * 0.5, rgb_fit[:, 0]
                ),
                pixel_sim.color.apply_screen(
                    np.ones_like(rgb_fit[:, 0]) * 0.5, rgb_fit[:, 1]
                ),
                pixel_sim.color.apply_screen(
                    np.ones_like(rgb_fit[:, 0]) * 0.5, rgb_fit[:, 2]
                ),
            )
        ).T

        ax = axes[2][1]
        pixel_sim.plotting.plot_color_ribbon(
            t2,
            rgb_screen2[:, 0],
            rgb_screen2[:, 1],
            rgb_screen2[:, 2],
            ax=ax,
        )
        ax.set_xlim(([-1.1, 1.1]))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    Fire(create_colormap)
