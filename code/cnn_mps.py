"""CNN detector for the Mac GPU (MPS). XuNet/SRNet-inspired: fixed KV high-pass front end, BN+ReLU conv blocks with a residual shortcut, global pooling.
fit_predict(train_cover, train_stego, val_cover, val_stego, test_cover, test_stego) -> (p_cover, p_stego) on test, model chosen by best val AUC."""
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from sklearn.metrics import roc_auc_score
dev = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
KV = torch.tensor([[-1,2,-2,2,-1],[2,-6,8,-6,2],[-2,8,-12,8,-2],[2,-6,8,-6,2],[-1,2,-2,2,-1]], dtype=torch.float32) / 12.0
class Res(nn.Module):
    def __init__(s, i, o, pool):
        super().__init__(); s.c1 = nn.Conv2d(i, o, 3, padding=1, bias=False); s.b1 = nn.BatchNorm2d(o)
        s.c2 = nn.Conv2d(o, o, 3, padding=1, bias=False); s.b2 = nn.BatchNorm2d(o)
        s.sk = nn.Conv2d(i, o, 1, bias=False) if i != o else nn.Identity(); s.pool = pool
    def forward(s, x):
        y = s.b2(s.c2(F.relu(s.b1(s.c1(x))))) + s.sk(x); y = F.relu(y)
        return F.avg_pool2d(y, 2) if s.pool else y
class Net(nn.Module):
    def __init__(s):
        super().__init__(); s.register_buffer("kv", KV[None, None])
        s.stem = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1, bias=False), nn.BatchNorm2d(16), nn.ReLU())
        s.body = nn.Sequential(Res(16, 16, 0), Res(16, 32, 1), Res(32, 64, 1), Res(64, 128, 1), Res(128, 128, 0)); s.fc = nn.Linear(128, 2)
    def forward(s, x):
        x = F.conv2d(x, s.kv, padding=2); x = torch.clamp(x, -3, 3)         # 'truncation' as in SRM-style front ends
        return s.fc(s.body(s.stem(x)).mean((2, 3)))
def _prob(net, I):
    net.eval(); out = []
    with torch.no_grad():
        for i in range(0, len(I), 128): out.append(net(torch.tensor(I[i:i+128], dtype=torch.float32, device=dev)[:, None]).softmax(1)[:, 1].cpu())
    return torch.cat(out).numpy()
def fit_predict(trc, trs, vac, vas, tec, tes, seed=0, epochs=30, bs=32, lr=1e-3, log=None):
    torch.manual_seed(seed); np.random.seed(seed); net = Net().to(dev); opt = torch.optim.AdamW(net.parameters(), lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=epochs * ((len(trc) + bs - 1) // bs))
    tc = torch.tensor(trc, dtype=torch.float32)[:, None]; ts = torch.tensor(trs, dtype=torch.float32)[:, None]; n = len(tc); best = (-1, None)
    for ep in range(epochs):
        net.train(); perm = torch.randperm(n)
        for b in range(0, n, bs):
            ix = perm[b:b+bs]; x = torch.cat([tc[ix], ts[ix]]).to(dev); y = torch.cat([torch.zeros(len(ix)), torch.ones(len(ix))]).long().to(dev)
            if torch.rand(1) < .5: x = x.flip(3)
            if torch.rand(1) < .5: x = x.flip(2)
            loss = F.cross_entropy(net(x), y); opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        pc, ps = _prob(net, vac), _prob(net, vas); a = roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps])
        if log: log(f"ep {ep} loss {loss.item():.3f} val_auc {a:.4f}")
        if a > best[0]: best = (a, {k: v.clone() for k, v in net.state_dict().items()})
    net.load_state_dict(best[1]); return _prob(net, tec), _prob(net, tes), best[0]
