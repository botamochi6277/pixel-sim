import matplotlib.pyplot as plt
import numpy as np
from fire import Fire

from pixel_sim import shapes


def plot_easing(duration: float = 1.0, a: float = 0.0):

    t = np.linspace(-1, 2, num=150)

    f = np.vectorize(lambda x: shapes.easeInOutQuad(x, duration))
    y = f(t - a)
    plt.plot(t, y)
    plt.xlabel("t")
    plt.ylabel("y")
    plt.show()


if __name__ == "__main__":
    Fire(plot_easing)
