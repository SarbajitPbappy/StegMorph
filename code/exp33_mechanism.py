"""E33 (descriptive, pre-registered): change-reversal analysis. For test stego slices of a scheme, the modified pixels lying in the most textured third (3x3 local std of the cover) are put back to the cover value, or those in the smoothest third; the drop of the detector's stego-score measures how much of the detection each region carries.
Detectors: CNN checkpoint of E26 (net, seed 0) and detector A refit on the same training stego set. Usage: python code/exp33_mechanism.py"""
import os, sys, json, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L, nets26 as N
from exp24 import cover_feats, feats_for, fit_score
def main():
    seed, bpp, NT = 0, 0.01, 400
    dtr, dte = L.load_split("ixi", "train"), L.load_split("ixi", "test"); tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8); te_ids = np.arange(0, len(dte["images"]), len(dte["images"]) // NT)[:NT]; Ctr, Cte = dtr["images"][tr_ids], dte["images"][te_ids]
    res = {}; cf_tr = cover_feats(Ctr, ["srm"])["srm"]
    for sch in ("RANDSEQ", "COSTKEY"):
        S = np.array([L.make_stego(im, sch, L.message(seed, bpp, 2, int(i), im.size), seed, bpp, 2, int(i))[0] for im, i in zip(Cte, te_ids)]); M = S != Cte
        tex = np.array([L._lstd(c.astype(float)) for c in Cte]); th = np.array([np.percentile(t, [33.3, 66.7]) for t in tex]); top = tex >= th[:, 1, None, None]; bot = tex <= th[:, 0, None, None]
        var = {"stego": S, "revert_textured": np.where(M & top, Cte, S), "revert_smooth": np.where(M & bot, Cte, S), "cover": Cte}; share = {"changed_in_textured": float((M & top).sum() / M.sum()), "changed_in_smooth": float((M & bot).sum() / M.sum())}
        out = {"share": share}
        ck = f"results/e26/net_{sch}_b0.01_s0.pt"
        if os.path.exists(ck):
            net = N.make("net").to(N.dev); net.load_state_dict(torch.load(ck, map_location=N.dev)); P = {k: N.prob(net, v).mean() for k, v in var.items()}; out["cnn"] = {k: float(v) for k, v in P.items()}
        Ftr = feats_for(Ctr, tr_ids, sch, seed, bpp, 0, ["srm"], None, None, False)[0]["srm"]
        from sklearn.linear_model import LogisticRegression; from sklearn.preprocessing import StandardScaler
        X = np.vstack([cf_tr, Ftr]); y = np.r_[np.zeros(len(cf_tr)), np.ones(len(Ftr))]; sc = StandardScaler().fit(X); lr = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y)
        out["A"] = {k: float(lr.predict_proba(sc.transform(cover_feats(v, ["srm"])["srm"]))[:, 1].mean()) for k, v in var.items()}; res[sch] = out; print(sch, out, flush=True)
    json.dump(res, open("results/e26/e33_mechanism.json", "w"), indent=1)
if __name__ == "__main__":
    main()
