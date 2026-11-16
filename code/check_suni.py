"""Checks the numpy S-UNIWARD cost (lab24.suni_cost) against the Octave reference output (rho returned by SUNI_mat) and the numpy HILL cost against HILL_mat; prints max relative differences."""
import sys, subprocess, numpy as np
sys.path.insert(0, "code"); import lab24 as L
d = np.load("data/splits/ixi_test.npz"); im = d["images"][::113][:10]; im.tofile("/tmp/c_in.bin"); N = len(im)
for m in ("hill", "suni"):
    subprocess.run(["octave-cli", "--quiet", "--path", "code/octave", "--eval", f"batch_embed('{m}','/tmp/c_in.bin','/tmp/c_out.bin','/tmp/c_rho_{m}.bin',{N},128,128,0.0125,1)"], check=True)
    rho = np.fromfile(f"/tmp/c_rho_{m}.bin", np.float32).reshape(N, 128, 128).astype(np.float64)
    mine = np.array([L.suni_cost(x) if m == "suni" else L.hill_cost(x) for x in im])
    print(m, "max relative difference", float((np.abs(mine - rho) / np.maximum(np.abs(rho), 1e-9)).max()))
