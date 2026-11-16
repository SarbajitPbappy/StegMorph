"""Subject-disjoint IXI T1 slice sets (replication collection; NIfTI, not JPEG-derived). IXI T1 volumes are 256x256x150 with axes (P,S,R); axial slices are taken along the S axis (13 slices per volume, indices 80..200 step 10), centre-cropped to 128x128 (P 64:192, R centred; the R extent is 130-150 voxels) and scaled per volume by the 99.5th percentile to 0-255 as for T2. Subject split 70/15/15 with seed 2026. Output data/splits/ixit1_{train,val,test}.npz"""
import glob, os, json, hashlib, numpy as np, nibabel as nib
fs = sorted(glob.glob("data/raw/IXI_T1/vol/*.nii*")); info = [(os.path.basename(f).split("-")[0], os.path.basename(f).split("-")[1], f) for f in fs]
subs = sorted({s for s, _, _ in info}); rng = np.random.default_rng(2026); perm = rng.permutation(len(subs)); n = len(subs)
cut = {"train": [subs[i] for i in perm[:int(.7 * n)]], "val": [subs[i] for i in perm[int(.7 * n):int(.85 * n)]], "test": [subs[i] for i in perm[int(.85 * n):]]}; where = {s: k for k, v in cut.items() for s in v}
buf = {k: dict(images=[], subject=[], site=[], slice=[]) for k in cut}
for s, site, f in info:
    v = np.asarray(nib.load(f).dataobj).astype(np.float32); hi = np.percentile(v[v > 0], 99.5)
    for y in range(80, 201, 10):
        sl = np.clip(np.round(v[:, y, :] / hi * 255), 0, 255).astype(np.uint8)[64:192, (v.shape[2] - 128) // 2:(v.shape[2] - 128) // 2 + 128]; b = buf[where[s]]; b["images"].append(sl); b["subject"].append(s); b["site"].append(site); b["slice"].append(y)
man = {}
for k, b in buf.items():
    p = f"data/splits/ixit1_{k}.npz"; np.savez_compressed(p, images=np.array(b["images"]), subject=np.array(b["subject"]), site=np.array(b["site"]), slice=np.array(b["slice"]))
    man[k] = dict(n_images=len(b["images"]), n_subjects=len(set(b["subject"])), sha256=hashlib.sha256(open(p, "rb").read()).hexdigest(), sites={t: b["site"].count(t) for t in set(b["site"])})
assert not (set(buf["train"]["subject"]) & set(buf["test"]["subject"])) and not (set(buf["train"]["subject"]) & set(buf["val"]["subject"])) and not (set(buf["val"]["subject"]) & set(buf["test"]["subject"]))
json.dump(man, open("data/splits/ixit1_split_manifest.json", "w"), indent=1); print(json.dumps(man, indent=1))
