"""V3.2 (V3-H23): key-known detector K with three seeds against the expectations declared on 2026-11-14 (state/CLAIMS.md):
(1) K AUC exceeds the key-unknown detector M by at least 0.02 for RANDSEQ and ORIG; (2) |ORIG - RANDSEQ| <= 0.02 under K; (3) the cost-guided gain is not larger with the key known than with the pool known, i.e. |Q1 under K| <= |Q1 under M|.
Reads results/e41/k/e37_seed{0,1,2}.json (K), results/e37/e37_seed*.json and results/e41/e37_seed*.json (M). Writes results/e41/k/summary_3seeds.json."""
import json
out = {"expectations": {}, "per_seed": {}}
for s in (0, 1, 2):
    K = json.load(open(f"results/e41/k/e37_seed{s}.json"))["results"]; M = json.load(open(f"results/e37/e37_seed{s}.json"))["results"]; MX = json.load(open(f"results/e41/e37_seed{s}.json"))["results"]; row = {}
    for b in ("0.01", "0.02"):
        k = K[f"ixi|K|{b}"]["auc"]; m = dict(M[f"ixi|M|{b}"]["auc"]); m.update(MX[f"ixi|M|{b}"]["auc"])
        row[b] = dict(K=k, M={x: m[x] for x in k}, e1_rand=round(k["RANDSEQ"] - m["RANDSEQ"], 4), e1_orig=round(k["ORIG"] - m["ORIG"], 4), e2=round(k["ORIG"] - k["RANDSEQ"], 4), q1_K=round(k["COSTKEY"] - k["RANDSEQ"], 4), q1_M=round(m["COSTKEY"] - m["RANDSEQ"], 4))
        row[b]["e1_met"] = bool(row[b]["e1_rand"] >= 0.02 and row[b]["e1_orig"] >= 0.02); row[b]["e2_met"] = bool(abs(row[b]["e2"]) <= 0.02); row[b]["e3_met"] = bool(abs(row[b]["q1_K"]) <= abs(row[b]["q1_M"]))
    out["per_seed"][s] = row
for e in ("e1_met", "e2_met", "e3_met"): out["expectations"][e] = bool(all(out["per_seed"][s][b][e] for s in (0, 1, 2) for b in ("0.01", "0.02")))
for b in ("0.01", "0.02"):
    for key in ("q1_K", "q1_M", "e2", "e1_rand", "e1_orig"): v = [out["per_seed"][s][b][key] for s in (0, 1, 2)]; out.setdefault("summary", {}).setdefault(b, {})[key] = dict(mean=round(sum(v) / 3, 4), min=min(v), max=max(v))
json.dump(out, open("results/e41/k/summary_3seeds.json", "w"), indent=1); print(json.dumps(out["expectations"])); print(json.dumps(out["summary"], indent=0))
