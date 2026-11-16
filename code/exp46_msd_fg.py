"""V3.3 (V3-H24b): runs exp37_fullsrm.py (detectors F, M) on a collection whose foreground schemes need a modification map for M.
For RANDFG the map is 1 on the foreground (5x5 local mean > 10), for COSTFG 1 on the lowest-HILL-cost third of the foreground, for ANTIFG on the highest-cost third (the pools the keys draw from); all other schemes use the original code/lab24.beta_for.
Usage as exp37_fullsrm.py: python code/exp46_msd_fg.py SEED ; env DS, SCH, PAY, DETS, OUT, ..."""
import os, sys, runpy, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L
_orig = L.beta_for
def beta_for(scheme, img, nb):
    sc = L.ALIAS.get(scheme, scheme)
    if sc in ("RANDFG", "COSTFG", "ANTIFG"):
        fg = L.fg_pixels(img); b = np.zeros(img.size, np.float32)
        if sc == "RANDFG": b[fg] = 1.0
        else:
            o = np.argsort(L.hill_cost(img).ravel()[fg], kind="stable"); n = len(fg) // 3; b[fg[o[:n]] if sc == "COSTFG" else fg[o[-n:]]] = 1.0
        return b.reshape(img.shape)
    return _orig(scheme, img, nb)
L.beta_for = beta_for
if __name__ == "__main__":
    sys.argv = [os.path.join(HERE, "exp37_fullsrm.py")] + sys.argv[1:]; runpy.run_path(sys.argv[0], run_name="__main__")
