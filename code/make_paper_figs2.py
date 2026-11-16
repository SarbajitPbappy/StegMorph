"""New paper figures drawn only from stored result files. Run from the project root: python code/make_paper_figs2.py [which ...]"""
import sys, glob, json, os, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "code"); from summarize import agg, load
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "font.family": "DejaVu Sans"}); OUT = "Overleaf/article/figures/"
DN = {"A": "SRM-lite\n+ logistic", "D": "SRM-lite\n+ trees", "B": "SPAM\n+ trees", "S": "selection-\nchannel-aware", "C": "CNN"}
def old_cnn():
    """CNN results of the earlier design (fixed training slices, 30 epochs): e16 (0.01 bpp) and e21 (0.02 bpp), e14 json format."""
    out = {}
    for bpp, fo in ((0.01, "e16"), (0.02, "e21")):
        rows = [json.load(open(f))["results"][f"IXI|C|{bpp}"] for f in sorted(glob.glob(f"results/{fo}/e14_seed*.json"))]
        out[bpp] = {c: dict(mean=float(np.mean([r["contrasts"][c]["diff"] for r in rows])), all_ci_below0=all(r["contrasts"][c]["ci95_subject_bootstrap"][1] < 0 for r in rows), all_ci_above0=all(r["contrasts"][c]["ci95_subject_bootstrap"][0] > 0 for r in rows)) for c in rows[0]["contrasts"]}
    return out
ROWS = [("P1  GA - random", "ORIG-RANDSEQ", "P1_ORIG-RANDSEQ"), ("Q1  cost-guided - random", "COSTKEY-RANDSEQ", "Q1_COSTKEY-RANDSEQ"), ("Q2  cost-guided - matched", "COSTKEY-COSTMIX", "Q2_COSTKEY-COSTMIX"), ("Q3  matched - random", "COSTMIX-RANDSEQ", "Q3_COSTMIX-RANDSEQ"),
        ("Q4  smooth - random", "ANTIKEY-RANDSEQ", None), ("B1  HILL (reference) - random", "HILLR-RANDSEQ", "B1_HILL-RANDSEQ"), ("B2  S-UNIWARD (reference) - random", "SUNIR-RANDSEQ", None)]
def heatmap():
    A = agg("e24"); C = old_cnn(); cols = [(det, bpp) for bpp in (0.01, 0.02) for det in "ADBSC"]; M = np.full((len(ROWS), len(cols)), np.nan); mark = [[""] * len(cols) for _ in ROWS]
    for j, (det, bpp) in enumerate(cols):
        for i, (lab, k, kc) in enumerate(ROWS):
            v = None
            if det == "C" and kc and kc in C[bpp]: v = C[bpp][kc]
            elif det != "C" and ("ixi", det, bpp) in A and k in A[("ixi", det, bpp)]["con"]: v = A[("ixi", det, bpp)]["con"][k]
            if v is None: continue
            M[i, j] = v["mean"]; mark[i][j] = ("*" if (v["all_ci_below0"] or v["all_ci_above0"]) and abs(v["mean"]) > 0.02 else "")
    fig, ax = plt.subplots(figsize=(7.2, 3.3)); im = ax.imshow(M, cmap="RdBu_r", vmin=-0.3, vmax=0.3, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if not np.isnan(M[i, j]): ax.text(j, i, f"{M[i,j]:+.2f}{mark[i][j]}", ha="center", va="center", fontsize=7, color="white" if abs(M[i, j]) > 0.18 else "black")
    ax.set_xticks(range(len(cols))); ax.set_xticklabels([DN[d] for d, _ in cols], fontsize=6.5); ax.set_yticks(range(len(ROWS))); ax.set_yticklabels([r[0] for r in ROWS]); ax.xaxis.tick_top(); ax.axvline(4.5, color="k", lw=1)
    ax.text(2, len(ROWS) - 0.1, "0.01 bpp", ha="center", va="top", fontsize=8, fontweight="bold"); ax.text(7, len(ROWS) - 0.1, "0.02 bpp", ha="center", va="top", fontsize=8, fontweight="bold")
    cb = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.01); cb.set_label("AUC difference (negative = harder to detect)", fontsize=7); ax.spines[:].set_visible(False)
    plt.savefig(OUT + "fig_heatmap.png", dpi=250, bbox_inches="tight"); plt.close()
def roc():
    from sklearn.metrics import roc_curve
    fig, axs = plt.subplots(1, 4, figsize=(7.2, 2.0), sharey=True); sc = np.load("results/e24/scores_s0_b0.01.npz", allow_pickle=True)
    for ax, det in zip(axs, "ADBS"):
        for s, col, lab in (("RANDSEQ", "#444444", "random"), ("ORIG", "#d95f02", "GA"), ("COSTKEY", "#1b7837", "cost-guided"), ("ANTIKEY", "#762a83", "smooth"), ("HILLR", "#1f78b4", "HILL")):
            pc, ps = sc[f"{det}|{s}|pc"], sc[f"{det}|{s}|ps"]; f, t, _ = roc_curve(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]); ax.plot(f, t, color=col, lw=1.1, label=lab)
        ax.plot([0, 1], [0, 1], color="0.8", lw=.6); ax.set_title(DN[det].replace("\n", " "), fontsize=7.5); ax.set_xlabel("false positive rate")
    axs[0].set_ylabel("true positive rate"); axs[0].legend(frameon=False, fontsize=6, loc="lower right"); plt.tight_layout(); plt.savefig(OUT + "fig_roc.png", dpi=250); plt.close()
def change_bars():
    A = agg("e24"); st = A[("ixi", "A", 0.01)]["stats"]; names = [("RANDSEQ", "random"), ("ORIG", "GA"), ("COSTKEY", "cost-guided"), ("COSTMIX", "matched ctrl"), ("ANTIKEY", "smooth"), ("HILLR", "HILL"), ("SUNIR", "S-UNIWARD")]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.1))
    for ax, (m, t) in zip(axs, (("changed_frac", "modified pixels (fraction)"), ("mse", "MSE"), ("pvd_pairs", "PVD pairs used"))):
        v = [st[s][m] if st[s][m] >= 0 else 0 for s, _ in names]; ax.bar(range(len(names)), v, color=["#444", "#d95f02", "#1b7837", "#a6d96a", "#762a83", "#1f78b4", "#6baed6"]); ax.set_xticks(range(len(names))); ax.set_xticklabels([n for _, n in names], rotation=60, ha="right", fontsize=6.5); ax.set_title(t, fontsize=7.5)
    plt.tight_layout(); plt.savefig(OUT + "fig_change.png", dpi=250); plt.close()
def hill_bars():
    A = agg("e24"); names = [("RANDSEQ", "random"), ("ORIG", "GA"), ("COSTKEY", "cost-guided"), ("ANTIKEY", "smooth"), ("HILLSIM", "HILL (numpy)"), ("HILLR", "HILL (ref.)"), ("SUNIR", "S-UNIWARD (ref.)")]
    fig, axs = plt.subplots(1, 4, figsize=(7.2, 2.2), sharey=True)
    for ax, det in zip(axs, "ADBS"):
        for k, bpp, hatch in ((0, 0.01, ""), (1, 0.02, "//")):
            if ("ixi", det, bpp) not in A: continue
            v = [A[("ixi", det, bpp)]["auc"][s][0] for s, _ in names]; ax.bar(np.arange(len(names)) + (k - 0.5) * 0.4, v, 0.4, color=["#444", "#d95f02", "#1b7837", "#762a83", "#9ecae1", "#1f78b4", "#6baed6"], hatch=hatch, edgecolor="white", lw=0.3)
        ax.set_xticks(range(len(names))); ax.set_xticklabels([n for _, n in names], rotation=60, ha="right", fontsize=6); ax.set_title(DN[det].replace("\n", " "), fontsize=7.5); ax.set_ylim(0.45, 1.0); ax.axhline(0.5, color="0.7", lw=.6)
    axs[0].set_ylabel("test AUC"); plt.tight_layout(); plt.savefig(OUT + "fig_hill.png", dpi=250); plt.close()

def dose():
    A = agg("e28"); fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.5)); fs = [0.1, 0.2, 0.33, 0.5, 0.7]; nm = lambda d, f: ("COSTKEY" if (d == "t" and f == 0.33) else "ANTIKEY" if (d == "s" and f == 0.33) else f"K:hill:{d}:{f}")
    for ax, bpp in zip(axs[:2], (0.01, 0.02)):
        for det, ls in (("A", "-"), ("D", "--")):
            for d, col, lab in (("t", "#1b7837", "textured pool"), ("s", "#762a83", "smooth pool")):
                y = [A[("ixi", det, bpp)]["con"][nm(d, f) + "-RANDSEQ"]["mean"] for f in fs]; lo = [A[("ixi", det, bpp)]["con"][nm(d, f) + "-RANDSEQ"]["lo"] for f in fs]; hi = [A[("ixi", det, bpp)]["con"][nm(d, f) + "-RANDSEQ"]["hi"] for f in fs]
                ax.plot(fs + [1.0], y + [0], ls, color=col, marker="o", ms=3, label=f"{lab}, {det}"); ax.fill_between(fs, lo, hi, color=col, alpha=.12, lw=0)
        ax.axhline(0, color="k", lw=.6); ax.axhspan(-.02, .02, color="0.9", zorder=0); ax.set_xlabel("share of pixels offered to the key"); ax.set_title(f"{bpp} bpp", fontsize=8)
    axs[0].set_ylabel("AUC difference vs random key"); axs[0].legend(frameon=False, fontsize=5.5)
    maps = [("hill", "HILL"), ("std", "local std"), ("grad", "gradient"), ("ent", "entropy"), ("suni", "S-UNIWARD")]; ax = axs[2]
    for k, (det, ofs) in enumerate((("A", -0.2), ("D", 0.2))):
        for m, (mp, ml) in enumerate(maps):
            for d, col in (("t", "#1b7837"), ("s", "#762a83")):
                key = nm(d, 0.33) if mp == "hill" else f"K:{mp}:{d}:0.33"; v = A[("ixi", det, 0.01)]["con"][key + "-RANDSEQ"]["mean"]; ax.bar(m * 1.0 + ofs + (0.0 if d == "t" else 0.0), v, 0.18, color=col, alpha=0.9 if det == "A" else 0.5, hatch="" if det == "A" else "//", edgecolor="white", lw=.3)
    ax.axhline(0, color="k", lw=.6); ax.set_xticks(range(len(maps))); ax.set_xticklabels([m[1] for m in maps], rotation=45, ha="right", fontsize=6); ax.set_title("five cost maps, 33% pool, 0.01 bpp\n(solid A, hatched D)", fontsize=7)
    plt.tight_layout(); plt.savefig(OUT + "fig_dose.png", dpi=250); plt.close()
def payload():
    A = agg("e29"); pays = sorted({b for (_, _, b) in A}); fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.5), sharey=True); names = [("RANDSEQ", "random", "#444444"), ("ORIG", "GA", "#d95f02"), ("COSTKEY", "cost-guided", "#1b7837"), ("ANTIKEY", "smooth", "#762a83"), ("HILLR", "HILL", "#1f78b4"), ("SUNIR", "S-UNIWARD", "#6baed6")]
    for ax, det in zip(axs, "AD"):
        for s, lab, col in names: ax.plot(pays, [A[("ixi", det, b)]["auc"][s][0] for b in pays], marker="o", ms=3, color=col, label=lab)
        ax.set_xscale("log"); ax.set_xticks(pays); ax.set_xticklabels([str(p) for p in pays], fontsize=6.5); ax.set_xlabel("payload (bpp)"); ax.set_title(DN[det].replace("\n", " "), fontsize=7.5); ax.axhline(0.5, color="0.8", lw=.6)
    axs[0].set_ylabel("test AUC"); axs[1].legend(frameon=False, fontsize=6, loc="center left", bbox_to_anchor=(1.0, 0.5)); plt.tight_layout(); plt.savefig(OUT + "fig_payload.png", dpi=250); plt.close()
def saturation():
    sets = []
    for lab, fo, ds in (("IXI T2", "e24", "ixi"), ("IXI T1", "e27", "ixit1"), ("CT", "e32", "ct")):
        if os.path.isdir(f"results/{fo}") and glob.glob(f"results/{fo}/e24_seed*.json"): sets.append((lab, agg(fo), ds))
    oas = {}
    for f in sorted(glob.glob("results/e19_oasis_cost/e14_seed*.json")):
        for k, v in json.load(open(f))["results"].items(): oas.setdefault(k, []).append(v["auc"]["RANDSEQ"])
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.2), sharey=True)
    for ax, bpp in zip(axs, (0.01, 0.02)):
        dets = "ADB"; cols = ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00"]; allsets = sets + [("OASIS (JPEG-derived)", None, None)]
        for j, (lab, A, ds) in enumerate(allsets):
            for i, det in enumerate(dets):
                v = (np.mean(oas[f"OASIS|{det}|{bpp}"]) if A is None and f"OASIS|{det}|{bpp}" in oas else (A[(ds, det, bpp)]["auc"]["RANDSEQ"][0] if A is not None and (ds, det, bpp) in A else np.nan)); ax.bar(i + (j - len(allsets) / 2 + .5) * .2, v, .18, color=cols[j], label=lab if i == 0 else None)
        ax.set_xticks(range(len(dets))); ax.set_xticklabels([DN[d].replace("\n", " ") for d in dets], fontsize=6.5); ax.set_title(f"random-key AUC, {bpp} bpp", fontsize=7.5); ax.axhline(1.0, color="0.7", lw=.6); ax.set_ylim(0.5, 1.02)
    axs[1].legend(frameon=False, fontsize=6, loc="center left", bbox_to_anchor=(1.0, 0.5)); plt.tight_layout(); plt.savefig(OUT + "fig_saturation.png", dpi=250, bbox_inches="tight"); plt.close()

if __name__ == "__main__":
    for w in (sys.argv[1:] or ["heatmap", "roc", "change_bars", "hill_bars"]): globals()[w](); print("made", w)
