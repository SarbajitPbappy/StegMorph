"""E14 (cost-guided key + HILL benchmark; derived from E11). HILL payload = bits embedded by StegMorph (message bits incl. header/delimiter, before 3x redundancy). Original E11 doc: faithful StegMorph (stegmorph.py) vs random-key and operator-matched controls, IXI subject-disjoint splits (data/splits), detectors A (SRM-lite+LR), B (SPAM+HGB), C (MPS CNN).
Subject-cluster bootstrap. Usage: python exp11_scale.py SEED   env: PAY (raw bpp list), NTR_FEAT, NTR_CNN, EPOCHS, NTE, DETS (A,B,C)"""
import os, sys, json, time, types, numpy as np
sys.modules.setdefault("cv2", types.ModuleType("cv2"))
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, HERE)
import stegmorph as SM, srm_lite as S
from hill_cost import hill_cost
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
seed = int(sys.argv[1]); T = 3; B = 2*T+1
PAY = [float(x) for x in os.environ.get("PAY", "0.02,0.05").split(",")]; DETS = os.environ.get("DETS", "A,B,C").split(",")
NF = int(os.environ.get("NTR_FEAT", "5239")); NC = int(os.environ.get("NTR_CNN", "3000")); NTE = int(os.environ.get("NTE", "1131")); EP = int(os.environ.get("EPOCHS", "15"))
DS = os.environ.get("DS", "ixi")
LD = lambda k: np.load(f"data/splits/{DS}_{k}.npz")
dtr, dva, dte = LD("train"), LD("val"), LD("test")
rs = np.random.default_rng(seed); sel = lambda d, n: np.sort(rs.permutation(len(d["images"]))[:n])
itr, iva, ite = sel(dtr, NF), sel(dva, 400), np.arange(min(NTE, len(dte["images"])))
Ctr, Cva, Cte = dtr["images"][itr], dva["images"][iva], dte["images"][ite]; Ste = dte["subject"][ite]
if "C" in DETS:
    import cnn_mps as C
def _trip(a, b, c):
    idx = ((a+T)*B + (b+T))*B + (c+T); cnt = np.bincount(idx.ravel(), minlength=B**3).astype(np.float64).reshape(B, B, B); return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T, T)
    Dh = f(x[:, :-1]-x[:, 1:]); Dv = f(x[:-1]-x[1:]); h = _trip(Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:]); v = _trip(Dv[:-2], Dv[1:-1], Dv[2:])
    Dd = f(x[:-1, :-1]-x[1:, 1:]); d1 = _trip(Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:]); xf = x[:, ::-1]; Da = f(xf[:-1, :-1]-xf[1:, 1:]); d2 = _trip(Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:])
    return np.concatenate([((h+v)/2).ravel(), ((d1+d2)/2).ravel()]).astype(np.float32)
def used_pairs(img, key, msg):
    flat = img.ravel(); nb = len(SM._text_to_bits(msg)); idx = nP = nL = 0
    for i in range(0, len(key)-1, 2):
        if idx >= nb: break
        if SM._use_pvd(flat[key[i]], flat[key[i+1]], SM.PVD_THRESHOLD): nP += 1; idx += 4
        else: nL += 1; idx += 2
    return nP, nL
def random_key(img, rng): n = img.size; return rng.permutation(n)[: (n//3)//2*2].astype(np.int64)
def mix_key(img, nP, nL, rng):
    flat = img.ravel(); n = flat.size; a = rng.integers(0, n, 400000); b = rng.integers(0, n, 400000)
    pv = np.abs((flat[a].astype(int) & 0xFC) - (flat[b].astype(int) & 0xFC)) > SM.PVD_THRESHOLD; used = set(); out = []
    for want, mask in ((nP, pv), (nL, ~pv)):
        got = 0
        for j in np.where(mask & (a != b))[0]:
            if got == want: break
            x, y = int(a[j]), int(b[j])
            if x in used or y in used: continue
            used.add(x); used.add(y); out.append((x, y)); got += 1
        if got < want: return None
    out = [out[i] for i in rng.permutation(len(out))]; return np.array([p for pr in out for p in pr], np.int64)

def cost_key(img, rng):
    rho = hill_cost(img).ravel(); pool = np.argsort(rho, kind="stable")[: img.size//3]; pool = rng.permutation(pool); return pool[: len(pool)//2*2].astype(np.int64)
def _H3(rp, rm, lam):
    e1 = np.exp(-lam*rp); e2 = np.exp(-lam*rm); z = 1 + e1 + e2; p1 = e1/z; p2 = e2/z; p0 = 1/z
    f = lambda p: -p*np.log2(np.maximum(p, 1e-300)); return (f(p1)+f(p2)+f(p0)), p1, p2
def hill_embed(img, cost, bits, rng):
    x = img.astype(np.float64); rp = np.minimum(cost, 1e10).copy(); rm = rp.copy(); rp[img == 255] = 1e10; rm[img == 0] = 1e10
    lo, hi = 0.0, 1e3
    while _H3(rp, rm, hi)[0].sum() > bits: hi *= 2
    for _ in range(60):
        mid = (lo+hi)/2
        if _H3(rp, rm, mid)[0].sum() > bits: lo = mid
        else: hi = mid
    _, p1, p2 = _H3(rp, rm, hi); u = rng.random(img.shape); y = x.copy(); y[u < p1] += 1; y[(u >= p1) & (u < p1+p2)] -= 1
    return np.clip(y, 0, 255).astype(np.uint8)
KEYS = {}
def make_all(imgs, bpp, tag):
    nraw = int(bpp*128*128); L = max(1, (nraw-32)//8); names = ("ORIG", "RANDSEQ", "COSTKEY", "COSTMIX", "HILL"); out = {k: [] for k in names}; st = {k: [] for k in out}; short = 0
    for i, im in enumerate(imgs):
        r = np.random.default_rng(seed*10**7 + int(bpp*1000)*10**4 + i + tag*7919); msg = "".join(chr(int(c)) for c in r.integers(0, 256, L))
        ck = (tag, i)
        if ck not in KEYS: KEYS[ck] = SM.generate_pixel_sequence(im, seed=int(r.integers(0, 2**31)))
        kG = KEYS[ck]; kR = random_key(im, r); kC = cost_key(im, r); nP, nL = used_pairs(im, kC, msg); kM = mix_key(im, nP, nL, r)
        if kM is None: short += 1; kM = kR
        nbits = len(SM._text_to_bits(msg))  # includes 3x redundancy = bits actually embedded
        for k, key in (("ORIG", kG), ("RANDSEQ", kR), ("COSTKEY", kC), ("COSTMIX", kM)):
            s = SM.embed(im, msg, key)
            if i < 2: assert SM.extract(s, key) == msg
            a_, b_ = used_pairs(im, key, msg); out[k].append(s); st[k].append((a_, b_, float(((s.astype(float)-im)**2).mean())))
        sH = hill_embed(im, hill_cost(im), float(nbits), r); out["HILL"].append(sH); st["HILL"].append((0, 0, float(((sH.astype(float)-im)**2).mean())))
    return out, {k: dict(pvd_pairs=round(float(np.mean([a for a, _, _ in v])), 1), lsb_pairs=round(float(np.mean([b for _, b, _ in v])), 1), mse=round(float(np.mean([c for _, _, c in v])), 4)) for k, v in st.items()}, short
SCH = ["RANDSEQ", "ORIG", "COSTKEY", "COSTMIX", "HILL"]; CON = {"P1_ORIG-RANDSEQ": ("ORIG", "RANDSEQ"), "Q1_COSTKEY-RANDSEQ": ("COSTKEY", "RANDSEQ"), "Q2_COSTKEY-COSTMIX": ("COSTKEY", "COSTMIX"), "Q3_COSTMIX-RANDSEQ": ("COSTMIX", "RANDSEQ"), "B1_HILL-RANDSEQ": ("HILL", "RANDSEQ")}
def feat_fit(fam, trc, trs, tec, tes):
    X = np.vstack([trc, trs]); y = np.r_[np.zeros(len(trc)), np.ones(len(trs))]; Z = np.vstack([tec, tes])
    if fam == "A": sc = StandardScaler().fit(X); p = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y).predict_proba(sc.transform(Z))[:, 1]
    else: p = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, y).predict_proba(Z)[:, 1]
    return p[:len(tec)], p[len(tec):]
def auc(pc, ps, idx): return roc_auc_score(np.r_[np.zeros(len(idx)), np.ones(len(idx))], np.r_[pc[idx], ps[idx]])
subj = sorted(set(Ste)); sidx = {s: np.where(Ste == s)[0] for s in subj}
def cluster_boot(sc, nb=1000):
    br = np.random.default_rng(seed+5); res = {c: [] for c in CON}
    for _ in range(nb):
        idx = np.concatenate([sidx[s] for s in br.choice(subj, len(subj))])
        for c, (a, b) in CON.items(): res[c].append(auc(*sc[a], idx) - auc(*sc[b], idx))
    return res
out = {"seed": seed, "n_train_feat": len(Ctr), "n_train_cnn": NC, "n_test": len(Cte), "n_test_subjects": len(subj), "epochs": EP, "results": {}}
FA = lambda L: np.array([S.features(x) for x in L]); FB = lambda L: np.array([spam(x) for x in L]); t0 = time.time()
fc = {}
if "A" in DETS: fc["A"] = (FA(Ctr), FA(Cte))
if "D" in DETS: fc["D"] = (FA(Ctr), FA(Cte))   # D = SRM-lite features + gradient boosting (stronger classifier)
if "B" in DETS: fc["B"] = (FB(Ctr), FB(Cte))
print("cover features", round(time.time()-t0), "s", flush=True)
for bpp in PAY:
    t0 = time.time(); str_, _, sh1 = make_all(Ctr, bpp, 11); sva, _, _ = make_all(Cva, bpp, 12); ste, stats_te, sh2 = make_all(Cte, bpp, 13)
    print("stego built", round(time.time()-t0), "s; stats(test)", stats_te, "mix_infeasible", sh1, sh2, flush=True)
    for fam in DETS:
        sc = {}
        for k in SCH:
            if fam in ("A", "B", "D"):
                F_ = FA if fam in ("A", "D") else FB; sc[k] = feat_fit(fam, fc[fam][0], F_(str_[k]), fc[fam][1], F_(ste[k]))
            else:
                pc, ps, v = C.fit_predict(Ctr[:NC], np.array(str_[k][:NC]), Cva, np.array(sva[k]), Cte, np.array(ste[k]), seed=seed*100, epochs=EP, log=None); sc[k] = (pc, ps); print("  cnn", k, "val_auc", round(v, 4), flush=True)
        allidx = np.arange(len(Cte)); row = {"auc": {k: round(float(auc(*sc[k], allidx)), 4) for k in SCH}, "stats_test": stats_te, "mix_infeasible": [sh1, sh2], "contrasts": {}}
        bs = cluster_boot(sc)
        for c, (a, b) in CON.items():
            d = row["auc"][a] - row["auc"][b]; x = np.array(bs[c]); row["contrasts"][c] = dict(diff=round(float(d), 4), ci95_subject_bootstrap=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)])
        out["results"][f"{DS.upper()}|{fam}|{bpp}"] = row; print(fam, bpp, row["auc"], {c: (v["diff"], v["ci95_subject_bootstrap"]) for c, v in row["contrasts"].items()}, flush=True)
        json.dump(out, open(f"e14_seed{seed}.json", "w"), indent=1)
    print("done", bpp, round(time.time()-t0), "s", flush=True)
print("DONE", seed)
