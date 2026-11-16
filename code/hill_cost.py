"""Numpy port of the HILL cost (Li et al. 2014) as in Aletheia's HILL.m f_cal_cost. cost(img uint8 HxW) -> float64 HxW."""
import numpy as np
from scipy.ndimage import convolve, uniform_filter
HF1 = np.array([[-1, 2, -1], [2, -4, 2], [-1, 2, -1]], float)
def hill_cost(img):
    x = img.astype(np.float64)
    R1 = convolve(x, HF1, mode="reflect")
    W1 = uniform_filter(np.abs(R1), size=3, mode="reflect")
    rho = 1.0 / (W1 + 1e-10)
    return uniform_filter(rho, size=15, mode="reflect")
