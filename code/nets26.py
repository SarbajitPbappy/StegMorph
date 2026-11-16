"""CNN detectors for E26 (Apple MPS). Net = the residual network used so far (cnn_mps.Net); SRNetStyle = a compact re-implementation of the layer layout of SRNet (Boroumand et al. 2019: 2 plain, 5 residual, 4 down-sampling blocks, global pooling), not the authors' code, trained without their pre-training or cover/stego batch tricks."""
import time, numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from sklearn.metrics import roc_auc_score
import cnn_mps as C
dev = C.dev
class T1(nn.Sequential):
    def __init__(s, i, o): super().__init__(nn.Conv2d(i, o, 3, padding=1, bias=False), nn.BatchNorm2d(o), nn.ReLU())
class T2(nn.Module):
    def __init__(s, c): super().__init__(); s.a = T1(c, c); s.b = nn.Sequential(nn.Conv2d(c, c, 3, padding=1, bias=False), nn.BatchNorm2d(c))
    def forward(s, x): return x + s.b(s.a(x))
class T3(nn.Module):
    def __init__(s, i, o): super().__init__(); s.a = T1(i, o); s.b = nn.Sequential(nn.Conv2d(o, o, 3, padding=1, bias=False), nn.BatchNorm2d(o), nn.AvgPool2d(3, 2, 1)); s.sk = nn.Sequential(nn.Conv2d(i, o, 1, 2, bias=False), nn.BatchNorm2d(o))
    def forward(s, x): return s.b(s.a(x)) + s.sk(x)
class SRNetStyle(nn.Module):
    def __init__(s):
        super().__init__(); s.f = nn.Sequential(T1(1, 64), T1(64, 16), *[T2(16) for _ in range(5)], T3(16, 16), T3(16, 64), T3(64, 128), T3(128, 256), nn.Conv2d(256, 512, 3, padding=1, bias=False), nn.BatchNorm2d(512)); s.fc = nn.Linear(512, 2)
    def forward(s, x): return s.fc(s.f(x / 255.0 * 2 - 1 if x.max() > 3 else x).mean((2, 3)))
def make(name): return C.Net() if name == "net" else SRNetStyle()
def prob(net, I):
    net.eval(); out = []
    with torch.no_grad():
        for i in range(0, len(I), 128): out.append(net(torch.tensor(I[i:i + 128], dtype=torch.float32, device=dev)[:, None]).softmax(1)[:, 1].cpu())
    return torch.cat(out).numpy()
def train(name, trc, trs, vac, vas, tec, tes, seed=0, max_epochs=60, patience=20, bs=32, lr=1e-3, log=print, ckpt=None):
    """Cosine schedule with 2 warm-up epochs, flip/rot90 augmentation (same transform for the cover/stego pair of a batch), early stopping on validation AUC, best-validation checkpoint restored."""
    torch.manual_seed(seed); np.random.seed(seed); net = make(name).to(dev); npar = sum(p.numel() for p in net.parameters())
    opt = torch.optim.AdamW(net.parameters(), lr, weight_decay=1e-4); spe = (len(trc) + bs - 1) // bs
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda st: min(1.0, (st + 1) / (2 * spe)) * 0.5 * (1 + np.cos(np.pi * min(st / (max_epochs * spe), 1.0))))
    tc = torch.tensor(trc, dtype=torch.float32)[:, None]; ts = torch.tensor(trs, dtype=torch.float32)[:, None]; n = len(tc); best = (-1, None, -1); hist = []; t0 = time.time()
    for ep in range(max_epochs):
        net.train(); perm = torch.randperm(n)
        for b in range(0, n, bs):
            ix = perm[b:b + bs]; x = torch.cat([tc[ix], ts[ix]]).to(dev); y = torch.cat([torch.zeros(len(ix)), torch.ones(len(ix))]).long().to(dev)
            if torch.rand(1) < .5: x = x.flip(3)
            if torch.rand(1) < .5: x = x.flip(2)
            k = int(torch.randint(0, 4, (1,)));  x = torch.rot90(x, k, (2, 3)) if k else x
            loss = F.cross_entropy(net(x), y); opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        pc, ps = prob(net, vac), prob(net, vas); a = roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]); hist.append(round(float(a), 4))
        log(f"ep {ep} loss {loss.item():.3f} val_auc {a:.4f} ({time.time()-t0:.0f}s)")
        if a > best[0]: best = (a, {k_: v.clone() for k_, v in net.state_dict().items()}, ep)
        if ep - best[2] >= patience: break
    net.load_state_dict(best[1])
    if ckpt: torch.save(best[1], ckpt)
    return prob(net, tec), prob(net, tes), dict(best_val_auc=round(float(best[0]), 4), best_epoch=best[2], epochs_run=ep + 1, minutes=round((time.time() - t0) / 60, 1), params=npar, val_auc_history=hist)
