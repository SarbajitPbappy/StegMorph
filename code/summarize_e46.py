"""V3.3 (V3-H24b): three-seed summary on the MSD brain-tumour collection (results/e46_msd; payload 0.005 bpp chosen on validation).
Per detector (A, D from e24_seed*.json; F, M from e37_seed*.json): AUC per scheme and seed, seed mean and range, contrasts P1fg = ORIG - RANDFG, Q1fg = COSTFG - RANDFG, Q4fg = ANTIFG - RANDFG, ORIG - RANDSEQ and RANDFG - RANDSEQ with the per-seed subject-bootstrap interval.
Decision rule of V3-H24b: |P1fg| <= 0.02 (seed mean) and full-SRM Q1fg < -0.05 (seed mean). Writes results/e46_msd/summary.json."""
import json, numpy as np
SCH = ["RANDFG", "ORIG", "RANDSEQ", "COSTFG", "ANTIFG"]; out = {"payload_bpp": 0.005, "detectors": {}}
def rows(det):
    f = "e24" if det in ("A", "D") else "e37"; r = []
    for s in (0, 1, 2):
        d = json.load(open(f"results/e46_msd/{f}_seed{s}.json")); r.append((d.get("n_train_subjects"), d.get("n_test_subjects"), d["results"][f"msdt2|{det}|0.005"]))
    return r
for det in ("A", "D", "F", "M"):
    R = rows(det); auc = {s: [r[2]["auc"][s] for r in R] for s in SCH}; con = {}
    for name, a, b in (("P1fg", "ORIG", "RANDFG"), ("Q1fg", "COSTFG", "RANDFG"), ("Q4fg", "ANTIFG", "RANDFG"), ("ORIG-RANDSEQ", "ORIG", "RANDSEQ"), ("RANDFG-RANDSEQ", "RANDFG", "RANDSEQ")):
        d = [round(auc[a][i] - auc[b][i], 4) for i in range(3)]; ci = [R[i][2]["contrasts"].get(f"{a}-{b}", {}).get("ci95_subject_bootstrap") for i in range(3)]
        con[name] = dict(per_seed=d, mean=round(float(np.mean(d)), 4), range=[min(d), max(d)], ci95_per_seed=ci)
    out["detectors"][det] = dict(auc_mean={s: round(float(np.mean(v)), 4) for s, v in auc.items()}, auc_per_seed=auc, contrasts=con)
out["n_train_subjects_seed"] = [r[0] for r in rows("A")]; out["n_test_subjects"] = rows("A")[0][1]
p1 = np.mean([out["detectors"][d]["contrasts"]["P1fg"]["mean"] for d in ("A", "D", "F", "M")]); out["H24b"] = dict(P1fg_mean_by_detector={d: out["detectors"][d]["contrasts"]["P1fg"]["mean"] for d in ("A", "D", "F", "M")},
    P1fg_met={d: bool(abs(out["detectors"][d]["contrasts"]["P1fg"]["mean"]) <= 0.02) for d in ("A", "D", "F", "M")}, Q1fg_F_mean=out["detectors"]["F"]["contrasts"]["Q1fg"]["mean"], Q1fg_F_met=bool(out["detectors"]["F"]["contrasts"]["Q1fg"]["mean"] < -0.05))
out["H24b"]["met"] = bool(out["H24b"]["Q1fg_F_met"] and out["H24b"]["P1fg_met"]["F"])  # the pre-registered rule names full SRM for Q1fg; P1fg is judged for every detector and all must be met for 'Met'
out["H24b"]["met_all_detectors"] = bool(out["H24b"]["Q1fg_F_met"] and all(out["H24b"]["P1fg_met"].values()))
json.dump(out, open("results/e46_msd/summary.json", "w"), indent=1); print(json.dumps({d: {c: (v["mean"], v["range"]) for c, v in out["detectors"][d]["contrasts"].items()} for d in out["detectors"]}, indent=0)); print(out["H24b"])
