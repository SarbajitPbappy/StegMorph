"""StegMorph-recon: reconstruction from the plan's description (assumptions A1-A5 in state/DECISIONS.md). NOT the original code."""
import numpy as np
from embed import RANGES, _rng_of
LOW_MAX, HIGH_MIN = 123, 132     # cover-mean guard bands; decoder: stego mean <=124 -> low, >=131 -> PVD
HEADER_BITS = 32; REP = 3

def pairs_of(img):
    f = img.astype(np.int32).flatten(); n = len(f)//2*2
    return f[0:n:2], f[1:n:2]
def capacity_and_branch(img):
    p1, p2 = pairs_of(img); m = (p1 + p2)//2; d = np.abs(p1 - p2)
    low = m <= LOW_MAX
    pvd = (m >= HIGH_MIN) & (m <= 222) & (d < 64)
    cap = np.zeros(len(p1), np.int32); cap[low] = 2
    nb = np.select([d <= 7, d <= 15, d <= 31, d <= 63], [3, 3, 4, 5], 0)
    cap[pvd] = nb[pvd]
    return cap, low, pvd
def expected_cost(img, rng, draws=12):
    """Expected squared error per pair under uniform random bits (Monte Carlo for PVD, analytic 1.0 for LSB)."""
    p1, p2 = pairs_of(img); cap, low, pvd = capacity_and_branch(img); cost = np.full(len(p1), np.inf)
    cost[low] = 1.0                                   # each pixel flips w.p. 1/2 by +-1 -> E[err]=0.5+0.5
    idx = np.where(pvd)[0]
    if len(idx):
        a, b = p1[idx], p2[idx]; d = np.abs(a-b); lo = np.select([d<=7,d<=15,d<=31],[0,8,16],32); nb = cap[idx]
        acc = np.zeros(len(idx))
        for _ in range(draws):
            bv = rng.integers(0, 2**nb); dn = lo + bv; m = np.abs(dn - d); c = (m+1)//2; fl = m//2
            acc += c*c + fl*fl
        cost[idx] = acc/draws
    return cost
def total_bits(nbits_payload): return (HEADER_BITS + nbits_payload)*REP

# ---- selection strategies: return boolean mask over pairs with capacity >= need ----
def _repair(mask, cap, need, rng):
    c = cap[mask].sum()
    if c < need:
        free = np.where(~mask & (cap > 0))[0]; free = free[rng.permutation(len(free))]
        cs = np.cumsum(cap[free]); k = np.searchsorted(cs, need - c) + 1; mask[free[:k]] = True
    else:
        sel = np.where(mask)[0]; sel = sel[rng.permutation(len(sel))]
        for i in sel:
            if c - cap[i] >= need: mask[i] = False; c -= cap[i]
    return mask
def select_random(cap, need, rng):
    m = np.zeros(len(cap), bool); return _repair(m, cap, need, rng)
def select_greedy(cap, cost, need):
    order = np.argsort(cost/np.maximum(cap, 1)); order = order[cap[order] > 0]
    cs = np.cumsum(cap[order]); k = np.searchsorted(cs, need) + 1; m = np.zeros(len(cap), bool); m[order[:k]] = True; return m
def select_ga(cap, cost, need, rng, pop=24, gens=30, pm=None):
    elig = np.where(cap > 0)[0]; G = len(elig); capE = cap[elig]; costE = cost[elig]
    if capE.sum() < need: raise ValueError("capacity")
    pm = pm or 2.0/G
    P = np.zeros((pop, G), bool)
    for i in range(pop): P[i] = _repair(np.zeros(G, bool), capE, need, rng)
    fit = lambda P: (P*costE).sum(1)
    for _ in range(gens):
        f = fit(P); new = [P[np.argmin(f)].copy()]                      # elitism
        while len(new) < pop:
            a = min(rng.integers(0, pop, 3), key=lambda i: f[i]); b = min(rng.integers(0, pop, 3), key=lambda i: f[i])
            x = np.where(rng.random(G) < 0.5, P[a], P[b]); x ^= (rng.random(G) < pm)
            new.append(_repair(x, capE, need, rng))
        P = np.array(new)
    best = P[np.argmin(fit(P))]; m = np.zeros(len(cap), bool); m[elig[best]] = True; return m

# ---- embedding / extraction given a selection mask (side-information key) ----
def _bits_in(payload):
    hdr = np.array([int(c) for c in format(len(payload), f"0{HEADER_BITS}b")], np.uint8)
    return np.repeat(np.concatenate([hdr, payload]), REP)
def embed(img, payload, mask):
    f = img.astype(np.int32).flatten(); out = f.copy(); bits = _bits_in(payload); k = 0
    cap, low, pvd = capacity_and_branch(img)
    for i in np.where(mask)[0]:
        a, b = f[2*i], f[2*i+1]
        if low[i]:
            ch = bits[k:k+2]; ch = np.concatenate([ch, np.zeros(2-len(ch), np.uint8)]); k += 2
            out[2*i] = (a & ~1) | ch[0]; out[2*i+1] = (b & ~1) | ch[1]
        else:
            d = abs(a-b); lo, nb = _rng_of(d); ch = bits[k:k+nb]; ch = np.concatenate([ch, np.zeros(nb-len(ch), np.uint8)]); k += nb
            dn = lo + int("".join(map(str, ch)), 2); m = abs(dn-d); c, fl = (m+1)//2, m//2
            if a >= b: q1, q2 = (a+c, b-fl) if dn > d else (a-c, b+fl)
            else:       q1, q2 = (a-fl, b+c) if dn > d else (a+fl, b-c)
            out[2*i], out[2*i+1] = q1, q2
    assert k >= len(bits)
    return out.astype(np.uint8).reshape(img.shape)
def extract(stego, mask):
    f = stego.astype(np.int32).flatten(); got = []
    for i in np.where(mask)[0]:
        a, b = f[2*i], f[2*i+1]; m = (a+b)//2
        if m <= LOW_MAX+1: got += [a & 1, b & 1]
        else:
            d = abs(a-b); lo, nb = _rng_of(d); got += [int(c) for c in format(d-lo, f"0{nb}b")]
    got = np.array(got, np.uint8)
    n_hdr = HEADER_BITS*REP; g = got[:n_hdr].reshape(-1, REP); hdr = (g.sum(1) >= 2).astype(int)
    n = int("".join(map(str, hdr)), 2); body = got[n_hdr:n_hdr + n*REP].reshape(-1, REP)
    return (body.sum(1) >= 2).astype(np.uint8)
