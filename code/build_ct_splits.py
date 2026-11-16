"""CT second modality: OrganAMNIST (MedMNIST+, 128 px, 8-bit) from the LiTS CT scans. MedMNIST's official split is by CT scan (115 train, 16 validation, 70 test scans), so the splits are scan-disjoint; scan identifiers are not distributed, so every image is its own cluster in the bootstrap (intervals are optimistic).
Fixed random subsample (seed 2026): 5000 train, 600 val, 1500 test images. Output data/splits/ct_{train,val,test}.npz"""
import numpy as np
d = np.load("data/raw/medmnist/organamnist_128.npz"); r = np.random.default_rng(2026)
for split, n in (("train", 5000), ("val", 600), ("test", 1500)):
    X = d[f"{split}_images"]; i = np.sort(r.permutation(len(X))[:n]); im = X[i].astype(np.uint8)
    np.savez_compressed(f"data/splits/ct_{split}.npz", images=im, subject=np.array([f"{split}{j}" for j in i]), site=np.array(["LiTS"] * n), slice=i); print(split, im.shape, im.dtype, im.mean())
