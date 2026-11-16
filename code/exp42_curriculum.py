"""V3.1 (pre-registered V3-H21, V3-H22): CNN trained with on-the-fly re-embedding, pair-constrained batches and a payload curriculum.
Usage: python code/exp42_curriculum.py SEED NET SCHEME   (NET = yedroudj | srnet; SCHEME = RANDSEQ | COSTKEY)
Env: OUT (default results/e42), TAG (suffix of the run name, e.g. a1 for attempt 1), WARMSTART (path of a checkpoint pattern for the cost-guided SRNet-style run, '{stage}' is replaced by the stage index).
Recipe is fixed in state/CLAIMS.md (V3 pre-registration and V3.1 recipe details); only max epochs, payloads and learning rates below come from there."""
import os, sys, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L, nets26 as N, nets39
import torch, torch.nn.functional as F
from sklearn.metrics import roc_auc_score
dev = N.dev
CFG = {  # bpp, max epochs, learning rate, warm-up epochs per stage
    "yedroudj": dict(stages=[(0.05, 40, 1e-3, 2), (0.02, 40, 5e-4, 2), (0.01, 100, 5e-4, 2)], clip=None),
    "srnet": dict(stages=[(0.1, 30, 3e-4, 5), (0.05, 30, 1e-4, 2), (0.02, 30, 1e-4, 2), (0.01, 60, 1e-4, 2)], clip=1.0),
}
PATIENCE = 25; BS_PAIRS = 16
def make(net): return nets39.Yedroudj() if net == "yedroudj" else N.SRNetStyle()
def logits(net, I):
    net.eval(); out = []
    with torch.no_grad():
        for i in range(0, len(I), 128): out.append(net(torch.tensor(I[i:i + 128], dtype=torch.float32, device=dev)[:, None]).float().cpu())
    return torch.cat(out)
def evaluate(net, vac, vas):
    lc, ls = logits(net, vac), logits(net, vas); pc, ps = lc.softmax(1)[:, 1].numpy(), ls.softmax(1)[:, 1].numpy()
    auc = roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]); loss = (F.cross_entropy(lc, torch.zeros(len(lc)).long()) + F.cross_entropy(ls, torch.ones(len(ls)).long())).item() / 2
    return float(auc), float(loss), pc, ps
def plateau(val_loss, k=10):
    """pre-registered: mean of the last k validation losses improves by less than 0.01 on the mean of the k before them (or rises)."""
    if len(val_loss) < 2 * k: return False
    return bool(np.mean(val_loss[-2 * k:-k]) - np.mean(val_loss[-k:]) < 0.01)
if __name__ == "__main__":
    seed = int(sys.argv[1]); netname = sys.argv[2]; sch = sys.argv[3]; cfg = CFG[netname]; ds = "ixi"
    if os.environ.get("LAST_EPOCHS"):  # attempt 2 (V3-H22): only the epoch cap of the final stage changes; declared in state/CLAIMS.md before the run
        cfg = dict(cfg); st = list(cfg["stages"]); b, _, lr, wu = st[-1]; st[-1] = (b, int(os.environ["LAST_EPOCHS"]), lr, wu); cfg["stages"] = st
    OUT = os.environ.get("OUT", "results/e42"); tagsfx = os.environ.get("TAG", ""); os.makedirs(OUT + "/ckpt", exist_ok=True)
    name = f"{netname}_{sch}_s{seed}{('_' + tagsfx) if tagsfx else ''}"; lf = open(f"{OUT}/{name}.log", "a")
    def log(m): print(m, flush=True); lf.write(m + "\n"); lf.flush()
    dtr, dva, dte = L.load_split(ds, "train"), L.load_split(ds, "val"), L.load_split(ds, "test")
    tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8); va_ids = np.sort(np.random.default_rng(seed + 31).permutation(len(dva["images"]))[:400]); te_ids = np.arange(len(dte["images"]))
    Ctr, Cva, Cte = dtr["images"][tr_ids], dva["images"][va_ids], dte["images"][te_ids]
    if os.environ.get("SMOKE"):  # pipeline check only, never a result
        tr_ids, va_ids, te_ids = tr_ids[:64], va_ids[:40], te_ids[:40]; Ctr, Cva, Cte = Ctr[:64], Cva[:40], Cte[:40]; cfg = dict(cfg, stages=[(b, 1, lr, w) for b, _, lr, w in cfg["stages"]])
    def stego(imgs, ids, tag, bpp):
        parts = L.chunks(len(imgs), 24); return np.concatenate(L.par(L.task_stego, [(imgs[a:b], ids[a:b], sch, seed, bpp, tag, None, None) for a, b in parts]))
    torch.manual_seed(seed * 100 + 7); np.random.seed(seed * 100 + 7); net = make(netname).to(dev); npar = sum(p.numel() for p in net.parameters())
    tc = torch.tensor(Ctr, dtype=torch.float32)[:, None]; n = len(tc); gep = 0; t0 = time.time(); hist = []; prev_best_state = None; run_ok = True
    for si, (bpp, max_ep, lr, warm) in enumerate(cfg["stages"]):
        Sva = stego(Cva, va_ids, 1, bpp)
        ws = os.environ.get("WARMSTART")
        if ws and si >= 0 and os.path.exists(ws.format(stage=si)): net.load_state_dict(torch.load(ws.format(stage=si), map_location=dev)); log(f"stage {si}: warm start from {ws.format(stage=si)}")
        elif prev_best_state is not None: net.load_state_dict(prev_best_state)
        opt = torch.optim.AdamW(net.parameters(), lr, weight_decay=1e-4); spe = (n + BS_PAIRS - 1) // BS_PAIRS
        sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda st: min(1.0, (st + 1) / (warm * spe)) * 0.5 * (1 + np.cos(np.pi * min(st / (max_ep * spe), 1.0))))
        best = (-1.0, None, -1); vloss = []; vauc = []; nxt = None
        for ep in range(max_ep):
            t_ep = time.time()
            S = nxt if nxt is not None else stego(Ctr, tr_ids, 1000 + gep, bpp)     # new messages and keys every epoch
            ts = torch.tensor(S, dtype=torch.float32)[:, None]; net.train(); perm = torch.randperm(n); tl = 0.0; nb = 0
            for b in range(0, n, BS_PAIRS):
                ix = perm[b:b + BS_PAIRS]; x = torch.cat([tc[ix], ts[ix]]).to(dev); y = torch.cat([torch.zeros(len(ix)), torch.ones(len(ix))]).long().to(dev)
                if torch.rand(1) < .5: x = x.flip(3)
                if torch.rand(1) < .5: x = x.flip(2)
                k = int(torch.randint(0, 4, (1,))); x = torch.rot90(x, k, (2, 3)) if k else x
                loss = F.cross_entropy(net(x), y); opt.zero_grad(); loss.backward()
                if cfg["clip"]: torch.nn.utils.clip_grad_norm_(net.parameters(), cfg["clip"])
                opt.step(); sched.step(); tl += loss.item(); nb += 1
            gep += 1; a, vl, _, _ = evaluate(net, Cva, Sva); vauc.append(round(a, 4)); vloss.append(round(vl, 4))
            log(f"stage {si} bpp {bpp} ep {ep} train_loss {tl / nb:.3f} val_loss {vl:.3f} val_auc {a:.4f} ({time.time() - t0:.0f}s, epoch {time.time() - t_ep:.0f}s)")
            if a > best[0]: best = (a, {k_: v.clone() for k_, v in net.state_dict().items()}, ep)
            if (ep + 1) % 5 == 0: torch.save(net.state_dict(), f"{OUT}/ckpt/{name}_stage{si}_ep{ep + 1}.pt")
            if ep - best[2] >= PATIENCE: log(f"stage {si}: early stop at epoch {ep} (best {best[2]})"); break
        hist.append(dict(stage=si, bpp=bpp, epochs_run=ep + 1, best_val_auc=round(best[0], 4), best_epoch=best[2], val_auc=vauc, val_loss=vloss))
        net.load_state_dict(best[1]); prev_best_state = {k_: v.clone() for k_, v in best[1].items()}; torch.save(best[1], f"{OUT}/ckpt/{name}_stage{si}_best.pt")
    bpp = cfg["stages"][-1][0]; Ste = stego(Cte, te_ids, 2, bpp); pc, ps = (lambda l: l.softmax(1)[:, 1].numpy())(logits(net, Cte)), (lambda l: l.softmax(1)[:, 1].numpy())(logits(net, Ste))
    test_auc = float(roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]))
    np.savez_compressed(f"{OUT}/{name}_scores.npz", pc=pc, ps=ps, subjects=dte["subject"][te_ids])
    last = hist[-1]; info = dict(net=netname, scheme=sch, seed=seed, tag=tagsfx, bpp=bpp, params=npar, best_val_auc=last["best_val_auc"], best_epoch=last["best_epoch"], plateau_val_loss=plateau(last["val_loss"]),
                                 test_auc=round(test_auc, 4), minutes=round((time.time() - t0) / 60, 1), stages=hist, n_train_pairs=int(n))
    json.dump(info, open(f"{OUT}/{name}.json", "w"), indent=1); log(f"DONE {name}: val {last['best_val_auc']} plateau {info['plateau_val_loss']} test {info['test_auc']} ({info['minutes']} min)")
