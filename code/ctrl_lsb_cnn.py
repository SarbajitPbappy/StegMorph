"""Ceiling control for the MPS CNN: plain random-position LSB replacement at BPP (default 0.4) on IXI subject-disjoint splits; cover-vs-cover chance control."""
import sys, os, time, numpy as np
from sklearn.metrics import roc_auc_score
import cnn_mps as C
bpp = float(sys.argv[1]) if len(sys.argv) > 1 else 0.4; N = int(sys.argv[2]) if len(sys.argv) > 2 else 1500; EP = int(sys.argv[3]) if len(sys.argv) > 3 else 15
L = lambda k, n: np.load(f"data/splits/ixi_{k}.npz")["images"][:n]
tr, va, te = L("train", N), L("val", 400), L("test", 600)
def lsb(imgs, seed):
    r = np.random.default_rng(seed); out = imgs.copy(); k = int(bpp * 128 * 128)
    for im in out:
        idx = r.permutation(im.size)[:k]; f = im.reshape(-1); f[idx] = (f[idx] & 0xFE) | r.integers(0, 2, k).astype(np.uint8)
    return out
t0 = time.time(); log = lambda s: print(s, flush=True)
pc, ps, v = C.fit_predict(tr, lsb(tr, 1), va, lsb(va, 2), te, lsb(te, 3), epochs=EP, log=log)
a = roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]); print(f"LSB bpp {bpp}: test AUC {a:.4f} (best val {v:.4f}) device {C.dev} {time.time()-t0:.0f}s")
pc, ps, v = C.fit_predict(tr, tr.copy(), va, va.copy(), te, te.copy(), epochs=max(3, EP // 3), log=None)
print("cover-vs-identical-cover (chance) test AUC", round(roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]), 4))
