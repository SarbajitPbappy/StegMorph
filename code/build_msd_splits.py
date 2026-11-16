"""V3.3: subject-disjoint slice sets from the Medical Segmentation Decathlon brain-tumour task (Task01_BrainTumour, imagesTr; CC BY-SA 4.0; NIfTI, not JPEG-derived).
Same preprocessing as IXI T2 (code/build_ixi_splits.py): channel 3 = T2-weighted (channel order FLAIR, T1w, T1gd, T2w), per volume scaled by the 99.5th percentile of non-zero voxels to 0-255,
axial slices 40..100 step 5, centre 128x128 crop, split by SUBJECT 70/15/15 with seed 2026.  Outputs data/splits/msdt2_{train,val,test}.npz and data/splits/msdt2_split_manifest.json (sha256).
Run from the project root after extracting data/msd_raw/Task01_BrainTumour/imagesTr."""
import glob, os, json, hashlib, numpy as np, nibabel as nib
R = "data/msd_raw/Task01_BrainTumour/imagesTr/"
fs = sorted(f for f in glob.glob(R + "BRATS_*.nii.gz") if not os.path.basename(f).startswith("._")); os.makedirs("data/splits", exist_ok=True)
subs = [os.path.basename(f)[:-7] for f in fs]; rng = np.random.default_rng(2026); perm = rng.permutation(len(subs)); n = len(subs)
cut = {"train": [subs[i] for i in perm[:int(.7 * n)]], "val": [subs[i] for i in perm[int(.7 * n):int(.85 * n)]], "test": [subs[i] for i in perm[int(.85 * n):]]}
where = {s: k for k, v in cut.items() for s in v}; buf = {k: dict(images=[], subject=[], slice=[]) for k in cut}
for s, f in zip(subs, fs):
    v = np.asarray(nib.load(f).dataobj)[..., 3].astype(np.float32); nz = v[v > 0]; hi = np.percentile(nz, 99.5)
    for z in range(40, min(101, v.shape[2]), 5):
        sl = np.clip(np.round(v[:, :, z] / hi * 255), 0, 255).astype(np.uint8); H, W = sl.shape; a, b = (H - 128) // 2, (W - 128) // 2; sl = sl[a:a + 128, b:b + 128]
        buf[where[s]]["images"].append(sl); buf[where[s]]["subject"].append(s); buf[where[s]]["slice"].append(z)
man = {}
for k, b in buf.items():
    p = f"data/splits/msdt2_{k}.npz"; np.savez_compressed(p, images=np.array(b["images"]), subject=np.array(b["subject"]), slice=np.array(b["slice"]))
    man[k] = dict(n_images=len(b["images"]), n_subjects=len(set(b["subject"])), sha256=hashlib.sha256(open(p, "rb").read()).hexdigest())
assert not (set(buf["train"]["subject"]) & set(buf["test"]["subject"])) and not (set(buf["train"]["subject"]) & set(buf["val"]["subject"])) and not (set(buf["val"]["subject"]) & set(buf["test"]["subject"]))
man["source"] = "Medical Segmentation Decathlon Task01_BrainTumour (imagesTr), CC BY-SA 4.0, https://registry.opendata.aws/msd/ ; T2-weighted channel; skull-stripped, co-registered, resampled to 1 mm (as distributed)"
json.dump(man, open("data/splits/msdt2_split_manifest.json", "w"), indent=1); print(json.dumps(man, indent=1))
