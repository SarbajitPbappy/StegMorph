"""V2.2: three seeds for the two deciding cells of the budget sweep (4 epochs and 60 epochs, 4186 pairs): cost-guided minus random-key AUC (Q1) with subject bootstrap. Writes results/e39/e39_seeds_summary.json."""
import json, numpy as np
from sklearn.metrics import roc_auc_score
def auc(pc, ps, ix): return roc_auc_score(np.r_[np.zeros(len(ix)), np.ones(len(ix))], np.r_[pc[ix], ps[ix]])
out = {}
for ep in (4, 60):
    rows = []
    for s in (0, 1, 2):
        R = np.load(f"results/e39/net_RANDSEQ_s{s}_e{ep}_n4186_scores.npz", allow_pickle=True); C = np.load(f"results/e39/net_COSTKEY_s{s}_e{ep}_n4186_scores.npz", allow_pickle=True)
        subj = R["subjects"]; us = sorted(set(subj)); sidx = {u: np.where(subj == u)[0] for u in us}; allix = np.arange(len(subj)); ar, ac = auc(R["pc"], R["ps"], allix), auc(C["pc"], C["ps"], allix)
        br = np.random.default_rng(5); x = np.array([auc(C["pc"], C["ps"], ix) - auc(R["pc"], R["ps"], ix) for ix in (np.concatenate([sidx[u] for u in br.choice(us, len(us))]) for _ in range(500))])
        rows.append(dict(seed=s, auc_random=round(float(ar), 4), auc_costkey=round(float(ac), 4), q1=round(float(ac - ar), 4), ci=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)]))
    out[f"e{ep}_n4186"] = dict(mean_q1=round(float(np.mean([r["q1"] for r in rows])), 4), mean_random_auc=round(float(np.mean([r["auc_random"] for r in rows])), 4), seeds=rows); print(ep, out[f"e{ep}_n4186"]["mean_q1"], out[f"e{ep}_n4186"]["mean_random_auc"], [(r["q1"], r["ci"]) for r in rows])
json.dump(out, open("results/e39/e39_seeds_summary.json", "w"), indent=1)
