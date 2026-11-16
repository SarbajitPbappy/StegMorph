"""V3.6 (V3-H26): patient-disjoint slice sets from the BraTS 2020 training data as stored in the Kaggle dataset awsaf49/brats2020-training-data (2D .h5 slices, CC0).
NOT RUN YET. Written before the download; run only after (1) the files are downloaded and inspected, (2) the data-format addendum is appended to state/CLAIMS.md, (3) CHANNEL below is set from that inspection.
Steps (rules fixed in state/CLAIMS.md, entry 'V3-H26 pre-registration'):
 1. re-assemble each volume from its slices; keep the T2 channel (CHANNEL); masks are never read;
 2. exclude every case that also appears in MSD Task01 (matching processed slice 80 against all MSD volumes, see overlap());
 3. sample N=120 patients (or all remaining) with numpy default_rng(2026), split by patient 60/20/20 BEFORE any slice is cut;
 4. per volume scale by the 99.5th percentile of non-zero voxels to 0-255, axial slices 40..100 step 5, centre 128x128 crop (no interpolation);
 5. write data/splits/bratst2_{train,val,test}.npz and data/splits/bratst2_split_manifest.json (patient IDs, slice indices, sha256, number excluded).
Usage (project root, after inspection): ROOT=<kagglehub path> CHANNEL=<int> python code/build_brats_splits.py"""
import os, re, glob, json, hashlib, numpy as np, h5py, nibabel as nib
ROOT = os.environ["ROOT"]; CHANNEL = os.environ.get("CHANNEL"); assert CHANNEL is not None, "set CHANNEL from the inspection addendum"; CHANNEL = int(CHANNEL); N = int(os.environ.get("NPAT", 120))
files = sorted(glob.glob(os.path.join(ROOT, "**", "volume_*_slice_*.h5"), recursive=True))
by = {}
for f in files:
    m = re.search(r"volume_(\d+)_slice_(\d+)\.h5$", f); by.setdefault(int(m.group(1)), {})[int(m.group(2))] = f
def load_slice(f):
    with h5py.File(f, "r") as h: return np.asarray(h["image"][..., CHANNEL], dtype=np.float32)   # 'image' only; 'mask' is never read
def vol(v, zs): return {z: load_slice(by[v][z]) for z in zs if z in by[v]}
def fp(a, k=32):  # 32 x 32 block-mean fingerprint of a 240 x 240 slice, z-scored (invariant to affine intensity scaling)
    H, W = a.shape; a = a[:H // k * k, :W // k * k].reshape(k, H // k, k, W // k).mean((1, 3)); return (a - a.mean()) / (a.std() + 1e-8)
def msd_fingerprints():
    m = np.load("data/brats_raw/msd_fp_z80.npz"); return {str(n): m["fp"][i, 3] for i, n in enumerate(m["names"])}   # T2 channel (index 3), slice 80, z-scored 32 x 32 block means (data/brats_raw/msd_fp.py)
def overlap(case, msd, thr=0.99):
    if 80 not in by[case]: return None
    a = fp(np.rot90(load_slice(by[case][80]), 2)); best = max(msd, key=lambda s: float((a * msd[s]).mean())); r = float((a * msd[best]).mean()); return (best, r) if r >= thr else None
if __name__ == "__main__":
    msd = msd_fingerprints(); keep, dropped = [], {}
    for c in sorted(by):
        o = overlap(c, msd)
        (dropped.__setitem__(c, o) if o else keep.append(c))
    rng = np.random.default_rng(2026); pick = [keep[i] for i in rng.permutation(len(keep))[:N]]; n = len(pick)
    cut = {"train": pick[:int(.6 * n)], "val": pick[int(.6 * n):int(.8 * n)], "test": pick[int(.8 * n):]}
    os.makedirs("data/splits", exist_ok=True); man = {}
    for k, cs in cut.items():
        imgs, pid, sl = [], [], []
        for c in cs:
            v = vol(c, range(155)); full = np.stack([v[z] for z in sorted(v)]); nz = full[full != full.min()]; hi = np.percentile(nz, 99.5)
            for z in range(40, 101, 5):
                if z not in v: continue
                s = np.rot90(np.clip(np.round((v[z] - full.min()) / (hi - full.min()) * 255), 0, 255).astype(np.uint8), 2); H, W = s.shape; a, b = (H - 128) // 2, (W - 128) // 2
                imgs.append(s[a:a + 128, b:b + 128]); pid.append(f"BraTS20_{c:03d}"); sl.append(z)
        p = f"data/splits/bratst2_{k}.npz"; np.savez_compressed(p, images=np.array(imgs), subject=np.array(pid), slice=np.array(sl))
        man[k] = dict(n_images=len(imgs), n_patients=len(set(pid)), patients=sorted(set(pid)), sha256=hashlib.sha256(open(p, "rb").read()).hexdigest())
    assert not any(set(man[a]["patients"]) & set(man[b]["patients"]) for a, b in (("train", "val"), ("train", "test"), ("val", "test")))
    man["overlap_excluded"] = {f"BraTS20_{c:03d}": o for c, o in dropped.items()}; man["n_cases_total"] = len(by); man["n_cases_after_exclusion"] = len(keep); man["channel"] = CHANNEL
    man["source"] = "Kaggle awsaf49/brats2020-training-data (BraTS 2020 training, CC0); T2 channel; masks unused; no interpolation"
    json.dump(man, open("data/splits/bratst2_split_manifest.json", "w"), indent=1); print(json.dumps({k: (v if not isinstance(v, dict) else {a: b for a, b in v.items() if a != "patients"}) for k, v in man.items() if k != "overlap_excluded"}, indent=1))
