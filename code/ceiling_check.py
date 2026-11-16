"""Plan 0.6 ceiling/chance check on REAL MRI (Alzheimer mirror, 128x128 JPEG-decoded). Pipeline validation, NOT a claim.
No subject IDs exist => split is image-level (leakage-prone); exact-duplicate files kept in the same split."""
import sys, json, glob, hashlib, numpy as np, time
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import embed as E, srm_lite as S
files = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
res = {}
for seed in (0, 1, 2):
    rng = np.random.default_rng(seed); sel = rng.permutation(len(files))[:N]
    imgs = [np.array(Image.open(files[i]).convert("L"), np.uint8) for i in sel]
    grp = [hashlib.sha256(im.tobytes()).hexdigest() for im in imgs]        # duplicates share a group
    ug = sorted(set(grp)); gperm = {g: k for k, g in enumerate(rng.permutation(ug))}
    isTrain = np.array([gperm[g] < 0.7*len(ug) for g in grp])
    t0 = time.time(); Fc = np.array([S.features(im) for im in imgs]); tf = time.time()-t0
    out = {}
    def run(name, mk):
        Fs = np.array([S.features(mk(im, i)) for i, im in enumerate(imgs)])
        Xtr = np.vstack([Fc[isTrain], Fs[isTrain]]); ytr = np.r_[np.zeros(isTrain.sum()), np.ones(isTrain.sum())]
        Xte = np.vstack([Fc[~isTrain], Fs[~isTrain]]); yte = np.r_[np.zeros((~isTrain).sum()), np.ones((~isTrain).sum())]
        sc = StandardScaler().fit(Xtr); clf = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(Xtr), ytr)
        p = clf.predict_proba(sc.transform(Xte))[:, 1]; auc = roc_auc_score(yte, p)
        pe = 0.5*min(((p < t) & (yte == 1)).mean() + ((p >= t) & (yte == 0)).mean() for t in np.unique(p)) if False else None
        out[name] = round(float(auc), 4)
    bits = lambda im, n: np.random.default_rng(seed*100000+n).integers(0, 2, n, dtype=np.uint8)
    run("LSB_seq_1.0bpp", lambda im, i: E.lsb_embed(im, bits(im, im.size))[0])
    run("LSB_keyed_0.4bpp", lambda im, i: E.lsb_embed(im, bits(im, int(.4*im.size)), key=i)[0])
    run("LSB_keyed_0.1bpp", lambda im, i: E.lsb_embed(im, bits(im, int(.1*im.size)), key=i)[0])
    run("HILL_sim_0.4bpp", lambda im, i: E.hill_simulate(im, 0.4, seed*100000+i)[0])
    # chance: 'stego' = untouched cover with fresh no-op (identical image) -> features identical => AUC must be 0.5
    run("cover_vs_cover", lambda im, i: im.copy())
    res[f"seed{seed}"] = {"n_images": N, "n_train_groups": int(isTrain.sum()), "feat_time_s": round(tf, 1), "auc": out}
    print(seed, out, flush=True)
json.dump(res, open("ceiling_check_result.json", "w"), indent=1)
