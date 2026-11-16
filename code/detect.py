"""Statistical detectors. Each returns a scalar score where larger = more likely stego."""
import numpy as np
from scipy.stats import chi2

def chi_square_score(img):
    """Westfeld pairs-of-values test over the full image; score = -log10(1-cdf) style: larger => more likely embedded."""
    h = np.bincount(img.flatten(), minlength=256).astype(float)
    ev, od = h[0::2], h[1::2]; avg = (ev+od)/2; m = avg > 4
    if m.sum() < 2: return 0.0
    stat = np.sum((ev[m]-avg[m])**2/avg[m])
    # small stat => pairs equalised => embedded. p_embed = P(chi2 >= stat); score = that probability
    return float(chi2.sf(stat, m.sum()-1))

def _disc(g): return np.abs(np.diff(g, axis=1)).sum(axis=1)
def _flip(g, m):
    g = g.copy().astype(np.int64)
    for j, mj in enumerate(m):
        x = g[:, j]
        if mj == 1: g[:, j] = x ^ 1
        elif mj == -1: g[:, j] = ((x + 1) ^ 1) - 1
    return g
def rs_score(img, mask=(0, 1, 1, 0)):
    """Fridrich RS analysis: returns estimated relative message length p (rate in LSB-plane units; ~ bpp*2 for random LSB)."""
    f = img.astype(np.int64).flatten(); f = f[: len(f)//4*4].reshape(-1, 4); m = list(mask); mn = [-v for v in m]
    def rsd(G, mm):
        d0 = _disc(G); d1 = _disc(_flip(G, mm)); return (d1 > d0).mean() - (d1 < d0).mean()
    d0, dn0 = rsd(f, m), rsd(f, mn)
    G1 = f ^ 1
    d1, dn1 = rsd(G1, m), rsd(G1, mn)
    a = 2*(d1 + d0); b = dn0 - dn1 - d1 - 3*d0; c = d0 - dn0
    if abs(a) < 1e-12: x = -c/b if abs(b) > 1e-12 else 0.0
    else:
        disc = max(b*b - 4*a*c, 0); r1 = (-b + np.sqrt(disc))/(2*a); r2 = (-b - np.sqrt(disc))/(2*a)
        x = r1 if abs(r1) < abs(r2) else r2
    return float(x / (x - 0.5)) if abs(x - 0.5) > 1e-12 else 0.0

def spa_score(img):
    """Sample-pair analysis (Dumitrescu et al.) on horizontal pairs. Returns estimated rate p.
    Quadratic: 0.5*W*p^2 + (2X-P)*p + (Y-X) = 0. VALIDATION REQUIRED: see tests/test_pipeline.py."""
    u = img.astype(np.int64); a, b = u[:, :-1].flatten(), u[:, 1:].flatten(); P = a.size
    ev = (b % 2 == 0)
    X = np.sum((ev & (a < b)) | (~ev & (a > b)))
    Y = np.sum((ev & (a > b)) | (~ev & (a < b)))
    W = np.sum(((a >> 1) == (b >> 1)) & (a != b))
    qa, qb, qc = 0.5*W, (2*X - P), (Y - X)
    if abs(qa) < 1e-12: return 0.0
    disc = max(qb*qb - 4*qa*qc, 0)
    r = [(-qb + np.sqrt(disc))/(2*qa), (-qb - np.sqrt(disc))/(2*qa)]
    return float(min(r, key=abs))
