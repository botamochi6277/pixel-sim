import json

import matplotlib.pyplot as plt
import numpy as np
from fire import Fire

import pixel_sim


def encode_cyclic_colormap(cmap_name: str, num: int = 101):
    print(f"encoding {cmap_name} ...")
    cyclic_params = pixel_sim.analysis.compute_cyclic_param(cmap_name, num=num)
    print(f"encoding completed")
    r, g, b = pixel_sim.analysis.compute_cyclic_color(cyclic_params)

    fig, axes = plt.subplots(3, sharex=True, sharey=True)
    fig.tight_layout()

    t = np.linspace(0.0, 1.0, num=num)
    pixel_sim.plotting.plot_rgb_curve(t, r, g, b, ax=axes[0])
    axes[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    axes[0].set_title(f"{cmap_name}")
    pixel_sim.plotting.plot_color_ribbon(t, r, g, b, ax=axes[1])

    plt.show()


if __name__ == "__main__":
    Fire(encode_cyclic_colormap)
