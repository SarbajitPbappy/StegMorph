"""Holm correction + equivalence (TOST) across E11-E14. Inputs: stored JSON only.
Per cell/contrast: mean diff over 3 seeds; SE from each seed's subject-bootstrap 95% CI ((hi-lo)/3.92); pooled SE = mean of seed SEs
(conservative: the three seeds reuse the same test subjects, so no 1/sqrt(3) shrinkage). Two-sided normal p for H0: diff=0.
TOST p for equivalence margin +/-0.02: max(p(diff>-0.02), p(diff<+0.02)). Holm over the whole family, separately for difference and equivalence tests."""
import json, glob, numpy as np
from scipy.stats import norm
FAM = {"E11": ("results/e11/e11_seed*.json", ["P1_ORIG-RANDSEQ", "P3_ORIG-RANDMIX"]),
       "E12": ("results/e12/e11_seed*.json", ["P1_ORIG-RANDSEQ", "P3_ORIG-RANDMIX"]),
       "E13noHH": ("results/e13/e13_noHH_seed*.json", ["P1_ORIG-RANDSEQ", "P3_ORIG-RANDMIX"]),
       "E13noIOP": ("results/e13/e13_noIOP_seed*.json", ["P1_ORIG-RANDSEQ", "P3_ORIG-RANDMIX"]),
       "E13oasis": ("results/e13/e13_oasis_seed*.json", ["P1_ORIG-RANDSEQ", "P3_ORIG-RANDMIX"]),
       "E14": ("results/e14/e14_seed*.json", ["P1_ORIG-RANDSEQ", "Q1_COSTKEY-RANDSEQ", "Q2_COSTKEY-COSTMIX"])}
M = 0.02; rows = []
for ex, (pat, cons) in FAM.items():
    R = {}
    for f in sorted(glob.glob(pat)):
        d = json.load(open(f))
        for k, v in d["results"].items(): R.setdefault(k, []).append(v)
    for k, L in sorted(R.items()):
        if len(L) < 3: continue
        for c in cons:
            if c not in L[0]["contrasts"]: continue
            dif = np.mean([v["contrasts"][c]["diff"] for v in L]); se = np.mean([(v["contrasts"][c]["ci95_subject_bootstrap"][1] - v["contrasts"][c]["ci95_subject_bootstrap"][0]) / 3.92 for v in L])
            se = max(se, 1e-4); p = 2 * (1 - norm.cdf(abs(dif) / se)); ptost = max(1 - norm.cdf((dif + M) / se), norm.cdf((dif - M) / se))
            rows.append(dict(exp=ex, cell=k, contrast=c, diff=dif, se=se, p=p, p_tost=ptost))
def holm(ps):
    o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for r, i in enumerate(o): run = max(run, min(1, (m - r) * ps[i])); adj[i] = run
    return adj
a = holm(np.array([r["p"] for r in rows])); b = holm(np.array([r["p_tost"] for r in rows]))
for r, x, y in zip(rows, a, b): r["p_holm"] = x; r["p_tost_holm"] = y
json.dump(rows, open("results/holm/holm_E11_E14.json", "w"), indent=1)
L = [f"# Holm correction across E11-E14 ({len(rows)} tests)", "", __doc__, "", "| exp | cell | contrast | diff | SE | p | p Holm | differs (Holm<0.05) | TOST p Holm | equivalent (<0.05) |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in rows: L.append(f"| {r['exp']} | {r['cell']} | {r['contrast']} | {r['diff']:+.3f} | {r['se']:.3f} | {r['p']:.3g} | {r['p_holm']:.3g} | {'YES' if r['p_holm']<.05 else 'no'} | {r['p_tost_holm']:.3g} | {'YES' if r['p_tost_holm']<.05 else 'no'} |")
nd = sum(r["p_holm"] < .05 for r in rows); ne = sum(r["p_tost_holm"] < .05 for r in rows)
L += ["", f"Differences surviving Holm: {nd}/{len(rows)}. Equivalences (within +/-0.02) surviving Holm: {ne}/{len(rows)}.",
      "Limitation: SE is derived from the bootstrap CI over test subjects only; detector refit variance is covered only by the seed spread. Treat p-values as approximate."]
open("results/holm/HOLM_E11_E14.md", "w").write("\n".join(L)); print("\n".join(L[-3:]));
for r in rows:
    if r["contrast"].startswith("P1") : print(r["exp"], r["cell"], f"{r['diff']:+.3f}", f"holm={r['p_holm']:.3g}", f"tost={r['p_tost_holm']:.3g}")
