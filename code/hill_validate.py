"""Validate the numpy HILL simulator against Aletheia's HILL.m (Octave) on N test slices: same cost map is already checked in hill_cost.py;
here compare the EMBEDDING STATISTICS (fraction of changed pixels, MSE) at the same payload. Both samplers are random, so compare means over slices."""
import os, sys, ast, subprocess, types, numpy as np
sys.modules.setdefault("cv2", types.ModuleType("cv2")); sys.path.insert(0, "code"); sys.path.insert(0, ".")
from hill_cost import hill_cost
import stegmorph as SM
from PIL import Image
src = open("code/exp14_costkey.py").read(); tree = ast.parse(src); ns = {"np": np}
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name in ("_H3", "hill_embed"): exec(compile(ast.Module([n], []), "x", "exec"), ns)
d = np.load("data/splits/ixi_test.npz"); imgs = d["images"][::97][:12]; SD = sys.argv[1]; rows = []
for bpp in (0.01, 0.02):
    L = max(1, (int(bpp*128*128)-32)//8); rng = np.random.default_rng(1)
    for i, im in enumerate(imgs):
        msg = "".join(chr(int(c)) for c in rng.integers(0, 256, L)); nbits = len(SM._text_to_bits(msg)); pay = nbits / im.size
        p = f"{SD}/s{i}.png"; Image.fromarray(im).save(p)
        r = subprocess.run(["octave-cli", "--quiet", "--eval", f"pkg load image; HILL('{p}', {pay}); disp('x')"], cwd=SD, capture_output=True, text=True)
        # HILL.m returns stego; wrap to save
        r = subprocess.run(["octave-cli", "--quiet", "--eval", f"pkg load image; s=HILL('{p}', {pay}); imwrite(uint8(s), '{SD}/o{i}.png');"], cwd=SD, capture_output=True, text=True)
        if r.returncode: print("octave err", r.stderr[:300]); sys.exit(1)
        so = np.array(Image.open(f"{SD}/o{i}.png")).astype(float); sn = ns["hill_embed"](im, hill_cost(im), nbits, rng).astype(float)
        rows.append((bpp, (so != im).mean(), (sn != im).mean(), ((so-im)**2).mean(), ((sn-im)**2).mean()))
rows = np.array(rows)
for bpp in (0.01, 0.02):
    r = rows[rows[:, 0] == bpp]; print(f"bpp {bpp}: changed-pixel fraction Octave {r[:,1].mean():.5f} vs numpy {r[:,2].mean():.5f} (ratio {r[:,2].mean()/r[:,1].mean():.3f}); MSE Octave {r[:,3].mean():.5f} vs numpy {r[:,4].mean():.5f}; per-slice change-fraction correlation {np.corrcoef(r[:,1], r[:,2])[0,1]:.3f}")
