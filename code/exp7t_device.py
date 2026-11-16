"""E6: corrected C1 re-test (pre-registered in state/CLAIMS.md 2026-11-10 10:10). Usage: python exp6.py SEED [SMOKE]"""
import sys, json, glob, time, numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import roc_auc_score
import stegmorph_recon as R, srm_lite as S
import torch, torch.nn as nn, torch.nn.functional as Fnn
torch.set_num_threads(2)
import os
EPOCHS=int(os.environ.get('EPOCHS','20')); seed = int(sys.argv[1]); SMOKE = len(sys.argv) > 2; PAY = [0.02] if SMOKE else [0.01, 0.02]; NA = 60 if SMOKE else 600; T = 3; B = 2*T+1; NF = 5
def _trip(a, b, c):
    idx = ((a+T)*B + (b+T))*B + (c+T); cnt = np.bincount(idx.ravel(), minlength=B**3).astype(np.float64).reshape(B, B, B)
    return cnt / np.maximum(cnt.sum(2, keepdims=True), 1)
def spam(img):
    x = img.astype(np.int32); f = lambda D: np.clip(D, -T, T)
    Dh = f(x[:, :-1]-x[:, 1:]); Dv = f(x[:-1]-x[1:]); h = _trip(Dh[:, :-2], Dh[:, 1:-1], Dh[:, 2:]); v = _trip(Dv[:-2], Dv[1:-1], Dv[2:])
    Dd = f(x[:-1, :-1]-x[1:, 1:]); d1 = _trip(Dd[:-2, :-2], Dd[1:-1, 1:-1], Dd[2:, 2:])
    xf = x[:, ::-1]; Da = f(xf[:-1, :-1]-xf[1:, 1:]); d2 = _trip(Da[:-2, :-2], Da[1:-1, 1:-1], Da[2:, 2:])
    return np.concatenate([((h+v)/2).ravel(), ((d1+d2)/2).ravel()]).astype(np.float32)
def noisy(im, key): return np.clip(np.round(im + np.random.default_rng(key).normal(0, 1.5, im.shape)), 0, 255).astype(np.uint8)
rng = np.random.default_rng(seed); need_max = R.total_bits(int(max(PAY)*128*128))
# ---- tumor crops grouped by source file (same construction as E5)
tf = sorted(glob.glob("DEVDATA/MRI_data/**/*.png", recursive=True)); Tc = []; Tg = []
for gi, f in enumerate(tf):
    im = np.array(Image.open(f).convert("L"), np.uint8); H, W = im.shape
    if H < 128 or W < 128: continue
    for j in range(2 if (H >= 256 or W >= 256) else 1):
        for _ in range(20):
            y = int(rng.integers(0, H-127)); x = int(rng.integers(0, W-127)); c = im[y:y+128, x:x+128]
            if R.capacity_and_branch(c)[0].sum() >= need_max: Tc.append(c.copy()); Tg.append(gi); break
if SMOKE: Tc, Tg = Tc[:60], Tg[:60]
# ---- alzheimer + noise, near-duplicate cluster groups (proxy)
af = sorted(glob.glob("DEVDATA/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True)); Ac = []; Araw = []
for i in rng.permutation(len(af)):
    raw = np.array(Image.open(af[i]).convert("L"), np.uint8); im = noisy(raw, int(i))
    if R.capacity_and_branch(im)[0].sum() >= need_max: Ac.append(im); Araw.append(raw)
    if len(Ac) == NA: break
V = np.array([np.array(Image.fromarray(r).resize((16, 16), Image.BILINEAR), float).ravel() for r in Araw]); V = (V - V.mean(1, keepdims=True)) / (V.std(1, keepdims=True) + 1e-6)
D = np.sqrt(((V[:, None] - V[None]) ** 2).sum(-1)); iu = np.triu_indices(len(V), 1); chosen = None
for q in [0.002, 0.005, 0.01, 0.02, 0.05, 0.1]:
    lab = AgglomerativeClustering(n_clusters=None, distance_threshold=float(np.quantile(D[iu], q)), metric="precomputed", linkage="complete").fit_predict(D)
    sz = np.bincount(lab)
    if sz.max() <= max(3, 0.05*len(V)): chosen = (q, lab, sz)
q, Ag, sz = chosen if chosen else (0, np.arange(len(V)), np.ones(len(V), int))
clinfo = dict(quantile=q, n_clusters=int(len(sz)), max_cluster=int(sz.max()), mean_cluster=round(float(sz.mean()), 2), n_images=len(V))
print("A clusters", clinfo, flush=True)
def foldsof(g):
    ug = rng.permutation(np.unique(g)); fm = {k: i % NF for i, k in enumerate(ug)}; return np.array([fm[k] for k in g])
sets = {"T_raw": (Tc, np.array(Tg))}
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
def oof(fam, Fc, Fs, folds):
    pc = np.zeros(len(Fc)); ps = np.zeros(len(Fc))
    for f in range(NF):
        tr = folds != f; te = ~tr
        X = np.vstack([Fc[tr], Fs[tr]]); y = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]; Z = np.vstack([Fc[te], Fs[te]])
        if fam == "C": p = np.r_[*cnn_pred(Fc[tr],Fs[tr],Fc[te],Fs[te],seed*100+f)]
        elif fam == "A": sc = StandardScaler().fit(X); m = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y); p = m.predict_proba(sc.transform(Z))[:, 1]
        else: m = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, y); p = m.predict_proba(Z)[:, 1]
        rk = (np.argsort(np.argsort(p)) + 0.5) / len(p); pc[te] = rk[:te.sum()]; ps[te] = rk[te.sum():]
    return pc, ps
def auc_of(pc, ps, idx): return roc_auc_score(np.r_[np.zeros(len(idx)), np.ones(len(idx))], np.r_[pc[idx], ps[idx]])
out = {"seed": seed, "cluster_info": clinfo, "smoke": SMOKE, "results": {}}
SCH = ["RAND", "GA", "RAND_GAMIX"]; CON = {"P1_GA-RAND": ("GA", "RAND"), "P3_GA-RANDGAMIX": ("GA", "RAND_GAMIX")}
for si, (name, (imgs, grp)) in enumerate(sets.items()):
    folds = foldsof(grp); ug = np.unique(grp); gi = {g: np.where(grp == g)[0] for g in ug}
    for bpp in PAY:
        t0 = time.time(); sts, stats = make_all(imgs, bpp, si); Fs = {k: (None, None, np.array(v)) for k, v in sts.items() if k in SCH}
        for fi, fam in ((2, "C"),):
            sc = {k: oof(fam, (None, None, np.array(imgs))[fi], Fs[k][fi], folds) for k in SCH}; allidx = np.arange(len(imgs))
            row = {"auc": {k: round(float(auc_of(*sc[k], allidx)), 4) for k in SCH}, "stats": stats, "n_images": len(imgs), "contrasts": {}}
            br = np.random.default_rng(seed+5); boots = {c: [] for c in CON}
            for _ in range(500):
                pick = br.integers(0, len(ug), len(ug)); idx = np.concatenate([gi[ug[j]] for j in pick])
                for c, (a, b) in CON.items(): boots[c].append(auc_of(*sc[a], idx) - auc_of(*sc[b], idx))
            for c, (a, b) in CON.items():
                d = row["auc"][a] - row["auc"][b]; bs = np.array(boots[c])
                row["contrasts"][c] = dict(diff=round(float(d), 4), ci95=[round(float(np.percentile(bs, 2.5)), 4), round(float(np.percentile(bs, 97.5)), 4)], ci90=[round(float(np.percentile(bs, 5)), 4), round(float(np.percentile(bs, 95)), 4)])
            out["results"][f"{name}|{fam}|{bpp}"] = row
        print("done", name, bpp, round(time.time()-t0, 1), flush=True)
        json.dump(out, open(f"e7t_seed{seed}{'_smoke' if SMOKE else ''}.json", "w"), indent=1)
print("DONE", seed)
