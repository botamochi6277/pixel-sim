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


def wipe(t: float, x: np.ndarray, name: str = "heviside"):
    # https://numpy.org/doc/stable/reference/generated/numpy.heaviside.html
    delta = 0.01
    if name == "quad":
        duration = 0.25
        # a = remap((1.0 - abs(t)), 0.0, 1.0, -1 * duration, 1.0)
        f = np.vectorize(lambda x: easeInOutQuad(x, duration))
        return 1.0 * f((t) - (x / (1.0 + 2 * duration)))
    # a = remap((1.0 - abs(t)), 0.0, 1.0, -0.1, 1.1)

    return np.heaviside((t - delta) - (x / (1.0 + 2 * delta)), 1.0)


def pulse(t: np.ndarray, x: np.ndarray, name: str = "", width: float = 0.1):

    f1 = np.vectorize(lambda x: easeInOutQuad(x + width / 2, width / 2))
    f2 = np.vectorize(lambda x: -1.0 * easeInOutQuad(x - width / 2, width / 2))
    v = 1.0 + 3.5 * width
    y = 1.0 * (f1((t - width) - x / v) + f2((t - width) - x / v))
    return y


def saw_wave(t: np.ndarray, x: np.ndarray):
    v = 1.001
    return np.ceil(t - x / v) - (t - x / v)


def sin_wave(t: np.ndarray, x: np.ndarray):
    return 0.5 * (np.sin(2.0 * np.pi * 1.0 * (t - x))) + 0.5


def wave(x: np.ndarray, t: float, name: str = "sin"):
    d = t / abs(t) if abs(t) > 1e-3 else 1.0
    a = 1.0 - abs(t)
    if name == "saw":
        return d * saw_wave(x - a)

    return d * (0.5 * (np.sin(2.0 * np.pi * 1.0 * (x - a))) + 0.5)
