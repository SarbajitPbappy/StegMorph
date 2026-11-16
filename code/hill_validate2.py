"""H24d: validation of the numpy HILL simulator against the reference HILL code on 200 IXI test slices (replaces the 12-slice check). Compares changed-pixel fraction, MSE (equal for +-1 changes) and per-slice correlation, and the spatial overlap of the change probability maps."""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, "code"); import lab24 as L
d = np.load("data/splits/ixi_test.npz"); ids = np.arange(0, len(d["images"]), len(d["images"]) // 200)[:200]; C = d["images"][ids]; sd = os.environ.get("TMPOCT", "/tmp/steg_oct"); os.makedirs(sd, exist_ok=True); C.tofile(sd + "/v_in.bin"); res = {}
for bpp in (0.01, 0.02):
    nb = L.payload_bits(bpp, 128 * 128); subprocess.run(["octave-cli", "--quiet", "--path", "code/octave", "--eval", f"batch_embed('hill','{sd}/v_in.bin','{sd}/v_out.bin','{sd}/v_rho.bin',{len(C)},128,128,{nb/16384:.8f},5)"], check=True)
    O = np.fromfile(sd + "/v_out.bin", np.uint8).reshape(-1, 128, 128); rho = np.fromfile(sd + "/v_rho.bin", np.float32).reshape(-1, 128, 128)
    N = np.array([L.hill_embed(c, L.hill_cost(c), float(nb), np.random.default_rng(i)) for i, c in enumerate(C)]); fo = (O != C).mean((1, 2)); fn = (N != C).mean((1, 2))
    # expected change-probability maps (numpy, from the numpy cost) versus Octave cost: same cost map -> same probabilities
    P = np.array([sum(L.change_probs(c, L.hill_cost(c), float(nb))) for c in C]); Po = np.array([sum(L.change_probs(c, r.astype(np.float64), float(nb))) for c, r in zip(C, rho)])
    res[str(bpp)] = dict(changed_octave=float(fo.mean()), changed_numpy=float(fn.mean()), ratio=float(fn.mean() / fo.mean()), per_slice_corr=float(np.corrcoef(fo, fn)[0, 1]), prob_map_max_abs_diff=float(np.abs(P - Po).max()), expected_changes_corr=float(np.corrcoef(P.sum((1, 2)), Po.sum((1, 2)))[0, 1]))
json.dump(res, open("results/hill_validation_200.json", "w"), indent=1); print(json.dumps(res, indent=1))
