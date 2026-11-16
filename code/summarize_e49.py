"""V3-H27 / V3-H28: converged residual CNN on a new collection with the foreground keys (code/exp49_resnet_fg.py).
Usage (project root): python code/summarize_e49.py DIR TAG   e.g. results/e49_resnet_fg msd   -> DIR/summary_TAG.json
Reads DIR/net_{RANDFG,COSTFG}_s{0,1,2}_e60_n*.json and _scores.npz. Per seed: test AUC of both keys, Q1fg = AUC(COSTFG) - AUC(RANDFG) with a subject-cluster bootstrap interval (1000 resamples, seed 5),
random-key best validation AUC. Competence (pre-registered): random-key best validation AUC >= 0.85 in every seed (the plateau test is not available in this script; see the V3-H27 entry).
Rule: valid only if competent in every seed; met if the seed mean and every seed have Q1fg >= -0.02; 'gain survives' if the seed mean is below -0.15."""
import sys, glob, json, os, numpy as np
from sklearn.metrics import roc_auc_score
D, TAG = sys.argv[1], sys.argv[2]; rows = []
def auc(pc, ps, ix): return roc_auc_score(np.r_[np.zeros(len(ix)), np.ones(len(ix))], np.r_[pc[ix], ps[ix]])
for s in (0, 1, 2):
    fr = glob.glob(f"{D}/net_RANDFG_s{s}_e60_n*.json"); fc = glob.glob(f"{D}/net_COSTFG_s{s}_e60_n*.json")
    if not (fr and fc): continue
    jr, jc = json.load(open(fr[0])), json.load(open(fc[0])); R, C = np.load(fr[0][:-5] + "_scores.npz", allow_pickle=True), np.load(fc[0][:-5] + "_scores.npz", allow_pickle=True)
    subj = R["subjects"]; us = sorted(set(subj)); sidx = {u: np.where(subj == u)[0] for u in us}; allix = np.arange(len(subj)); ar, ac = auc(R["pc"], R["ps"], allix), auc(C["pc"], C["ps"], allix)
    br = np.random.default_rng(5); x = np.array([auc(C["pc"], C["ps"], ix) - auc(R["pc"], R["ps"], ix) for ix in (np.concatenate([sidx[u] for u in br.choice(us, len(us))]) for _ in range(1000))])
    rows.append(dict(seed=s, auc_random=round(float(ar), 4), auc_cost=round(float(ac), 4), q1fg=round(float(ac - ar), 4), ci=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)],
                     val_auc_random=jr["best_val_auc"], val_auc_cost=jc["best_val_auc"], competent=bool(jr["best_val_auc"] >= 0.85), n_train_pairs=jr.get("n_train_pairs"), n_test_patients=len(us)))
q = [r["q1fg"] for r in rows]; valid = len(rows) == 3 and all(r["competent"] for r in rows)
out = dict(tag=TAG, dir=D, n_seeds=len(rows), seeds=rows, mean_q1fg=round(float(np.mean(q)), 4) if q else None, range_q1fg=[min(q), max(q)] if q else None, valid_contrast=valid,
           rule_met=bool(valid and np.mean(q) >= -0.02 and all(v >= -0.02 for v in q)), gain_survives=bool(valid and np.mean(q) < -0.15))
json.dump(out, open(f"{D}/summary_{TAG}.json", "w"), indent=1); print(json.dumps(out, indent=1))
