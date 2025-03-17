from typing import NamedTuple

import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit


class SpectrumParam(NamedTuple):
    z: list[np.complex128]
    f: list[float]  # Hz


class SineWaveParam(NamedTuple):
    amp: list[float]
    freq: list[float]
    init_phase: list[float]

    offset: float  # direct current factor

    @classmethod
    def from_spectrum(cls, spectrum: SpectrumParam):

        offset = float(spectrum.z[0].real)
        amp = [0.0] * (len(spectrum.z) - 1)
        phase = [0.0] * (len(spectrum.z) - 1)
        for i in range(len(spectrum.z) - 1):
            a = spectrum.z[i + 1].real
            b = -spectrum.z[i + 1].imag

            amp[i] = float(abs(spectrum.z[i + 1]))
            phase[i] = float(np.arctan2(a, b))
        return cls(amp, spectrum.f[1:], phase, offset)

    def to_dict(self):
        return dict(
            amp=self.amp, freq=self.freq, init_phase=self.init_phase, offset=self.offset
        )


def compute_cyclic_param(
    red: np.ndarray, green: np.ndarray, blue: np.ndarray, order: int = 4
):

    num = len(red)
    t = np.linspace(0, 1.0, num=num)
    # compute values in freq space
    freq = np.fft.fftfreq(num, d=t[1])
    # https://numpy.org/doc/2.1/reference/generated/numpy.fft.fft.html#numpy.fft.fft
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
        SpectrumParam(
            (r_fft[r_order[:order]] / (num * 0.5)).tolist(),
            (freq[r_order[:order]]).tolist(),
        ),
        SpectrumParam(
            (g_fft[g_order[:order]] / (num * 0.5)).tolist(),
            freq[g_order[:order]].tolist(),
        ),
        SpectrumParam(
            (b_fft[b_order[:order]] / (num * 0.5)).tolist(),
            freq[b_order[:order]].tolist(),
        ),
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


def compute_sine_color(
    sine_params: tuple[SineWaveParam, SineWaveParam, SineWaveParam], num: int = 101
):
    t = np.linspace(0, 1.0, num=num)
    rgb = np.zeros((num, 3))
    for channel_idx in range(3):
        param = sine_params[channel_idx]
        rgb[:, channel_idx] += param.offset
        for j in range(len(param.amp)):
            rgb[:, channel_idx] += param.amp[j] * np.sin(
                2.0 * np.pi * param.freq[j] * t + param.init_phase[j]
            )
    rgb[rgb > 1.0] = 1.0
    rgb[rgb < 0.0] = 0.0
    return rgb[:, 0], rgb[:, 1], rgb[:, 2]


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


def compute_sine_params_from_colors(
    color1: tuple[float, float, float], color2: tuple[float, float, float]
):
    amps = [0.5 * (color1[i] - color2[i]) for i in range(3)]
    return [
        SineWaveParam([amps[i]], [1.0], [np.pi / 2], 0.5 * (color1[i] + color2[i]))
        for i in range(3)
    ]
