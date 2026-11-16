"""Driver for E24-E34 (pre-registered in state/CLAIMS.md). Usage: python code/exp24.py SEED   (run from the project root)
env: DS (dataset prefix in data/splits, default ixi), PAY (0.01,0.02), SCH (comma list of schemes, see lab24), DETS (A,B,D,S), OUT (results folder), NBOOT (1000), FRAC (training-subject fraction 0.8), NTE (max test slices),
     NTR (cap on training slices, for smoke tests)"""
import os, sys, json, time, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lab24 as L
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
KIND = {"A": "srm", "D": "srm", "B": "spam", "S": "sca"}
def octave_stego(ds, split, ids, imgs, method, bpp, seed, tag):
    """Reference HILL / S-UNIWARD simulators in Octave for the covers imgs (ids = original indices). Cached on disk; 5 parallel Octave processes."""
    n, H, W = imgs.shape; pay = L.payload_bits(bpp, H * W) / (H * W)
    key = f"{ds}_{split}_{method}_b{bpp}_s{seed}_n{n}_{int(ids.sum())}"; fp = os.path.join(L.CACHE, f"oct_{key}.npy")
    if os.path.exists(fp): return np.load(fp)
    tmp = os.path.join(os.environ.get("TMPOCT", "/tmp/steg_oct"), f"tmp_{key}"); os.makedirs(tmp, exist_ok=True); procs = []; parts = L.chunks(n, 5)  # tmp path must not contain an apostrophe (Octave --eval quoting)
    for c, (a, b) in enumerate(parts):
        np.ascontiguousarray(imgs[a:b]).tofile(f"{tmp}/in{c}.bin"); s0 = seed * 10 ** 6 + int(bpp * 1000) * 10 ** 3 + tag * 10 ** 5 + a
        cmd = f"batch_embed('{method}','{tmp}/in{c}.bin','{tmp}/out{c}.bin','none',{b - a},{H},{W},{pay:.8f},{s0})"
        procs.append(subprocess.Popen(["octave-cli", "--quiet", "--path", os.path.join(L.ROOT, "code", "octave"), "--eval", cmd], stderr=subprocess.PIPE))
    for p in procs:
        _, err = p.communicate()
        if p.returncode: raise RuntimeError(err.decode()[:500])
    out = np.concatenate([np.fromfile(f"{tmp}/out{c}.bin", np.uint8).reshape(-1, H, W) for c in range(len(parts))]); np.save(fp, out)
    for c in range(len(parts)): os.remove(f"{tmp}/in{c}.bin"); os.remove(f"{tmp}/out{c}.bin")
    return out
def feats_for(imgs, ids, scheme, seed, bpp, tag, kinds, cache_rows, pre, want_cover_sca):
    n = len(imgs); parts = L.chunks(n, 36)
    args = [(imgs[a:b], ids[a:b], scheme, seed, bpp, tag, kinds, None if cache_rows is None else cache_rows[a:b], None if pre is None else pre[a:b], want_cover_sca) for a, b in parts]
    res = L.par(L.task_scheme, args); F = {k: np.concatenate([r[0][k] for r in res]) for k in kinds}; st = np.concatenate([r[1] for r in res]); cf = np.concatenate([r[2] for r in res]) if want_cover_sca else None
    return F, st, cf, sum(r[3] for r in res)
def cover_feats(imgs, kinds):
    parts = L.chunks(len(imgs), 36); res = L.par(L.task_cover_feats, [(imgs[a:b], kinds) for a, b in parts]); return {k: np.concatenate([r[k] for r in res]) for k in kinds}
def key_rows(imgs, ids, scheme, seed, tag, ds, split):
    fp = os.path.join(L.CACHE, f"keys_{ds}_{split}_{scheme}_s{seed}_{int(ids.sum())}.npy")
    if os.path.exists(fp): return np.load(fp)
    parts = L.chunks(len(imgs), 36); res = L.par(L.task_keys, [(imgs[a:b], ids[a:b], scheme, seed, tag) for a, b in parts]); K = np.concatenate(res); np.save(fp, K); return K
def trim_rows(K): return [r[r >= 0].astype(np.int64) for r in K]
def fit_score(det, Xtr_c, Xtr_s, Xte_c, Xte_s, seed):
    X = np.vstack([Xtr_c, Xtr_s]); y = np.r_[np.zeros(len(Xtr_c)), np.ones(len(Xtr_s))]; Z = np.vstack([Xte_c, Xte_s])
    if det == "A": sc = StandardScaler().fit(X); p = LogisticRegression(C=0.05, max_iter=300).fit(sc.transform(X), y).predict_proba(sc.transform(Z))[:, 1]
    else: p = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, max_depth=4, random_state=seed).fit(X, y).predict_proba(Z)[:, 1]
    return p[:len(Xte_c)], p[len(Xte_c):]
def auc(pc, ps, idx): return roc_auc_score(np.r_[np.zeros(len(idx)), np.ones(len(idx))], np.r_[pc[idx], ps[idx]])
if __name__ == "__main__":
    seed = int(sys.argv[1]); ds = os.environ.get("DS", "ixi"); PAY = [float(x) for x in os.environ.get("PAY", "0.01,0.02").split(",")]; SCH = os.environ["SCH"].split(","); DETS = os.environ.get("DETS", "A,D").split(",")
    OUT = os.environ.get("OUT", "results/e24"); NB = int(os.environ.get("NBOOT", "1000")); FRAC = float(os.environ.get("FRAC", "0.8")); NTE = int(os.environ.get("NTE", "100000")); NTR = int(os.environ.get("NTR", "100000"))
    os.makedirs(OUT, exist_ok=True); dtr, dte = L.load_split(ds, "train"), L.load_split(ds, "test")
    tr_ids = L.seed_train_idx(dtr["subject"], seed, FRAC)[:NTR]; te_ids = np.arange(min(NTE, len(dte["images"]))); Ctr, Cte = dtr["images"][tr_ids], dte["images"][te_ids]; Ste = dte["subject"][te_ids]
    kinds_needed = sorted({KIND[d] for d in DETS} - {"sca"}); t0 = time.time(); fc_tr, fc_te = cover_feats(Ctr, kinds_needed), cover_feats(Cte, kinds_needed);
    print(f"seed {seed} ds {ds}: train {len(Ctr)} slices ({len(set(dtr['subject'][tr_ids]))} subjects), test {len(Cte)} ({len(set(Ste))} subjects); cover features {time.time()-t0:.0f}s", flush=True)
    for sch in SCH:
        if sch in L.KEYED_CACHE: key_rows(Ctr, tr_ids, sch, seed, 0, ds, "train"); key_rows(Cte, te_ids, sch, seed, 2, ds, "test")
    subj = sorted(set(Ste)); sidx = {s: np.where(Ste == s)[0] for s in subj}; out = {"seed": seed, "ds": ds, "n_train": len(Ctr), "n_train_subjects": len(set(dtr["subject"][tr_ids])), "n_test": len(Cte), "n_test_subjects": len(subj), "results": {}}
    for bpp in PAY:
        scores = {}; stats = {}; fails = {}; t1 = time.time()
        for sch in SCH:
            base = L.ALIAS.get(sch, sch); kinds = sorted({KIND[d] for d in DETS}); skinds = [k for k in kinds]; ts = time.time()
            def build(imgs, ids, tag, split, want_cov):
                rows = trim_rows(key_rows(imgs, ids, base, seed, tag, ds, split)) if base in L.KEYED_CACHE else None
                pre = octave_stego(ds, split, ids, imgs, "hill" if base == "HILLR" else "suni", bpp, seed, tag) if base in ("HILLR", "SUNIR") else None
                return feats_for(imgs, ids, sch, seed, bpp, tag, skinds, rows, pre, want_cov)
            wants = "sca" in skinds; Ftr, st_tr, cf_tr, f1 = build(Ctr, tr_ids, 0, "train", wants); Fte, st_te, cf_te, f2 = build(Cte, te_ids, 2, "test", wants)
            stats[sch] = dict(pvd_pairs=round(float(st_te[:, 0].mean()), 1), lsb_pairs=round(float(st_te[:, 1].mean()), 1), mse=round(float(st_te[:, 2].mean()), 5), changed_frac=round(float(st_te[:, 3].mean()), 5)); fails[sch] = [f1, f2]
            for det in DETS:
                k = KIND[det]; ctr = cf_tr if k == "sca" else fc_tr[k]; cte = cf_te if k == "sca" else fc_te[k]
                pc, ps = fit_score(det, ctr, Ftr[k], cte, Fte[k], seed); scores[(det, sch)] = (pc, ps)
            print(f"  bpp {bpp} {sch}: {time.time()-ts:.0f}s fails {f1},{f2} stats {stats[sch]}", flush=True)
        for det in DETS:
            sc = {s: scores[(det, s)] for s in SCH}; allidx = np.arange(len(Cte)); row = {"auc": {s: round(float(auc(*sc[s], allidx)), 4) for s in SCH}, "stats_test": stats, "failures": fails, "contrasts": {}}
            br = np.random.default_rng(seed + 5); reps = [np.concatenate([sidx[s] for s in br.choice(subj, len(subj))]) for _ in range(NB)]
            MATCH = {"COSTKEY": "COSTMIX", "ANTIKEY": "ANTIMIX"}; ref = lambda s: ("LSBK:R" if s.startswith("LSBK:") else "LSBM:R" if s.startswith("LSBM:") else "RANDFG" if (s.endswith("FG") and s != "RANDFG") or s.startswith("M:") and s.endswith("FG") else "RANDSEQ")
            pairs = [(s, ref(s)) for s in SCH if s != ref(s) and ref(s) in SCH] + [(s, MATCH.get(s, "M:" + s)) for s in SCH if MATCH.get(s, "M:" + s) in SCH]
            for a, b in pairs:
                d = row["auc"][a] - row["auc"][b]; x = np.array([auc(*sc[a], ix) - auc(*sc[b], ix) for ix in reps]); row["contrasts"][f"{a}-{b}"] = dict(diff=round(float(d), 4), ci95_subject_bootstrap=[round(float(np.percentile(x, 2.5)), 4), round(float(np.percentile(x, 97.5)), 4)])
            out["results"][f"{ds}|{det}|{bpp}"] = row; print(f"{det} {bpp} AUC {row['auc']}", flush=True)
            print("   ", {c: (v["diff"], v["ci95_subject_bootstrap"]) for c, v in row["contrasts"].items()}, flush=True)
        np.savez_compressed(f"{OUT}/scores_s{seed}_b{bpp}.npz", **{f"{d}|{s}|{w}": v for (d, s), (pc, ps) in scores.items() for w, v in (("pc", pc), ("ps", ps))}, subjects=Ste)
        json.dump(out, open(f"{OUT}/e24_seed{seed}.json", "w"), indent=1); print(f"payload {bpp} done {time.time()-t1:.0f}s", flush=True)
    print("DONE", seed)
