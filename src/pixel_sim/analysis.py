from typing import NamedTuple

import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit


class SpectrumParam(NamedTuple):
    z: list[np.complex128]
    f: list[float]


def compute_cyclic_param(
    red: np.ndarray, green: np.ndarray, blue: np.ndarray, order: int = 4
):

    num = len(red)
    t = np.linspace(0, 1.0, num=num)
    # compute values in freq space
    freq = np.fft.fftfreq(num, d=t[1])

    r_fft = np.fft.fft(red)
    r_amp = abs(r_fft / (num * 0.5))

    g_fft = np.fft.fft(green)
    g_amp = abs(g_fft / (num * 0.5))

    b_fft = np.fft.fft(blue)
    b_amp = abs(b_fft / (num * 0.5))

    # picking up significant freq factor
    r_order = np.argsort(r_amp[: int(num * 0.5)])[::-1]
    g_order = np.argsort(g_amp[: int(num * 0.5)])[::-1]
    b_order = np.argsort(b_amp[: int(num * 0.5)])[::-1]
    # dc params
    r_fft[0] *= 0.5
    g_fft[0] *= 0.5
    b_fft[0] *= 0.5
    return (
        SpectrumParam(r_fft[r_order[:order]] / (num * 0.5), freq[r_order[:order]]),
        SpectrumParam(g_fft[g_order[:order]] / (num * 0.5), freq[g_order[:order]]),
        SpectrumParam(b_fft[b_order[:order]] / (num * 0.5), freq[b_order[:order]]),
    )


def compute_poly_param(
    red: np.ndarray, green: np.ndarray, blue: np.ndarray, order: int = 6
):
    # get rgb value from colormap
    num = len(red)
    t = np.linspace(0, 1.0, num=num)

    # init weight
    weight = np.ones(num)
    weight[0] = 1e3
    weight[-1] = 1e3
    # Polynomial coefficients, highest power first
    r_param = np.polyfit(t, red, order, w=weight)
    g_param = np.polyfit(t, green, order, w=weight)
    b_param = np.polyfit(t, blue, order, w=weight)
    # reverse for lowest power first
    return r_param[::-1], g_param[::-1], b_param[::-1]


def compute_cyclic_color(
    cyclic_params: tuple[SpectrumParam, SpectrumParam, SpectrumParam], num: int = 101
):
    t = np.linspace(0, 1.0, num=num)
    r_spectrum, g_spectrum, b = cyclic_params
    red = np.zeros_like(t)
    for z, f in zip(r_spectrum.z, r_spectrum.f):
        red += z.real * np.cos(2 * np.pi * f * t) - z.imag * np.sin(2 * np.pi * f * t)
    green = np.zeros_like(t)
    for z, f in zip(g_spectrum[0], g_spectrum[1]):
        green += z.real * np.cos(2 * np.pi * f * t) - z.imag * np.sin(2 * np.pi * f * t)

    blue = np.zeros_like(t)
    for z, f in zip(b[0], b[1]):
        blue += z.real * np.cos(2 * np.pi * f * t) - z.imag * np.sin(2 * np.pi * f * t)

    red[red > 1.0] = 1.0
    red[red < 0.0] = 0.0
    green[green > 1.0] = 1.0
    green[green < 0.0] = 0.0
    blue[blue > 1.0] = 1.0
    blue[blue < 0.0] = 0.0

    return red, green, blue


def compute_poly_color(
    poly_params: tuple[np.ndarray, np.ndarray, np.ndarray], num: int = 101
):
    t = np.linspace(0, 1.0, num=num)
    red_param, green_param, blue_param = poly_params
    red = np.zeros(num)
    for i, a in enumerate(red_param):
        red += a * (t**i)
    green = np.zeros(num)
    for i, a in enumerate(green_param):
        green += a * (t**i)
    blue = np.zeros(num)
    for i, a in enumerate(blue_param):
        blue += a * (t**i)

    # clip
    red[red > 1.0] = 1.0
    red[red < 0.0] = 0.0
    green[green > 1.0] = 1.0
    green[green < 0.0] = 0.0
    blue[blue > 1.0] = 1.0
    blue[blue < 0.0] = 0.0
    return red, green, blue
