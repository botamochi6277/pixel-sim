import numpy as np


def compute_luminance(red: np.ndarray, green: np.ndarray, blue: np.ndarray):
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue
