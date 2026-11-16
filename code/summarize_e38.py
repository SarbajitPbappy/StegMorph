"""V2.3 summary: reference embedders (HILL, S-UNIWARD) against the hybrid keys at equal modification count, from stored score files (same test slices). Writes results/e38/e38_summary.json.
Equal ~1.4% changed pixels: HILL/S-UNIWARD at 0.032 bpp (e38/hi) against RANDSEQ/COSTKEY at 0.01 bpp (e37).
Equal ~0.37% changed pixels: RANDSEQ/COSTKEY at 0.0027 bpp (e38/lo) against HILL at 0.01 bpp (e37) and S-UNIWARD at 0.01 bpp (e38/su)."""
import json, numpy as np
from sklearn.metrics import roc_auc_score
def ld(p): return np.load(p, allow_pickle=True)
def auc(pc, ps, ix): return roc_auc_score(np.r_[np.zeros(len(ix)), np.ones(len(ix))], np.r_[pc[ix], ps[ix]])
out = {}
for det in ("F", "M"):
    for label, pairs in {"1.4pct": [(("e38/hi", "0.032", "HILLR"), ("e37", "0.01", "RANDSEQ")), (("e38/hi", "0.032", "SUNIR"), ("e37", "0.01", "RANDSEQ")), (("e38/hi", "0.032", "HILLR"), ("e37", "0.01", "COSTKEY")), (("e38/hi", "0.032", "SUNIR"), ("e37", "0.01", "COSTKEY"))],
                         "0.37pct": [(("e37", "0.01", "HILLR"), ("e38/lo", "0.0027", "RANDSEQ")), (("e38/su", "0.01", "SUNIR"), ("e38/lo", "0.0027", "RANDSEQ")), (("e37", "0.01", "HILLR"), ("e38/lo", "0.0027", "COSTKEY")), (("e38/su", "0.01", "SUNIR"), ("e38/lo", "0.0027", "COSTKEY"))]}.items():
        for a, b in pairs:
            rows = []
            for s in (0, 1, 2):
                A, B = ld(f"results/{a[0]}/scores_s{s}_b{a[1]}.npz"), ld(f"results/{b[0]}/scores_s{s}_b{b[1]}.npz"); subj = A["subjects"]; us = sorted(set(subj)); sidx = {u: np.where(subj == u)[0] for u in us}
                pa, sa, pb, sb = A[f"{det}|{a[2]}|pc"], A[f"{det}|{a[2]}|ps"], B[f"{det}|{b[2]}|pc"], B[f"{det}|{b[2]}|ps"]; allix = np.arange(len(pa)); d = auc(pa, sa, allix) - auc(pb, sb, allix)
                br = np.random.default_rng(s + 5); x = np.array([auc(pa, sa, ix) - auc(pb, sb, ix) for ix in (np.concatenate([sidx[u] for u in br.choice(us, len(us))]) for _ in range(500))])
                rows.append(dict(seed=s, auc_a=round(float(auc(pa, sa, allix)), 4), auc_b=round(float(auc(pb, sb, allix)), 4), diff=round(float(d), 4), ci=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)]))
            out[f"{det}|{label}|{a[2]}@{a[1]} minus {b[2]}@{b[1]}"] = dict(mean=round(float(np.mean([r['diff'] for r in rows])), 4), seeds=rows)
json.dump(out, open("results/e38/e38_summary.json", "w"), indent=1)
for k, v in out.items(): print(k, v["mean"], [r["diff"] for r in v["seeds"]], [r["ci"] for r in v["seeds"]][0])
