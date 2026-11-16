"""E3 (pre-registered in state/CLAIMS.md): C2 branch ablation + C4 cross-payload/cross-method. Covers = MRI + Gaussian noise sigma 1.5 (SYNTHETIC). Usage: python exp3.py SEED"""
import sys, json, glob, hashlib, time, numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from skimage.metrics import peak_signal_noise_ratio as psnr
import stegmorph_recon as R, srm_lite as S
seed = int(sys.argv[1]); N = 300; PAY = [0.005, 0.01, 0.02, 0.05]
SCH = ["RAND_ALL", "RAND_LOW", "RAND_PVD", "GA_ALL"]
files = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True))
rng = np.random.default_rng(seed); order = rng.permutation(len(files)); imgs = []; ids = []; skipped = 0
need_max = R.total_bits(int(max(PAY)*128*128))
for i in order:
    im = np.array(Image.open(files[i]).convert("L"), np.uint8)
    im = np.clip(np.round(im + np.random.default_rng(i).normal(0, 1.5, im.shape)), 0, 255).astype(np.uint8)
    cap, low, pvd = R.capacity_and_branch(im)
    if cap[low].sum() >= need_max and cap[pvd].sum() >= need_max: imgs.append(im); ids.append(i)
    else: skipped += 1
    if len(imgs) == N: break
ex = [hashlib.sha256(im.tobytes()).hexdigest() for im in imgs]; first = {}; grp = []
for i, k in enumerate(ex): grp.append(first.setdefault(k, i))
grp = np.array(grp); ug = rng.permutation(np.unique(grp)); rank = {g: k for k, g in enumerate(ug)}
tr = np.array([rank[g] < 0.7*len(ug) for g in grp]); nt = int((~tr).sum())
Fc = np.array([S.features(im) for im in imgs]); costs = [R.expected_cost(im, np.random.default_rng(seed*7+i)) for i, im in enumerate(imgs)]
caps = [R.capacity_and_branch(im) for im in imgs]
yte = np.r_[np.zeros(nt), np.ones(nt)]
def fit(Fs):
    Xtr = np.vstack([Fc[tr], Fs[tr]]); ytr = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]
    sc = StandardScaler().fit(Xtr); return sc, LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(Xtr), ytr)
def score(m, Fs):
    sc, clf = m; return clf.predict_proba(sc.transform(np.vstack([Fc[~tr], Fs[~tr]])))[:, 1]
FE = {}; info = {}; models = {}; P = {}
for bpp in PAY:
    n = int(bpp*imgs[0].size); need = R.total_bits(n)
    for sch in SCH:
        t0 = time.time(); sts = []; lowf = []; mse = []
        for i, im in enumerate(imgs):
            r = np.random.default_rng(seed*10**6 + int(bpp*1000)*1000 + i); pay = r.integers(0, 2, n).astype(np.uint8)
            cap, low, pvd = caps[i]
            if sch == "RAND_ALL": m = R.select_random(cap, need, r)
            elif sch == "RAND_LOW": m = R.select_random(np.where(low, cap, 0), need, r)
            elif sch == "RAND_PVD": m = R.select_random(np.where(pvd, cap, 0), need, r)
            else: m = R.select_ga(cap, costs[i], need, r)
            st = R.embed(im, pay, m); sts.append(st); lowf.append(float(low[m].mean())); mse.append(float(((st.astype(float)-im)**2).mean()))
            if i < 3: assert (R.extract(st, m) == pay).all()
        Fs = np.array([S.features(s) for s in sts]); FE[(sch, bpp)] = Fs
        models[(sch, bpp)] = fit(Fs); P[(sch, bpp)] = score(models[(sch, bpp)], Fs)
        info[f"{sch}_{bpp}"] = dict(auc=round(float(roc_auc_score(yte, P[(sch, bpp)])), 4), low_branch_frac=round(float(np.mean(lowf)), 3), mse=round(float(np.mean(mse)), 4),
                                    psnr=round(float(np.mean([psnr(imgs[i], sts[i], data_range=255) for i in range(100)])), 2), secs=round(time.time()-t0, 1))
        print(sch, bpp, info[f"{sch}_{bpp}"], flush=True)
# C2: LOW vs PVD paired bootstrap per payload
c2 = {}
br = np.random.default_rng(seed+5)
for bpp in PAY:
    d = []
    for _ in range(500):
        ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]
        d.append(roc_auc_score(yte[idx], P[("RAND_LOW", bpp)][idx]) - roc_auc_score(yte[idx], P[("RAND_PVD", bpp)][idx]))
    c2[str(bpp)] = dict(diff=round(info[f"RAND_LOW_{bpp}"]["auc"]-info[f"RAND_PVD_{bpp}"]["auc"], 4), ci95=[round(float(np.percentile(d, 2.5)), 4), round(float(np.percentile(d, 97.5)), 4)])
# C4: cross-payload (per scheme) and cross-method (per payload)
xp = {sch: {f"train{a}": {f"test{b}": round(float(roc_auc_score(yte, score(models[(sch, a)], FE[(sch, b)]))), 4) for b in PAY} for a in PAY} for sch in SCH}
xm = {str(b): {f"train_{a}": {f"test_{c}": round(float(roc_auc_score(yte, score(models[(a, b)], FE[(c, b)]))), 4) for c in SCH} for a in SCH} for b in PAY}
json.dump(dict(seed=seed, N=N, n_test=nt, skipped=skipped, info=info, c2=c2, cross_payload=xp, cross_method=xm), open(f"/home/claude/work/e3_seed{seed}.json", "w"), indent=1)
print("DONE", seed)
