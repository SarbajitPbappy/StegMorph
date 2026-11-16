"""IXI T2 at 256x256 (full in-plane slice, 7 axial slices per volume: z = 40..100 step 10), same subject split as the 128x128 set (seed 2026). Output data/splits/ixi256_{train,val,test}.npz"""
import glob, json, numpy as np, nibabel as nib
R = "data/raw/IXI_T2/datasets/thintrnvn/ixi-dataset-t2/versions/1/"; fs = sorted(glob.glob(R + "*/*.nii*"))
info = [(f.split("/versions/1/")[1].split("-")[0], f.split("/versions/1/")[1].split("-")[1], f) for f in fs]; subs = sorted({s for s, _, _ in info}); rng = np.random.default_rng(2026); perm = rng.permutation(len(subs)); n = len(subs)
cut = {"train": [subs[i] for i in perm[:int(.7 * n)]], "val": [subs[i] for i in perm[int(.7 * n):int(.85 * n)]], "test": [subs[i] for i in perm[int(.85 * n):]]}; where = {s: k for k, v in cut.items() for s in v}
buf = {k: dict(images=[], subject=[], site=[], slice=[]) for k in cut}
for s, site, f in info:
    v = np.asarray(nib.load(f).dataobj).astype(np.float32); hi = np.percentile(v[v > 0], 99.5)
    for z in range(40, min(101, v.shape[2]), 10):
        b = buf[where[s]]; b["images"].append(np.clip(np.round(v[:, :, z] / hi * 255), 0, 255).astype(np.uint8)); b["subject"].append(s); b["site"].append(site); b["slice"].append(z)
for k, b in buf.items(): np.savez_compressed(f"data/splits/ixi256_{k}.npz", images=np.array(b["images"]), subject=np.array(b["subject"]), site=np.array(b["site"]), slice=np.array(b["slice"])); print(k, np.array(b["images"]).shape, len(set(b["subject"])))
