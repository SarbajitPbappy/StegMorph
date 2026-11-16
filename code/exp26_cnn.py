"""E26: stronger CNN training (pre-registered). Usage: python code/exp26_cnn.py SEED NET SCHEMES(comma) [BPP] ; env MAXEP (100), PATIENCE (10), OUT (results/e26), NPROC (3)"""
import os, sys, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L, nets26 as N
from exp24 import octave_stego
if __name__ == "__main__":
    seed = int(sys.argv[1]); net = sys.argv[2]; SCH = sys.argv[3].split(","); bpp = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01; MAXEP = int(os.environ.get("MAXEP", "100")); PAT = int(os.environ.get("PATIENCE", "10")); OUT = os.environ.get("OUT", "results/e26"); ds = "ixi"
    os.makedirs(OUT, exist_ok=True); dtr, dva, dte = L.load_split(ds, "train"), L.load_split(ds, "val"), L.load_split(ds, "test")
    tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8); va_ids = np.sort(np.random.default_rng(seed + 31).permutation(len(dva["images"]))[:400]); te_ids = np.arange(len(dte["images"]))
    Ctr, Cva, Cte = dtr["images"][tr_ids], dva["images"][va_ids], dte["images"][te_ids]
    def stego(imgs, ids, tag, split, sch):
        base = L.ALIAS.get(sch, sch); pre = octave_stego(ds, split, ids, imgs, "hill" if base == "HILLR" else "suni", bpp, seed, tag) if base in ("HILLR", "SUNIR") else None
        rows = None
        if base in L.KEYED_CACHE:
            from exp24 import key_rows, trim_rows; rows = trim_rows(key_rows(imgs, ids, base, seed, tag, ds, split))
        parts = L.chunks(len(imgs), 24); res = L.par(L.task_stego, [(imgs[a:b], ids[a:b], sch, seed, bpp, tag, None if rows is None else rows[a:b], None if pre is None else pre[a:b]) for a, b in parts]); return np.concatenate(res)
    for sch in SCH:
        INIT = int(os.environ.get("INIT", "0")); fn = f"{OUT}/{net}_{sch.replace(':', '_')}_b{bpp}_s{seed}" + (f"_i{INIT}" if INIT else "")
        if os.path.exists(fn + ".json"): print("skip", fn); continue
        t0 = time.time(); Str, Sva, Ste = stego(Ctr, tr_ids, 0, "train", sch), stego(Cva, va_ids, 1, "val", sch), stego(Cte, te_ids, 2, "test", sch); print(f"{sch}: stego built {time.time()-t0:.0f}s", flush=True)
        lf = open(fn + ".log", "w"); log = lambda m: (lf.write(m + "\n"), lf.flush(), print(m, flush=True))
        pc, ps, info = N.train(net, Ctr, Str, Cva, Sva, Cte, Ste, seed=seed * 100 + INIT, max_epochs=MAXEP, patience=PAT, log=log, ckpt=fn + ".pt")
        np.savez_compressed(fn + "_scores.npz", pc=pc, ps=ps, subjects=dte["subject"][te_ids]); info.update(init=INIT, net=net, scheme=sch, seed=seed, bpp=bpp, n_train_pairs=len(Ctr), max_epochs=MAXEP, patience=PAT)
        from sklearn.metrics import roc_auc_score; info["test_auc"] = round(float(roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps])), 4); json.dump(info, open(fn + ".json", "w"), indent=1); print(sch, info, flush=True)
