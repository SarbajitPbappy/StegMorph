"""V2.4 summary: OASIS and CT at 0.002 bpp, detectors A and D, seeds 0-2, from results/e40/{ds}/e24_seed{s}.json. Writes results/e40/e40_summary.json."""
import json, numpy as np
out = {}
for ds in ("oasis", "ct"):
    for det in ("A", "D"):
        R = [json.load(open(f"results/e40/{ds}/e24_seed{s}.json"))["results"][f"{ds}|{det}|0.002"] for s in (0, 1, 2)]
        row = {"mean_auc": {k: round(float(np.mean([r["auc"][k] for r in R])), 4) for k in R[0]["auc"]}, "contrasts": {}}
        for c in ("COSTKEY-RANDSEQ", "COSTMIX-RANDSEQ", "ANTIKEY-RANDSEQ", "COSTKEY-COSTMIX"):
            v = [r["contrasts"][c]["diff"] for r in R]; row["contrasts"][c] = dict(mean=round(float(np.mean(v)), 4), per_seed=v, worst_lower=min(r["contrasts"][c]["ci95_subject_bootstrap"][0] for r in R), worst_upper=max(r["contrasts"][c]["ci95_subject_bootstrap"][1] for r in R))
        out[f"{ds}|{det}"] = row; print(ds, det, "random AUC", row["mean_auc"]["RANDSEQ"], {c: (x["mean"], x["per_seed"]) for c, x in row["contrasts"].items()})
json.dump(out, open("results/e40/e40_summary.json", "w"), indent=1)
