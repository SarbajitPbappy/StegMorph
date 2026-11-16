# E5: second MRI source (brain tumor mirror) + cross-dataset. EXPLORATORY, NOT CLAIMABLE.
Pre-registered in state/CLAIMS.md (2026-11-10) before the run. StegMorph-recon GA vs RAND, payload 0.005/0.01/0.02 raw bpp, seeds 0,1,2. Sets: T_raw = tumor-set native-pixel 128x128 crops, NO added noise (435 crops/seed, 130-131 test pairs, split grouped by source image); T_noise = same + Gaussian sigma 1.5; A_noise = Alzheimer mirror + noise (N=400, 120 test pairs). Detector A = SRM-lite+LR; B = SPAM-style+HGB. Code: code/exp5.py, exp5_psnr.py; data: results/e5/e5_all_seeds.json, e5_psnr.json.
Provenance caveat: the tumor mirror's pre-processing history (JPEG origin, resizing) is unknown; images are native 8-bit PNG of varying size, so these are real covers without synthetic noise, but not guaranteed never JPEG-compressed.

## GA - RAND AUC difference (mean of 3 seeds; 90% CI from per-seed bootstrap SEs; margin +/-0.02)
| set | det | 0.005 | 0.01 | 0.02 |
|---|---|---|---|---|
| T_raw | A | -.002 [-.015,.010] EQUIV | +.005 [-.005,.015] EQUIV | .000 [-.005,.005] EQUIV |
| T_raw | B | +.004 [-.018,.027] inconcl. | +.013 [-.006,.033] inconcl. | .000 [-.017,.016] EQUIV |
| T_noise | A | -.004 [-.017,.010] EQUIV | -.004 [-.020,.012] inconcl. | +.001 [-.016,.017] EQUIV |
| T_noise | B | +.035 [.006,.065] GA worse | +.049 [.018,.080] GA worse | +.005 [-.025,.036] inconcl. |
| A_noise | A | +.028 [.013,.042] GA worse | +.060 [.045,.076] GA worse | +.023 [.014,.033] GA worse |
| A_noise | B | +.085 [.062,.107] GA worse | +.091 [.074,.108] GA worse | +.050 [.039,.061] GA worse |
(AUC levels: T_raw A .79/.89/.96, B .63/.71/.79 => not at ceiling; no GA > RAND security benefit in any cell.)
PSNR on T_raw (150 crops, seed 0): GA 67.6/65.0/62.1 dB vs RAND 64.5/62.0/59.3 dB (+3 dB). GA low-branch share .94-.96 vs RAND .89.
Reading (exploratory): GA's PSNR advantage never translates into a security advantage. On real (un-noised) tumor-set covers the two are statistically equivalent under detector A at all payloads and not distinguishable under detector B; on the Alzheimer set with synthetic noise the GA is significantly MORE detectable under both detectors. The size of the harm is dataset/cover-dependent (A-noise covers have large smooth dark backgrounds where the GA concentrates embedding). In no tested cell is the GA less detectable.

## Cross-dataset transfer (noise covers; mean AUC over seeds 0,1,2; per-seed values in the JSON)
| det | scheme | bpp | A->T | T->T (in-domain) | T->A | A->A (in-domain) |
|---|---|---|---|---|---|---|
| A | GA | 0.005 / 0.01 / 0.02 | .555 / .566 / .607 | .593 / .672 / .808 | .606 / .716 / .845 | .676 / .812 / .960 |
| A | RAND | 0.005 / 0.01 / 0.02 | .556 / .557 / .569 | .597 / .676 / .807 | .597 / .658 / .807 | .648 / .751 / .936 |
| B | GA | 0.005 / 0.01 / 0.02 | .510 / .508 / .536 | .524 / .559 / .584 | .575 / .742 / .919 | .667 / .812 / .964 |
| B | RAND | 0.005 / 0.01 / 0.02 | .498 / .525 / .540 | .489 / .510 / .579 | .529 / .611 / .840 | .583 / .721 / .914 |
Reading (descriptive only): a detector trained on the Alzheimer covers is close to chance on tumor covers (A->T .51-.61), clearly worse than in-domain tumor training only at 0.02 bpp with detector A (.61 vs .81); a detector trained on the tumor covers keeps most of its power on Alzheimer covers at 0.02 bpp (T->A .85-.92 vs in-domain .96) but loses much at lower payloads. So transfer is asymmetric. Control note: the Alzheimer training split (280 pairs) is smaller than the tumor split (~304), so the weaker tumor in-domain detectors are not a training-size artefact. The generic fact that detectors transfer badly across datasets is already reported (SADBench, natural images; MI-STEG used a mismatch MRI test set for adaptive schemes).
