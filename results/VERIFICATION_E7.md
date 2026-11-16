# Verification of E7 (CNN detector) and E8 description
Verdict: REPRODUCES on code review (no leakage or bug that creates a spurious GA-vs-RAND gap). CNN was NOT re-run. Several overstatements in the write-up.

## 1. Code review of exp7.py
- Train/test: each fold trains the CNN on Fc[tr]/Fs[tr] only; test fold is scored once. OK.
- Cover and stego share one index and one `folds` array; groups (source file / cluster) are assigned to folds, so a cover and its stego never straddle folds. OK.
- Rank normalisation: done per test fold over concatenated [cover; stego] scores; cover = first te.sum() entries. Correct. AUC pools the per-fold ranks (standard, slight cross-fold calibration noise only).
- BatchNorm: net.train() during training, net.eval() before scoring. Training batches are balanced (cover+stego of the same images, labels 0/1), flips applied to the whole batch (labels unaffected). No ordering/label leak.
- Same payload per image across schemes (pay drawn before selection from the same rng r); need = total_bits(n) identical (585 bits, 163 payload bits at 0.01 bpp). The first 2 images per scheme assert extraction == payload.
- Selection quotas for RAND_GAMIX come from the GA mask, so P3 is a valid operator-mix control.
- Only weak points (none create GA/RAND bias): A_noise fold groups are a proxy (near-duplicate clustering at the loosest allowed threshold, q=0.1, mean cluster 4.5, max 22), so absolute AUCs may be optimistic; no subject IDs for T_raw; bootstrap CIs are not retrained. Docstring says "E6/exp6.py" (stale).
- Write-up says 15 epochs; code default is EPOCHS=20 (env override). Not recorded in the JSON, so unverifiable.

### Stego-vs-cover script (seed 0, 0.01 bpp, first 60 images per set, same make_all logic; /tmp/chk.py)
| set | scheme | stego != cover | mean changed px (median, min) | mean max abs change | mean pairs | low(LSB) share | cap used / need |
|---|---|---|---|---|---|---|---|
| T_raw | RAND | 60/60 | 285.3 (287, 245) | 8.6 (max 16) | 266.1 | 0.82 | 585.8/585 |
| T_raw | GA | 60/60 | 287.9 (289, 250) | 2.35 (max 7) | 280.6 | 0.90 | 585.5/585 |
| A_noise | RAND | 60/60 | 271.2 (271, 248) | 13.3 (max 16) | 245.7 | 0.75 | 585.7/585 |
| A_noise | GA | 60/60 | 282.2 (282, 255) | 4.4 (max 7) | 275.6 | 0.88 | 585.4/585 |
- No empty masks; no stego identical to its cover; payload bit count identical (163) in both schemes.
- Changed-pixel counts are nearly equal (GA +1% to +4%). The difference is amplitude: RAND uses PVD pairs (changes up to 16 grey levels), GA mostly LSB (+-1) with a few PVD pairs. No clipping/saturation artefact (the saturated-pixel count differs by a few px per image in both schemes).
- Implication: the GA-vs-RAND CNN gap is a genuine property of the schemes (mostly a lower-amplitude operator mix), not a data bug. P3 (RAND_GAMIX) isolates the position effect: ~0 on tumour MRI, -0.10..-0.15 on noisy Alzheimer.

## 2. RESULTS_E7_cnn.md vs JSONs
- All table entries (AUC, P1, P3, ci90, MSE) match e7_seed0.json to rounding. Seed-1 lines are correct: the "AUC mean" figures are means of seed0 and seed1 (this is not stated clearly; the stray ")" in the lines is a typo). The P1/P3 pairs are [seed0, seed1] and match.
- Overstatement: "seed-to-seed difference <= 0.006" holds for P1 only (max 0.0055). For P3 it is up to 0.0134 (A_noise 0.01: -0.112 vs -0.0986), and for raw AUCs up to 0.012 (A_noise RAND 0.01).
- Header says "One CNN training seed, one stego replicate" but the body reports 2 seeds; contradictory/stale. Seed 1 changes crops, stego and CNN init but not the image pool (stated).
- Architecture description approximate: first block is conv+BN+Hardtanh (no pool); last block has no pool.

## 3. E8 description vs exp8.py / e8_seed0.json
- Numbers match: A_noise HGB (family B) P1 +0.0895 (~+0.09), SRM-lite (family A) +0.0612 (~+0.06); tumour A -0.0078, B +0.0193 (the "-0.008..+0.019" range is right). Seed 0, 0.01 bpp only.
- Overstatement: "untruncated" magnitude features are in fact histograms of signed differences clipped at +-24 (mag(): np.clip(D,-24,24), 49 bins; 1st and 2nd order, horizontal/vertical), not |difference| and not truly untruncated. Clipping at 24 vs T=3 is a reasonable test of truncation but the label is loose. T_raw B P1 CI90 (0.0009,0.0384) barely excludes 0, so "~equal" is fine only loosely.
- "SRM-lite re-run" is a logistic regression (C=0.05) on S.features (T=2, a different feature family from the spam T=3 of E6); "HGB" applies only to the magnitude histograms. The description conflates this a little.
- Omitted: in E8 P3 on A_noise is ~0 (+0.003 A, +0.009 B), so the hand-feature detectors see the GA excess as a pure operator-mix effect, while the CNN sees -0.11 for position. This is the real disagreement and the file only says "unexplained".
- The E8 conclusion "truncation explanation not supported" is valid for these features; single seed, no CNN-side ablation.

## Bugs by severity
- None critical or high on leakage/label correctness.
- Low: stale docstring; epochs 15 vs default 20; proxy groups for A_noise; unretrained bootstrap CIs.
