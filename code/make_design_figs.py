"""Redraws the embedder diagram and the control-design diagram (no embedded titles; same bit counts and contrast labels as the text). Run from the project root."""
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
OUT = "Overleaf/article/figures/"; C = {"b": "#e8eef8", "r": "#f6d7da", "g": "#d5ebdc", "y": "#fff0cc", "p": "#e6dcf0"}
def box(ax, x, y, w, h, t, c="b", fs=9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=C[c], ec="#2b3a55", lw=1.2)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
def arr(ax, a, b): ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, lw=1.2, color="#2b3a55"))
plt.rcParams["font.family"] = "DejaVu Sans"
# ---- embedder
fig, ax = plt.subplots(figsize=(10, 3.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 3.4); ax.axis("off")
box(ax, 0.1, 1.2, 1.5, 1.0, "Cover MR slice\n128 x 128, 8 bit"); box(ax, 2.0, 1.1, 2.2, 1.2, "GA key\nchain of N/3 random pixels\nfitness = sum of |differences|\nbetween consecutive pixels", fs=8.5)
box(ax, 4.6, 1.2, 1.6, 1.0, "Consecutive pairs\nmasked difference\n> 128 ?", "y", 8.5); box(ax, 6.7, 2.2, 1.7, 0.9, "PVD branch\n2 bits per pixel\n(4 bits per pair)", "r", 8.5); box(ax, 6.7, 0.3, 1.7, 0.9, "LSB branch\n1 bit per pixel\n(2 bits per pair)", "g", 8.5)
box(ax, 8.7, 1.1, 1.2, 1.2, "Message:\n16-bit length,\n8-bit characters,\ndelimiter; each\nbit repeated 3x", fs=7.5)
arr(ax, (1.6, 1.7), (2.0, 1.7)); arr(ax, (4.2, 1.7), (4.6, 1.7)); arr(ax, (6.2, 1.95), (6.7, 2.6)); arr(ax, (6.2, 1.45), (6.7, 0.8)); arr(ax, (8.4, 2.6), (8.7, 1.95)); arr(ax, (8.4, 0.8), (8.7, 1.45))
plt.savefig(OUT + "fig1_stegmorph_pipeline.png", dpi=250, bbox_inches="tight"); plt.close()
# ---- control design
fig, ax = plt.subplots(figsize=(10, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")
box(ax, 0.1, 1.9, 1.1, 0.8, "Cover x"); rows = [("RANDSEQ  random key (reference)", "g", 3.65), ("ORIG  GA contrast key", "r", 2.9), ("COSTKEY  lowest-cost third, random order", "y", 2.15), ("COSTMIX  random positions, COSTKEY's\nPVD/LSB pair counts", "y", 1.35), ("ANTIKEY  highest-cost (smooth) third", "p", 0.6)]
for t, c, y in rows: box(ax, 1.7, y - 0.3, 3.9, 0.6, t, c, 8.5); arr(ax, (1.2, 2.3), (1.7, y))
box(ax, 6.1, 1.8, 1.4, 1.0, "Same message,\nsame embedding\nfunction", fs=8.5); box(ax, 7.8, 1.8, 1.0, 1.0, "Detectors\nA, B, C, D, S", fs=8); box(ax, 9.05, 1.8, 0.9, 1.0, "Test AUC", fs=8.5)
for t, c, y in rows: arr(ax, (5.6, y), (6.1, 2.3))
arr(ax, (7.5, 2.3), (7.8, 2.3)); arr(ax, (8.8, 2.3), (9.05, 2.3))
ax.text(5.0, 0.05, "P1 = ORIG - RANDSEQ     Q1 = COSTKEY - RANDSEQ     Q2 = COSTKEY - COSTMIX     Q3 = COSTMIX - RANDSEQ     Q4 = ANTIKEY - RANDSEQ", ha="center", fontsize=8.5)
plt.savefig(OUT + "fig2_control_design.png", dpi=250, bbox_inches="tight"); plt.close(); print("ok")
