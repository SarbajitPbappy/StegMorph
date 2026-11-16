"""V3.4/V3.6: converged residual CNN (net) on a new collection with the foreground keys. Copy of exp39_budget.py with env DS (default msdt2), BPP (default 0.005), SCHEMES (default RANDFG,COSTFG), OUT (default results/e49_resnet_fg) and N = ALL training pairs. Fixed recipe of the budget sweep: 60 epochs, cosine schedule, 2 warm-up epochs, best-validation checkpoint; no early stopping.
Original docstring: V2.2 budget sweep (pre-registered V2-H3): residual CNN (net) or Yedroudj-Net-style network (yedroudj) on RANDSEQ and COSTKEY, IXI T2, 0.01 bpp.
Grid: epochs {4,10,30,60} x training pairs {600,1000,2500,4186}; cosine schedule over the stated number of epochs (2 warm-up epochs), no early stopping, best-validation checkpoint restored.
Usage: python code/exp39_budget.py SEED NET "EPOCHS:PAIRS,EPOCHS:PAIRS,..." ; env OUT (results/e39), NPROC"""
import os, sys, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L, nets26 as N, nets39
from sklearn.metrics import roc_auc_score
_orig = N.make; N.make = lambda name: nets39.Yedroudj() if name == "yedroudj" else _orig(name)
if __name__ == "__main__":
    seed = int(sys.argv[1]); net = sys.argv[2]; cfgs = [tuple(int(v) if v != "ALL" else 10 ** 9 for v in c.split(":")) for c in sys.argv[3].split(",")]; OUT = os.environ.get("OUT", "results/e49_resnet_fg"); ds = os.environ.get("DS", "msdt2"); bpp = float(os.environ.get("BPP", "0.005")); SCHS = os.environ.get("SCHEMES", "RANDFG,COSTFG").split(","); os.makedirs(OUT, exist_ok=True)
    dtr, dva, dte = L.load_split(ds, "train"), L.load_split(ds, "val"), L.load_split(ds, "test")
    tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8); va_ids = np.sort(np.random.default_rng(seed + 31).permutation(len(dva["images"]))[:400]); te_ids = np.arange(len(dte["images"]))
    Ctr, Cva, Cte = dtr["images"][tr_ids], dva["images"][va_ids], dte["images"][te_ids]; sub = dtr["subject"][tr_ids]
    order = np.random.default_rng(seed + 99).permutation(len(Ctr))  # fixed random order of training pairs; a smaller budget uses the first n
    def stego(imgs, ids, tag, sch):
        parts = L.chunks(len(imgs), 24); return np.concatenate(L.par(L.task_stego, [(imgs[a:b], ids[a:b], sch, seed, bpp, tag, None, None) for a, b in parts]))
    S = {}
    for sch in SCHS: S[sch] = (stego(Ctr, tr_ids, 0, sch), stego(Cva, va_ids, 1, sch), stego(Cte, te_ids, 2, sch))
    print("stego built", flush=True)
    for ep, n in cfgs:
        for sch in SCHS:
            fn = f"{OUT}/{net}_{sch}_s{seed}_e{ep}_n{n}"
            if os.path.exists(fn + ".json"): print("skip", fn); continue
            ix = order[:n]; lf = open(fn + ".log", "w"); log = lambda m: (lf.write(m + "\n"), lf.flush())
            pc, ps, info = N.train(net, Ctr[ix], S[sch][0][ix], Cva, S[sch][1], Cte, S[sch][2], seed=seed * 100, max_epochs=ep, patience=10 ** 6, log=log)
            np.savez_compressed(fn + "_scores.npz", pc=pc, ps=ps, subjects=dte["subject"][te_ids])
            info.update(net=net, scheme=sch, seed=seed, bpp=bpp, n_train_pairs=int(n), max_epochs=ep, test_auc=round(float(roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps])), 4), valid_run=bool(info["best_val_auc"] >= 0.55))
            json.dump(info, open(fn + ".json", "w"), indent=1); print(f"{net} {sch} s{seed} ep{ep} n{n}: val {info['best_val_auc']} test {info['test_auc']} ({info['minutes']} min)", flush=True)
