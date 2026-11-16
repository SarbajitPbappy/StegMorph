"""E7b: selection-channel-aware detector (maxSRM-lite): SRM-lite co-occurrences weighted by an embedding-probability map estimated from the (stego) image itself, max-pooled over 3x3.
Usage: python exp7b_sca.py SEED DATASET(A_raw|T_raw) BPP"""
import sys, json, glob, hashlib, numpy as np
from PIL import Image
from scipy.signal import convolve2d
from scipy.ndimage import maximum_filter
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import stegmorph_recon as R, srm_lite as S
seed = int(sys.argv[1]); DS = sys.argv[2]; BPP = float(sys.argv[3]); N = 400; T = 2; B = 2*T+1
KB = np.array([[-1, 2, -2, 2, -1], [2, -6, 8, -6, 2], [-2, 8, -12, 8, -2], [2, -6, 8, -6, 2], [-1, 2, -2, 2, -1]]) / 12.0
AV3 = np.ones((3, 3))/9.0; AV7 = np.ones((7, 7))/49.0
def rho_map(img):
    x = img.astype(np.float64); r = np.abs(convolve2d(x, KB, mode="same", boundary="symm")); xi = convolve2d(r, AV3, mode="same", boundary="symm")
    rho = 1.0/(xi + 1e-2); return convolve2d(rho, AV7, mode="same", boundary="symm")
def tex_pair_cost(img):
    rho = rho_map(img); rho = rho/np.median(rho); f = rho.flatten(); n = len(f)//2*2; return 0.5*(f[0:n:2] + f[1:n:2])
def sca_features(img):
    x = img.astype(np.float32); rho = rho_map(img); p = np.exp(-rho/np.median(rho)); p = p/p.max()          # high prob where cost low (textured)
    out = []
    for name, f in S.F.items():
        r = np.clip(np.round(convolve2d(x, f, mode="valid")), -T, T).astype(np.int64)
        kh, kw = f.shape; ph, pw = (kh-1)//2, (kw-1)//2
        pm = p[ph:ph+r.shape[0], pw:pw+r.shape[1]]; pm = maximum_filter(pm, size=3, mode="nearest")
        h = np.zeros(B**4, np.float64)
        for axis in (0, 1):
            if axis == 1: a, b, c, d = r[:, :-3], r[:, 1:-2], r[:, 2:-1], r[:, 3:]; w = np.maximum.reduce([pm[:, :-3], pm[:, 1:-2], pm[:, 2:-1], pm[:, 3:]])
            else: a, b, c, d = r[:-3], r[1:-2], r[2:-1], r[3:]; w = np.maximum.reduce([pm[:-3], pm[1:-2], pm[2:-1], pm[3:]])
            idx = (((a+T)*B + (b+T))*B + (c+T))*B + (d+T); h += np.bincount(idx.ravel(), weights=w.ravel(), minlength=B**4)
            idx2 = (((-a+T)*B + (-b+T))*B + (-c+T))*B + (-d+T); h += np.bincount(idx2.ravel(), weights=w.ravel(), minlength=B**4)
        out.append((h/max(h.sum(), 1e-9)).astype(np.float32))
    return np.concatenate(out)
tex_cost = tex_pair_cost
rng = np.random.default_rng(seed); n = int(BPP*128*128); need = R.total_bits(n)
imgs = []
if DS == "A_raw":
    af = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True)); order = rng.permutation(len(af))
    for i in order:
        im = np.array(Image.open(af[i]).convert("L"), np.uint8)
        if R.capacity_and_branch(im)[0].sum() >= need: imgs.append(im)
        if len(imgs) == N: break
    ex = [hashlib.sha256(im.tobytes()).hexdigest() for im in imgs]; first = {}; grp = np.array([first.setdefault(k, i) for i, k in enumerate(ex)])
else:
    tf = sorted(glob.glob("/home/claude/data/MRI_data/**/*.png", recursive=True)); grp = []
    for gi, f in enumerate(tf):
        im = np.array(Image.open(f).convert("L"), np.uint8); H, W = im.shape
        if H < 128 or W < 128: continue
        k = 2 if (H >= 256 or W >= 256) else 1
        for j in range(k):
            for _ in range(20):
                y = int(rng.integers(0, H-127)); x = int(rng.integers(0, W-127)); c = im[y:y+128, x:x+128]
                if R.capacity_and_branch(c)[0].sum() >= need: imgs.append(c.copy()); grp.append(gi); break
    grp = np.array(grp)
ug = rng.permutation(np.unique(grp)); rk = {g: i for i, g in enumerate(ug)}; tr = np.array([rk[g] < 0.7*len(ug) for g in grp]); nt = int((~tr).sum())
def stego(sch):
    out = []
    for i, im in enumerate(imgs):
        r = np.random.default_rng(seed*10**6 + i); pay = r.integers(0, 2, n).astype(np.uint8); cap = R.capacity_and_branch(im)[0]; mse = R.expected_cost(im, np.random.default_rng(seed*7+i))
        if sch == "RAND": m = R.select_random(cap, need, r)
        elif sch == "GA_MSE": m = R.select_ga(cap, mse, need, r)
        else: m = R.select_greedy(cap, mse*tex_cost(im), need)
        out.append(R.embed(im, pay, m))
    return out
cover = imgs; Fc = {"srm": np.array([S.features(im) for im in cover]), "sca": np.array([sca_features(im) for im in cover])}
y = np.r_[np.zeros(nt), np.ones(nt)]; res = {}; P = {}
for sch in ["RAND", "GA_MSE", "GREEDY_TEX"]:
    st = stego(sch); Fs = {"srm": np.array([S.features(s) for s in st]), "sca": np.array([sca_features(s) for s in st])}
    for det in ("srm", "sca"):
        X = np.vstack([Fc[det][tr], Fs[det][tr]]); yt = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]; sc = StandardScaler().fit(X); m = LogisticRegression(C=0.05, max_iter=500).fit(sc.transform(X), yt)
        p = m.predict_proba(sc.transform(np.vstack([Fc[det][~tr], Fs[det][~tr]])))[:, 1]; P[(sch, det)] = p; res[f"{sch}|{det}"] = round(float(roc_auc_score(y, p)), 4)
    print(sch, {k: v for k, v in res.items() if k.startswith(sch)}, flush=True)
br = np.random.default_rng(seed+3); diffs = {}
for det in ("srm", "sca"):
    for s in ("GA_MSE", "GREEDY_TEX"):
        d = []
        for _ in range(500):
            ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]; d.append(roc_auc_score(y[idx], P[(s, det)][idx]) - roc_auc_score(y[idx], P[("RAND", det)][idx]))
        diffs[f"{s}|{det}"] = dict(diff=round(res[f"{s}|{det}"]-res[f"RAND|{det}"], 4), ci95=[round(float(np.percentile(d, 2.5)), 4), round(float(np.percentile(d, 97.5)), 4)])
json.dump(dict(seed=seed, ds=DS, bpp=BPP, n_test=nt, auc=res, diffs=diffs), open(f"/home/claude/work/e7b_{DS}_{BPP}_seed{seed}.json", "w"), indent=1); print("DONE", res, diffs)
