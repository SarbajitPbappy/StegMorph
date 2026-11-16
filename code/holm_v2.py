"""Honest Holm v2 (responds to verifier defects 1 and 5). Inputs: stored JSON only.
SE per cell = sqrt(bootstrap_SE^2 + seed_SD^2): subject-bootstrap SE (test-subject variance) plus between-seed SD (detector refit / key / message
variance across the 3 runs). Still NOT covering training-subject resampling (seeds reuse the full train split): stated limitation.
Family: PRIMARY contrasts only, non-duplicated cells: P1 (GA key vs random key) for E11 (0.02, 0.05), E12 (0.005 only; its 0.01 duplicates E14), E13 (3 scenarios), E14 (0.01, 0.02);
plus Q1 (cost-guided vs random) for E14. Floor SE 0.005 (no p below what AUC resolution supports). Two-sided normal p; TOST for +/-0.02."""
import json, glob, numpy as np
from scipy.stats import norm
SRC = {"E11": ("results/e11/e11_seed*.json", lambda k: k.endswith(("|0.02", "|0.05")), ["P1_ORIG-RANDSEQ"]),
       "E12": ("results/e12/e11_seed*.json", lambda k: k.endswith("|0.005"), ["P1_ORIG-RANDSEQ"]),
       "E13": ("results/e13/e13_*_seed*.json", lambda k: True, ["P1_ORIG-RANDSEQ"]),
       "E14": ("results/e14/e14_seed*.json", lambda k: True, ["P1_ORIG-RANDSEQ", "Q1_COSTKEY-RANDSEQ"])}
M = 0.02; FLOOR = 0.005; rows = []
for ex, (pat, keep, cons) in SRC.items():
    R = {}
    for f in sorted(glob.glob(pat)):
        for k, v in json.load(open(f))["results"].items():
            if keep(k): R.setdefault(k, []).append(v)
    for k, L in sorted(R.items()):
        if len(L) < 3: continue
        for c in cons:
            d = np.array([v["contrasts"][c]["diff"] for v in L]); b = np.array([(v["contrasts"][c]["ci95_subject_bootstrap"][1] - v["contrasts"][c]["ci95_subject_bootstrap"][0]) / 3.92 for v in L])
            se = max(float(np.sqrt(b.mean() ** 2 + d.std(ddof=1) ** 2)), FLOOR); m = float(d.mean())
            rows.append(dict(exp=ex, cell=k, contrast=c, diff=m, se=se, p=2 * (1 - norm.cdf(abs(m) / se)), p_tost=max(1 - norm.cdf((m + M) / se), norm.cdf((m - M) / se))))
def holm(ps):
    o = np.argsort(ps); n = len(ps); a = np.empty(n); run = 0
    for r, i in enumerate(o): run = max(run, min(1, (n - r) * ps[i])); a[i] = run
    return a
a = holm(np.array([r["p"] for r in rows])); b = holm(np.array([r["p_tost"] for r in rows]))
for r, x, y in zip(rows, a, b): r["p_holm"] = float(x); r["p_tost_holm"] = float(y)
json.dump(rows, open("results/holm/holm_v2.json", "w"), indent=1)
L = [f"# Holm v2 ({len(rows)} primary tests)", "", __doc__, "", "| exp | cell | contrast | diff | SE | p Holm | differs | TOST p Holm | equivalent |", "|---|---|---|---|---|---|---|---|---|"]
for r in rows: L.append(f"| {r['exp']} | {r['cell']} | {r['contrast']} | {r['diff']:+.3f} | {r['se']:.3f} | {r['p_holm']:.3g} | {'YES' if r['p_holm']<.05 else 'no'} | {r['p_tost_holm']:.3g} | {'YES' if r['p_tost_holm']<.05 else 'no'} |")
nd = sum(r["p_holm"] < .05 for r in rows); ne = sum(r["p_tost_holm"] < .05 for r in rows)
L += ["", f"Differences surviving Holm: {nd}/{len(rows)}; equivalences within +/-0.02: {ne}/{len(rows)}."]
open("results/holm/HOLM_v2.md", "w").write("\n".join(L)); print("\n".join(L[4:]))
