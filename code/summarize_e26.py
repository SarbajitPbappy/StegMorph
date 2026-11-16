"""E26 summary: AUC per (net, scheme, seed), contrasts against RANDSEQ with subject-cluster bootstrap, and the training-budget table. Writes results/e26/e26_summary.json and Overleaf/article/tables/tab_budget.tex"""
import glob, json, os, numpy as np
from sklearn.metrics import roc_auc_score
R = {}
ALL = []
for f in sorted(glob.glob("results/e26/*_b0.01_s*.json")):
    info = json.load(open(f)); sc_ = np.load(f.replace(".json", "_scores.npz"), allow_pickle=True); info["failed"] = info["best_val_auc"] < 0.55; ALL.append((info, sc_))
    if not info["failed"] and (info["net"], info["scheme"], info["seed"]) not in R: R[(info["net"], info["scheme"], info["seed"])] = (info, sc_)
def auc(pc, ps, idx): return roc_auc_score(np.r_[np.zeros(len(idx)), np.ones(len(idx))], np.r_[pc[idx], ps[idx]])
out = {}; rng = np.random.default_rng(11)
for (net, sch, seed), (info, sc) in R.items():
    if sch == "RANDSEQ": continue
    if (net, "RANDSEQ", seed) not in R: continue
    r = R[(net, "RANDSEQ", seed)][1]; subj = sc["subjects"]; us = sorted(set(subj)); sidx = {s: np.where(subj == s)[0] for s in us}
    d = auc(sc["pc"], sc["ps"], np.arange(len(subj))) - auc(r["pc"], r["ps"], np.arange(len(subj))); bs = []
    for _ in range(500): ix = np.concatenate([sidx[s] for s in rng.choice(us, len(us))]); bs.append(auc(sc["pc"], sc["ps"], ix) - auc(r["pc"], r["ps"], ix))
    out[f"{net}|{sch}|{seed}"] = dict(diff=round(float(d), 4), ci95=[round(float(np.percentile(bs, 2.5)), 4), round(float(np.percentile(bs, 97.5)), 4)], auc=info["test_auc"], rand_auc=R[(net, "RANDSEQ", seed)][0]["test_auc"])
json.dump(out, open("results/e26/e26_summary.json", "w"), indent=1)
rows = [(i["net"], i["scheme"], i["seed"], i["params"], i["n_train_pairs"], i["epochs_run"], i["best_epoch"], i["minutes"], i["best_val_auc"], i["test_auc"], i.get("init", 0), i["failed"]) for (i, _s) in ALL]
NETN = {"net": "Residual CNN", "srnet": "SRNet-style"}
tex = "\\setlength{\\tabcolsep}{3pt}\\begin{tabular}{@{}llcccc@{}}\n\\toprule\nNetwork & Key & Seed & Best ep. & Val AUC & Test AUC \\\\\n\\midrule\n"
for r in sorted(rows): tex += f"{NETN[r[0]].replace('Residual CNN','Residual')} & {r[1]}{'$^{\\dagger}$' if r[11] else ''}{' (init ' + str(r[10]) + ')' if r[10] or r[11] else ''} & {r[2]} & {r[6]+1} & {r[8]:.3f} & {r[9]:.3f} \\\\\n"
tex += "\\bottomrule\n\\end{tabular}\n"; open("Overleaf/article/tables/tab_budget.tex", "w").write(tex); print(tex); print(json.dumps(out, indent=1))
