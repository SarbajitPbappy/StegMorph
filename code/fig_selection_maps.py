"""Figure: where the changes land. Top: one slice, positions changed by each key. Bottom: share of changed pixels in the most textured / middle / smoothest third of pixels (HILL cost ranking), 300 test slices, 0.02 bpp. Run from the project root."""
import sys, os, subprocess, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "code"); import lab24 as L
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"}); OUT = "Overleaf/article/figures/"
d = np.load("data/splits/ixi_test.npz"); imgs = d["images"]; bpp = 0.02; seed = 0; NS = 300; ids = np.arange(0, len(imgs), len(imgs) // NS)[:NS]; C = imgs[ids]
SCH = [("RANDSEQ", "Random key"), ("ORIG", "GA contrast key"), ("COSTKEY", "Cost-guided key"), ("ANTIKEY", "Smooth-pixel key"), ("HILLR", "HILL (reference code)")]
# real HILL via Octave
sd = "/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct"; os.makedirs(sd, exist_ok=True); C.tofile(sd + "/m_in.bin"); nb = L.payload_bits(bpp, 128 * 128)
subprocess.run(["octave-cli", "--quiet", "--path", "code/octave", "--eval", f"batch_embed('hill','{sd}/m_in.bin','{sd}/m_out.bin','none',{len(C)},128,128,{nb/16384:.8f},7)"], check=True); H = np.fromfile(sd + "/m_out.bin", np.uint8).reshape(-1, 128, 128)
ST = {k: [] for k, _ in SCH}
for j, (i, im) in enumerate(zip(ids, C)):
    msg = L.message(seed, bpp, 2, int(i), im.size)
    for k, _ in SCH:
        ST[k].append(H[j] if k == "HILLR" else L.make_stego(im, k, msg, seed, bpp, 2, int(i))[0])
ST = {k: np.array(v) for k, v in ST.items()}; ex = 40
fig = plt.figure(figsize=(7.2, 5.2)); gs = fig.add_gridspec(2, 5, height_ratios=[1, 0.9], hspace=0.08, wspace=0.08)
rk = L.hill_cost(C[ex]).ravel().argsort(); third = np.zeros(C[ex].size, int); third[rk[:C[ex].size // 3]] = 2; third[rk[-(C[ex].size // 3):]] = 0; third[(third == 0) & (np.arange(C[ex].size) != -1)] = third[(third == 0)]
for c, (k, name) in enumerate(SCH):
    ax = fig.add_subplot(gs[0, c]); ax.imshow(C[ex], cmap="gray", vmin=0, vmax=255); ch = ST[k][ex] != C[ex]; ys, xs = np.where(ch); ax.scatter(xs, ys, s=5, c="#e41a1c", marker="s", linewidths=0, alpha=.9); ax.set_title(f"{name}\n{ch.sum()} pixels changed", fontsize=7.5); ax.axis("off")
# bottom: share of changed pixels by texture third (rank within each image by HILL cost)
ax = fig.add_subplot(gs[1, :]); share = {k: np.zeros(3) for k, _ in SCH}
for j, im in enumerate(C):
    r = np.empty(im.size, int); r[L.hill_cost(im).ravel().argsort()] = np.arange(im.size); g = np.minimum(r * 3 // im.size, 2)  # 0 = most textured (lowest cost), 2 = smoothest
    for k, _ in SCH:
        m = (ST[k][j] != im).ravel(); share[k] += np.bincount(g[m], minlength=3) / max(m.sum(), 1)
w = 0.16; cols = ["#1b7837", "#999999", "#762a83"]
for c, (k, name) in enumerate(SCH):
    v = share[k] / len(C) * 100
    for t in range(3): ax.bar(c + (t - 1) * w * 1.15, v[t], w, color=cols[t], label=["most textured third", "middle third", "smoothest third"][t] if c == 0 else None)
ax.set_xticks(range(len(SCH))); ax.set_xticklabels([n.replace(" (reference code)", "\n(reference code)") for _, n in SCH]); ax.set_ylabel("changed pixels (%)"); ax.legend(frameon=False, ncol=3, loc="upper center"); ax.spines[["top", "right"]].set_visible(False); ax.set_ylim(0, 128)
plt.savefig(OUT + "fig_selection_maps.png", dpi=250, bbox_inches="tight"); print({k: np.round(v / len(C) * 100, 1).tolist() for k, v in share.items()})
