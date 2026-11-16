# E8 (2026-11-10 scheduled run): StegMorph-recon variants vs idealised HILL baseline
Code: code/exp8.py (derived from exp6b.py); data: Alzheimer mirror @a1c2ca6 raw covers (no noise), N=400, 70/30 split (exact-hash grouping, effectively image-level), raw 0.02 bpp (embedded bits = 3*(32+327)), 3 seeds, 500-resample bootstrap over test images. Detector A = SRM-lite+LR, B = SPAM+HGB.
HILL_SIM = embed.hill_simulate (+-1 entropy-matched simulator, NOT real STC, no extraction) at the same embedded bpp (0.0657).
| Detector | RAND | GREEDY_TEX | HILL_SIM |
| A, seeds 0/1/2 | 1.000 | .788/.792/.801 | .552/.549/.548 |
| B, seeds 0/1/2 | 1.000 | .713/.709/.681 | .485/.485/.562 |
PSNR (dB): RAND 54.5, GREEDY_TEX 62.7, HILL_SIM 68.7-68.8. All CIs for diff vs RAND exclude 0 (see JSONs).
Reading: pre-registered expectation confirmed. Idealised adaptive baseline is near chance under both detectors; texture-aware StegMorph-recon is clearly less detectable than random but far above HILL_SIM. Contribution is limited to "fixing the fitness of GA-style LSB/PVD schemes", not a competitive secure scheme. HILL_SIM is idealised (an upper bound for the baseline).
Not done: SCA-lite (E7b) and E7b numbers have NO code/result files in this folder (only CLAIMS.md text) => UNVERIFIED per rule 1; E8 run with detectors A and B only; T_raw not run; CNN untested; seeds are not independent (same image pool structure).
