"""V3.1: Q1 (cost-guided minus random-key AUC) per seed for a CNN trained with exp42_curriculum.py, with the pre-registered competence rule (V3 pre-registration).
Usage: python code/summarize_e42.py NET   (yedroudj | srnet) -> results/e42/summary_NET.json.  Rule: both keys reach a validation-loss plateau AND random-key validation AUC >= 0.85, per seed; the contrast is valid only if all seeds comply.
H21 (yedroudj): Q1 >= -0.02 on the seed mean and in every seed (only meaningful if the contrast is valid)."""
import sys, json, os, numpy as np
from sklearn.metrics import roc_auc_score
def auc(pc, ps, ix): return roc_auc_score(np.r_[np.zeros(len(ix)), np.ones(len(ix))], np.r_[pc[ix], ps[ix]])
net = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else ""; sfx = f"_{tag}" if tag else ""; rows = []
for s in (0, 1, 2):
    fr, fc = f"results/e42/{net}_RANDSEQ_s{s}{sfx}", f"results/e42/{net}_COSTKEY_s{s}{sfx}"
    if not (os.path.exists(fr + ".json") and os.path.exists(fc + ".json")): continue
    jr, jc = json.load(open(fr + ".json")), json.load(open(fc + ".json")); R, C = np.load(fr + "_scores.npz", allow_pickle=True), np.load(fc + "_scores.npz", allow_pickle=True)
    subj = R["subjects"]; us = sorted(set(subj)); sidx = {u: np.where(subj == u)[0] for u in us}; allix = np.arange(len(subj)); ar, ac = auc(R["pc"], R["ps"], allix), auc(C["pc"], C["ps"], allix)
    br = np.random.default_rng(5); x = np.array([auc(C["pc"], C["ps"], ix) - auc(R["pc"], R["ps"], ix) for ix in (np.concatenate([sidx[u] for u in br.choice(us, len(us))]) for _ in range(1000))])
    comp = bool(jr["plateau_val_loss"] and jc["plateau_val_loss"] and jr["best_val_auc"] >= 0.85)
    rows.append(dict(seed=s, auc_random=round(float(ar), 4), auc_costkey=round(float(ac), 4), q1=round(float(ac - ar), 4), ci=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)],
                     val_auc_random=jr["best_val_auc"], val_auc_costkey=jc["best_val_auc"], plateau_random=jr["plateau_val_loss"], plateau_costkey=jc["plateau_val_loss"], competent=comp))
valid = len(rows) == 3 and all(r["competent"] for r in rows); q = [r["q1"] for r in rows]
out = dict(net=net, tag=tag, n_seeds=len(rows), seeds=rows, mean_q1=round(float(np.mean(q)), 4) if q else None, range_q1=[min(q), max(q)] if q else None, mean_random_auc=round(float(np.mean([r["auc_random"] for r in rows])), 4) if rows else None,
           valid_contrast=valid, H21_met=bool(valid and np.mean(q) >= -0.02 and all(v >= -0.02 for v in q)) if net == "yedroudj" else None)
json.dump(out, open(f"results/e42/summary_{net}{sfx}.json", "w"), indent=1); print(json.dumps(out, indent=1))
