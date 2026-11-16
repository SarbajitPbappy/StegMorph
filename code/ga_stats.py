"""How much does the StegMorph GA improve its own objective, and do its keys lean toward textured pixels? 300 test slices. Writes results/ga_stats.json"""
import sys, json, numpy as np
sys.path.insert(0, "code"); import lab24 as L
d = np.load("data/splits/ixi_test.npz"); imgs = d["images"]; ids = np.arange(0, len(imgs), len(imgs) // 300)[:300]; r = {"contrast_gain": [], "len_ratio": [], "tex_share": [], "cost_ratio": []}
for i in ids:
    im = imgs[i]; f = im.ravel().astype(int); kG = L.compute_cached_key(im, "ORIG", 0, 2, int(i)); kR = L.random_key(im, np.random.default_rng(int(i)))
    cg = np.abs(np.diff(f[kG])).mean() / np.abs(np.diff(f[kR])).mean(); c = L.hill_cost(im).ravel(); rank = np.empty(im.size, int); rank[c.argsort()] = np.arange(im.size)
    r["contrast_gain"].append(cg); r["len_ratio"].append(len(kG) / len(kR)); r["tex_share"].append(float((rank[kG] < im.size // 3).mean())); r["cost_ratio"].append(float(c[kG].mean() / c[kR].mean()))
out = {k: dict(mean=float(np.mean(v)), sd=float(np.std(v))) for k, v in r.items()}; json.dump(out, open("results/ga_stats.json", "w"), indent=1); print(json.dumps(out, indent=1))
