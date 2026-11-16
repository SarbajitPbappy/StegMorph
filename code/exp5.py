"""E5 (pre-registered in state/CLAIMS.md): second MRI source + cross-dataset. Usage: python exp5.py SEED"""
import sys, json, glob, hashlib, time, numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import stegmorph_recon as R, srm_lite as S
seed = int(sys.argv[1]); PAY = [0.005, 0.01, 0.02]; T = 3; B = 2*T+1; NA = 400
def _trip(a, b, c):
    idx = ((a+T)*B + (b+T))*B + (c+T); cnt = np.bincount(idx.ravel(), minlength=B**3).astype(np.float64).reshape(B, B, B)
    return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T, T)
    Dh = f(x[:, :-1]-x[:, 1:]); Dv = f(x[:-1]-x[1:]); h = _trip(Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:]); v = _trip(Dv[:-2], Dv[1:-1], Dv[2:])
    Dd = f(x[:-1, :-1]-x[1:, 1:]); d1 = _trip(Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:])
    xf = x[:, ::-1]; Da = f(xf[:-1, :-1]-xf[1:, 1:]); d2 = _trip(Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:])
    return np.concatenate([((h+v)/2).ravel(), ((d1+d2)/2).ravel()]).astype(np.float32)
def noisy(im, key): return np.clip(np.round(im + np.random.default_rng(key).normal(0, 1.5, im.shape)), 0, 255).astype(np.uint8)
rng = np.random.default_rng(seed); need_max = R.total_bits(int(max(PAY)*128*128))
# ---- tumor crops (raw native pixels) grouped by source image
tf = sorted(glob.glob("/home/claude/data/MRI_data/**/*.png", recursive=True)); Tc = []; Tg = []
for gi, f in enumerate(tf):
    im = np.array(Image.open(f).convert("L"), np.uint8); H, W = im.shape
    if H < 128 or W < 128: continue
    k = 2 if (H >= 256 or W >= 256) else 1
    for j in range(k):
        for _ in range(20):
            y = int(rng.integers(0, H-127)); x = int(rng.integers(0, W-127)); c = im[y:y+128, x:x+128]
            if R.capacity_and_branch(c)[0].sum() >= need_max: Tc.append(c.copy()); Tg.append(gi); break
Tg = np.array(Tg); ug = rng.permutation(np.unique(Tg)); rk = {g: i for i, g in enumerate(ug)}; Ttr = np.array([rk[g] < 0.7*len(ug) for g in Tg])
# ---- alzheimer noise covers
af = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True)); order = rng.permutation(len(af)); Ac = []
for i in order:
    im = noisy(np.array(Image.open(af[i]).convert("L"), np.uint8), i)
    if R.capacity_and_branch(im)[0].sum() >= need_max: Ac.append(im)
    if len(Ac) == NA: break
ex = [hashlib.sha256(im.tobytes()).hexdigest() for im in Ac]; first = {}; ag = np.array([first.setdefault(k, i) for i, k in enumerate(ex)])
ua = rng.permutation(np.unique(ag)); ra = {g: i for i, g in enumerate(ua)}; Atr = np.array([ra[g] < 0.7*len(ua) for g in ag])
sets = {"T_raw": (Tc, Ttr), "T_noise": ([noisy(c, seed*100000+i) for i, c in enumerate(Tc)], Ttr), "A_noise": (Ac, Atr)}
print("sizes", {k: (len(v[0]), int(v[1].sum()), int((~v[1]).sum())) for k, v in sets.items()}, flush=True)
def stego(imgs, bpp, sch, tag):
    n = int(bpp*128*128); need = R.total_bits(n); out = []
    for i, im in enumerate(imgs):
        r = np.random.default_rng(seed*10**6 + int(bpp*1000)*1000 + i + tag*7919); pay = r.integers(0, 2, n).astype(np.uint8); cap = R.capacity_and_branch(im)[0]
        if sch == "GA": m = R.select_ga(cap, R.expected_cost(im, np.random.default_rng(seed*7+i)), need, r)
        else: m = R.select_random(cap, need, r)
        st = R.embed(im, pay, m); out.append(st)
        if i < 2: assert (R.extract(st, m) == pay).all()
    return out
feats = {}; res = {}
for si, (name, (imgs, tr)) in enumerate(sets.items()):
    FcA = np.array([S.features(im) for im in imgs]); FcB = np.array([spam(im) for im in imgs]); feats[name] = {"cover": (FcA, FcB), "tr": tr}
    for bpp in PAY:
        for sch in ("GA", "RAND"):
            sts = stego(imgs, bpp, sch, si); feats[name][(sch, bpp)] = (np.array([S.features(s) for s in sts]), np.array([spam(s) for s in sts]))
        print("done", name, bpp, flush=True)
def fitdet(fam, name, sch, bpp, sub=None):
    d = feats[name]; tr = d["tr"].copy(); k = 0 if fam == "A" else 1; Fc = d["cover"][k][tr]; Fs = d[(sch, bpp)][k][tr]
    if sub is not None: Fc, Fs = Fc[:sub], Fs[:sub]
    X = np.vstack([Fc, Fs]); y = np.r_[np.zeros(len(Fc)), np.ones(len(Fs))]
    if fam == "A": sc = StandardScaler().fit(X); m = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y); return lambda Z: m.predict_proba(sc.transform(Z))[:, 1]
    m = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, y); return lambda Z: m.predict_proba(Z)[:, 1]
def evalon(fn, fam, name, sch, bpp):
    d = feats[name]; te = ~d["tr"]; k = 0 if fam == "A" else 1
    Z = np.vstack([d["cover"][k][te], d[(sch, bpp)][k][te]]); y = np.r_[np.zeros(te.sum()), np.ones(te.sum())]; p = fn(Z); return p, y
out = {"seed": seed, "sizes": {k: (len(v[0]), int(v[1].sum()), int((~v[1]).sum())) for k, v in sets.items()}, "in_domain": {}, "cross": {}}
br = np.random.default_rng(seed+3)
for name in sets:
    for bpp in PAY:
        for fam in ("A", "B"):
            P = {}
            for sch in ("GA", "RAND"):
                fn = fitdet(fam, name, sch, bpp); P[sch], y = evalon(fn, fam, name, sch, bpp)
            nt = len(y)//2; d = []
            for _ in range(500):
                ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]; d.append(roc_auc_score(y[idx], P["GA"][idx]) - roc_auc_score(y[idx], P["RAND"][idx]))
            out["in_domain"][f"{name}|{fam}|{bpp}"] = dict(n_test=nt, auc_GA=round(float(roc_auc_score(y, P["GA"])), 4), auc_RAND=round(float(roc_auc_score(y, P["RAND"])), 4), diff=round(float(roc_auc_score(y, P["GA"])-roc_auc_score(y, P["RAND"])), 4), ci95=[round(float(np.percentile(d, 2.5)), 4), round(float(np.percentile(d, 97.5)), 4)])
ntrT = int(feats["T_noise"]["tr"].sum())
for fam in ("A", "B"):
    for bpp in PAY:
        for sch in ("GA", "RAND"):
            for src, dst, sub in (("A_noise", "T_noise", None), ("T_noise", "A_noise", None), ("A_noise", "A_noise", ntrT), ("A_noise", "A_noise", None), ("T_noise", "T_noise", None)):
                fn = fitdet(fam, src, sch, bpp, sub); p, y = evalon(fn, fam, dst, sch, bpp)
                out["cross"][f"{fam}|{bpp}|{sch}|train_{src}{'_sub'+str(sub) if sub else ''}->test_{dst}"] = round(float(roc_auc_score(y, p)), 4)
json.dump(out, open(f"/home/claude/work/e5_seed{seed}.json", "w"), indent=1); print("DONE", seed)
