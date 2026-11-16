"""E1 exploratory payload sweep (see CLAIMS.md amendment 2026-11-09). Usage: python exp1.py SEED"""
import sys, json, glob, hashlib, time, numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, roc_curve
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
import embed as E, srm_lite as S
seed = int(sys.argv[1]); N = 800; PAY = [0.05, 0.1, 0.2, 0.4]
files = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True))
rng = np.random.default_rng(seed); sel = rng.permutation(len(files))[:N]
imgs = [np.array(Image.open(files[i]).convert("L"), np.uint8) for i in sel]
def ahash(im):
    s = np.array(Image.fromarray(im).resize((8, 8), Image.BILINEAR), float); return (s > s.mean()).tobytes().hex()
exact = [hashlib.sha256(im.tobytes()).hexdigest() for im in imgs]; ah = [ahash(im) for im in imgs]
# union-find over exact-hash and aHash equality
par = list(range(N)); 
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for keys in (exact,):
    first = {}
    for i, k in enumerate(keys):
        if k in first: par[find(i)] = find(first[k])
        else: first[k] = i
grp = np.array([find(i) for i in range(N)]); ug = rng.permutation(np.unique(grp)); rank = {g: k for k, g in enumerate(ug)}
trG = np.array([rank[g] < 0.7*len(ug) for g in grp])
trR = np.zeros(N, bool); trR[rng.permutation(N)[:int(0.7*N)]] = True      # random image-level split (leakage proxy)
Fc = np.array([S.features(im) for im in imgs])
def evaluate(Fs, tr):
    Xtr = np.vstack([Fc[tr], Fs[tr]]); ytr = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]
    Xte = np.vstack([Fc[~tr], Fs[~tr]]); yte = np.r_[np.zeros((~tr).sum()), np.ones((~tr).sum())]
    sc = StandardScaler().fit(Xtr); clf = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(Xtr), ytr)
    p = clf.predict_proba(sc.transform(Xte))[:, 1]
    fpr, tpr, _ = roc_curve(yte, p); pe = float(np.min(0.5*(fpr + 1 - tpr))); t1 = float(np.interp(0.01, fpr, tpr))
    auc = roc_auc_score(yte, p)
    nt = (~tr).sum(); bs = []; br = np.random.default_rng(seed+7)
    for _ in range(1000):
        ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]; 
        bs.append(roc_auc_score(yte[idx], p[idx]))
    return dict(auc=round(float(auc), 4), ci=[round(float(np.percentile(bs, 2.5)), 4), round(float(np.percentile(bs, 97.5)), 4)], pe=round(pe, 4), tpr1=round(t1, 4))
bitsf = lambda n, k: np.random.default_rng(seed*10**6+k).integers(0, 2, n, dtype=np.uint8)
def make(scheme, bpp, im, i):
    n = int(bpp*im.size)
    if scheme == "LSB_seq": return E.lsb_embed(im, bitsf(n, i))[0]
    if scheme == "LSB_keyed": return E.lsb_embed(im, bitsf(n, i), key=seed*10**6+i)[0]
    if scheme == "PVD6":
        cap = E.pvd_capacity(im); return E.pvd_embed(im, bitsf(min(n, cap), i))
    if scheme == "HILL_sim": return E.hill_simulate(im, bpp, seed*10**6+i)[0]
out = []
for scheme in ["LSB_seq", "LSB_keyed", "PVD6", "HILL_sim"]:
    for bpp in PAY:
        t0 = time.time(); st = [make(scheme, bpp, im, i) for i, im in enumerate(imgs)]
        Fs = np.array([S.features(s) for s in st])
        rg = evaluate(Fs, trG)
        q = [(psnr(imgs[i], st[i], data_range=255), ssim(imgs[i], st[i], data_range=255)) for i in range(0, 200)]
        pcap = int(np.mean([E.pvd_capacity(im) for im in imgs[:50]])) if scheme == "PVD6" else None
        actual = float(np.mean([(imgs[i] != st[i]).mean() for i in range(200)]))
        row = dict(seed=seed, scheme=scheme, bpp=bpp, exact_hash_group_split=rg, psnr=round(float(np.mean([a for a, _ in q])), 3),
                   ssim=round(float(np.mean([b for _, b in q])), 5), pixel_change_rate=round(actual, 4), pvd_mean_capacity_bits=pcap, secs=round(time.time()-t0, 1))
        out.append(row); print(json.dumps(row), flush=True)
        json.dump(out, open(f"e1_seed{seed}.json", "w"), indent=1)
json.dump(dict(seed=seed, N=N, n_groups=int(len(ug)), n_train_groups_frac=float(trG.mean()), rows=out), open(f"e1_seed{seed}.json", "w"), indent=1)
