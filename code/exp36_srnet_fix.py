"""V2.2 (pre-registered V2-H4): ONE fixed attempt at training the SRNet-style network on the random-key set.
Changes against E26: He initialisation, AdamW lr 2e-4 with 3-epoch warm-up, gradient clipping 1.0, and a 0.05 bpp -> 0.01 bpp curriculum (8 epochs at 0.05 bpp, then up to 60 epochs at 0.01 bpp, cosine).
Valid run = best validation AUC (0.01 bpp) >= 0.55. If it stays at chance after this one attempt the network is dropped.
Usage: python code/exp36_srnet_fix.py SEED SCHEME ; env OUT (results/e36), NPROC"""
import os, sys, json, time, numpy as np, torch, torch.nn as nn, torch.nn.functional as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L, nets26 as N
from sklearn.metrics import roc_auc_score
dev = N.dev
def he_init(m):
    if isinstance(m, nn.Conv2d): nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
def run_phase(net, opt, tc, ts, vac, vas, epochs, lr, warm, bs, log, tag, patience=None, best=None):
    n = len(tc); spe = (n + bs - 1) // bs; step = 0; total = epochs * spe; best = best or (-1, None, -1)
    for ep in range(epochs):
        net.train(); perm = torch.randperm(n)
        for b in range(0, n, bs):
            f = min(1.0, (step + 1) / (warm * spe)) * 0.5 * (1 + np.cos(np.pi * min(step / total, 1.0)))
            for g in opt.param_groups: g["lr"] = lr * f
            ix = perm[b:b + bs]; x = torch.cat([tc[ix], ts[ix]]).to(dev); y = torch.cat([torch.zeros(len(ix)), torch.ones(len(ix))]).long().to(dev)
            if torch.rand(1) < .5: x = x.flip(3)
            if torch.rand(1) < .5: x = x.flip(2)
            k = int(torch.randint(0, 4, (1,))); x = torch.rot90(x, k, (2, 3)) if k else x
            loss = F.cross_entropy(net(x), y); opt.zero_grad(); loss.backward(); nn.utils.clip_grad_norm_(net.parameters(), 1.0); opt.step(); step += 1
        pc, ps = N.prob(net, vac), N.prob(net, vas); a = roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]); log(f"{tag} ep {ep} loss {loss.item():.3f} val_auc {a:.4f}")
        if a > best[0]: best = (a, {k_: v.clone() for k_, v in net.state_dict().items()}, ep)
        if patience and ep - best[2] >= patience: break
    return best, ep + 1
if __name__ == "__main__":
    seed = int(sys.argv[1]); sch = sys.argv[2]; OUT = os.environ.get("OUT", "results/e36"); ds = "ixi"; os.makedirs(OUT, exist_ok=True)
    dtr, dva, dte = L.load_split(ds, "train"), L.load_split(ds, "val"), L.load_split(ds, "test")
    tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8); va_ids = np.sort(np.random.default_rng(seed + 31).permutation(len(dva["images"]))[:400]); te_ids = np.arange(len(dte["images"]))
    Ctr, Cva, Cte = dtr["images"][tr_ids], dva["images"][va_ids], dte["images"][te_ids]
    def stego(imgs, ids, tag, split, bpp):
        parts = L.chunks(len(imgs), 24); res = L.par(L.task_stego, [(imgs[a:b], ids[a:b], sch, seed, bpp, tag, None, None) for a, b in parts]); return np.concatenate(res)
    INIT = int(os.environ.get("INIT", "0")); fn = f"{OUT}/srnetfix_{sch}_s{seed}" + (f"_i{INIT}" if INIT else ""); lf = open(fn + ".log", "w"); log = lambda m: (lf.write(m + "\n"), lf.flush(), print(m, flush=True)); t0 = time.time()
    S5tr, S5va = stego(Ctr, tr_ids, 0, "train", 0.05), stego(Cva, va_ids, 1, "val", 0.05)
    S1tr, S1va, S1te = stego(Ctr, tr_ids, 0, "train", 0.01), stego(Cva, va_ids, 1, "val", 0.01), stego(Cte, te_ids, 2, "test", 0.01); log(f"stego built {time.time()-t0:.0f}s")
    torch.manual_seed(seed * 100 + 7 + 13 * INIT); np.random.seed(seed); net = N.make("srnet").to(dev); net.apply(he_init); opt = torch.optim.AdamW(net.parameters(), 2e-4, weight_decay=1e-4)
    T = lambda a: torch.tensor(a, dtype=torch.float32)[:, None]
    _, e1 = run_phase(net, opt, T(Ctr), T(S5tr), Cva, S5va, 8, 2e-4, 3, 32, log, "phase1@0.05")
    best, e2 = run_phase(net, opt, T(Ctr), T(S1tr), Cva, S1va, 60, 2e-4, 2, 32, log, "phase2@0.01", patience=20)
    net.load_state_dict(best[1]); torch.save(best[1], fn + ".pt"); pc, ps = N.prob(net, Cte), N.prob(net, S1te)
    auc = float(roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]))
    info = dict(net="srnet_fixed", scheme=sch, seed=seed, bpp=0.01, best_val_auc=round(float(best[0]), 4), best_epoch=best[2], epochs_phase2=e2, minutes=round((time.time() - t0) / 60, 1), test_auc=round(auc, 4), valid_run=bool(best[0] >= 0.55), attempt="V2-H4 single fixed attempt" if sch == "RANDSEQ" else f"partner run, init {INIT}", init=INIT)
    np.savez_compressed(fn + "_scores.npz", pc=pc, ps=ps, subjects=dte["subject"][te_ids]); json.dump(info, open(fn + ".json", "w"), indent=1); log(json.dumps(info))
