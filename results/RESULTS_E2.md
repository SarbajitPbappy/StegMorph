# E2 / E2b: C1 test (GA vs random pair selection) with StegMorph-recon. EXPLORATORY, NOT CLAIMABLE.
Method: StegMorph-recon (reconstruction, assumptions A1-A5 in state/DECISIONS.md; NOT the original code). Alzheimer mirror (JPEG-decoded 128x128). SRM-lite + logistic regression. Seeds 0,1,2. Split by exact-hash group (image-level). Pre-registrations and amendments: state/CLAIMS.md.
Embedded bits = 3 x (32 header + payload) because of triplication; payload bpp below is raw (before triplication).

## E2 (raw covers, N=600/seed, 0.02-0.2 raw bpp)
All schemes (GA, RAND, GREEDY) AUC = 1.0 at every payload and seed => C1 INCONCLUSIVE (detector ceiling, not equivalence). GA still reduces distortion (e.g. 0.02 bpp: PSNR 59.6 GA vs 54.6 RAND vs 62.8 GREEDY).

## E2b (escalation 1: raw MRI + Gaussian noise sigma=1.5, SYNTHETIC degradation; N=600/seed; payload 0.005-0.05 raw bpp)
AUC per seed (0,1,2); diff = GA - RAND with paired-bootstrap 95% CI (per seed)
| raw bpp | GA | RAND | GREEDY | diff GA-RAND (CI) | PSNR GA / RAND |
|---|---|---|---|---|---|
| 0.005 | .691 .696 .674 | .649 .649 .641 | .776 .762 .778 | +.042 (.017,.066); +.047 (.019,.072); +.033 (.011,.055) | 67.2 / 60.1 |
| 0.01 | .822 .830 .811 | .770 .757 .765 | .912 .911 .916 | +.052 (.027,.079); +.073 (.045,.100); +.045 (.017,.074) | 63.6 / 57.3 |
| 0.02 | .970 .978 .960 | .950 .961 .946 | .995 .993 .997 | +.019 (.007,.034); +.017 (.003,.031); +.014 (-.001,.028) | 59.6 / 54.6 |
| 0.05 | 1.0 | 1.0 | 1.0 | 0 | 54.1 / 50.8 |
Reading (exploratory): on noise-augmented covers, GA-selected pairs are MORE detectable than random-selected pairs at the three lowest payloads, in all 3 seeds, even though GA gives 3-7 dB higher PSNR. The more strongly the selection minimises distortion (GREEDY), the more detectable. Low-branch share of selected pairs: GA ~0.93 at 0.005 bpp (RAND 0.74), i.e. selection concentrates embedding in smooth dark background. This is the opposite of a security benefit, i.e. supports the direction "GA gives no benefit / worse" (C1 negative-outcome branch), but equivalence (TOST) is rejected rather than shown: GA is worse by more than the +/-0.02 margin at 0.005-0.01 bpp.
Why it is not claimable yet: (1) StegMorph-recon is not the original; (2) covers are noise-augmented JPEG-decoded slices, 1 dataset, image-level split (leakage-prone), 1 detector family (no CNN); (3) Novelty Gate unrun (state/LEDGER.md: 4 queries, 0 full-text reads); (4) side-information key assumption (A5).
Files: code/stegmorph_recon.py, exp2*.py; per-seed JSON in results/e2, e2b, e2diag.
