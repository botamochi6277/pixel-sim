import numpy as np


def remap(
    x: float | np.ndarray, in_min: float, in_max: float, out_min: float, out_max: float
):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def easeInOutQuad(x: float, duration: float = 1.0):
    if x < 0.0:
        return 0.0
    elif x < duration / 2:
        return 2 * ((x / duration) ** 2)
    elif x < duration:
        return 1 - ((-2 * (x / duration) + 2) ** 2) / 2
    else:
        return 1.0


def wipe(x: np.ndarray, t: float, name: str = "heviside"):
    # https://numpy.org/doc/stable/reference/generated/numpy.heaviside.html

    d = t / abs(t) if abs(t) > 1e-3 else 1.0

    if name == "quad":
        a = remap((1.0 - abs(t)), 0.0, 1.0, -0.15, 1.15)
        f = np.vectorize(lambda x: easeInOutQuad(x, 0.1))
        return d * f(x - a)
    a = remap((1.0 - abs(t)), 0.0, 1.0, -0.1, 1.1)
    return d * np.heaviside(x - a, 1.0)
