# E6: corrected C1 re-test with operator-mix control. EXPLORATORY, NOT CLAIMABLE.
Pre-registration: state/CLAIMS.md (2026-11-10 10:10). Code: code/exp6.py. Per-seed JSON: results/e6/.
Fixes vs E4/E5 (VERIFICATION_REPORT): grouped 5-fold CV, every image tested once out-of-fold (scores rank-normalised within fold); Alzheimer groups = complete-linkage clusters of 16x16 slices (near-duplicate PROXY; mean cluster 4.6, max 22; no true subject IDs); tumor groups = source file; bootstrap over groups (500). Two stego-randomisation replicates (seeds 0,1) (the seed also changes crop positions and the Alzheimer permutation, so pools and cluster structure differ slightly: 133 vs 127 clusters; replicates share the same source images, so NOT independent): values below are means of the 2 replicates; CI endpoints are averaged 90% CIs (approximate, optimistic).
Schemes: RAND; GA; GA_RANDMIX = GA restricted to RAND's per-branch bit quotas; RAND_GAMIX = random restricted to GA's per-branch quotas. Sets: T_raw (tumor crops, native pixels, ~430 crops), A_noise (Alzheimer + synthetic Gaussian noise sigma 1.5, 600 images). Detector A = SRM-lite+LR; B = SPAM-style+HGB. Payload = raw bpp (embedded = 3x + header).
Contrasts (AUC difference, mean over replicates, approx 90% CI): P1 = GA-RAND; P2 = GA_RANDMIX-RAND (position choice only, mix fixed); P3 = GA-RAND_GAMIX (GA vs random with the SAME mix).
| set | det | raw bpp | AUC RAND | AUC GA | AUC GA_RANDMIX | AUC RAND_GAMIX | P1 | P2 | P3 |
|---|---|---|---|---|---|---|---|---|---|
| T_raw | A | 0.005 | 0.781 | 0.775 | 0.783 | 0.767 | -0.006 (-0.019,+0.009) | +0.002 (-0.009,+0.014) | +0.008 (-0.002,+0.020) |
| T_raw | B | 0.005 | 0.651 | 0.646 | 0.639 | 0.646 | -0.005 (-0.024,+0.015) | -0.012 (-0.033,+0.009) | +0.000 (-0.020,+0.021) |
| T_raw | A | 0.01 | 0.867 | 0.869 | 0.875 | 0.869 | +0.002 (-0.008,+0.013) | +0.008 (-0.001,+0.016) | +0.000 (-0.009,+0.010) |
| T_raw | B | 0.01 | 0.711 | 0.720 | 0.716 | 0.742 | +0.009 (-0.010,+0.028) | +0.004 (-0.013,+0.022) | -0.022 (-0.039,-0.004) |
| T_raw | A | 0.02 | 0.936 | 0.938 | 0.936 | 0.933 | +0.001 (-0.004,+0.007) | -0.000 (-0.005,+0.005) | +0.005 (+0.000,+0.009) |
| T_raw | B | 0.02 | 0.802 | 0.814 | 0.819 | 0.822 | +0.011 (-0.004,+0.027) | +0.017 (+0.001,+0.032) | -0.009 (-0.024,+0.006) |
| A_noise | A | 0.005 | 0.664 | 0.686 | 0.673 | 0.675 | +0.021 (+0.009,+0.034) | +0.009 (-0.001,+0.019) | +0.011 (-0.000,+0.022) |
| A_noise | B | 0.005 | 0.589 | 0.664 | 0.624 | 0.660 | +0.075 (+0.060,+0.091) | +0.035 (+0.018,+0.052) | +0.004 (-0.011,+0.019) |
| A_noise | A | 0.01 | 0.771 | 0.820 | 0.771 | 0.817 | +0.049 (+0.036,+0.064) | +0.001 (-0.012,+0.014) | +0.003 (-0.008,+0.014) |
| A_noise | B | 0.01 | 0.729 | 0.820 | 0.743 | 0.818 | +0.090 (+0.077,+0.103) | +0.014 (-0.000,+0.028) | +0.002 (-0.010,+0.015) |
| A_noise | A | 0.02 | 0.945 | 0.969 | 0.950 | 0.969 | +0.025 (+0.018,+0.031) | +0.006 (-0.002,+0.013) | +0.000 (-0.005,+0.005) |
| A_noise | B | 0.02 | 0.924 | 0.970 | 0.933 | 0.969 | +0.045 (+0.037,+0.054) | +0.009 (+0.001,+0.017) | +0.001 (-0.004,+0.006) |

Operator mix (seed 0, 0.005 bpp): T_raw low-branch share RAND .84, GA .94; A_noise RAND .74, GA .94. GA also touches more pairs (A_noise 164 vs 141) but MSE is lower (0.0125 vs 0.071).
Reading (exploratory):
1. A_noise: the GA's extra detectability (P1 +0.02..+0.09) is largely, not fully, reproduced by a RANDOM selector that copies the GA's branch-bit mix (P3 = +0.00..+0.01; averaged CIs include 0 in all 6 cells, but A/0.005 is borderline at +0.011 vs P1 +0.021, about half, and seed 1 alone has CI90 (+0.0001,+0.0223)). With the mix held fixed, GA positions add modestly (P2 +0.00..+0.01; exceptions B/A_noise/0.005 +0.035, about half of P1, and B/A_noise/0.02 +0.009 (+0.001,+0.017)). Quotas are held only at branch-bit level, so P2/P3 are approximate (e.g. A_noise 0.005: low-share .71 vs .74, 147.5 vs 141.5 pairs). The operator-shift explanation (2-LSB replacement in smooth dark background) is an untested inference, not a demonstrated mechanism.
2. T_raw (real covers): all three contrasts are small (mostly |diff| <= ~0.02; exceptions: B/0.01 P3 -0.022, and single replicates up to ~0.027); H4's prediction (P3 > 0 on A_noise only) is NOT supported: P3 ~ 0 on A_noise, and slightly negative at T_raw B 0.01 (-0.022 (-0.039,-0.004)), i.e. a random scheme with GA's mix was a bit MORE detectable there.
3. Pre-registered H3 (P2 ~ 0): largely supported; exceptions B/A_noise/0.005 (+0.035), B/A_noise/0.02 (+0.009) and B/T_raw/0.02 (+0.017 (0.001,0.032)).
Limits: reconstruction not original; weak simplified detectors (no CNN, no ensemble, no selection-channel-aware features); synthetic noise on A_noise; JPEG-decoded Alzheimer set and unknown provenance for the tumor set; leakage only reduced; 2 non-independent replicates; payload 0.015-0.06 embedded bpp only. Not claimable until the full-text gate (state/LEDGER.md) and verification gate are repeated on this result.


Verification (independent agent, see VERIFICATION_E6.md): seed-0 cells at 0.005 reproduce bit-exactly; no leakage found. Caveats: bootstrap does not refit (CIs optimistic), 36 contrasts uncorrected, cluster proxy not subject IDs, GA weak (pop 24, 30 gens). Exploratory only.
