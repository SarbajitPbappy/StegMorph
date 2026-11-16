"""Paper figures drawn only from stored JSON in results/. Run from the project root: python code/make_paper_figs.py"""
import json, glob, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "font.family": "serif"})
OUT = "Overleaf/article/figures/"
def load(folder):
    R = {}
    for f in sorted(glob.glob(f"results/{folder}/e14_seed*.json")):
        for k, v in json.load(open(f))["results"].items(): R.setdefault(k, []).append(v)
    return R
def con(R, key, c): return np.array([v["contrasts"][c]["diff"] for v in R[key]])
COL = {"IXI": "#1f4e79", "OASIS": "#c55a11", "texture": "#548235"}
# ---- Fig A: summary forest of GA-key (P1) and cost-guided (Q1) contrasts by detector, payload, collection
rows = []
def add(lab, folder, key, c, col): 
    R = load(folder)
    if key in R and c in R[key][0]["contrasts"]: rows.append((lab, con(R, key, c), col))
panels = {"P1_ORIG-RANDSEQ": "GA key minus random key", "Q1_COSTKEY-RANDSEQ": "Cost-guided key minus random key"}
names = {"A": "SRM-lite + LR", "B": "SPAM + trees", "C": "CNN", "D": "SRM-lite + trees"}
fig, axs = plt.subplots(1, 2, figsize=(7.2, 5.2), sharey=True)
OFF = {"IXI": 0.0, "OASIS": 0.28, "texture": 0.56}; groups = [(bpp, fam) for bpp in ("0.01", "0.02") for fam in "ABCD"]
def draw(ax, v, y, ds, mk="o"):
    ax.scatter(v, [y]*len(v), color=COL[ds], s=12, alpha=.8, zorder=3, marker=mk); ax.plot([v.mean()]*2, [y-.11, y+.11], color=COL[ds], lw=2)
for ax, (c, ttl) in zip(axs, panels.items()):
    for gi, (bpp, fam) in enumerate(groups):
        y0 = gi * 1.0 + (0.4 if bpp == "0.02" else 0)
        for ds, folders, tag in (("IXI", {"A": "e14", "B": "e14", "C": ("e16" if bpp == "0.01" else "e21"), "D": "e17"}, "IXI"), ("OASIS", {f: "e19_oasis_cost" for f in "ABCD"}, "OASIS")):
            key = f"{tag}|{fam}|{bpp}"; R = load(folders[fam])
            if key in R: draw(ax, con(R, key, c), y0 + OFF[ds], ds)
        if c.startswith("Q1") and fam in "AD":
            R = load("e20"); key = f"IXI|{fam}|{bpp}"
            if key in R: draw(ax, con(R, key, c), y0 + OFF["texture"], "texture", "s")
    ax.axvline(0, color="k", lw=.7); ax.axvspan(-.02, .02, color="0.9", zorder=0); ax.set_title(ttl); ax.set_xlabel("AUC difference (negative = harder to detect)")
axs[0].set_yticks([gi * 1.0 + (0.4 if bpp == "0.02" else 0) + 0.28 for gi, (bpp, fam) in enumerate(groups)]); axs[0].set_yticklabels([f"{names[fam]}, {bpp} bpp" for bpp, fam in groups]); axs[0].invert_yaxis()
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([], [], marker="o", ls="", color=COL["IXI"], label="IXI, HILL-cost key"), Line2D([], [], marker="o", ls="", color=COL["OASIS"], label="OASIS, HILL-cost key"), Line2D([], [], marker="s", ls="", color=COL["texture"], label="IXI, plain local-texture key (SRM-lite detectors)")], loc="lower center", ncol=3, frameon=False)
plt.tight_layout(rect=(0, 0.05, 1, 1)); plt.savefig(OUT + "fig8_forest_summary.png", dpi=300); plt.close()
# ---- Fig B: CNN learning curve
fig, ax = plt.subplots(figsize=(3.4, 2.6)); ax2 = ax.twinx(); sizes = [("1000", "e22_n1000"), ("2500", "e22_n2500"), ("5239", "e16")]
xs = [1000, 2500, 5239]; q = []; auc = []
for (lab, folder), x in zip(sizes, xs):
    R = load(folder)["IXI|C|0.01"]; v = np.array([r["contrasts"]["Q1_COSTKEY-RANDSEQ"]["diff"] for r in R]); a = np.mean([r["auc"]["RANDSEQ"] for r in R]); q.append(v.mean()); auc.append(a); ax.scatter([x]*len(v), v, color="#1f4e79", s=14, alpha=.7)
ax.plot(xs, q, color="#1f4e79", marker="o", label="cost-guided minus random (CNN)"); ax.axhline(0, color="k", lw=.7); ax.axhspan(-.02, .02, color="0.9", zorder=0)
ax2.plot(xs, auc, color="#c55a11", ls="--", marker="s", label="random-key AUC"); ax.set_xticks(xs); ax.set_xticklabels([str(x) for x in xs]); ax.set_xlim(500, 5800); ax.set_xlabel("training slices (30 epochs)"); ax.set_ylabel("AUC difference", color="#1f4e79"); ax2.set_ylabel("random-key AUC", color="#c55a11"); ax2.spines["right"].set_visible(True)
ax.set_ylim(-.25, .1); plt.tight_layout(); plt.savefig(OUT + "fig9_cnn_learning_curve.png", dpi=300); plt.close()
# ---- Fig C: refit-aware bootstrap intervals (E23)
E23 = json.load(open("results/e23/e23_seed0.json"))["results"]
fig, ax = plt.subplots(figsize=(3.4, 2.4)); y = 0; yl = []
for bpp in ("0.01", "0.02"):
    for c, lab in (("P1_ORIG-RANDSEQ", "GA key"), ("Q1_COSTKEY-RANDSEQ", "cost-guided"), ("Q3_COSTMIX-RANDSEQ", "matched control")):
        r = E23[f"IXI|A|{bpp}"]["contrasts"][c]; ax.errorbar(r["mean"], y, xerr=[[r["mean"]-r["ci95"][0]], [r["ci95"][1]-r["mean"]]], fmt="o", color="#1f4e79", capsize=2); yl.append((y, f"{lab}, {bpp} bpp")); y += 1
    y += .5
ax.axvline(0, color="k", lw=.7); ax.axvspan(-.02, .02, color="0.9", zorder=0); ax.set_yticks([p for p, _ in yl]); ax.set_yticklabels([l for _, l in yl]); ax.invert_yaxis(); ax.set_xlabel("AUC difference (95% interval)")
plt.tight_layout(); plt.savefig(OUT + "fig10_refit_bootstrap.png", dpi=300); plt.close()
print("figures written")
