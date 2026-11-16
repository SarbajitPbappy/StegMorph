"""V2.1 (pre-registered V2-H1, V2-H2): full SRM (34,671-d) and real maxSRM (DDE Lab MEX code, tools/dde) with an FLD ensemble (random subspaces, pair bootstrap).
Detector F = full SRM; detector M = maxSRM with the modification-probability map of the scheme (computed from the image under test, as for detector S).
Usage: SCH=RANDSEQ,COSTKEY PAY=0.01 DETS=F,M OUT=results/e37 python code/exp37_fullsrm.py SEED"""
import os, sys, json, time, subprocess, tempfile, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); ROOT = os.path.dirname(HERE)
import lab24 as L
from exp24 import key_rows, trim_rows, octave_stego, auc
from scipy.io import savemat
from sklearn.metrics import roc_auc_score
NW = int(os.environ.get("NW", "5")); TMPD = os.environ.get("TMPOCT", tempfile.gettempdir())
def extract(imgs, maps, mode):
    """Features of N images (N x H x W uint8) with maps (N x H x W) in NW parallel Octave processes."""
    n = len(imgs); parts = L.chunks(n, NW); procs = []; tag = f"{os.getpid()}_{time.time_ns()}"
    for j, (a, b) in enumerate(parts):
        fin = f"{TMPD}/f_{tag}_{j}.mat"; fout = f"{TMPD}/f_{tag}_{j}.bin"; savemat(fin, dict(imgs=imgs[a:b], maps=(maps[a:b] if maps is not None else np.zeros((b - a, 1, 1)))), do_compression=False)
        env = dict(os.environ, FEAT_IN=fin, FEAT_OUT=fout, FEAT_MODE=mode, FEAT_TMP=f"{TMPD}/f_{tag}_{j}.pgm", FEAT_BIN=os.path.join(ROOT, "tools/dde/bin"))
        procs.append((subprocess.Popen(["octave-cli", "--no-gui", "-q", os.path.join(ROOT, "tools/dde/feat.m")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE), fin, fout, b - a))
    out = []
    for p, fin, fout, m in procs:
        err = p.communicate()[1]
        if p.returncode: raise RuntimeError(err.decode()[-800:])
        out.append(np.fromfile(fout, dtype=np.float32).reshape(m, 34671)); os.remove(fin); os.remove(fout)
    return np.concatenate(out)
def fld_ensemble(Xc, Xs, Zs, seed, dsub=2000, nl=100, lam=1e-3):
    """Kodovsky-style FLD ensemble: nl base learners on random feature subspaces and pair bootstraps; score = mean standardised projection. Zs = list of arrays to score.
    ENGINE=mps (default when available) does the matrix products on the Apple GPU (feature columns are gathered on the CPU per learner, so no large copy is made); ENGINE=np uses numpy only. Same algorithm and random draws."""
    import torch
    use = os.environ.get("ENGINE", "mps") == "mps" and torch.backends.mps.is_available(); dev = torch.device("mps" if use else "cpu")
    rng = np.random.default_rng(seed); mu = np.vstack([Xc, Xs]).mean(0); sd = np.vstack([Xc, Xs]).std(0) + 1e-6; n, D = Xc.shape; out = [np.zeros(len(z)) for z in Zs]
    for l in range(nl):
        cols = np.sort(rng.choice(D, dsub, replace=False)); bi = rng.integers(0, n, n); m_, s_ = mu[cols], sd[cols]
        C = torch.from_numpy(((Xc[bi][:, cols] - m_) / s_).astype(np.float32)).to(dev); S = torch.from_numpy(((Xs[bi][:, cols] - m_) / s_).astype(np.float32)).to(dev)
        mc, ms = C.mean(0), S.mean(0); C0, S0 = C - mc, S - ms; Sw = ((C0.T @ C0 + S0.T @ S0) / (2 * n)).cpu().double() + lam * torch.eye(dsub, dtype=torch.float64)
        w = torch.linalg.solve(Sw, (ms - mc).cpu().double()).float().to(dev); pc, ps = C @ w, S @ w; thr = ((pc.mean() + ps.mean()) / 2).item(); sc = float(np.sqrt((pc.var().item() + ps.var().item()) / 2) + 1e-9)
        for k, z in enumerate(Zs): out[k] += ((torch.from_numpy(((z[:, cols] - m_) / s_).astype(np.float32)).to(dev) @ w).cpu().numpy() - thr) / sc
    return [o / nl for o in out]
if __name__ == "__main__":
    seed = int(sys.argv[1]); ds = os.environ.get("DS", "ixi"); PAY = [float(x) for x in os.environ.get("PAY", "0.01,0.02").split(",")]; SCH = os.environ["SCH"].split(","); DETS = os.environ.get("DETS", "F,M").split(",")
    OUT = os.environ.get("OUT", "results/e37"); NB = int(os.environ.get("NBOOT", "1000")); NTR = int(os.environ.get("NTR", "100000")); NTE = int(os.environ.get("NTE", "100000")); DSUB = int(os.environ.get("DSUB", "2000")); NL = int(os.environ.get("NL", "100")); os.makedirs(OUT, exist_ok=True)
    dtr, dte = L.load_split(ds, "train"), L.load_split(ds, "test"); tr_ids = L.seed_train_idx(dtr["subject"], seed, 0.8)[:NTR]; te_ids = np.arange(min(NTE, len(dte["images"]))); Ctr, Cte = dtr["images"][tr_ids], dte["images"][te_ids]; Ste = dte["subject"][te_ids]
    subj = sorted(set(Ste)); sidx = {s: np.where(Ste == s)[0] for s in subj}; t0 = time.time(); print(f"seed {seed}: train {len(Ctr)} test {len(Cte)}", flush=True)
    cover_srm = None
    for sch in SCH:
        if L.ALIAS.get(sch, sch) in L.KEYED_CACHE: key_rows(Ctr, tr_ids, L.ALIAS.get(sch, sch), seed, 0, ds, "train"); key_rows(Cte, te_ids, L.ALIAS.get(sch, sch), seed, 2, ds, "test")
    out = {"seed": seed, "n_train": len(Ctr), "n_test": len(Cte), "dsub": DSUB, "n_learners": NL, "results": {}}; allscores = {}
    for bpp in PAY:
        scores = {}
        for sch in SCH:
            base = L.ALIAS.get(sch, sch); ts = time.time()
            def stego(imgs, ids, tag, split):
                rows = trim_rows(key_rows(imgs, ids, base, seed, tag, ds, split)) if base in L.KEYED_CACHE else None
                pre = octave_stego(ds, split, ids, imgs, "hill" if base == "HILLR" else "suni", bpp, seed, tag) if base in ("HILLR", "SUNIR") else None
                parts = L.chunks(len(imgs), 24); return np.concatenate(L.par(L.task_stego, [(imgs[a:b], ids[a:b], sch, seed, bpp, tag, None if rows is None else rows[a:b], None if pre is None else pre[a:b]) for a, b in parts]))
            Str, Ste_ = stego(Ctr, tr_ids, 0, "train"), stego(Cte, te_ids, 2, "test")
            def nbits(i, npix): return len(L.SM._text_to_bits(L.message(seed, bpp, 0, int(i), npix)))
            for det in DETS:
                if det == "F":
                    if cover_srm is None: cover_srm = (extract(Ctr, None, "srm"), extract(Cte, None, "srm"))
                    Ftr_s, Fte_s = extract(Str, None, "srm"), extract(Ste_, None, "srm"); Ftr_c, Fte_c = cover_srm
                elif det == "K":   # key-known detector (V2.5): maxSRM with the map = the pixels the key visits for this message (same map for cover and stego)
                    def kmap(imgs, ids, tag, split):
                        rows = trim_rows(key_rows(imgs, ids, base, seed, tag, ds, split)) if base in L.KEYED_CACHE else None; out_ = []
                        for j, im in enumerate(imgs):
                            i_ = int(ids[j]); nb_ = len(L.SM._text_to_bits(L.message(seed, bpp, tag, i_, im.size))); key = L.get_key(im, sch, seed, bpp, tag, i_, None if rows is None else rows[j]); nP, nL = L.used_pairs(im, key, nb_)
                            m_ = np.zeros(im.size); m_[np.asarray(key)[:2 * (nP + nL)]] = 1.0; out_.append(m_.reshape(im.shape))
                        return np.array(out_)
                    mtr, mte = kmap(Ctr, tr_ids, 0, "train"), kmap(Cte, te_ids, 2, "test")
                    Ftr_c, Fte_c = extract(Ctr, mtr, "max"), extract(Cte, mte, "max"); Ftr_s, Fte_s = extract(Str, mtr, "max"), extract(Ste_, mte, "max")
                else:
                    mp = lambda imgs, ids, tag: np.clip(np.array([L.beta_for(sch, im, len(L.SM._text_to_bits(L.message(seed, bpp, tag, int(ids[j]), im.size)))) for j, im in enumerate(imgs)]), 0, 1).astype(np.float64)
                    Ftr_c, Fte_c = extract(Ctr, mp(Ctr, tr_ids, 0), "max"), extract(Cte, mp(Cte, te_ids, 2), "max"); Ftr_s, Fte_s = extract(Str, mp(Str, tr_ids, 0), "max"), extract(Ste_, mp(Ste_, te_ids, 2), "max")
                pc, ps = fld_ensemble(Ftr_c, Ftr_s, [Fte_c, Fte_s], seed * 7 + 1, DSUB, NL); scores[(det, sch)] = (pc, ps); del Ftr_c, Ftr_s, Fte_c, Fte_s
                print(f"  bpp {bpp} {sch} {det}: AUC {roc_auc_score(np.r_[np.zeros(len(pc)), np.ones(len(ps))], np.r_[pc, ps]):.4f} ({time.time()-ts:.0f}s)", flush=True)
        for det in DETS:
            sc = {s: scores[(det, s)] for s in SCH}; allidx = np.arange(len(Cte)); row = {"auc": {s: round(float(auc(*sc[s], allidx)), 4) for s in SCH}, "contrasts": {}}
            br = np.random.default_rng(seed + 5); reps = [np.concatenate([sidx[s] for s in br.choice(subj, len(subj))]) for _ in range(NB)]
            MATCH = {"COSTKEY": "COSTMIX", "ANTIKEY": "ANTIMIX"}; pairs = [(s, "RANDSEQ") for s in SCH if s != "RANDSEQ" and "RANDSEQ" in SCH] + [(s, MATCH[s]) for s in SCH if s in MATCH and MATCH[s] in SCH]
            for a, b in pairs:
                d = row["auc"][a] - row["auc"][b]; x = np.array([auc(*sc[a], ix) - auc(*sc[b], ix) for ix in reps]); row["contrasts"][f"{a}-{b}"] = dict(diff=round(float(d), 4), ci95_subject_bootstrap=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)])
            out["results"][f"{ds}|{det}|{bpp}"] = row; print(f"{det} {bpp} AUC {row['auc']}", flush=True); print("   ", {c: (v["diff"], v["ci95_subject_bootstrap"]) for c, v in row["contrasts"].items()}, flush=True)
        np.savez_compressed(f"{OUT}/scores_s{seed}_b{bpp}.npz", **{f"{d}|{s}|{w}": v for (d, s), (pc, ps) in scores.items() for w, v in (("pc", pc), ("ps", ps))}, subjects=Ste)
        json.dump(out, open(f"{OUT}/e37_seed{seed}.json", "w"), indent=1)
    print("DONE", seed, f"{time.time()-t0:.0f}s")
