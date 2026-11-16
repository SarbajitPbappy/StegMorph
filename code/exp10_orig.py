"""E10: faithful StegMorph (user's stegmorph.py: GA fitness = max contrast of chained random pixels, thr 128, 3x redundancy)
vs random-key controls on IABI (subject-disjoint). Schemes: ORIG, RANDSEQ, RANDMIX (random positions, same #PVD/#LSB pairs as ORIG).
Usage: python exp10_orig.py SEED   (env: IABI_DIR, STEGPY_DIR, NTR, NTE, PAY)"""
import os, sys, json, time, types
import numpy as np
sys.modules.setdefault("cv2", types.ModuleType("cv2"))        # stegmorph.py imports cv2 only for file I/O
sys.path.insert(0, os.environ.get("STEGPY_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import stegmorph as SM
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import srm_lite as S

seed = int(sys.argv[1]); T = 3; B = 2*T+1
NTR = int(os.environ.get("NTR", "800")); NTE = int(os.environ.get("NTE", "200"))
PAY = [float(x) for x in os.environ.get("PAY", "0.01,0.02,0.05").split(",")]
D = os.environ.get("IABI_DIR", "data/raw/IABI")
def load(name, n):
    a = np.load(os.path.join(D, name))["images"].astype(np.float32); a = np.clip(np.round(a*255), 0, 255).astype(np.uint8)
    return a[:n, 16:144, 16:144]
Ctr = list(load("train.npz", NTR)); Cte = list(load("test.npz", NTE)); print("covers", len(Ctr), len(Cte), flush=True)

def _trip(a, b, c):
    idx = ((a+T)*B + (b+T))*B + (c+T); cnt = np.bincount(idx.ravel(), minlength=B**3).astype(np.float64).reshape(B, B, B)
    return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T, T)
    Dh = f(x[:, :-1]-x[:, 1:]); Dv = f(x[:-1]-x[1:]); h = _trip(Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:]); v = _trip(Dv[:-2], Dv[1:-1], Dv[2:])
    Dd = f(x[:-1, :-1]-x[1:, 1:]); d1 = _trip(Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:])
    xf = x[:, ::-1]; Da = f(xf[:-1, :-1]-xf[1:, 1:]); d2 = _trip(Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:])
    return np.concatenate([((h+v)/2).ravel(), ((d1+d2)/2).ravel()]).astype(np.float32)

def used_pairs(img, key, msg):
    """number of PVD / LSB pairs actually consumed when embedding msg along key (same walk as SM.embed)."""
    flat = img.ravel(); nbits = len(SM._text_to_bits(msg)); idx = nP = nL = 0
    for i in range(0, len(key)-1, 2):
        if idx >= nbits: break
        if SM._use_pvd(flat[key[i]], flat[key[i+1]], SM.PVD_THRESHOLD): nP += 1; idx += 4
        else: nL += 1; idx += 2
    return nP, nL

def random_key(img, rng):
    n = img.size; k = rng.permutation(n)[: (n//3)//2*2]; return k.astype(np.int64)

def mix_key(img, nP, nL, rng):
    """random disjoint pixel pairs with exactly nP PVD-branch pairs and nL LSB-branch pairs (None if infeasible)."""
    flat = img.ravel(); n = flat.size
    a = rng.integers(0, n, 400000); b = rng.integers(0, n, 400000)
    pv = np.abs((flat[a].astype(int) & 0xFC) - (flat[b].astype(int) & 0xFC)) > SM.PVD_THRESHOLD
    used = set(); out = []
    for want, mask in ((nP, pv), (nL, ~pv)):
        got = 0
        for j in np.where(mask & (a != b))[0]:
            x, y = int(a[j]), int(b[j])
            if x in used or y in used: continue
            used.add(x); used.add(y); out.append((x, y)); got += 1
            if got == want: break
        if got < want: return None
    out = [out[i] for i in rng.permutation(len(out))]
    return np.array([p for pr in out for p in pr], np.int64)

def make_all(imgs, bpp, tag):
    nraw = int(bpp*128*128); L = max(1, (nraw-32)//8)
    out = {k: [] for k in ("ORIG", "RANDSEQ", "RANDMIX")}; st = {k: [] for k in out}; short = 0
    for i, im in enumerate(imgs):
        r = np.random.default_rng(seed*10**6 + int(bpp*1000)*1000 + i + tag*7919)
        msg = "".join(chr(int(c)) for c in r.integers(0, 256, L))
        kG = SM.generate_pixel_sequence(im, seed=int(r.integers(0, 2**31))); kR = random_key(im, r)
        nP, nL = used_pairs(im, kG, msg); kM = mix_key(im, nP, nL, r)
        if kM is None: short += 1; kM = kR            # infeasible quota: fall back (counted)
        for k, key in (("ORIG", kG), ("RANDSEQ", kR), ("RANDMIX", kM)):
            s = SM.embed(im, msg, key)
            if i < 2: assert SM.extract(s, key) == msg
            nPk, nLk = used_pairs(im, key, msg)
            out[k].append(s); st[k].append((nPk, nLk, float(((s.astype(float)-im)**2).mean())))
    return out, {k: dict(pvd_pairs=round(float(np.mean([a for a, _, _ in v])), 1), lsb_pairs=round(float(np.mean([b for _, b, _ in v])), 1),
                         mse=round(float(np.mean([c for _, _, c in v])), 4)) for k, v in st.items()}, short

SCH = ["RANDSEQ", "ORIG", "RANDMIX"]
CON = {"P1_ORIG-RANDSEQ": ("ORIG", "RANDSEQ"), "P4_RANDMIX-RANDSEQ": ("RANDMIX", "RANDSEQ"), "P3_ORIG-RANDMIX": ("ORIG", "RANDMIX")}
def fitpred(fam, tr_c, tr_s, te_c, te_s):
    X = np.vstack([tr_c, tr_s]); y = np.r_[np.zeros(len(tr_c)), np.ones(len(tr_s))]; Z = np.vstack([te_c, te_s])
    if fam == "A": sc = StandardScaler().fit(X); p = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y).predict_proba(sc.transform(Z))[:, 1]
    else: p = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, y).predict_proba(Z)[:, 1]
    return p[:len(te_c)], p[len(te_c):]
def auc(pc, ps, idx): return roc_auc_score(np.r_[np.zeros(len(idx)), np.ones(len(idx))], np.r_[pc[idx], ps[idx]])
out = {"seed": seed, "n_train": len(Ctr), "n_test": len(Cte), "results": {}}
FA = lambda L: np.array([S.features(x) for x in L]); FB = lambda L: np.array([spam(x) for x in L])
trA, trB, teA, teB = FA(Ctr), FB(Ctr), FA(Cte), FB(Cte)
for bpp in PAY:
    t0 = time.time(); str_, stats_tr, sh1 = make_all(Ctr, bpp, 11); ste, stats_te, sh2 = make_all(Cte, bpp, 13)
    print("stats(test)", stats_te, "mix_infeasible", sh1, sh2, flush=True)
    for fam in ("A", "B"):
        sc = {}
        for k in SCH:
            sc[k] = fitpred(fam, trA if fam == "A" else trB, (FA if fam == "A" else FB)(str_[k]), teA if fam == "A" else teB, (FA if fam == "A" else FB)(ste[k]))
        allidx = np.arange(len(Cte)); row = {"auc": {k: round(float(auc(*sc[k], allidx)), 4) for k in SCH}, "stats_test": stats_te, "mix_infeasible": [sh1, sh2], "contrasts": {}}
        br = np.random.default_rng(seed+5); boots = {c: [] for c in CON}
        for _ in range(500):
            idx = br.integers(0, len(Cte), len(Cte))
            for c, (a, b) in CON.items(): boots[c].append(auc(*sc[a], idx) - auc(*sc[b], idx))
        for c, (a, b) in CON.items():
            d = row["auc"][a] - row["auc"][b]; bs = np.array(boots[c])
            row["contrasts"][c] = dict(diff=round(float(d), 4), ci90=[round(float(np.percentile(bs, 5)), 4), round(float(np.percentile(bs, 95)), 4)])
        out["results"][f"IABI|{fam}|{bpp}"] = row; print(fam, bpp, row["auc"], {c: v["diff"] for c, v in row["contrasts"].items()}, flush=True)
        json.dump(out, open(f"e10_seed{seed}.json", "w"), indent=1)
    print("done", bpp, round(time.time()-t0, 1), flush=True)
print("DONE", seed)
