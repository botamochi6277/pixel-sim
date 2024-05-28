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
        duration = 0.25
        a = remap((1.0 - abs(t)), 0.0, 1.0, -1 * duration, 1.0)
        f = np.vectorize(lambda x: easeInOutQuad(x, duration))
        return d * f(x - a)
    a = remap((1.0 - abs(t)), 0.0, 1.0, -0.1, 1.1)
    return d * np.heaviside(x - a, 1.0)


def pulse(x: np.ndarray, t: float, name: str = ""):
    d = t / abs(t) if abs(t) > 1e-3 else 1.0
    width = 0.1
    a = remap((1.0 - abs(t)), 0.0, 1.0, -width, 1.0 + width)

    f1 = np.vectorize(lambda x: easeInOutQuad(x + width, width))
    f2 = np.vectorize(lambda x: -1.0 * easeInOutQuad(x - width, width))
    y = d * (f1(x - a) + f2(x - a))
    return y


def saw_wave(x: np.ndarray, period: float = 1.0):
    xx = x / (period + 1e-9)
    return xx - np.floor(xx + 0.5) + 0.5


def wave(x: np.ndarray, t: float, name: str = "sin"):
    d = t / abs(t) if abs(t) > 1e-3 else 1.0
    a = 1.0 - abs(t)
    if name == "saw":
        return d * saw_wave(x - a)

    return d * (0.5 * (np.sin(2.0 * np.pi * 1.0 * (x - a))) + 0.5)
