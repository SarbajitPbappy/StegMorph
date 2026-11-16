"""Embedding simulators for the StegMorph evaluation harness (Phase 0.4).
STAND-INS: these are generic schemes, not StegMorph. StegMorph spec awaits the GA notebook."""
import numpy as np
from scipy.ndimage import convolve, correlate

def _bits(n, rng): return rng.integers(0, 2, n, dtype=np.uint8)

# ---- LSB ----
def lsb_embed(img, bits, key=None):
    """key=None: sequential positions; else keyed random permutation. Returns (stego, positions)."""
    flat = img.flatten().astype(np.uint8)
    n = len(bits); assert n <= flat.size
    pos = np.arange(n) if key is None else np.random.default_rng(key).permutation(flat.size)[:n]
    flat[pos] = (flat[pos] & 0xFE) | bits
    return flat.reshape(img.shape), pos

def lsb_extract(stego, n, key=None):
    flat = stego.flatten()
    pos = np.arange(n) if key is None else np.random.default_rng(key).permutation(flat.size)[:n]
    return (flat[pos] & 1).astype(np.uint8)

# ---- PVD-6 (Wu-Tsai style, ranges capped at d<64 so extraction is exactly invertible) ----
RANGES = [(0, 7, 3), (8, 15, 3), (16, 31, 4), (32, 63, 5)]  # (lo, hi, bits)
def _eligible(p1, p2):
    d = abs(int(p1) - int(p2)); m = (int(p1) + int(p2)) // 2
    return d < 64 and 33 <= m <= 222
def _rng_of(d):
    for lo, hi, nb in RANGES:
        if lo <= d <= hi: return lo, nb
def pvd_capacity(img):
    f = img.astype(np.int32).flatten(); f = f[: len(f)//2*2]
    return sum(_rng_of(abs(f[i]-f[i+1]))[1] for i in range(0, len(f), 2) if _eligible(f[i], f[i+1]))
def pvd_embed(img, bits):
    f = img.astype(np.int32).flatten(); out = f.copy(); k = 0
    for i in range(0, len(f)//2*2, 2):
        if k >= len(bits): break
        p1, p2 = int(f[i]), int(f[i+1])
        if not _eligible(p1, p2): continue
        d = abs(p1-p2); lo, nb = _rng_of(d)
        chunk = bits[k:k+nb]
        if len(chunk) < nb: chunk = np.concatenate([chunk, np.zeros(nb-len(chunk), np.uint8)])
        b = int("".join(map(str, chunk)), 2); k += min(nb, len(bits)-k)
        dn = lo + b; m = abs(dn-d); c, fl = (m+1)//2, m//2
        if p1 >= p2: q1, q2 = (p1+c, p2-fl) if dn > d else (p1-c, p2+fl)
        else:        q1, q2 = (p1-fl, p2+c) if dn > d else (p1+fl, p2-c)
        assert 0 <= q1 <= 255 and 0 <= q2 <= 255
        out[i], out[i+1] = q1, q2
    assert k >= len(bits), "payload exceeds PVD capacity"
    return out.astype(np.uint8).reshape(img.shape)
def pvd_extract(stego, n):
    f = stego.astype(np.int32).flatten(); res = []
    for i in range(0, len(f)//2*2, 2):
        if len(res) >= n: break
        if not _eligible(f[i], f[i+1]): continue
        d = abs(f[i]-f[i+1]); lo, nb = _rng_of(d)
        res += [int(c) for c in format(d-lo, f"0{nb}b")]
    return np.array(res[:n], np.uint8)

# ---- HILL-style cost + ternary optimal-coder simulator ----
def hill_cost(img):
    x = img.astype(np.float64)
    KB = np.array([[-1,2,-1],[2,-4,2],[-1,2,-1]], float)
    r = np.abs(correlate(x, KB, mode="reflect"))
    xi = convolve(r, np.ones((3,3))/9, mode="reflect")
    return 1.0 / (convolve(xi, np.ones((15,15))/225, mode="reflect") + 1e-10)
def _entropy(lmb, c):
    e = np.exp(-lmb*c); p = e/(1+2*e); q = 1-2*p
    return float(np.sum(-2*p*np.log2(np.maximum(p,1e-300)) - q*np.log2(np.maximum(q,1e-300))))
def hill_simulate(img, bpp, seed):
    """Simulates optimal-coder +-1 embedding at payload bpp (entropy-matched). No extraction."""
    c = hill_cost(img).flatten(); target = bpp*img.size
    lo, hi = 1e-6, 1e3
    for _ in range(80):
        mid = np.sqrt(lo*hi)
        if _entropy(mid, c) > target: lo = mid
        else: hi = mid
    lmb = np.sqrt(lo*hi); e = np.exp(-lmb*c); p = e/(1+2*e)
    u = np.random.default_rng(seed).random(c.size)
    delta = np.where(u < p, 1, np.where(u < 2*p, -1, 0))
    s = np.clip(img.flatten().astype(np.int32) + delta, 0, 255).astype(np.uint8)
    return s.reshape(img.shape), _entropy(lmb, c)/img.size
