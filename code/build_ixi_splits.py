"""Build subject-disjoint IXI T2 slice sets (uint8, native resolution, centre 128x128 crop of axial slices).
Per volume: scale by its 99.5th percentile to 0-255 (non-JPEG), slices 40..100 step 5. Split by SUBJECT 70/15/15 (seed 2026).
Outputs data/splits/ixi_{train,val,test}.npz (images, subject, site, slice) + data/splits/ixi_split_manifest.json (sha256)."""
import glob, os, json, hashlib, numpy as np, nibabel as nib
R = "data/raw/IXI_T2/datasets/thintrnvn/ixi-dataset-t2/versions/1/"
fs = sorted(glob.glob(R + "*/*.nii*")); os.makedirs("data/splits", exist_ok=True)
info = [(f.split("/versions/1/")[1].split("-")[0], f.split("/versions/1/")[1].split("-")[1], f) for f in fs]
subs = sorted({s for s, _, _ in info}); rng = np.random.default_rng(2026); perm = rng.permutation(len(subs))
n = len(subs); cut = {"train": subs and [subs[i] for i in perm[:int(.7*n)]], "val": [subs[i] for i in perm[int(.7*n):int(.85*n)]], "test": [subs[i] for i in perm[int(.85*n):]]}
where = {s: k for k, v in cut.items() for s in v}
buf = {k: dict(images=[], subject=[], site=[], slice=[]) for k in cut}
for s, site, f in info:
    v = np.asarray(nib.load(f).dataobj).astype(np.float32); hi = np.percentile(v[v > 0], 99.5)
    for z in range(40, min(101, v.shape[2]), 5):
        sl = np.clip(np.round(v[:, :, z] / hi * 255), 0, 255).astype(np.uint8)[64:192, 64:192]
        b = buf[where[s]]; b["images"].append(sl); b["subject"].append(s); b["site"].append(site); b["slice"].append(z)
man = {}
for k, b in buf.items():
    p = f"data/splits/ixi_{k}.npz"; np.savez_compressed(p, images=np.array(b["images"]), subject=np.array(b["subject"]), site=np.array(b["site"]), slice=np.array(b["slice"]))
    man[k] = dict(n_images=len(b["images"]), n_subjects=len(set(b["subject"])), sha256=hashlib.sha256(open(p, "rb").read()).hexdigest(), sites={t: b["site"].count(t) for t in set(b["site"])})
assert not (set(buf["train"]["subject"]) & set(buf["test"]["subject"])) and not (set(buf["train"]["subject"]) & set(buf["val"]["subject"]))
json.dump(man, open("data/splits/ixi_split_manifest.json", "w"), indent=1); print(json.dumps(man, indent=1))
