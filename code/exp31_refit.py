"""E31: refit-aware bootstrap (extension of E23; pre-registered). Usage: python code/exp31_refit.py SEED ; env DET (A|D), NREP, PAY, OUT.
In each replicate the training subjects AND the test subjects are resampled with replacement (a subject keeps its cover and all stego versions), the detector is refit for every scheme, AUC is computed on the resampled test set."""
import os, sys, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L
from exp24 import cover_feats, feats_for, fit_score
from sklearn.metrics import roc_auc_score
from joblib import Parallel, delayed
SCH = ["RANDSEQ", "ORIG", "COSTKEY", "COSTMIX"]
def rep(r, det, Ftr, Cftr, Fte, Cfte, sidx_tr, sidx_te, subj_tr, subj_te, seed):
    rr = np.random.default_rng([seed, r]); tr = np.concatenate([sidx_tr[s] for s in rr.choice(subj_tr, len(subj_tr))]); te = np.concatenate([sidx_te[s] for s in rr.choice(subj_te, len(subj_te))]); a = {}
    for s in SCH:
        pc, ps = fit_score(det, Cftr[tr], Ftr[s][tr], Cfte[te], Fte[s][te], seed); a[s] = roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps])
    return a
if __name__ == "__main__":
    seed = int(sys.argv[1]); det = os.environ.get("DET", "A"); NREP = int(os.environ.get("NREP", "200")); PAY = [float(x) for x in os.environ.get("PAY", "0.01,0.02").split(",")]; OUT = os.environ.get("OUT", "results/e31"); os.makedirs(OUT, exist_ok=True)
    dtr, dte = L.load_split("ixi", "train"), L.load_split("ixi", "test"); tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8); te_ids = np.arange(len(dte["images"])); Ctr, Cte = dtr["images"][tr_ids], dte["images"][te_ids]
    Str_, Ste_ = dtr["subject"][tr_ids], dte["subject"][te_ids]; subj_tr, subj_te = sorted(set(Str_)), sorted(set(Ste_)); sidx_tr = {s: np.where(Str_ == s)[0] for s in subj_tr}; sidx_te = {s: np.where(Ste_ == s)[0] for s in subj_te}
    cf_tr, cf_te = cover_feats(Ctr, ["srm"])["srm"], cover_feats(Cte, ["srm"])["srm"]; res = {"seed": seed, "det": det, "nrep": NREP, "results": {}}
    for bpp in PAY:
        t0 = time.time(); Ftr, Fte = {}, {}
        for s in SCH: Ftr[s] = feats_for(Ctr, tr_ids, s, seed, bpp, 0, ["srm"], None, None, False)[0]["srm"]; Fte[s] = feats_for(Cte, te_ids, s, seed, bpp, 2, ["srm"], None, None, False)[0]["srm"]
        if "ORIG" in SCH:
            pass
        out = Parallel(n_jobs=int(os.environ.get("NJOBS", "6" if det == "A" else "1")))(delayed(rep)(r, det, Ftr, cf_tr, Fte, cf_te, sidx_tr, sidx_te, subj_tr, subj_te, seed) for r in range(NREP))
        A = {s: np.array([o[s] for o in out]) for s in SCH}; C = {"P1_ORIG-RANDSEQ": A["ORIG"] - A["RANDSEQ"], "Q1_COSTKEY-RANDSEQ": A["COSTKEY"] - A["RANDSEQ"], "Q3_COSTMIX-RANDSEQ": A["COSTMIX"] - A["RANDSEQ"]}
        res["results"][f"IXI|{det}|{bpp}"] = {"mean_auc": {s: float(A[s].mean()) for s in SCH}, "contrasts": {c: dict(mean=float(v.mean()), ci95=[float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]) for c, v in C.items()}}
        print(bpp, res["results"][f"IXI|{det}|{bpp}"], f"{time.time()-t0:.0f}s", flush=True); json.dump(res, open(f"{OUT}/e31_{det}_seed{seed}.json", "w"), indent=1)
