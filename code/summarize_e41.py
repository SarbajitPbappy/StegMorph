"""V2.5 summary: larger GA (GAMINX) against the random key and the cost-guided key (detectors F and M; same test slices), seeds 0-2, subject bootstrap. Writes results/e41/e41_summary.json."""
import json, numpy as np
from sklearn.metrics import roc_auc_score
def auc(pc, ps, ix): return roc_auc_score(np.r_[np.zeros(len(ix)), np.ones(len(ix))], np.r_[pc[ix], ps[ix]])
out = {}
for det in ("F", "M"):
    for bpp in (0.01, 0.02):
        for lab, b in (("RANDSEQ", "RANDSEQ"), ("COSTKEY", "COSTKEY"), ("ORIG", "ORIG")):
            rows = []
            for s in (0, 1, 2):
                A = np.load(f"results/e41/scores_s{s}_b{bpp}.npz", allow_pickle=True); B = np.load(f"results/e37/scores_s{s}_b{bpp}.npz", allow_pickle=True)
                subj = A["subjects"]; us = sorted(set(subj)); sidx = {u: np.where(subj == u)[0] for u in us}; al = np.arange(len(subj))
                pa, sa, pb, sb = A[f"{det}|GAMINX|pc"], A[f"{det}|GAMINX|ps"], B[f"{det}|{b}|pc"], B[f"{det}|{b}|ps"]; d = auc(pa, sa, al) - auc(pb, sb, al)
                br = np.random.default_rng(s + 5); x = np.array([auc(pa, sa, ix) - auc(pb, sb, ix) for ix in (np.concatenate([sidx[u] for u in br.choice(us, len(us))]) for _ in range(500))])
                rows.append(dict(seed=s, auc_gaminx=round(float(auc(pa, sa, al)), 4), diff=round(float(d), 4), ci=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)]))
            out[f"{det}|{bpp}|GAMINX-{lab}"] = dict(mean=round(float(np.mean([r["diff"] for r in rows])), 4), seeds=rows)
            if det == "F": print(bpp, "GAMINX minus", lab, out[f"{det}|{bpp}|GAMINX-{lab}"]["mean"], [r["diff"] for r in rows], "worst CI", min(r["ci"][0] for r in rows), max(r["ci"][1] for r in rows))
json.dump(out, open("results/e41/e41_summary.json", "w"), indent=1)
