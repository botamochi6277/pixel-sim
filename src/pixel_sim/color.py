import numpy as np


def compute_luminance(red: np.ndarray, green: np.ndarray, blue: np.ndarray):
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def apply_screen(top: np.ndarray, bottom: np.ndarray):
    return bottom + top - bottom * top


def apply_screen_inverse(top: np.ndarray, y: np.ndarray):

    bottom = (y - top) / (1.0 - top + 1e-9)
    bottom[bottom < 0.0] = 0.0
    bottom[1.0 < bottom] = 1.0
    return bottom
