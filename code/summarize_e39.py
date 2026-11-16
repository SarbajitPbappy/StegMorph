"""V2.2 budget sweep summary (V2-H3): cost-guided minus random-key AUC (Q1) of the residual CNN per budget cell, seed 0, subject-cluster bootstrap (no refit). Writes results/e39/e39_summary.json and Overleaf/article/figures/fig_budget.png."""
import json, numpy as np
from sklearn.metrics import roc_auc_score
def auc(pc, ps, ix): return roc_auc_score(np.r_[np.zeros(len(ix)), np.ones(len(ix))], np.r_[pc[ix], ps[ix]])
EP, NN = (4, 10, 30, 60), (600, 1000, 2500, 4186); out = {}; rows = []
for ep in EP:
    for n in NN:
        R = np.load(f"results/e39/net_RANDSEQ_s0_e{ep}_n{n}_scores.npz", allow_pickle=True); C = np.load(f"results/e39/net_COSTKEY_s0_e{ep}_n{n}_scores.npz", allow_pickle=True)
        subj = R["subjects"]; us = sorted(set(subj)); sidx = {u: np.where(subj == u)[0] for u in us}; allix = np.arange(len(subj)); ar, ac = auc(R["pc"], R["ps"], allix), auc(C["pc"], C["ps"], allix)
        br = np.random.default_rng(5); x = np.array([auc(C["pc"], C["ps"], ix) - auc(R["pc"], R["ps"], ix) for ix in (np.concatenate([sidx[u] for u in br.choice(us, len(us))]) for _ in range(500))])
        r = dict(epochs=ep, pairs=n, auc_random=round(float(ar), 4), auc_costkey=round(float(ac), 4), q1=round(float(ac - ar), 4), ci=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)]); rows.append(r); out[f"e{ep}_n{n}"] = r
        print(r)
json.dump(out, open("results/e39/e39_summary.json", "w"), indent=1)
comp = [r for r in rows if r["auc_random"] > 0.85]; print("cells with random-key AUC > 0.85:", len(comp), "; Q1 range", min(r["q1"] for r in comp), max(r["q1"] for r in comp), "; all >= -0.02:", all(r["q1"] >= -0.02 for r in comp), "; lower CI bounds", min(r["ci"][0] for r in comp))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.7)); cols = ["#9ecae1", "#6baed6", "#3182bd", "#08519c"]
for i, ep in enumerate(EP):
    rr = [r for r in rows if r["epochs"] == ep]; ax[0].errorbar([r["auc_random"] for r in rr], [r["q1"] for r in rr], yerr=[[r["q1"] - r["ci"][0] for r in rr], [r["ci"][1] - r["q1"] for r in rr]], marker="o", ms=3, lw=1, capsize=1.5, color=cols[i], label=f"{ep} epochs")
ax[0].axvline(0.85, color="grey", ls=":", lw=1); ax[0].axhline(0, color="k", lw=.6); ax[0].axhline(-0.02, color="C3", ls="--", lw=.8); ax[0].set_xlabel("random-key AUC (detector competence)"); ax[0].set_ylabel("cost-guided minus random AUC"); ax[0].legend(fontsize=6, frameon=False)
for i, n in enumerate(NN):
    rr = [r for r in rows if r["pairs"] == n]; ax[1].plot([r["epochs"] for r in rr], [r["q1"] for r in rr], marker="o", ms=3, lw=1, label=f"{n} pairs")
ax[1].set_xscale("log"); ax[1].set_xticks(EP); ax[1].set_xticklabels(EP); ax[1].axhline(0, color="k", lw=.6); ax[1].axhline(-0.02, color="C3", ls="--", lw=.8); ax[1].set_xlabel("training epochs"); ax[1].legend(fontsize=6, frameon=False)
for a in ax: a.tick_params(labelsize=7); a.xaxis.label.set_size(7.5); a.yaxis.label.set_size(7.5)
plt.tight_layout(); plt.savefig("Overleaf/article/figures/fig_budget.png", dpi=200)
