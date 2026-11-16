"""Version 3 summary figure: (a) Q1 on the foreground-baseline collections (MSD, BraTS) by detector, seed mean and range; (b) SRNet-style network, Q1 per seed with 95% CI, attempt 2. Reads stored summaries only."""
import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
msd = json.load(open("results/e46_msd/summary.json"))["detectors"]; br = json.load(open("results/e48_brats/summary.json"))["detectors"]; sr = json.load(open("results/e42/summary_srnet_a2.json"))
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1.5, 1]))
dets = ["A", "D", "F", "M"]; x = np.arange(len(dets)); w = 0.36
for off, name, d, c in ((-w / 2, "MSD", msd, "#3b6ea8"), (w / 2, "BraTS", br, "#d98f2b")):
    m = [d[k]["contrasts"]["Q1fg"]["mean"] for k in dets]; lo = [m[i] - d[k]["contrasts"]["Q1fg"]["range"][0] for i, k in enumerate(dets)]; hi = [d[k]["contrasts"]["Q1fg"]["range"][1] - m[i] for i, k in enumerate(dets)]
    a.bar(x + off, m, w, yerr=[np.abs(lo), np.abs(hi)], color=c, label=name, capsize=2, lw=0.6)
a.axhline(-0.05, color="k", ls=":", lw=0.8); a.axhline(0, color="k", lw=0.6); a.set_xticks(x); a.set_xticklabels(["A", "D", "F", "M\n(maxSRM)"]); a.set_ylabel("$Q_1$ (cost-guided minus foreground random key, AUC)"); a.set_title("(a) Feature detectors, foreground baseline", fontsize=8.5); a.legend(fontsize=7, frameon=False); a.tick_params(labelsize=7.5); a.yaxis.label.set_size(7)
s = sr["seeds"]; q = [t["q1"] for t in s]; ci = np.array([t["ci"] for t in s]); xs = np.arange(len(s))
b.errorbar(xs, q, yerr=[np.array(q) - ci[:, 0], ci[:, 1] - np.array(q)], fmt="o", color="#2e7d4f", capsize=3, ms=5); b.axhline(0, color="k", lw=0.6); b.axhline(sr["mean_q1"], color="#2e7d4f", ls="--", lw=0.8)
b.set_xticks(xs); b.set_xticklabels([f"seed {t['seed']}" for t in s]); b.set_xlim(-0.6, len(s) - 0.4); b.set_ylim(-0.005, 0.06); b.set_ylabel("$Q_1$ (AUC)", fontsize=7); b.set_title("(b) SRNet-style network, IXI T2", fontsize=8.5); b.tick_params(labelsize=7.5)
b.text(0.97, 0.05, f"mean {sr['mean_q1']:+.3f}", transform=b.transAxes, ha="right", fontsize=7.5, color="#2e7d4f")
plt.tight_layout(); plt.savefig("Overleaf/article/figures/fig_v3_summary.png", dpi=250, bbox_inches="tight")
