"""Aggregates e24-style result JSONs over seeds. agg(folder) -> {(det, bpp): {'auc': {scheme: (mean, min, max)}, 'con': {contrast: dict(mean, lo, hi, ci_lo, ci_hi, n, ci_excl0)}, 'stats': {...}}}"""
import glob, json, numpy as np
def load(folder):
    R = {}
    for f in sorted(glob.glob(f"results/{folder}/e24_seed*.json")):
        for k, v in json.load(open(f))["results"].items(): R.setdefault(k, []).append(v)
    return R
def agg(folder):
    out = {}
    for k, rows in load(folder).items():
        ds, det, bpp = k.split("|"); o = {"auc": {}, "con": {}, "stats": {}, "n": len(rows)}
        for s in rows[0]["auc"]: a = [r["auc"][s] for r in rows if s in r["auc"]]; o["auc"][s] = (float(np.mean(a)), float(min(a)), float(max(a)))
        for c in rows[0]["contrasts"]:
            d = [r["contrasts"][c]["diff"] for r in rows if c in r["contrasts"]]; lo = [r["contrasts"][c]["ci95_subject_bootstrap"][0] for r in rows if c in r["contrasts"]]; hi = [r["contrasts"][c]["ci95_subject_bootstrap"][1] for r in rows if c in r["contrasts"]]
            o["con"][c] = dict(mean=float(np.mean(d)), lo=float(min(d)), hi=float(max(d)), ci_lo=float(np.mean(lo)), ci_hi=float(np.mean(hi)), n=len(d), all_ci_below0=all(h < 0 for h in hi), all_ci_above0=all(l > 0 for l in lo), all_ci_below_m02=all(h < -0.02 for h in hi), lower_ci_min=float(min(lo)))
        for s in rows[0]["stats_test"]: o["stats"][s] = {m: float(np.mean([r["stats_test"][s][m] for r in rows])) for m in rows[0]["stats_test"][s]}
        out[(ds, det, float(bpp))] = o
    return out
if __name__ == "__main__":
    import sys; A = agg(sys.argv[1])
    for (ds, det, bpp), o in sorted(A.items()):
        print(f"== {ds} det {det} bpp {bpp} seeds {o['n']}"); print("  AUC", {s: round(v[0], 3) for s, v in o["auc"].items()})
        for c, v in o["con"].items(): print(f"   {c:28s} mean {v['mean']:+.3f} [{v['lo']:+.3f},{v['hi']:+.3f}]  CI(mean) [{v['ci_lo']:+.3f},{v['ci_hi']:+.3f}]  allCI<0 {v['all_ci_below0']} allCI>0 {v['all_ci_above0']}")
