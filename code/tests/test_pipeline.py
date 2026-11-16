"""Pipeline sanity (plan 0.1/0.4/0.6) on NON-MRI covers (skimage bundled images). Pipeline validation only; no claim."""
import sys, numpy as np, json; sys.path.insert(0, "..")
from skimage import data
from sklearn.metrics import roc_auc_score
import embed as E, detect as D
rng = np.random.default_rng(0)
def covers(n=60, sz=128):
    srcs = []
    for nm in ["camera", "moon", "coins", "page", "astronaut", "brick", "gravel", "grass", "rocket", "chelsea"]:
        try:
            im = getattr(data, nm)()
            if im.ndim == 3: im = (im[..., :3] @ [0.299, 0.587, 0.114])
            srcs.append(np.clip(im, 0, 255).astype(np.uint8))
        except Exception as e: print("skip", nm, type(e).__name__)
    out = []
    for i in range(n):
        s = srcs[i % len(srcs)]; y = rng.integers(0, s.shape[0]-sz); x = rng.integers(0, s.shape[1]-sz)
        out.append(s[y:y+sz, x:x+sz].copy())
    return out, len(srcs)
C, nsrc = covers(); res = {"n_covers": len(C), "n_source_images": nsrc, "note": "non-MRI, crops of few images; pipeline sanity only"}
# 1 round trips + payload accounting
im = C[0]; bits = rng.integers(0, 2, 5000).astype(np.uint8)
s, _ = E.lsb_embed(im, bits); assert (E.lsb_extract(s, 5000) == bits).all()
s, _ = E.lsb_embed(im, bits, key=7); assert (E.lsb_extract(s, 5000, key=7) == bits).all()
assert (E.lsb_extract(s, 5000, key=8) != bits).mean() > 0.3          # wrong key fails
cap = E.pvd_capacity(im); nb = min(cap, 6000); b2 = rng.integers(0, 2, nb).astype(np.uint8)
sp = E.pvd_embed(im, b2); assert (E.pvd_extract(sp, nb) == b2).all(); res["pvd_capacity_bits_cover0"] = int(cap)
assert np.abs(sp.astype(int)-im.astype(int)).max() <= 32
for bpp in (0.1, 0.4, 1.0):
    s2, ach = E.hill_simulate(im, bpp, 1); assert abs(ach-bpp) < 0.01, (bpp, ach)
res["roundtrips"] = "pass"
# 2 detector sanity: AUC on plain LSB 1.0 bpp (ceiling) and cover-vs-cover (chance), per detector
def auc(det, mk):
    sc0 = [det(c) for c in C]; sc1 = [det(mk(c, i)) for i, c in enumerate(C)]
    return float(roc_auc_score([0]*len(C)+[1]*len(C), sc0+sc1))
def lsb(bpp, key=None):
    return lambda c, i: E.lsb_embed(c, rng.integers(0, 2, int(bpp*c.size)).astype(np.uint8), key if key is None else 1000+i)[0]
half = len(C)//2
def chance(det):
    s = [det(c) for c in C]; return float(roc_auc_score([0]*half+[1]*half, s[:half]+s[half:2*half])) if False else float(roc_auc_score([0]*half+[1]*(len(C)-half), s))
# cover-vs-cover: labels assigned at random permutation (should be ~0.5)
def chance_auc(det):
    s = np.array([det(c) for c in C]); lab = rng.permutation([0, 1]*(len(C)//2)); return float(roc_auc_score(lab, s))
tab = {}
for name, det in [("chi2", D.chi_square_score), ("RS", D.rs_score), ("SPA", D.spa_score)]:
    tab[name] = {"LSB_seq_1.0": auc(det, lsb(1.0)), "LSB_seq_0.4": auc(det, lsb(0.4)), "LSB_seq_0.1": auc(det, lsb(0.1)),
                 "LSB_rand_1.0": auc(det, lsb(1.0, 1)), "LSB_rand_0.4": auc(det, lsb(0.4, 1)), "cover_vs_cover(chance)": chance_auc(det)}
res["auc"] = tab
# 3 SPA/RS estimate tracks true rate for random LSB (relative length p = bpp * 2 since each LSB flips w.p. 1/2)
est = {}
for bpp in (0.0, 0.2, 0.4, 0.8):
    est[bpp] = {"RS_mean": float(np.mean([D.rs_score(lsb(bpp, 1)(c, i)) if bpp else D.rs_score(c) for i, c in enumerate(C)])),
                "SPA_mean": float(np.mean([D.spa_score(lsb(bpp, 1)(c, i)) if bpp else D.spa_score(c) for i, c in enumerate(C)]))}
res["rate_estimates_random_LSB"] = est
print(json.dumps(res, indent=1)); json.dump(res, open("pipeline_sanity_result.json", "w"), indent=1)
