"""V2.1 summary: seed means and ranges of the pre-registered contrasts for detectors F (full SRM + FLD ensemble) and M (maxSRM + FLD ensemble). Writes results/e37/e37_summary.json."""
import json, numpy as np
R = {}
for s in (0, 1, 2): R[s] = json.load(open(f"results/e37/e37_seed{s}.json"))["results"]
out = {}
for det in ("F", "M"):
    for bpp in (0.01, 0.02):
        row = {}
        for c in ("COSTKEY-RANDSEQ", "ORIG-RANDSEQ", "COSTMIX-RANDSEQ", "ANTIKEY-RANDSEQ", "HILLR-RANDSEQ", "COSTKEY-COSTMIX"):
            d = [R[s][f"ixi|{det}|{bpp}"]["contrasts"][c] for s in (0, 1, 2)]; v = [x["diff"] for x in d]
            row[c] = dict(mean=round(float(np.mean(v)), 4), per_seed=v, worst_lower=min(x["ci95_subject_bootstrap"][0] for x in d), worst_upper=max(x["ci95_subject_bootstrap"][1] for x in d))
        auc = {k: round(float(np.mean([R[s][f"ixi|{det}|{bpp}"]["auc"][k] for s in (0, 1, 2)])), 4) for k in R[0][f"ixi|{det}|{bpp}"]["auc"]}
        out[f"{det}|{bpp}"] = dict(contrasts=row, mean_auc=auc)
json.dump(out, open("results/e37/e37_summary.json", "w"), indent=1)
for k, v in out.items():
    print(k, "mean AUC", v["mean_auc"]); [print("   ", c, x["mean"], x["per_seed"], "worst CI", x["worst_lower"], x["worst_upper"]) for c, x in v["contrasts"].items() if c in ("COSTKEY-RANDSEQ", "ORIG-RANDSEQ", "HILLR-RANDSEQ")]
