"""E5 side measurement: PSNR of GA vs RAND on tumor-set raw crops (same crop procedure as exp5.py seed 0, first 150 crops). No detector."""
import glob, json, numpy as np
from PIL import Image
import stegmorph_recon as R
from skimage.metrics import peak_signal_noise_ratio as psnr
seed = 0; PAY = [0.005, 0.01, 0.02]; rng = np.random.default_rng(seed); need_max = R.total_bits(int(max(PAY)*128*128))
tf = sorted(glob.glob("/home/claude/data/MRI_data/**/*.png", recursive=True)); Tc = []
for gi, f in enumerate(tf):
    im = np.array(Image.open(f).convert("L"), np.uint8); H, W = im.shape
    if H < 128 or W < 128: continue
    k = 2 if (H >= 256 or W >= 256) else 1
    for j in range(k):
        for _ in range(20):
            y = int(rng.integers(0, H-127)); x = int(rng.integers(0, W-127)); c = im[y:y+128, x:x+128]
            if R.capacity_and_branch(c)[0].sum() >= need_max: Tc.append(c.copy()); break
Tc = Tc[:150]; out = {}
for bpp in PAY:
    n = int(bpp*128*128); need = R.total_bits(n); ps = {"GA": [], "RAND": []}; low = {"GA": [], "RAND": []}
    for i, im in enumerate(Tc):
        r = np.random.default_rng(i); pay = r.integers(0, 2, n).astype(np.uint8); cap, lw, pvd = R.capacity_and_branch(im)
        cost = R.expected_cost(im, np.random.default_rng(i))
        for sch in ps:
            m = R.select_ga(cap, cost, need, np.random.default_rng(i)) if sch == "GA" else R.select_random(cap, need, np.random.default_rng(i))
            st = R.embed(im, pay, m); ps[sch].append(psnr(im, st, data_range=255)); low[sch].append(float(lw[m].mean()))
    out[str(bpp)] = {s: dict(psnr=round(float(np.mean(ps[s])), 2), low_branch_frac=round(float(np.mean(low[s])), 3)) for s in ps}
    print(bpp, out[str(bpp)], flush=True)
json.dump(dict(n_crops=len(Tc), res=out), open("e5_psnr.json", "w"), indent=1)
