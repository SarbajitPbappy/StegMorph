"""E7 (to be pre-registered before running): small CNN steganalysis detector (XuNet-lite, fixed KB high-pass front end) for RAND vs GA_MSE vs GREEDY_TEX.
Usage: PYTHONPATH=/tmp/torchlib python exp7_cnn.py SEED DATASET(A_raw|A_noise) BPP N_IMAGES"""
import sys, json, glob, hashlib, time, numpy as np
sys.path.insert(0, "/tmp/torchlib")
import torch, torch.nn as nn, torch.nn.functional as F
from PIL import Image
from scipy.signal import convolve2d
from sklearn.metrics import roc_auc_score
import stegmorph_recon as R
seed = int(sys.argv[1]); DS = sys.argv[2]; BPP = float(sys.argv[3]); N = int(sys.argv[4]); torch.set_num_threads(2); torch.manual_seed(seed)
KB = np.array([[-1, 2, -2, 2, -1], [2, -6, 8, -6, 2], [-2, 8, -12, 8, -2], [2, -6, 8, -6, 2], [-1, 2, -2, 2, -1]]) / 12.0
AV3 = np.ones((3, 3))/9.0; AV7 = np.ones((7, 7))/49.0
def tex_pair_cost(img):
    x = img.astype(np.float64); r = np.abs(convolve2d(x, KB, mode="same", boundary="symm")); xi = convolve2d(r, AV3, mode="same", boundary="symm")
    rho = 1.0/(xi + 1e-2); rho = convolve2d(rho, AV7, mode="same", boundary="symm"); rho = rho/np.median(rho)
    f = rho.flatten(); n = len(f)//2*2
    return 0.5*(f[0:n:2] + f[1:n:2])
rng = np.random.default_rng(seed); n = int(BPP*128*128); need = R.total_bits(n)
af = sorted(glob.glob("/home/claude/data/Alzheimer-MRI-Preprocessed-Dataset/Alzheimer (Preprocessed Data)/**/*.jpg", recursive=True)); order = rng.permutation(len(af)); imgs = []
for i in order:
    im = np.array(Image.open(af[i]).convert("L"), np.uint8)
    if DS == "A_noise": im = np.clip(np.round(im + np.random.default_rng(i).normal(0, 1.5, im.shape)), 0, 255).astype(np.uint8)
    if R.capacity_and_branch(im)[0].sum() >= need: imgs.append(im)
    if len(imgs) == N: break
ex = [hashlib.sha256(im.tobytes()).hexdigest() for im in imgs]; first = {}; grp = np.array([first.setdefault(k, i) for i, k in enumerate(ex)])
ug = rng.permutation(np.unique(grp)); rk = {g: i for i, g in enumerate(ug)}; tr = np.array([rk[g] < 0.7*len(ug) for g in grp])
SCH = ["RAND", "GA_MSE", "GREEDY_TEX"]
def stego(sch):
    out = []
    for i, im in enumerate(imgs):
        r = np.random.default_rng(seed*10**6 + i); pay = r.integers(0, 2, n).astype(np.uint8); cap = R.capacity_and_branch(im)[0]
        if sch == "RAND": m = R.select_random(cap, need, r)
        elif sch == "GA_MSE": m = R.select_ga(cap, R.expected_cost(im, np.random.default_rng(seed*7+i)), need, r)
        else: m = R.select_greedy(cap, R.expected_cost(im, np.random.default_rng(seed*7+i))*tex_pair_cost(im), need)
        out.append(R.embed(im, pay, m))
    return np.array(out)
class Net(nn.Module):
    def __init__(s):
        super().__init__(); k = torch.tensor(KB, dtype=torch.float32)[None, None]; s.register_buffer("k", k)
        s.c1 = nn.Conv2d(1, 8, 5, padding=2); s.b1 = nn.BatchNorm2d(8); s.c2 = nn.Conv2d(8, 16, 5, padding=2); s.b2 = nn.BatchNorm2d(16)
        s.c3 = nn.Conv2d(16, 32, 3, padding=1); s.b3 = nn.BatchNorm2d(32); s.c4 = nn.Conv2d(32, 64, 3, padding=1); s.b4 = nn.BatchNorm2d(64); s.fc = nn.Linear(64, 2)
    def forward(s, x):
        x = F.conv2d(x, s.k, padding=2); x = F.avg_pool2d(torch.tanh(s.b1(s.c1(x).abs())), 3, 2, 1); x = F.avg_pool2d(torch.tanh(s.b2(s.c2(x))), 3, 2, 1)
        x = F.avg_pool2d(F.relu(s.b3(s.c3(x))), 3, 2, 1); x = F.relu(s.b4(s.c4(x))); return s.fc(x.mean((2, 3)))
def train_eval(cover, st, EP=25):
    Xtr = np.concatenate([cover[tr], st[tr]]); ytr = np.r_[np.zeros(tr.sum()), np.ones(tr.sum())]; Xte = np.concatenate([cover[~tr], st[~tr]]); yte = np.r_[np.zeros((~tr).sum()), np.ones((~tr).sum())]
    net = Net(); opt = torch.optim.Adam(net.parameters(), 1e-3, weight_decay=1e-5); Xt = torch.tensor(Xtr, dtype=torch.float32)[:, None]/255.; yt = torch.tensor(ytr, dtype=torch.long)
    for ep in range(EP):
        net.train(); perm = torch.randperm(len(Xt));
        for b in range(0, len(Xt), 32):
            idx = perm[b:b+32]; xb = Xt[idx]
            if np.random.rand() < 0.5: xb = xb.flip(3)           # horizontal flip only (keeps pair structure)
            opt.zero_grad(); loss = F.cross_entropy(net(xb), yt[idx]); loss.backward(); opt.step()
    net.eval()
    with torch.no_grad(): p = F.softmax(net(torch.tensor(Xte, dtype=torch.float32)[:, None]/255.), 1)[:, 1].numpy()
    return p, yte
t0 = time.time(); cover = np.array(imgs); res = {}; P = {}
for sch in SCH:
    st = stego(sch); p, y = train_eval(cover, st); P[sch] = p; res[sch] = round(float(roc_auc_score(y, p)), 4); print(sch, res[sch], round(time.time()-t0), flush=True)
nt = int((~tr).sum()); br = np.random.default_rng(seed+3); diffs = {}
for s in SCH[1:]:
    d = []
    for _ in range(500):
        ii = br.integers(0, nt, nt); idx = np.r_[ii, nt+ii]; d.append(roc_auc_score(y[idx], P[s][idx]) - roc_auc_score(y[idx], P["RAND"][idx]))
    diffs[s] = dict(diff=round(res[s]-res["RAND"], 4), ci95=[round(float(np.percentile(d, 2.5)), 4), round(float(np.percentile(d, 97.5)), 4)])
json.dump(dict(seed=seed, ds=DS, bpp=BPP, N=N, n_test=nt, auc=res, diff_vs_RAND=diffs), open(f"/home/claude/work/e7_{DS}_{BPP}_seed{seed}.json", "w"), indent=1); print("DONE", res, diffs)
