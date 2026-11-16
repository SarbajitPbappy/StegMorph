"""V3.3 (V3-H24): choose the payload for a new collection on the VALIDATION split only.
Detector A (SRM-lite + logistic regression) is fitted on the training stego sets of the random key (seed 0, 80% of training subjects) and scored on the validation split (no test images are read).
Candidates 0.0027, 0.005, 0.01, 0.02 bpp; the chosen payload is the one whose random-key validation AUC is closest to 0.75 among those inside 0.60..0.85.
Usage: python code/exp44_payload_select.py DS ; env OUT (default results/e44)."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L
from exp24 import cover_feats, feats_for, fit_score
from sklearn.metrics import roc_auc_score
if __name__ == "__main__":
    ds = sys.argv[1]; SCH = os.environ.get("SCHEME", "RANDSEQ"); OUT = os.environ.get("OUT", "results/e44"); os.makedirs(OUT, exist_ok=True); seed = 0
    dtr, dva = L.load_split(ds, "train"), L.load_split(ds, "val"); tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8); va_ids = np.arange(len(dva["images"])); Ctr, Cva = dtr["images"][tr_ids], dva["images"][va_ids]
    fc_tr, fc_va = cover_feats(Ctr, ["srm"])["srm"], cover_feats(Cva, ["srm"])["srm"]; res = {}
    for bpp in (0.0027, 0.005, 0.01, 0.02):
        Ftr = feats_for(Ctr, tr_ids, SCH, seed, bpp, 0, ["srm"], None, None, False)[0]["srm"]; Fva = feats_for(Cva, va_ids, SCH, seed, bpp, 1, ["srm"], None, None, False)[0]["srm"]
        pc, ps = fit_score("A", fc_tr, Ftr, fc_va, Fva, seed); a = float(roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps])); res[str(bpp)] = round(a, 4); print(ds, bpp, "validation AUC (A, random key):", round(a, 4), flush=True)
    ok = {b: a for b, a in res.items() if 0.60 <= a <= 0.85}; chosen = min(ok, key=lambda b: abs(ok[b] - 0.75)) if ok else None
    json.dump(dict(dataset=ds, detector="A", seed=seed, scheme=SCH, validation_auc=res, rule="closest to 0.75 within 0.60..0.85", chosen_bpp=chosen), open(f"{OUT}/payload_{ds}" + ("" if SCH == "RANDSEQ" else "_" + SCH) + ".json", "w"), indent=1); print("chosen payload:", chosen)
