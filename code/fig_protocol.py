"""Flowchart of the recommended minimum evaluation protocol for pixel-selection steganography."""
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
steps = [("1  Fix the operator", "Same embedding function, message and payload for every key; only the key changes."),
 ("2  Add operator-matched controls", "Random key, and random positions with the same PVD/LSB (or +1/-1) counts as the tested key; for covers with an empty background, a random key restricted to the foreground."),
 ("3  Split by subject first", "Train, validation and test subjects are disjoint; every detector component is fitted on training subjects only."),
 ("4  Report the amount of change", "Modified-pixel fraction, MSE and branch counts per scheme, so a position effect is not a change-count effect."),
 ("5  Use detectors of different kinds", "Hand-crafted features, maxSRM given the rule, a key-known check and two CNN types; a CNN counts only if competent (plateau, random-key validation AUC 0.85 or more)."),
 ("6  Add reference points", "A reference content-adaptive embedder at equal payload and at equal numbers of changed pixels, and a reversed (smooth-pixel) key to show the scale and the direction of any effect."),
 ("7  Quantify uncertainty", "Several seeds that also vary the training subjects, subject-cluster bootstrap intervals, refit-aware bootstrap, margin stated in advance."),
 ("8  Check the second collection", "Replicate on a non-saturated, non-JPEG collection; if detectors reach AUC near 1 the replication is uninformative."),
 ("9  Pre-register the rules", "Write each hypothesis and decision rule before the runs it covers, in an append-only log; report failed rules as failed.")]
fig, ax = plt.subplots(figsize=(7.2, 7.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 9.64); ax.axis("off")
for i, (t, d) in enumerate(steps):
    y = 9.64 - (i + 1) * 1.04 + 0.1
    ax.add_patch(FancyBboxPatch((0.2, y), 9.6, 0.86, boxstyle="round,pad=0.02,rounding_size=0.1", fc="#e8eef8" if i % 2 == 0 else "#d5ebdc", ec="#2b3a55", lw=1.1)); import textwrap; ax.text(0.45, y + 0.64, t, fontsize=9, fontweight="bold", va="center"); ax.text(0.45, y + 0.28, textwrap.fill(d, 92), fontsize=7.3, va="center", linespacing=1.15)
    if i < len(steps) - 1: ax.add_patch(FancyArrowPatch((5, y), (5, y - 0.16), arrowstyle="-|>", mutation_scale=10, lw=1, color="#2b3a55"))
plt.savefig("Overleaf/article/figures/fig_protocol.png", dpi=250, bbox_inches="tight")
