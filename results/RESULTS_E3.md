# E3: C2 branch ablation + C4 within-dataset transfer (StegMorph-recon). EXPLORATORY, NOT CLAIMABLE.
Setup as pre-registered in state/CLAIMS.md (2026-11-10): Alzheimer mirror (JPEG-decoded 128x128) + Gaussian noise sigma 1.5 (SYNTHETIC), N=300/seed (3 seeds; 0/3/3 images skipped for capacity), n_test=90 pairs/seed, image-level split, SRM-lite + logistic regression, raw payload 0.005-0.05 bpp. Code: code/exp3.py. Per-seed data: results/e3/e3_all_seeds.json.

## C2: branch ablation (AUC per seed 0,1,2)
| raw bpp | RAND_LOW (2-LSB branch only) | RAND_PVD (PVD branch only) | LOW - PVD (per-seed diff; 95% CI) | PSNR LOW / PVD |
|---|---|---|---|---|
| 0.005 | .685 .715 .702 | .762 .727 .737 | -.077 (-.127,-.023); -.012 (-.060,.037); -.034 (-.092,.020) | 68.4 / 56.1 |
| 0.01 | .864 .874 .870 | .886 .835 .857 | -.022; +.039; +.013 (all CIs include 0) | 65.9 / 53.6 |
| 0.02 | .990 .992 .987 | .974 .958 .967 | +.015 (-.006,.034); +.034 (.010,.056); +.020 (-.005,.045) | 63.1 / 50.8 |
| 0.05 | 1.0 | 1.0 / .9998 / .999 | ~0 | 59.3 / 47.0 |
Reading: the pre-registered directional hypothesis H2 (LOW branch more detectable than PVD at equal embedded bits) is NOT supported. Sign flips with payload: PVD is more detectable at the lowest payload (all 3 seeds, 1 CI excludes 0), LOW is slightly more detectable at 0.02 (all 3 seeds positive, 1 CI excludes 0), tie at 0.05. No single branch dominates detection; the LOW branch gives 7-9 dB higher PSNR at similar detectability. Power is low (n_test=90).
GA_ALL (reference): AUC .687-.705 (0.005), .797-.824 (0.01), .950-.972 (0.02); low-branch share 0.93 -> 0.79 as payload grows. RAND_ALL: .644-.660, .752-.783, .941-.949.

## C4 (within one dataset only; cross-DATASET not testable)
Cross-payload (mean AUC of 3 seeds; train row payload, test column payload): detectors transfer almost without loss across payloads for all schemes, e.g. RAND_ALL trained at 0.005 tests .65/.75/.91/1.0 at 0.005/0.01/0.02/0.05 vs trained-in-place .65/.77/.945/1.0. A detector trained on a low payload loses at most ~0.03 AUC at 0.02 (RAND_ALL .91 vs .945) and nothing at 0.05.
Cross-method (mean AUC, train scheme -> test scheme at the same payload):
| bpp | LOW->PVD | PVD->LOW | ALL->LOW | ALL->PVD | GA->PVD | LOW->GA |
|---|---|---|---|---|---|---|
| 0.005 | .52 | .52 | .66 | .67 | .56 | .69 |
| 0.01 | .52 | .52 | .82 | .75 | .60 | .81 |
| 0.02 | .54 | .54 | .98 | .85 | .70 | .96 |
| 0.05 | .62 | .57 | 1.0 | .99 | .94 | 1.0 |
Reading (exploratory): a detector trained on one branch's stego is near chance on the other branch's stego (.52-.62 even where in-place AUC is .86-1.0), while a detector trained on the mixed scheme (RAND_ALL) detects both, and GA/LOW-trained detectors detect each other (GA is mostly LOW-branch). So the two branches leave different traces; cross-method transfer fails across branch type but not across payload or selection strategy. Caveats: synthetic noise covers, JPEG-decoded single dataset, reconstruction not original, SRM-lite+LR only, n_test=90, no CIs on transfer cells.
Gate note: generic "detectors fail to transfer across datasets/unseen methods" is already reported on natural images with learned methods (SADBench, arXiv 2605.05789, partial read). The branch-specific pattern for classical LSB/PVD on MRI is not yet gate-checked.
