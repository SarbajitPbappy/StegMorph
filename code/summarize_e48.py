"""V3.6 (V3-H26): three-seed summary on the BraTS 2020 cohort of 107 non-MSD patients (results/e48_brats; payload chosen on validation only, results/e48_brats/payload_bratst2_RANDFG.json).
Per detector (A, D from e24_seed*.json; F, M from e37_seed*.json): AUC per scheme and seed, seed mean and range, contrasts P1fg = ORIG - RANDFG, Q1fg = COSTFG - RANDFG, Q4fg = ANTIFG - RANDFG, ORIG - RANDSEQ, RANDFG - RANDSEQ, and COSTKEY/COSTMIX/ANTIKEY minus RANDSEQ (descriptive), with the per-seed subject(patient)-bootstrap interval.
Pre-registered rules (state/CLAIMS.md, V3-H26 pre-registration), seed means, per detector:
 H26a (position effect replicates): Q1fg < -0.05 for F, A and D.   H26b (GA key no advantage): P1fg >= -0.02 for A, D, F and M.   H26c (maxSRM given the pool does not remove the gain, a prediction from MSD): Q1fg < -0.05 for M.
 H26d (converged residual CNN) is judged by code/summarize_e49.py on results/e49_resnet_fg_brats.
Writes results/e48_brats/summary.json."""
import json, os, numpy as np
OUT = "results/e48_brats"; pay = json.load(open(f"{OUT}/payload_bratst2_RANDFG.json"))["chosen_bpp"]; ds = "bratst2"
SCH = ["RANDFG", "ORIG", "RANDSEQ", "COSTFG", "ANTIFG", "COSTKEY", "COSTMIX", "ANTIKEY"]
def rows(det):
    f = "e24" if det in ("A", "D") else "e37"; r = []
    for s in (0, 1, 2):
        d = json.load(open(f"{OUT}/{f}_seed{s}.json")); r.append((d.get("n_train_subjects"), d.get("n_test_subjects"), d["results"][f"{ds}|{det}|{pay}"]))
    return r
CON = (("P1fg", "ORIG", "RANDFG"), ("Q1fg", "COSTFG", "RANDFG"), ("Q4fg", "ANTIFG", "RANDFG"), ("ORIG-RANDSEQ", "ORIG", "RANDSEQ"), ("RANDFG-RANDSEQ", "RANDFG", "RANDSEQ"),
       ("Q1", "COSTKEY", "RANDSEQ"), ("Q3", "COSTMIX", "RANDSEQ"), ("Q4", "ANTIKEY", "RANDSEQ"))
out = {"payload_bpp": pay, "detectors": {}}
for det in ("A", "D", "F", "M"):
    R = rows(det); auc = {s: [r[2]["auc"].get(s) for r in R] for s in SCH}; con = {}
    for name, a, b in CON:
        if None in auc[a] or None in auc[b]: continue
        d = [round(auc[a][i] - auc[b][i], 4) for i in range(3)]; ci = [R[i][2].get("contrasts", {}).get(f"{a}-{b}", {}).get("ci95_subject_bootstrap") for i in range(3)]
        con[name] = dict(per_seed=d, mean=round(float(np.mean(d)), 4), range=[min(d), max(d)], ci95_per_seed=ci)
    out["detectors"][det] = dict(auc_mean={s: (round(float(np.mean(v)), 4) if None not in v else None) for s, v in auc.items()}, auc_per_seed=auc, contrasts=con)
out["n_train_patients_seed"] = [r[0] for r in rows("A")]; out["n_test_patients"] = rows("A")[0][1]
g = lambda d, c: out["detectors"][d]["contrasts"][c]["mean"]
out["rules"] = dict(
    H26a=dict(values={d: g(d, "Q1fg") for d in ("F", "A", "D")}, met=bool(all(g(d, "Q1fg") < -0.05 for d in ("F", "A", "D")))),
    H26b=dict(values={d: g(d, "P1fg") for d in ("A", "D", "F", "M")}, met=bool(all(g(d, "P1fg") >= -0.02 for d in ("A", "D", "F", "M")))),
    H26c=dict(value=g("M", "Q1fg"), met=bool(g("M", "Q1fg") < -0.05)))
json.dump(out, open(f"{OUT}/summary.json", "w"), indent=1); print(json.dumps(out["rules"], indent=1))
