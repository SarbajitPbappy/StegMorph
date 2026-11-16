import sys, glob, time, numpy as np; sys.path.insert(0, "..")
from PIL import Image
import stegmorph_recon as R
files = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/**/*.jpg", recursive=True))
rng = np.random.default_rng(0)
for k in range(6):
    im = np.array(Image.open(files[k*900]).convert("L"), np.uint8); cap, low, pvd = R.capacity_and_branch(im)
    cost = R.expected_cost(im, rng)
    for bpp in (0.02, 0.1, 0.2):
        n = int(bpp*im.size); pay = rng.integers(0, 2, n).astype(np.uint8); need = R.total_bits(n)
        if cap.sum() < need: print("img", k, "bpp", bpp, "capacity short", cap.sum(), need); continue
        for name, m in [("rand", R.select_random(cap, need, rng)), ("greedy", R.select_greedy(cap, cost, need)), ("ga", None)]:
            t = time.time()
            if m is None: m = R.select_ga(cap, cost, need, rng)
            st = R.embed(im, pay, m); ok = (R.extract(st, m) == pay).all(); dt = time.time()-t
            print(f"img{k} bpp{bpp} {name:6s} roundtrip={ok} cost={cost[m].sum():9.0f} sel={m.sum()} secs={dt:.2f}")
            assert ok
