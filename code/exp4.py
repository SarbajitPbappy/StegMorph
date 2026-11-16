"""E4 (pre-registered in state/CLAIMS.md): GA vs RAND under two detector families. Usage: python exp4.py SEED"""
import sys, json, glob, hashlib, time, numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from skimage.metrics import peak_signal_noise_ratio as psnr
import stegmorph_recon as R, srm_lite as S
seed = int(sys.argv[1]); N = 600; PAY = [0.005, 0.01, 0.02]; T = 3; B = 2*T+1
def _trip(D, axis_pairs):
    a, b, c = axis_pairs
    idx = ((a+T)*B + (b+T))*B + (c+T)
    cnt = np.bincount(idx.ravel(), minlength=B**3).astype(np.float64).reshape(B, B, B)
    return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T, T)
    Dh = f(x[:, :-1]-x[:, 1:]); Dv = f(x[:-1]-x[1:])
    h = _trip(Dh, (Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:])); v = _trip(Dv, (Dv[:-2], Dv[1:-1], Dv[2:]))
    Dd = f(x[:-1, :-1]-x[1:, 1:]); d1 = _trip(Dd, (Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:]))
    xf = x[:, ::-1]; Da = f(xf[:-1, :-1]-xf[1:, 1:]); d2 = _trip(Da, (Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:]))
    return np.concatenate([((h+v)/2).ravel(), ((d1+d2)/2).ravel()]).astype(np.float32)
files = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True))
rng = np.random.default_rng(seed); order = rng.permutation(len(files)); imgs = []; skipped = 0; need_max = R.total_bits(int(max(PAY)*128*128))
for i in order:
    im = np.array(Image.open(files[i]).convert("L"), np.uint8)
    im = np.clip(np.round(im + np.random.default_rng(i).normal(0, 1.5, im.shape)), 0, 255).astype(np.uint8)
    if R.capacity_and_branch(im)[0].sum() >= need_max: imgs.append(im)
    else: skipped += 1
    if len(imgs) == N: break
ex = [hashlib.sha256(im.tobytes()).hexdigest() for im in imgs]; first = {}; grp = []
for i, k in enumerate(ex): grp.append(first.setdefault(k, i))
grp = np.array(grp); ug = rng.permutation(np.unique(grp)); rank = {g: k for k, g in enumerate(ug)}
tr = np.array([rank[g] < 0.7*len(ug) for g in grp]); nt = int((~tr).sum())
FcA = np.array([S.features(im) for im in imgs]); FcB = np.array([spam(im) for im in imgs])
costs = [R.expected_cost(im, np.random.default_rng(seed*7+i)) for i, im in enumerate(imgs)]; caps = [R.capacity_and_branch(im) for im in imgs]
yte = np.r_[np.zeros(nt), np.ones(nt)]; ytr = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]
def detA(Fs):
    X = np.vstack([FcA[tr], Fs[tr]]); sc = StandardScaler().fit(X); m = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), ytr)
    return m.predict_proba(sc.transform(np.vstack([FcA[~tr], Fs[~tr]])))[:, 1]
def detB(Fs):
    X = np.vstack([FcB[tr], Fs[tr]]); m = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, ytr)
    return m.predict_proba(np.vstack([FcB[~tr], Fs[~tr]]))[:, 1]
res = []
for bpp in PAY:
    n = int(bpp*imgs[0].size); need = R.total_bits(n); sc = {}; st_ = {}
    for sch in ("GA", "RAND"):
        sts = []; mse = []
        for i, im in enumerate(imgs):
            r = np.random.default_rng(seed*10**6 + int(bpp*1000)*1000 + i); pay = r.integers(0, 2, n).astype(np.uint8); cap = caps[i][0]
            m = R.select_ga(cap, costs[i], need, r) if sch == "GA" else R.select_random(cap, need, r)
            st = R.embed(im, pay, m); sts.append(st); mse.append(float(((st.astype(float)-im)**2).mean()))
            if i < 3: assert (R.extract(st, m) == pay).all()
        FsA = np.array([S.features(s) for s in sts]); FsB = np.array([spam(s) for s in sts])
        sc[("A", sch)] = detA(FsA); sc[("B", sch)] = detB(FsB)
        st_[sch] = dict(aucA=round(float(roc_auc_score(yte, sc[("A", sch)])), 4), aucB=round(float(roc_auc_score(yte, sc[("B", sch)])), 4),
                        psnr=round(float(np.mean([psnr(imgs[i], sts[i], data_range=255) for i in range(150)])), 2))
    br = np.random.default_rng(seed+11); dA = []; dB = []
    for _ in range(500):
        ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]
        dA.append(roc_auc_score(yte[idx], sc[("A", "GA")][idx]) - roc_auc_score(yte[idx], sc[("A", "RAND")][idx]))
        dB.append(roc_auc_score(yte[idx], sc[("B", "GA")][idx]) - roc_auc_score(yte[idx], sc[("B", "RAND")][idx]))
    ci = lambda d: [round(float(np.percentile(d, 2.5)), 4), round(float(np.percentile(d, 97.5)), 4)]
    row = dict(seed=seed, bpp_raw=bpp, n_test=nt, stats=st_, diffA=round(st_["GA"]["aucA"]-st_["RAND"]["aucA"], 4), ciA=ci(dA), diffB=round(st_["GA"]["aucB"]-st_["RAND"]["aucB"], 4), ciB=ci(dB))
    res.append(row); print(json.dumps(row), flush=True)
    json.dump(dict(seed=seed, N=N, skipped=skipped, rows=res), open(f"/home/claude/work/e4_seed{seed}.json", "w"), indent=1)
print("DONE", seed)
