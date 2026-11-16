"""V3.2 (V3-H23): refit-aware bootstrap for detector D, seeds 0 to 2, 100 replicates each, IXI T2 (results/e43). Rules as E23/E31: (a) Q1 interval entirely below -0.02; (b) P1 interval lower bound >= -0.02; (c) Q3 interval within [-0.02, +0.02]; at both payloads, in each seed. Writes results/e43/summary.json."""
import json
out = {}; allmet = {"a": True, "b": True, "c": True}
for b in ("0.01", "0.02"):
    for s in (0, 1, 2):
        c = json.load(open(f"results/e43/e31_D_seed{s}.json"))["results"][f"IXI|D|{b}"]["contrasts"]; q1, p1, q3 = c["Q1_COSTKEY-RANDSEQ"], c["P1_ORIG-RANDSEQ"], c["Q3_COSTMIX-RANDSEQ"]
        row = dict(P1=[round(p1["mean"], 4), [round(x, 4) for x in p1["ci95"]]], Q1=[round(q1["mean"], 4), [round(x, 4) for x in q1["ci95"]]], Q3=[round(q3["mean"], 4), [round(x, 4) for x in q3["ci95"]]],
                   a=bool(q1["ci95"][1] < -0.02), b=bool(p1["ci95"][0] >= -0.02), c=bool(q3["ci95"][0] >= -0.02 and q3["ci95"][1] <= 0.02))
        for k in "abc": allmet[k] = allmet[k] and row[k]
        out[f"{b}|seed{s}"] = row
out["rule_met"] = allmet; json.dump(out, open("results/e43/summary.json", "w"), indent=1)
for k, v in out.items():
    if k != "rule_met": print(k, "P1", v["P1"], "Q1", v["Q1"], "Q3", v["Q3"], "a,b,c =", v["a"], v["b"], v["c"])
print(out["rule_met"])
