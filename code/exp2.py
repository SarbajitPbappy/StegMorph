"""E2: C1 test, StegMorph-recon GA vs random selection (pre-registered in state/CLAIMS.md). Usage: python exp2.py SEED"""
import sys, json, glob, hashlib, time, numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, roc_curve
from skimage.metrics import peak_signal_noise_ratio as psnr
import stegmorph_recon as R, srm_lite as S
seed = int(sys.argv[1]); N = 600; PAY = [0.02, 0.05, 0.1, 0.2]
files = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True))
rng = np.random.default_rng(seed); order = rng.permutation(len(files)); imgs = []; skipped = 0; need_max = R.total_bits(int(max(PAY)*128*128))
for i in order:
    im = np.array(Image.open(files[i]).convert("L"), np.uint8)
    if R.capacity_and_branch(im)[0].sum() >= need_max: imgs.append(im)
    else: skipped += 1
    if len(imgs) == N: break
ex = [hashlib.sha256(im.tobytes()).hexdigest() for im in imgs]; first = {}; grp = []
for i, k in enumerate(ex): grp.append(first.setdefault(k, i))
grp = np.array(grp); ug = rng.permutation(np.unique(grp)); rank = {g: k for k, g in enumerate(ug)}
tr = np.array([rank[g] < 0.7*len(ug) for g in grp]); nt = int((~tr).sum())
Fc = np.array([S.features(im) for im in imgs]); costs = [R.expected_cost(im, np.random.default_rng(seed*7+i)) for i, im in enumerate(imgs)]
caps = [R.capacity_and_branch(im) for im in imgs]
def scores(Fs):
    Xtr = np.vstack([Fc[tr], Fs[tr]]); ytr = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]
    sc = StandardScaler().fit(Xtr); clf = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(Xtr), ytr)
    return clf.predict_proba(sc.transform(np.vstack([Fc[~tr], Fs[~tr]])))[:, 1]
yte = np.r_[np.zeros(nt), np.ones(nt)]
def summ(p):
    fpr, tpr, _ = roc_curve(yte, p); return dict(auc=round(float(roc_auc_score(yte, p)), 4), pe=round(float(np.min(0.5*(fpr+1-tpr))), 4), tpr1=round(float(np.interp(0.01, fpr, tpr)), 4))
res = []; feats = {"cover": Fc.astype(np.float16), "train": tr}
for bpp in PAY:
    n = int(bpp*128*128); need = R.total_bits(n); S_ = {}; stats = {}
    for scheme in ("SM_GA", "SM_RAND", "SM_GREEDY"):
        t0 = time.time(); sts = []; low_frac = []; mse = []
        for i, im in enumerate(imgs):
            r = np.random.default_rng(seed*10**6 + int(bpp*1000)*1000 + i); pay = r.integers(0, 2, n).astype(np.uint8)
            cap, low, pvd = caps[i]
            m = R.select_ga(cap, costs[i], need, r) if scheme == "SM_GA" else (R.select_random(cap, need, r) if scheme == "SM_RAND" else R.select_greedy(cap, costs[i], need))
            st = R.embed(im, pay, m); sts.append(st); low_frac.append(float(low[m].mean())); mse.append(float(((st.astype(float)-im)**2).mean()))
            if i < 5: assert (R.extract(st, m) == pay).all()
        Fs = np.array([S.features(s) for s in sts]); feats[f"{scheme}_{bpp}"] = Fs.astype(np.float16)
        p = scores(Fs); S_[scheme] = p
        stats[scheme] = dict(**summ(p), low_branch_frac=round(float(np.mean(low_frac)), 3), mse=round(float(np.mean(mse)), 4),
                             psnr=round(float(np.mean([psnr(imgs[i], sts[i], data_range=255) for i in range(150)])), 2), secs=round(time.time()-t0, 1))
    # paired bootstrap on test images
    br = np.random.default_rng(seed+11); d = []; 
    for _ in range(1000):
        ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]
        d.append(roc_auc_score(yte[idx], S_["SM_GA"][idx]) - roc_auc_score(yte[idx], S_["SM_RAND"][idx]))
    diff = dict(auc_diff_GA_minus_RAND=round(stats["SM_GA"]["auc"]-stats["SM_RAND"]["auc"], 4), ci95=[round(float(np.percentile(d, 2.5)), 4), round(float(np.percentile(d, 97.5)), 4)], ci90=[round(float(np.percentile(d, 5)), 4), round(float(np.percentile(d, 95)), 4)])
    row = dict(seed=seed, bpp_raw=bpp, embedded_bits=need, bpp_embedded=round(need/16384, 4), n_test=nt, stats=stats, diff=diff); res.append(row); print(json.dumps(row), flush=True)
    json.dump(dict(seed=seed, N=N, skipped_low_capacity=skipped, rows=res), open(f"e2_seed{seed}.json", "w"), indent=1)
np.savez_compressed(f"e2_feats_seed{seed}.npz", **feats)
