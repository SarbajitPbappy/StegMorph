# E4: GA vs random under TWO detector families (C1 robustness) + C3 rank test. EXPLORATORY, NOT CLAIMABLE.
Pre-registered in state/CLAIMS.md (2026-11-10) before the run. StegMorph-recon (reconstruction), Alzheimer mirror (JPEG-decoded 128x128) + Gaussian noise sigma 1.5 (SYNTHETIC), N=600/seed (0 skipped), n_test=180 pairs/seed, 3 seeds, image-level split. Detector A = SRM-lite + logistic (same as E2b); detector B = SPAM-style second-order Markov features (T=3, 686-d) + HistGradientBoosting. Code: code/exp4.py; data: results/e4/e4_all_seeds.json.

AUC GA - RAND (paired bootstrap 95% CI, 500 resamples), per seed 0,1,2
| raw bpp | detector A | detector B | PSNR GA / RAND |
|---|---|---|---|
| 0.005 | +.042 (.017,.064); +.047 (.020,.073); +.033 (.009,.055) | +.080 (.042,.117); +.097 (.060,.135); +.072 (.036,.107) | 67.2 / 60.0 |
| 0.01 | +.052 (.026,.079); +.073 (.045,.099); +.045 (.015,.077) | +.084 (.053,.111); +.075 (.047,.105); +.077 (.046,.103) | 63.5 / 57.3 |
| 0.02 | +.019 (.008,.033); +.017 (.004,.031); +.014 (-.001,.029) | +.036 (.021,.050); +.035 (.019,.051); +.032 (.017,.047) | 59.5 / 54.6 |
Pre-registered replication criterion (detector B CI > 0 in >= 2 of 3 seeds at 0.005 and 0.01): MET (in 3/3 seeds, and also at 0.02). Detector A reproduces E2b within noise (e.g. 0.005: GA .691 vs RAND .649 here vs .691/.649 in E2b seed 0). Detector B finds an even larger gap (GA .67-.69 vs RAND .57-.61 at 0.005 bpp).
Reading (exploratory): on noise-augmented covers, GA-selected (low-distortion) pair selection is more detectable than random selection at every tested low payload, by two unrelated detector families, with 3-7 dB higher PSNR. Equivalence (+/-0.02) is rejected for B at all payloads and for A at 0.005-0.01. This is the direction "GA gives no security benefit; it is worse", with PSNR/SSIM pointing the opposite way.
Limits: reconstruction not original code; synthetic noise covers (raw covers saturate at AUC 1.0); JPEG-decoded single dataset; image-level split (no subject IDs); no CNN detector; n_test=180.

## C3 rank test (E3 cells, scheme ranking by PSNR vs by AUC within each payload x seed group; 0.05 bpp excluded, AUC saturated)
Spearman(PSNR, AUC) over the 4 schemes (RAND_ALL, RAND_LOW, RAND_PVD, GA_ALL), 9 groups: values -0.4 .. +0.8, mean +0.13, bootstrap 95% CI of the mean [-0.13, 0.40]. Note the sign: a positive value means higher PSNR goes with MORE detection. Interpretation: PSNR does not predict the security ranking (no reliable relation in either direction); combined with E1 (LSB higher PSNR than PVD yet more detectable) and E4 (GA +3..7 dB PSNR yet more detectable than random), quality metrics are not a security proxy in this setting. Low power (4 schemes per group); exploratory. Gate: the generic claim is already reported on natural images (SADBench arXiv 2605.05789: StegFormer/DeepMIH high fidelity yet F1 > 0.98), so only an MRI/classical-scheme version could be open.
