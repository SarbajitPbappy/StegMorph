"""SRM-lite features: 6 residual filters, quantised (q=1) and truncated (T=2), 4-pixel horizontal+vertical
co-occurrences, symmetrised (merged by +/- sign). Simplified stand-in for SRM/maxSRM, NOT the 34,671-d original."""
import numpy as np
from scipy.signal import convolve2d
F = {"d1": np.array([[-1, 1]]), "d2": np.array([[1, -2, 1]]), "d3": np.array([[-1, 3, -3, 1]]),
     "kb": np.array([[-1,2,-1],[2,-4,2],[-1,2,-1]])/4.0, "s5": np.array([[-1,2,-2,2,-1],[2,-6,8,-6,2],[-2,8,-12,8,-2],[2,-6,8,-6,2],[-1,2,-2,2,-1]])/12.0,
     "e3": np.array([[-1,2,-1],[2,-4,2],[0,0,0]])/4.0}
T = 2; B = 2*T+1
def _cooc(r, axis):
    if axis == 1: a, b, c, d = r[:, :-3], r[:, 1:-2], r[:, 2:-1], r[:, 3:]
    else: a, b, c, d = r[:-3], r[1:-2], r[2:-1], r[3:]
    idx = (((a+T)*B + (b+T))*B + (c+T))*B + (d+T)
    return np.bincount(idx.ravel(), minlength=B**4).astype(np.float32)
def features(img):
    x = img.astype(np.float32); out = []
    for k, f in F.items():
        r = np.clip(np.round(convolve2d(x, f, mode="valid")), -T, T).astype(np.int64)
        h = _cooc(r, 1) + _cooc(r, 0)
        h2 = _cooc(-r, 1) + _cooc(-r, 0)          # sign symmetrisation
        out.append(((h + h2) / max(h.sum() * 2, 1)))
    return np.concatenate(out)
