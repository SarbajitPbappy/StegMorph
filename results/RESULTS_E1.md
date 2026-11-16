# E1 exploratory results (2026-11-10 Dhaka). NOT CLAIMABLE: Novelty Gate not run; not StegMorph; JPEG-decoded data; no subject IDs.
Setup: Alzheimer mirror (128x128 JPEG-decoded), N=800 images per seed, 70/30 split (exact-hash groups; every image is its own group in these samples, so this is effectively an image-level split), SRM-lite + logistic regression, 3 seeds (0,1,2). Code: code/exp1.py. Per-seed rows with bootstrap CIs: results/e1/.
AUC mean over 3 seeds (per-seed range in JSON); PSNR dB; SSIM; pixel change rate
| scheme | bpp | AUC | P_E | TPR@1%FPR | PSNR | SSIM |
|---|---|---|---|---|---|---|
| LSB seq | 0.05-0.4 | 1.000 | 0.000 | 1.00 | 64.2-55.1 | 0.9991-0.9940 |
| LSB keyed | 0.05-0.4 | 1.000 | 0.000 | 1.00 | 64.2-55.1 | 0.9998-0.9968 |
| PVD-6 stand-in | 0.05 | 0.746 | 0.304 | 0.10 | 52.3 | 0.99987 |
| PVD-6 | 0.1 | 0.920 | 0.154 | 0.37 | 49.3 | 0.99971 |
| PVD-6 | 0.2 | 0.997 | 0.023 | 0.95 | 46.5 | 0.99939 |
| PVD-6 | 0.4 | 1.000 | 0.000 | 1.00 | 43.8 | 0.99872 |
| HILL-style sim | 0.05 | 0.528 | 0.459 | 0.01 | 70.2 | 1.00000 |
| HILL-style sim | 0.1 | 0.583 | 0.422 | 0.04 | 66.6 | 0.99999 |
| HILL-style sim | 0.2 | 0.742 | 0.313 | 0.08 | 63.0 | 0.99997 |
| HILL-style sim | 0.4 | 0.974 | 0.081 | 0.61 | 59.1 | 0.99991 |
Observations (exploratory): (1) LSB is detected perfectly even at 0.05 bpp, which is likely an artifact of JPEG-decoded cover statistics and must be rechecked on non-JPEG MRI. (2) Across schemes, higher PSNR does not mean lower detectability: LSB has higher PSNR than PVD-6 at the same payload yet is detected more. Spearman(PSNR, AUC) over 16 cells = -0.24 (ns); over the 8 PVD-6/HILL cells = -0.93; Spearman(SSIM, AUC) = -0.84. These are heavily tied (LSB all at AUC 1.0), have no CIs, and are within-this-setup only. (3) Run 1 (results/e1_run1_VOID) used a broken group split and is void.
Not tested: C1 (needs StegMorph GA), C4 (one dataset only), C5 leakage (no IDs), CNN detectors, statistical detectors on real data.
