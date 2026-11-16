"""E6 (pre-registered in state/CLAIMS.md): texture-aware GA fitness. Usage: python exp6.py SEED"""
import sys, json, glob, hashlib, numpy as np
from PIL import Image
from scipy.signal import convolve2d
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from skimage.metrics import peak_signal_noise_ratio as psnr
import stegmorph_recon as R, srm_lite as S
seed = int(sys.argv[1]); PAY = [0.02, 0.05]; T = 3; B = 2*T+1; NA = 400
def _trip(a, b, c):
    idx = ((a+T)*B + (b+T))*B + (c+T); cnt = np.bincount(idx.ravel(), minlength=B**3).astype(np.float64).reshape(B, B, B)
    return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T, T)
    Dh = f(x[:, :-1]-x[:, 1:]); Dv = f(x[:-1]-x[1:]); h = _trip(Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:]); v = _trip(Dv[:-2], Dv[1:-1], Dv[2:])
    Dd = f(x[:-1, :-1]-x[1:, 1:]); d1 = _trip(Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:])
    xf = x[:, ::-1]; Da = f(xf[:-1, :-1]-xf[1:, 1:]); d2 = _trip(Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:])
    return np.concatenate([((h+v)/2).ravel(), ((d1+d2)/2).ravel()]).astype(np.float32)
KB = np.array([[-1, 2, -2, 2, -1], [2, -6, 8, -6, 2], [-2, 8, -12, 8, -2], [2, -6, 8, -6, 2], [-1, 2, -2, 2, -1]]) / 12.0
AV3 = np.ones((3, 3))/9.0; AV7 = np.ones((7, 7))/49.0
def tex_pair_cost(img):
    """HILL-style pixel cost (high-pass -> low-pass -> inverse -> low-pass), mean over each horizontal pair, normalised by image median."""
    x = img.astype(np.float64); r = np.abs(convolve2d(x, KB, mode="same", boundary="symm")); xi = convolve2d(r, AV3, mode="same", boundary="symm")
    rho = 1.0/(xi + 1e-2); rho = convolve2d(rho, AV7, mode="same", boundary="symm"); rho = rho/np.median(rho)
    f = rho.flatten(); n = len(f)//2*2
    return 0.5*(f[0:n:2] + f[1:n:2])
def noisy(im, key): return np.clip(np.round(im + np.random.default_rng(key).normal(0, 1.5, im.shape)), 0, 255).astype(np.uint8)
rng = np.random.default_rng(seed); need_max = R.total_bits(int(max(PAY)*128*128))
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
af = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True)); order = rng.permutation(len(af)); Ac = []
for i in order:
    im = np.array(Image.open(af[i]).convert("L"), np.uint8)
    if R.capacity_and_branch(im)[0].sum() >= need_max: Ac.append(im)
    if len(Ac) == NA: break
ex = [hashlib.sha256(im.tobytes()).hexdigest() for im in Ac]; first = {}; ag = np.array([first.setdefault(k, i) for i, k in enumerate(ex)])
ua = rng.permutation(np.unique(ag)); ra = {g: i for i, g in enumerate(ua)}; Atr = np.array([ra[g] < 0.7*len(ua) for g in ag])
sets = {"A_raw": (Ac, Atr)}
SCH = ["RAND", "GA_MSE", "GA_TEX", "GREEDY_TEX"]
def stego(imgs, bpp, sch, tag):
    n = int(bpp*128*128); need = R.total_bits(n); out = []
    for i, im in enumerate(imgs):
        r = np.random.default_rng(seed*10**6 + int(bpp*1000)*1000 + i + tag*7919); pay = r.integers(0, 2, n).astype(np.uint8); cap = R.capacity_and_branch(im)[0]
        mse = R.expected_cost(im, np.random.default_rng(seed*7+i))
        if sch == "RAND": m = R.select_random(cap, need, r)
        elif sch == "GA_MSE": m = R.select_ga(cap, mse, need, r)
        else:
            c = mse*tex_pair_cost(im)
            m = R.select_ga(cap, c, need, r) if sch == "GA_TEX" else R.select_greedy(cap, c, need)
        st = R.embed(im, pay, m); out.append(st)
        if i < 2: assert (R.extract(st, m) == pay).all()
    return out
feats = {}; ps = {}
for si, (name, (imgs, tr)) in enumerate(sets.items()):
    feats[name] = {"cover": (np.array([S.features(im) for im in imgs]), np.array([spam(im) for im in imgs])), "tr": tr}
    for bpp in PAY:
        for sch in SCH:
            sts = stego(imgs, bpp, sch, si); feats[name][(sch, bpp)] = (np.array([S.features(s) for s in sts]), np.array([spam(s) for s in sts]))
            ps[f"{name}|{sch}|{bpp}"] = round(float(np.mean([psnr(imgs[i], sts[i], data_range=255) for i in range(min(100, len(imgs)))])), 2)
        print("done", name, bpp, flush=True)
def fitdet(fam, name, sch, bpp):
    d = feats[name]; tr = d["tr"]; k = 0 if fam == "A" else 1; X = np.vstack([d["cover"][k][tr], d[(sch, bpp)][k][tr]]); y = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]
    if fam == "A": sc = StandardScaler().fit(X); m = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y); return lambda Z: m.predict_proba(sc.transform(Z))[:, 1]
    m = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, y); return lambda Z: m.predict_proba(Z)[:, 1]
out = {"seed": seed, "psnr": ps, "res": {}}; br = np.random.default_rng(seed+3)
for name in sets:
    d = feats[name]; te = ~d["tr"]; nt = int(te.sum()); y = np.r_[np.zeros(nt), np.ones(nt)]
    for bpp in PAY:
        for fam in ("A", "B"):
            k = 0 if fam == "A" else 1; P = {}
            for sch in SCH:
                fn = fitdet(fam, name, sch, bpp); P[sch] = fn(np.vstack([d["cover"][k][te], d[(sch, bpp)][k][te]]))
            row = {"n_test": nt, "auc": {s: round(float(roc_auc_score(y, P[s])), 4) for s in SCH}, "diff_vs_RAND": {}}
            for s in SCH[1:]:
                dd = []
                for _ in range(500):
                    ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]; dd.append(roc_auc_score(y[idx], P[s][idx]) - roc_auc_score(y[idx], P["RAND"][idx]))
                row["diff_vs_RAND"][s] = dict(diff=round(row["auc"][s]-row["auc"]["RAND"], 4), ci95=[round(float(np.percentile(dd, 2.5)), 4), round(float(np.percentile(dd, 97.5)), 4)])
            out["res"][f"{name}|{fam}|{bpp}"] = row
json.dump(out, open(f"/home/claude/work/e6b_seed{seed}.json", "w"), indent=1); print("DONE", seed)
