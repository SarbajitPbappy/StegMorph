# Independent verification of E10-E14 and the Holm table (2026-11-11)

Scope: read-only audit. Nothing in code/, results/e*/ or state/ was modified. Scratch files are in the session scratchpad.
Method: recomputed all contrasts from the stored JSON, re-ran code/holm_power.py on a scratch copy, read the code, did an embed/extract round trip, and ran a reduced E14 cell.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | GA key never robustly more secure than a random key (P1 >= 0 in E10-E14); against SPAM slightly less secure | PARTIALLY |
| 2 | E14: COSTKEY beats RANDSEQ and COSTMIX only for detector A; CNN shows no gain; HILL far less detectable | PARTIALLY (numbers verified; the interpretation is fragile, see below) |
| 3 | Holm: 13/60 differences and 19/60 equivalences survive | VERIFIED as arithmetic, NOT VERIFIED as inference (the SE is too optimistic) |

### Claim 1, PARTIALLY
Evidence for it, from the 3-seed means in the JSON:
- SPAM (B) P1 is positive in every IXI cell: E11 +0.037/+0.033, E12 +0.026/+0.025, E14 +0.022/+0.036. In E11 and E14 at 0.02 bpp the CI excludes 0.
- Detectors A and C are within about +/-0.02 of 0 or slightly positive in all IXI cells.

Evidence against the literal wording "P1 >= 0 in E10-E14":
- E13 OASIS, detector A: P1 = -0.035, mean CI [-0.049,-0.021]. This is Holm-significant (p_holm 4e-5 in the table).
- Per seed it is -0.004 (CI crosses 0), -0.035 and -0.068. The spread across seeds is about 0.03, roughly 4x the bootstrap SE.
- Confounds: OASIS is JPEG-derived, and the CNN on OASIS has RANDSEQ AUC 0.465, below chance.
- E10 has per-seed negatives of about -0.014 (CI crossing 0), and E13 noHH detector A is -0.005.
- The correct wording is "never robustly more secure on IXI. One shifted-domain cell (OASIS, detector A) shows a significant GA advantage of 0.035 that is not stable across seeds." CLAIMS.md does mention this in the Holm section, but the E14 reading line, "the GA key is never more secure", does not.

### Claim 2, PARTIALLY
The numbers match CLAIMS.md and the notebook. Mean over 3 seeds, 1131 test slices:

| Detector | Payload | Q1 (COSTKEY - RANDSEQ) | Q2 (COSTKEY - COSTMIX) |
|---|---|---|---|
| A | 0.01 | -0.145 | -0.148 |
| A | 0.02 | -0.183 | -0.185 |
| B | 0.01 | -0.025 | -0.024 |
| B | 0.02 | -0.028 (seed 0 CI crosses 0) | -0.048 |
| C | 0.01 | +0.014 (CI [-0.005,+0.033]) | +0.003 |
| C | 0.02 | +0.005 | +0.003 |

- HILL AUCs: A 0.53 / 0.57, C 0.58 / 0.69. COSTKEY AUCs: A 0.62 / 0.72, C 0.90 / 0.98. These match.
- The COSTMIX control does match COSTKEY's operator counts and payload. PVD/LSB pair counts at 0.01 bpp are 28.2/183.7 (COSTKEY) vs 28.2/183.6 (COSTMIX). The message is identical across schemes. Q3 is about 0, so the effect is positional.
- The claim "no gain for C" holds only for the full-strength CNN (3000 train pairs, 15 epochs). In my reduced run (600 pairs, 4 epochs, seed 7, 300 test slices, 0.01 bpp):

| Detector | RANDSEQ AUC | Q1 (COSTKEY - RANDSEQ) | Q1 CI |
|---|---|---|---|
| A | 0.676 | -0.113 | [-0.145,-0.084] |
| B | 0.552 | +0.002 | CI crosses 0 |
| C | 0.743 | -0.197 | [-0.239,-0.160] |

  C then behaves like A. COSTKEY's validation AUC was only 0.54, so the CNN had barely learned to detect it. The "A-only gain" is therefore a detector-strength effect, not a property of the CNN architecture. The C null depends on training budget. A fully trained SRM or a bigger CNN could remove A's gain too.
- "HILL far less detectable under every detector" is overstated for B at 0.01 bpp: HILL 0.535 vs COSTKEY 0.566.
- The HILL used here is a numpy ternary-entropy simulator at the entropy bound. It has no extraction or syndrome-coding loss, and it is not Aletheia's HILL.m.
- I did not find an artifact for the claimed "checked against Aletheia HILL.m on 20 slices" (rank correlation of changed positions vs cost). I only checked that the port matches the published formula. It uses reflect padding where HILL.m uses symmetric.
- The COSTKEY pool is the 1/3 lowest-cost pixels, so it embeds in textured tissue. A random-key-inside-the-same-region control would separate "cost" from "texture mask". Only about 1-2% of pixels are <=2, so the background-zero explanation is weak. That control is missing.
- Detectors are retrained per scheme, which is a fair informed attacker.

### Claim 3
- I re-ran holm_power.py in a scratch directory (results symlinked, nothing in results/holm touched). It reproduces 13/60 differences and 19/60 equivalences.
- The SE is not conservative in the way the script comment states. The seeds do NOT resample the training set: NF=5239 equals the whole train split, so every seed trains on the same slices and tests on the same 1131 test slices. Seeds only change messages, keys, HGB and CNN initialisation.
- The bootstrap resamples test subjects only and never refits the detector. Detector-training variance, key/message variance and shifted-domain variance are therefore missing from the SE.
- The ratio of seed SD to bootstrap SE over the P1/Q1/Q2 cells has median 0.79 but a 90th percentile of 1.73. It is >1.5 in 18% of cells, and about 4x for OASIS A.
- Sensitivity of the Holm survivor counts (differences / equivalences):

| SE treatment | Differences surviving | Equivalences surviving |
|---|---|---|
| As coded | 13 | 19 |
| SE/sqrt(3) | 29 | 24 |
| SE x 1.5 | 5 | 10 |
| SE x 2 | 4 | 7 |

  The headline counts are therefore fragile.
- Several "equivalences" are trivial ceiling effects: E11 A and C at 0.05 bpp (AUC 0.994 / 1.000, p = 0 from the SE floor of 1e-4), and the C cells with AUC 0.975.
- The family of 60 is not independent. E12 (0.01 bpp) and E14 (0.01 bpp) are replicate cells on the same covers, and P1 and P3 share ORIG.
- The family is post hoc. P1 and Q1 are different questions and are pooled into one Holm family.
- Normal-approximation p-values go to 1e-200. That is not meaningful.

## Defects ranked

1. HIGH. Holm SE ignores detector-training and key/message variance, and treats shared test data as the only noise source. The OASIS A seed spread contradicts it. The 13/19 counts are not defensible as stated.
2. HIGH. The Q1/Q2 interpretation ("CNN shows no gain") depends on CNN training budget. A weak CNN reproduces A's gain (-0.20). No convergence evidence or learning curve is shown. The CNN uses `Ctr[:NC]` after a sorted subset, i.e. the first 3000 slices of the sorted train array, which is not a random subset of subjects (231 of 403 train subjects). No stronger detector (full SRM or an ensemble classifier) was run.
3. MEDIUM. There is no texture-matched random-key control, so COSTKEY's effect cannot be attributed to the cost map rather than to avoiding flat or noisy regions.
4. MEDIUM. The HILL benchmark is an idealised simulator, not validated against HILL.m (no stored evidence). The "far less detectable" claim is overstated for B. HILL changes far fewer pixels (MSE 0.0037 vs 0.0226), so it is not matched on distortion.
5. MEDIUM. The claim "P1 >= 0 in E10-E14" is false literally (E13 OASIS A, E10 per-seed). The CLAIMS E14 wording should be softened.
6. LOW. In the code, extract(embed(x)) is asserted only for the first 2 images per make_all call (`if i < 2: assert`). My round trip on 20 test slices x 3 key types (GA, random, COSTKEY) was 60/60 correct. HILL has no extractor.
7. LOW. The `KEYS` cache reuses the GA key across payloads. This is harmless.
8. LOW. A LogisticRegression ConvergenceWarning (max_iter=300) appears for detector A in the reduced run. A is not fully converged. Check whether the full runs also warn (logs in results/e14/*.log).
9. LOW. The results/e12 JSON files are named e11_seed*.json. They are easy to mix up with E11, and the notebook and Holm script depend on the inherited name.
10. LOW. Splits: I found no train/val/test subject overlap (403/87/87 subjects, all intersections empty). Slice-level covers within a subject are correlated, which is handled by the subject bootstrap in the test set only.

Checked and clean: the labels are correct (cover 0 / stego 1). Cover features are shared across schemes. The StandardScaler is fit on train only. The CNN picks its epoch by val AUC, never test. The same message is used for all schemes within an image. The bootstrap resamples subjects within a fixed test set.

## Reproduction (Task C)
Reduced run of code/exp14_costkey.py, seed 7, PAY=0.01, NTR_FEAT=1500 NTR_CNN=600 NTE=300 EPOCHS=4, took 5 min 16 s. A full reproduction would take hours, so I did not run it. The Q1 results are in the table under Claim 2.

- Q1 for A is negative, as claimed.
- Q1 for C is negative here (-0.197), not about 0 or positive as claimed. The CNN was undertrained.
- Embed/extract round trip: 60/60 correct on 20 test slices x 3 key types (GA, random, COSTKEY), in the scratchpad rt.py script.
- The operator-count match for COSTMIX holds in both the stored full runs and my run: 25.0/190.1 vs 25.0/190.0.

## Must be fixed before any SUCCESS_* state
1. Recompute the inference. Use a cluster bootstrap that also refits the detector, or a seed x training-subset design where the seeds resample the training subjects. Report Holm on honest SEs. Restrict the family to independent cells and drop the ceiling-saturated TOSTs.
2. Run a strong-detector check for Q1. Train the CNN on the full train split to convergence with a learning curve, plus a full SRM or ensemble classifier. State the A-only gain as detector-specific unless it survives.
3. Add a texture-matched random control, i.e. a random key restricted to the pool with an equal-texture distribution.
4. Validate hill_cost against HILL.m on the 20 slices, with stored evidence. Soften the HILL wording, or run the real HILL, and match on payload and distortion.
5. Rewrite CLAIMS wording: "GA key never more secure" becomes "not robustly more secure on IXI; one unstable OASIS-A cell favours GA by 0.035".
6. Assert the round trip for every image or a random sample, not only i < 2.
