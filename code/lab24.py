"""Shared library for experiments E24-E34 (see state/CLAIMS.md, pre-registration of 13 Nov 2026).
Everything that builds stego images, extracts features and scores detectors lives here; drivers (exp24.py ...) only choose schemes, payloads and detectors.
Scheme names:
  RANDSEQ ORIG GAMIN GAMINS          StegMorph embedder with random / GA-contrast / GA-min-cost (same budget) / GA-min-cost (stronger search) key
  COSTKEY ANTIKEY                    = K:hill:t:0.33 and K:hill:s:0.33 (lowest / highest HILL-cost third of pixels, random order)
  K:<map>:<t|s>:<f>                  key from the fraction f of pixels ranked most textured (t) or most smooth (s) under map in {hill,std,grad,ent,suni}
  M:<keyscheme>                      operator-matched control: random positions with the same PVD/LSB pair counts as <keyscheme>
  COSTMIX ANTIMIX                    = M:COSTKEY, M:ANTIKEY
  LSBK:<R|C|A>  LSBM:<R|C|A>         keyed LSB replacement / +-1 LSB matching of the same bits with a random / cost-guided / smooth key
  HILLSIM                            numpy HILL simulator;  HILLR, SUNIR: reference simulators run in Octave (loaded from cache)
"""
import os, sys, zlib, json, time, types, numpy as np
sys.modules.setdefault("cv2", types.ModuleType("cv2"))
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
import stegmorph as SM, srm_lite as S
from hill_cost import hill_cost
from scipy.ndimage import uniform_filter, sobel, convolve
from scipy.signal import convolve2d
from numpy.lib.stride_tricks import sliding_window_view

T3 = 3; B3 = 2 * T3 + 1
CACHE = os.path.join(ROOT, "cache"); os.makedirs(CACHE, exist_ok=True)

# ----------------------------------------------------------------------------- cost / texture maps
_hp = np.array([-0.0544158422, 0.3128715909, -0.6756307363, 0.5853546837, 0.0158291053, -0.2840155430, -0.0004724846, 0.1287474266, 0.0173693010, -0.0440882539, -0.0139810279, 0.0087460940, 0.0048703530, -0.0003917404, -0.0006754494, -0.0001174768])
_lp = (-1.0) ** np.arange(len(_hp)) * _hp[::-1]
_SF = [np.outer(_lp, _hp), np.outer(_hp, _lp), np.outer(_hp, _hp)]
def _conv_same(a, f):
    """MATLAB/Octave conv2(a, f, 'same') (offset ceil((size(f)-1)/2); scipy's 'same' differs for even kernels)."""
    full = convolve2d(a, f, mode="full"); o0 = -(-(f.shape[0] - 1) // 2); o1 = -(-(f.shape[1] - 1) // 2); return full[o0:o0 + a.shape[0], o1:o1 + a.shape[1]]
def suni_cost(img):
    """S-UNIWARD distortion rho (Holub et al. 2014), numpy port of the DDE code (sigma = 1, Daubechies-8 directional filters). Checked against the Octave output in code/check_suni.py."""
    x = img.astype(np.float64); k, l = x.shape; ps = 16
    xp = np.pad(x, ps, mode="symmetric"); rho = np.zeros((k, l))
    for F in _SF:
        R = _conv_same(xp, F)
        xi = _conv_same(1.0 / (np.abs(R) + 1.0), np.rot90(np.abs(F), 2))
        if F.shape[0] % 2 == 0: xi = np.roll(xi, 1, axis=0)
        if F.shape[1] % 2 == 0: xi = np.roll(xi, 1, axis=1)
        rho += xi[ps:ps + k, ps:ps + l]
    return rho
def _lstd(x, s=3):
    m = uniform_filter(x, s, mode="reflect"); return np.sqrt(np.maximum(uniform_filter(x * x, s, mode="reflect") - m * m, 0))
def _lent(x, s=5, nb=32):
    q = np.minimum((x // (256 // nb)).astype(int), nb - 1); H = np.zeros(x.shape)
    for b in range(nb):
        p = uniform_filter((q == b).astype(np.float64), s, mode="reflect"); H -= np.where(p > 0, p * np.log2(np.maximum(p, 1e-12)), 0)
    return H
def texscore(img, name):
    """Larger = more textured (lower embedding cost)."""
    x = img.astype(np.float64)
    if name == "hill": return -hill_cost(img)
    if name == "std": return _lstd(x)
    if name == "grad": return np.hypot(sobel(x, 0, mode="reflect"), sobel(x, 1, mode="reflect"))
    if name == "ent": return _lent(x)
    if name == "suni": return -suni_cost(img)
    raise ValueError(name)

# ----------------------------------------------------------------------------- features
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T3, T3)
    def _t(a, b, c):
        idx = ((a + T3) * B3 + (b + T3)) * B3 + (c + T3); cnt = np.bincount(idx.ravel(), minlength=B3 ** 3).astype(np.float64).reshape(B3, B3, B3); return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
    Dh = f(x[:, :-1] - x[:, 1:]); Dv = f(x[:-1] - x[1:]); h = _t(Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:]); v = _t(Dv[:-2], Dv[1:-1], Dv[2:])
    Dd = f(x[:-1, :-1] - x[1:, 1:]); d1 = _t(Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:]); xf = x[:, ::-1]; Da = f(xf[:-1, :-1] - xf[1:, 1:]); d2 = _t(Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:])
    return np.concatenate([((h + v) / 2).ravel(), ((d1 + d2) / 2).ravel()]).astype(np.float32)
def sca_features(img, beta):
    """Selection-channel-aware SRM-lite ('maxSRM-lite'): each 4-pixel co-occurrence window is counted with weight = max of the modification-probability map beta over the pixels the four residuals depend on."""
    x = img.astype(np.float32); out = []; T = S.T; B = S.B
    for k, f in S.F.items():
        r = np.clip(np.round(convolve2d(x, f, mode="valid")), -T, T).astype(np.int64); fh, fw = f.shape
        w = sliding_window_view(beta, (fh, fw)).max((2, 3)).astype(np.float32)
        hh = np.zeros(B ** 4, np.float32)
        for sgn in (1, -1):
            rr = sgn * r
            a, b, c, d = rr[:, :-3], rr[:, 1:-2], rr[:, 2:-1], rr[:, 3:]; idx = (((a + T) * B + (b + T)) * B + (c + T)) * B + (d + T); ww = np.maximum.reduce([w[:, :-3], w[:, 1:-2], w[:, 2:-1], w[:, 3:]])
            hh += np.bincount(idx.ravel(), weights=ww.ravel(), minlength=B ** 4).astype(np.float32)
            a, b, c, d = rr[:-3], rr[1:-2], rr[2:-1], rr[3:]; idx = (((a + T) * B + (b + T)) * B + (c + T)) * B + (d + T); ww = np.maximum.reduce([w[:-3], w[1:-2], w[2:-1], w[3:]])
            hh += np.bincount(idx.ravel(), weights=ww.ravel(), minlength=B ** 4).astype(np.float32)
        out.append(hh / img.size)
    return np.concatenate(out)

# ----------------------------------------------------------------------------- adaptive-embedding probabilities (for the S detector and the numpy HILL simulator)
def _H3(rp, rm, lam):
    e1 = np.exp(-lam * rp); e2 = np.exp(-lam * rm); z = 1 + e1 + e2; p1 = e1 / z; p2 = e2 / z; p0 = 1 / z
    f = lambda p: -p * np.log2(np.maximum(p, 1e-300)); return (f(p1) + f(p2) + f(p0)), p1, p2
def change_probs(img, cost, bits):
    rp = np.minimum(cost, 1e10).copy(); rm = rp.copy(); rp[img == 255] = 1e10; rm[img == 0] = 1e10; lo, hi = 0.0, 1e3
    while _H3(rp, rm, hi)[0].sum() > bits: hi *= 2
    for _ in range(60):
        mid = (lo + hi) / 2
        if _H3(rp, rm, mid)[0].sum() > bits: lo = mid
        else: hi = mid
    _, p1, p2 = _H3(rp, rm, hi); return p1, p2
def hill_embed(img, cost, bits, rng):
    p1, p2 = change_probs(img, cost, bits); u = rng.random(img.shape); y = img.astype(np.float64); y[u < p1] += 1; y[(u >= p1) & (u < p1 + p2)] -= 1
    return np.clip(y, 0, 255).astype(np.uint8)

# ----------------------------------------------------------------------------- keys
def used_pairs(img, key, nb):
    flat = img.ravel(); idx = nP = nL = 0
    for i in range(0, len(key) - 1, 2):
        if idx >= nb: break
        if SM._use_pvd(flat[key[i]], flat[key[i + 1]], SM.PVD_THRESHOLD): nP += 1; idx += 4
        else: nL += 1; idx += 2
    return nP, nL
def random_key(img, rng): n = img.size; return rng.permutation(n)[: (n // 3) // 2 * 2].astype(np.int64)
def mix_key(img, nP, nL, rng, domain=None):
    flat = img.ravel(); n = flat.size; a = rng.integers(0, n, 400000) if domain is None else rng.choice(domain, 400000); b = rng.integers(0, n, 400000) if domain is None else rng.choice(domain, 400000)
    pv = np.abs((flat[a].astype(int) & 0xFC) - (flat[b].astype(int) & 0xFC)) > SM.PVD_THRESHOLD; used = set(); out = []
    for want, mask in ((nP, pv), (nL, ~pv)):
        got = 0
        for j in np.where(mask & (a != b))[0]:
            if got == want: break
            x, y = int(a[j]), int(b[j])
            if x in used or y in used: continue
            used.add(x); used.add(y); out.append((x, y)); got += 1
        if got < want: return None
    out = [out[i] for i in rng.permutation(len(out))]; return np.array([p for pr in out for p in pr], np.int64)
def pool_key(img, mp, direction, f, rng):
    sc = texscore(img, mp); order = np.argsort(-sc.ravel() if direction == "t" else sc.ravel(), kind="stable")[: int(round(f * img.size))]
    pool = rng.permutation(order); return pool[: len(pool) // 2 * 2].astype(np.int64)
def fg_pixels(img, thr=10): return np.where(uniform_filter(img.astype(np.float64), 5, mode="reflect").ravel() > thr)[0]
def fg_key(img, kind, rng):
    """Keys restricted to the image foreground (5x5 mean intensity > 10; excludes the empty background): RANDFG random foreground pixels (up to N/3), COSTFG the lowest-HILL-cost third of the foreground, ANTIFG the highest-cost third."""
    fg = fg_pixels(img)
    if kind == "RANDFG": pool = rng.permutation(fg)[: img.size // 3]
    else:
        o = np.argsort(hill_cost(img).ravel()[fg], kind="stable"); n = len(fg) // 3; pool = rng.permutation(fg[o[:n]] if kind == "COSTFG" else fg[o[-n:]])
    return pool[: len(pool) // 2 * 2].astype(np.int64)
def ga_key(img, seed, objective, pop_size=SM.POP_SIZE, generations=SM.GENERATIONS, mut=None, per_coord=0.0):
    """Same genetic algorithm as StegMorph (random chains of N/3 coordinates, truncation selection, single-point crossover) but a chosen fitness.
    objective 'contrast' = StegMorph's own; 'mincost' = minimise the summed HILL cost of the chain (distortion-minimising objective).
    per_coord > 0: stronger search, each child coordinate is re-drawn with that probability (instead of one coordinate with probability 0.1)."""
    rng = np.random.default_rng(seed); flat = img.ravel(); n = flat.size; L = max(2, int(n * SM.SEQ_FRACTION)); cost = hill_cost(img).ravel() if objective == "mincost" else None
    fit_fn = (lambda pop: SM._fitness(pop, flat)) if objective == "contrast" else (lambda pop: -cost[pop].sum(1))
    pop = rng.integers(0, n, size=(pop_size, L)); mp = SM.MUTATION_PROB if mut is None else mut
    for _ in range(generations):
        fit = fit_fn(pop); order = np.argsort(-fit); parents = pop[order[: pop_size // 2]]; nc = pop_size - len(parents)
        ia = rng.integers(len(parents), size=nc); ib = rng.integers(len(parents), size=nc); cut = rng.integers(1, L, size=nc)
        mask = np.arange(L)[None, :] < cut[:, None]; children = np.where(mask, parents[ia], parents[ib])
        if per_coord > 0:
            mm = rng.random(children.shape) < per_coord; children = np.where(mm, rng.integers(0, n, size=children.shape), children)
        else:
            for c in np.where(rng.random(nc) < mp)[0]: children[c, rng.integers(L)] = rng.integers(n)
        pop = np.vstack([parents, children])
    best = pop[np.argmax(fit_fn(pop))]; _, first = np.unique(best, return_index=True); best = best[np.sort(first)]
    if len(best) % 2: best = best[:-1]
    return best.astype(np.int64)

# ----------------------------------------------------------------------------- scheme parsing and embedding
ALIAS = {"COSTKEY": "K:hill:t:0.33", "ANTIKEY": "K:hill:s:0.33", "COSTMIX": "M:K:hill:t:0.33", "ANTIMIX": "M:K:hill:s:0.33"}
KEYED_CACHE = ("ORIG", "GAMIN", "GAMINS", "GAMINX")
def _h(s): return zlib.crc32(s.encode())
def rng_for(seed, bpp, tag, i, scheme=""): return np.random.default_rng([seed, int(round(bpp * 1000)), tag, i, _h(scheme)])
def message(seed, bpp, tag, i, npix):
    L = max(1, (int(bpp * npix) - 32) // 8); r = np.random.default_rng([seed, int(round(bpp * 1000)), tag, i]); return "".join(chr(int(c)) for c in r.integers(0, 256, L))
def payload_bits(bpp, npix): L = max(1, (int(bpp * npix) - 32) // 8); return (16 + 8 * L + 16) * 3
def get_key(img, scheme, seed, bpp, tag, i, cache_row=None):
    scheme = ALIAS.get(scheme, scheme); r = rng_for(seed, bpp, tag, i, scheme)
    if scheme == "RANDSEQ": return random_key(img, r)
    if scheme in KEYED_CACHE:
        if cache_row is not None: return cache_row
        return compute_cached_key(img, scheme, seed, tag, i)
    if scheme in ("RANDFG", "COSTFG", "ANTIFG"): return fg_key(img, scheme, r)
    if scheme.startswith("K:"):
        _, mp, d, f = scheme.split(":"); return pool_key(img, mp, d, float(f), r)
    raise ValueError(scheme)
def compute_cached_key(img, scheme, seed, tag, i):
    s = int(np.random.default_rng([seed, tag, i, _h(scheme)]).integers(2 ** 31))
    if scheme == "ORIG": return ga_key(img, s, "contrast")
    if scheme == "GAMIN": return ga_key(img, s, "mincost")
    if scheme == "GAMINS": return ga_key(img, s, "mincost", generations=200, per_coord=0.02)
    if scheme == "GAMINX": return ga_key(img, s, "mincost", pop_size=200, generations=400, per_coord=0.02)   # V2.5: 16x the evaluations of GAMIN, 4x GAMINS
def _lsb_embed(img, bits, key, match, r):
    f = img.ravel().astype(np.int32).copy(); k = key[: len(bits)]; b = np.frombuffer(bits.encode(), np.uint8) - 48; cur = f[k] & 1; diff = cur != b
    if not match: f[k] = (f[k] & ~1) | b
    else:
        d = r.choice([-1, 1], size=len(k)); d = np.where(f[k] == 0, 1, np.where(f[k] == 255, -1, d)); f[k] = np.where(diff, f[k] + d, f[k])
    return f.astype(np.uint8).reshape(img.shape)
def make_stego(img, scheme, msg, seed, bpp, tag, i, cache_row=None, pre=None):
    """Returns (stego, (nPVD, nLSB)) ; nPVD/nLSB = -1 for non-StegMorph embedders."""
    nb = len(SM._text_to_bits(msg)); sc = ALIAS.get(scheme, scheme)
    if sc in ("HILLR", "SUNIR"): return pre, (-1, -1)
    if sc == "HILLSIM": return hill_embed(img, hill_cost(img), float(nb), rng_for(seed, bpp, tag, i, "HILLSIM")), (-1, -1)
    if sc.startswith("LSBK:") or sc.startswith("LSBM:"):
        kind, kt = sc.split(":"); base = {"R": "RANDSEQ", "C": "K:hill:t:0.33", "A": "K:hill:s:0.33"}[kt]; key = get_key(img, base, seed, bpp, tag, i)
        return _lsb_embed(img, SM._text_to_bits(msg), key, kind == "LSBM", rng_for(seed, bpp, tag, i, sc)), (-1, -1)
    if sc.startswith("M:"):
        base = sc[2:]; kb = get_key(img, base, seed, bpp, tag, i, cache_row); nP, nL = used_pairs(img, kb, nb); km = mix_key(img, nP, nL, rng_for(seed, bpp, tag, i, sc), fg_pixels(img) if base.endswith("FG") else None)
        if km is None: km = random_key(img, rng_for(seed, bpp, tag, i, "RANDSEQ"))
        key = km
    else: key = get_key(img, sc, seed, bpp, tag, i, cache_row)
    s = SM.embed(img, msg, key); return s, used_pairs(img, key, nb)
def beta_for(scheme, img, nb):
    """Modification-probability map the selection-channel-aware detector assumes for a scheme (computed from the image under test)."""
    sc = ALIAS.get(scheme, scheme)
    if sc in ("HILLR", "HILLSIM"): p1, p2 = change_probs(img, hill_cost(img), float(nb)); return (p1 + p2).astype(np.float32)
    if sc == "SUNIR": p1, p2 = change_probs(img, suni_cost(img), float(nb)); return (p1 + p2).astype(np.float32)
    mp = None
    if sc.startswith("K:"): mp, d, f = sc.split(":")[1:]
    elif sc.startswith("LSBK:") or sc.startswith("LSBM:"):
        kt = sc.split(":")[1]; mp, d, f = {"C": ("hill", "t", "0.33"), "A": ("hill", "s", "0.33")}.get(kt, (None, None, None))
    if mp is None: return np.ones(img.shape, np.float32)
    ts = texscore(img, mp).ravel(); order = np.argsort(-ts if d == "t" else ts, kind="stable")[: int(round(float(f) * img.size))]; b = np.zeros(img.size, np.float32); b[order] = 1.0; return b.reshape(img.shape)

# ----------------------------------------------------------------------------- worker tasks (top-level so they can be pickled by multiprocessing)
def task_cover_feats(imgs, kinds):
    out = {}
    if "srm" in kinds: out["srm"] = np.array([S.features(x) for x in imgs])
    if "spam" in kinds: out["spam"] = np.array([spam(x) for x in imgs])
    return out
def task_scheme(imgs, ids, scheme, seed, bpp, tag, kinds, cache_rows, pre, want_cover_sca):
    """Builds the stego images of one scheme for a chunk of covers and returns their features (kinds: srm, spam, sca) plus change statistics. If want_cover_sca also returns SCA features of the covers under this scheme's assumed channel."""
    npix = imgs[0].size; stego = []; stats = []; feats = {k: [] for k in kinds}; cf = []; fails = 0
    for j, im in enumerate(imgs):
        i = int(ids[j]); msg = message(seed, bpp, tag, i, npix)
        try: s, (nP, nL) = make_stego(im, scheme, msg, seed, bpp, tag, i, None if cache_rows is None else cache_rows[j], None if pre is None else pre[j])
        except ValueError: fails += 1; s, nP, nL = im.copy(), -2, -2
        stego.append(s); stats.append((nP, nL, float(((s.astype(float) - im) ** 2).mean()), float((s != im).mean())))
        if "srm" in kinds: feats["srm"].append(S.features(s))
        if "spam" in kinds: feats["spam"].append(spam(s))
        if "sca" in kinds:
            nb = len(SM._text_to_bits(msg)); feats["sca"].append(sca_features(s, beta_for(scheme, s, nb)))
            if want_cover_sca: cf.append(sca_features(im, beta_for(scheme, im, nb)))
    return {k: np.array(v) for k, v in feats.items()}, np.array(stats), (np.array(cf) if cf else None), fails
def task_keys(imgs, ids, scheme, seed, tag):
    Lk = imgs[0].size // 3
    return np.array([np.pad(k, (0, Lk - len(k)), constant_values=-1) if len(k) < Lk else k[:Lk] for k in (compute_cached_key(im, scheme, seed, tag, int(ids[j])) for j, im in enumerate(imgs))]).astype(np.int32)

_POOL = None
def pool(n=None):
    global _POOL
    if _POOL is None:
        import multiprocessing as mp; _POOL = mp.get_context("spawn").Pool(n or int(os.environ.get("NPROC", "9")))
    return _POOL
def chunks(n, k):
    b = np.linspace(0, n, k + 1).astype(int); return [(b[j], b[j + 1]) for j in range(k) if b[j + 1] > b[j]]
def par(fn, arglist): return pool().starmap(fn, arglist)

# ----------------------------------------------------------------------------- data
def load_split(ds, split): return np.load(os.path.join(ROOT, "data", "splits", f"{ds}_{split}.npz"), allow_pickle=True)
def seed_train_idx(subjects, seed, frac=0.8):
    subs = sorted(set(subjects)); r = np.random.default_rng(seed + 777); keep = set(r.permutation(subs)[: int(round(frac * len(subs)))]); return np.array([i for i, s in enumerate(subjects) if s in keep])

def task_stego(imgs, ids, scheme, seed, bpp, tag, cache_rows, pre):
    """Stego images only (used by the CNN drivers and figure scripts)."""
    npix = imgs[0].size; out = []
    for j, im in enumerate(imgs):
        i = int(ids[j]); msg = message(seed, bpp, tag, i, npix)
        s, _ = make_stego(im, scheme, msg, seed, bpp, tag, i, None if cache_rows is None else cache_rows[j], None if pre is None else pre[j]); out.append(s)
    return np.array(out)
