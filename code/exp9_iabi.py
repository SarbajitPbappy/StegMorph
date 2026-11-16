"""E9: subject-disjoint real-cover test (IABI = IXI T2 slices, subject-disjoint train/val/test splits, no JPEG).
Detectors trained on train-split covers/stegos, tested on the disjoint test split. Schemes RAND, GA, GA_RANDMIX, RAND_GAMIX.
Usage: python exp9_iabi.py SEED  (env: IABI_DIR, EPOCHS, NTR, NTE, USE_CNN, PAY)"""
import os, sys, json, time, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import stegmorph_recon as R, srm_lite as S
USE_CNN = os.environ.get("USE_CNN", "1") == "1"
if USE_CNN:
    import torch, torch.nn as nn, torch.nn.functional as Fnn
    torch.set_num_threads(os.cpu_count())
EPOCHS = int(os.environ.get("EPOCHS", "15")); seed = int(sys.argv[1]); T = 3; B = 2*T+1
NTR = int(os.environ.get("NTR", "800")); NTE = int(os.environ.get("NTE", "200")); PAY = [float(x) for x in os.environ.get("PAY", "0.01,0.02").split(",")]
D = os.environ.get("IABI_DIR", "data/raw/IABI")
def load(name, n):
    a = np.load(os.path.join(D, name))["images"].astype(np.float32); a = np.clip(np.round(a*255), 0, 255).astype(np.uint8)
    a = a[:, 16:144, 16:144]                                  # centre 128x128 crop of 160x160
    return a[:n]
need_max = R.total_bits(int(max(PAY)*128*128))
def keep(ims): return [im for im in ims if R.capacity_and_branch(im)[0].sum() >= need_max]
Ctr = keep(load("train.npz", NTR)); Cte = keep(load("test.npz", NTE)); print("covers", len(Ctr), len(Cte), flush=True)

def _trip(a, b, c):
    idx = ((a+T)*B + (b+T))*B + (c+T); cnt = np.bincount(idx.ravel(), minlength=B**3).astype(np.float64).reshape(B, B, B)
    return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T, T)
    Dh = f(x[:, :-1]-x[:, 1:]); Dv = f(x[:-1]-x[1:]); h = _trip(Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:]); v = _trip(Dv[:-2], Dv[1:-1], Dv[2:])
    Dd = f(x[:-1, :-1]-x[1:, 1:]); d1 = _trip(Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:])
    xf = x[:, ::-1]; Da = f(xf[:-1, :-1]-xf[1:, 1:]); d2 = _trip(Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:])
    return np.concatenate([((h+v)/2).ravel(), ((d1+d2)/2).ravel()]).astype(np.float32)

if USE_CNN:
    KV=torch.tensor([[-1,2,-2,2,-1],[2,-6,8,-6,2],[-2,8,-12,8,-2],[2,-6,8,-6,2],[-1,2,-2,2,-1]],dtype=torch.float32)/12.0
    class Net(nn.Module):
        def __init__(s):
            super().__init__(); s.register_buffer("kv",KV[None,None])
            def blk(i,o,p): return nn.Sequential(nn.Conv2d(i,o,3,padding=1,bias=False),nn.BatchNorm2d(o),nn.ReLU(),*( [nn.AvgPool2d(2)] if p else []))
            s.f=nn.Sequential(nn.Conv2d(1,12,5,padding=2,bias=False),nn.BatchNorm2d(12),nn.Hardtanh(-3,3),blk(12,16,1),blk(16,32,1),blk(32,64,1),blk(64,64,0)); s.fc=nn.Linear(64,2)
        def forward(s,x):
            x=Fnn.conv2d(x,s.kv,padding=2); return s.fc(s.f(x).mean((2,3)))
    def cnn_pred(Itr_c,Itr_s,Ite_c,Ite_s,seed_,epochs=EPOCHS):
        torch.manual_seed(seed_); net=Net(); opt=torch.optim.Adam(net.parameters(),1e-3,weight_decay=1e-5)
        tc=torch.tensor(Itr_c,dtype=torch.float32)[:,None]; ts=torch.tensor(Itr_s,dtype=torch.float32)[:,None]; n=len(tc)
        sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,epochs)
        for ep in range(epochs):
            net.train(); perm=torch.randperm(n)
            for b in range(0,n,16):
                ix=perm[b:b+16]; x=torch.cat([tc[ix],ts[ix]]); y=torch.cat([torch.zeros(len(ix)),torch.ones(len(ix))]).long()
                if torch.rand(1)<0.5: x=x.flip(3)
                if torch.rand(1)<0.5: x=x.flip(2)
                loss=Fnn.cross_entropy(net(x),y); opt.zero_grad(); loss.backward(); opt.step()
            sched.step()
        net.eval()
        with torch.no_grad():
            f=lambda I: torch.cat([net(torch.tensor(I[i:i+64],dtype=torch.float32)[:,None]).softmax(1)[:,1] for i in range(0,len(I),64)]).numpy()
            return f(Ite_c),f(Ite_s)


def make_all(imgs, bpp, tag):
    n = int(bpp*128*128); need = R.total_bits(n); out = {k: [] for k in ("RAND", "GA", "GA_RANDMIX", "RAND_GAMIX")}; st = {k: [] for k in out}
    for i, im in enumerate(imgs):
        r = np.random.default_rng(seed*10**6 + int(bpp*1000)*1000 + i + tag*7919); pay = r.integers(0, 2, n).astype(np.uint8)
        cap, low, pvd = R.capacity_and_branch(im); cost = R.expected_cost(im, np.random.default_rng(seed*7+i))
        mR = R.select_random(cap, need, r); mG = R.select_ga(cap, cost, need, r)
        def quota(m): return int(cap[m & low].sum()), int(cap[m & pvd].sum())
        def ga_in(capb, nb): return R.select_ga(capb, cost, nb, r) if nb > 0 else np.zeros(len(cap), bool)
        def rnd_in(capb, nb): return R.select_random(capb, nb, r) if nb > 0 else np.zeros(len(cap), bool)
        capL = np.where(low, cap, 0); capP = np.where(pvd, cap, 0)
        qL, qP = quota(mR); mGR = ga_in(capL, qL) | ga_in(capP, qP)
        qL, qP = quota(mG); mRG = rnd_in(capL, qL) | rnd_in(capP, qP)
        for k, m in (("RAND", mR), ("GA", mG), ("GA_RANDMIX", mGR), ("RAND_GAMIX", mRG)):
            s = R.embed(im, pay, m); out[k].append(s); st[k].append((int(m.sum()), float(low[m].mean()), float(((s.astype(float)-im)**2).mean())))
            if i < 2: assert (R.extract(s, m) == pay).all()
    return out, {k: dict(pairs=round(float(np.mean([a for a, _, _ in v])), 1), low_share=round(float(np.mean([b for _, b, _ in v])), 3), mse=round(float(np.mean([c for _, _, c in v])), 4)) for k, v in st.items()}

SCH = ["RAND", "GA", "GA_RANDMIX", "RAND_GAMIX"]; CON = {"P1_GA-RAND": ("GA", "RAND"), "P2_GARANDMIX-RAND": ("GA_RANDMIX", "RAND"), "P3_GA-RANDGAMIX": ("GA", "RAND_GAMIX")}
def fitpred(fam, tr_c, tr_s, te_c, te_s, f):
    if fam == "C":
        pc, ps = cnn_pred(tr_c, tr_s, te_c, te_s, seed*100+f); return pc, ps
    X = np.vstack([tr_c, tr_s]); y = np.r_[np.zeros(len(tr_c)), np.ones(len(tr_s))]; Z = np.vstack([te_c, te_s])
    if fam == "A": sc = StandardScaler().fit(X); p = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y).predict_proba(sc.transform(Z))[:, 1]
    else: p = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, y).predict_proba(Z)[:, 1]
    return p[:len(te_c)], p[len(te_c):]
def auc(pc, ps, idx): return roc_auc_score(np.r_[np.zeros(len(idx)), np.ones(len(idx))], np.r_[pc[idx], ps[idx]])
out = {"seed": seed, "n_train": len(Ctr), "n_test": len(Cte), "results": {}}
FA = lambda L: np.array([S.features(x) for x in L]); FB = lambda L: np.array([spam(x) for x in L])
trA, trB, teA, teB = FA(Ctr), FB(Ctr), FA(Cte), FB(Cte)
for bpp in PAY:
    t0 = time.time(); str_, stats_tr = make_all(Ctr, bpp, 11); ste, stats_te = make_all(Cte, bpp, 13)
    fams = ["A", "B"] + (["C"] if USE_CNN else [])
    for fam in fams:
        sc = {}
        for k in SCH:
            if fam == "A": r = fitpred("A", trA, FA(str_[k]), teA, FA(ste[k]), 0)
            elif fam == "B": r = fitpred("B", trB, FB(str_[k]), teB, FB(ste[k]), 0)
            else: r = fitpred("C", np.array(Ctr), np.array(str_[k]), np.array(Cte), np.array(ste[k]), 0)
            sc[k] = r
        allidx = np.arange(len(Cte)); row = {"auc": {k: round(float(auc(*sc[k], allidx)), 4) for k in SCH}, "stats_test": stats_te, "contrasts": {}}
        br = np.random.default_rng(seed+5); boots = {c: [] for c in CON}
        for _ in range(500):
            idx = br.integers(0, len(Cte), len(Cte))
            for c, (a, b) in CON.items(): boots[c].append(auc(*sc[a], idx) - auc(*sc[b], idx))
        for c, (a, b) in CON.items():
            d = row["auc"][a] - row["auc"][b]; bs = np.array(boots[c])
            row["contrasts"][c] = dict(diff=round(float(d), 4), ci90=[round(float(np.percentile(bs, 5)), 4), round(float(np.percentile(bs, 95)), 4)])
        out["results"][f"IABI|{fam}|{bpp}"] = row; print(fam, bpp, row["auc"], {c: v["diff"] for c, v in row["contrasts"].items()}, flush=True)
        json.dump(out, open(f"e9_seed{seed}.json", "w"), indent=1)
    print("done", bpp, round(time.time()-t0, 1), flush=True)
print("DONE", seed)
