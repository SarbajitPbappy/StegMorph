# Verification of E6 (independent)

## Verdict: REPRODUCES (numbers) / PARTIAL (interpretation)
Cell-level reproduction is bit-exact. The review found no leakage bug and no fatal bug. One factual claim in RESULTS_E6.md is wrong (the "SAME image pool"), and the reading in bullet 1 is stronger than the data.

## What was run
- Copied exp6.py, stegmorph_recon.py, srm_lite.py to /tmp/verify. I also had to copy /home/claude/sm/embed.py, which stegmorph_recon imports and which the task did not list.
- Edited only the copy: PAY = [0.005]. Ran `python3 exp6.py 0` (about 11 min).
- A second variant in /tmp/verify2 replaced argsort-argsort ranking with tie-averaged scipy rankdata, to test the tie risk.

## Compared numbers (seed 0, 0.005 bpp; original JSON vs my rerun)
All 4 AUCs, 3 diffs, 3 CI90 pairs and all stats (pairs, low_share, mse) were identical in 4 of 4 cells, to 4 decimals. Largest AUC difference: 0.0000 (limit 0.02).

| cell | RAND | GA | GA_RANDMIX | RAND_GAMIX | P1 | P2 | P3 |
|---|---|---|---|---|---|---|---|
| T_raw A | .7897 | .7784 | .7928 | .7773 | -.0113 | +.0031 | +.0011 |
| T_raw B | .6660 | .6511 | .6392 | .6541 | -.0149 | -.0268 | -.0030 |
| A_noise A | .6618 | .6892 | .6714 | .6784 | +.0274 | +.0096 | +.0108 |
| A_noise B | .5969 | .6791 | .6209 | .6704 | +.0822 | +.0240 | +.0087 |

Rerun equals JSON in every column (diff 0.0000). The tie-averaged variant changes AUC by at most 0.0001. HGB score ties are at most about 1.8% of scores, so the tie risk is negligible.
The two-seed means in the RESULTS_E6.md table were recomputed from the JSONs and all match to 3 decimals.

## Bugs / risks (severity)
1. MEDIUM (false statement): RESULTS says the two replicates use "the SAME image pool". They do not. `rng = default_rng(seed)` drives the tumor crop positions and the Alzheimer `rng.permutation`, so the 600 A_noise images differ by seed. Cluster info is 133 clusters / max 22 for seed 0 and 127 / max 20 for seed 1, and the tumor crops are redrawn. The replicates therefore also resample images, so they are less non-independent than claimed. The "optimistic CI" caveat still applies because averaged CIs are not a valid joint CI. The stated "max 22" holds for seed 0 only.
2. MEDIUM (design): quotas are held at the branch-bit level only. They are approximate and bit-level, so the mix is not fully held.
   - A_noise 0.005: GA_RANDMIX low_share is .710 vs RAND .740, with 147.5 vs 141.5 pairs. RAND_GAMIX has 163.1 pairs vs GA 164.3.
   - GA picks cheap, small-capacity PVD pairs, so more pairs are needed for the same bits. MSE of GA_RANDMIX is 0.025 vs RAND 0.071.
   - P2 therefore contains a within-PVD change (capacity and difference-range mix) as well as position choice. P3 is cleaner but still not a pure position effect.
3. LOW-MED (quota exactness): quota = capacity of the mask per branch. Each branch is solved to capacity >= quota, so the total overshoots `need` by a few bits. Payload bits are consumed in pair-index order and the tail is zero-padded. Embedded bits are equal in payload terms, but the pair counts and zero padding differ slightly by scheme.
4. LOW-MED (CI validity): the bootstrap resamples out-of-fold scores only and does not refit the models. It is paired correctly (same idx for both schemes) and clusters are resampled. CIs ignore training and selection variance, so they are optimistic. There are 36 contrasts with 90% CIs and no multiplicity correction.
5. LOW (leakage proxy): Alzheimer groups are 16x16 complete-linkage clusters on the raw (pre-noise) images, which is the correct images. The grouping is a proxy: at q=0.1 the threshold is lenient, but there are no subject IDs. Same-subject neighbouring slices can still cross folds, which inflates absolute AUC but affects all schemes equally. Tumor groups are by source file; duplicates across files are unchecked.
6. LOW (rank normalisation): ranks are computed within the test fold over cover+stego together, then pooled across folds. This is not leakage. Ties are broken by index (covers first), but the effect was measured at <= 0.0001 AUC.
7. LOW (GA strength): select_ga uses pop 24 and 30 generations, which is a weak optimiser. "GA" results are specific to this setup.
8. OK, checked and found no problem:
   - StandardScaler is fit on the training fold only, with fixed hyperparameters.
   - Folds are built on groups. The cover and stego of one image share a fold, and cover features are shared across schemes.
   - The same images and the same payload are used per scheme.
   - The noise key is the file index, identical across schemes.
   - The extract assert runs on 2 images per scheme.

## Overstatements / errors in RESULTS_E6.md
1. "on the SAME image pool" is false (see bug 1).
2. Reading 1: "mostly reproduced by a RANDOM selector that copies the GA's mix". Supported on A_noise, but at A/0.005 P3 is +0.011 vs P1 +0.021, about half, so it is not "mostly".
3. Reading 1: "approx. 90% CIs include 0 in all 6 cells". Averaged CIs do, but seed 1 alone has A_noise A 0.005 CI90 = (+0.0001, +0.0223), which excludes 0. Absence of evidence is not evidence of absence, given the CI width of about +-0.015.
4. Reading 1: "the harm comes mainly from the MSE-driven shift to 2-LSB replacement in smooth dark background". The mechanism was not tested. Only the branch-share correlation was observed. GA also has lower MSE yet is more detectable, which fits the story but is not shown.
5. Reading 1: "GA positions add little (P2 +0.00..+0.01, one cell +0.035)". P2 is +0.014 for B at A_noise 0.01 (borderline) and +0.009 (0.001, 0.017) for B at A_noise 0.02. The latter has a CI excluding 0 and is omitted from the "exceptions" in reading 3, which lists only 2 exceptions. P2 for B 0.005 (+0.035) is about 47% of P1 (+0.075), which is not "little".
6. Reading 2: "|diff| <= ~0.02". The T_raw B 0.01 P3 is -0.022. Per-seed values reach P2 -0.027 (seed 0, B 0.005) and P1 +0.025 (seed 1, B 0.02), so the bound is too tight at the replicate level.
7. Header "every image tested once out-of-fold" is true. "Leakage only reduced" is a fair statement.
