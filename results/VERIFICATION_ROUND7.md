# Verification round 7 (independent, V2 article)

Scope: Overleaf/article (article.tex, sections/*.tex, tables/tab_main.tex, tab_hyp.tex, tab_budget.tex), state/CLAIMS.md (V2 sections), results e24, e26, e36, e37, e38, e39, e39y, e40, e41 (incl. k), data/splits. No file other than this report was written. Scratch scripts: /private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/verify7/ (t1-t4.py). All AUCs were recomputed from the stored score npz files (pc/ps arrays) with sklearn. Bootstrap intervals were recomputed with 300 subject-cluster resamples, so they differ slightly from the stored 500/1000-resample values. I compared against the stored JSON values where the article quotes them.

## Summary

- Numeric items checked: about 150 (tab_main 48 cells, all V2 passages in results.tex, abstract and highlights, discussion/method/limitations numbers, tab_budget, hypothesis rows).
- Matched: all but the items below.
- Mismatched numbers: 3 (HILL "0.003" at 1.4 percent; 0.844 vs 0.843 mixing seed-0 and seed-mean in the K paragraph; "positive in every column" vs CNN^a GA cell -0.003). Wording or definition mismatches: 4 (see defects).
- Overstated or unsupported statements: 7.
- tab_main: 48 of 48 cells match to the third decimal (A, D, B, S, F, M, CNN^a, CNN^b). All six rows were recomputed.
- Integrity: no test-set model selection found. The compared score files have identical subjects arrays. IXI, T1, 256, OASIS splits are subject-disjoint. CT subject-disjointness cannot be checked from the stored files (see 4b).
- Hypothesis labels: H5, H7, H9 (disputed), H14, H15, H16, H17, H18, H19 are justified by the logged rule. H9 and H20 carry overstatement (see Task 3).

## Task 1: tab_main (IXI T2, 0.01 bpp, seed means of 3 seeds, key minus random key)

Recomputed from results/e24/scores_s*_b0.01.npz (A, D, B, S) and results/e37/scores_s*_b0.01.npz (F, M); GAMINX from results/e41/scores plus the e37 RANDSEQ scores.

| Row | A | D | B | S | F | M | verdict |
|---|---|---|---|---|---|---|---|
| GA contrast | +0.0078 (+0.008) | +0.0124 (+0.012) | +0.0289 (+0.029) | +0.0124 (+0.012) | +0.0117 (+0.012) | +0.0117 (+0.012) | match |
| GAMINX large search | -- | -- | -- | -- | -0.0656 (-0.066) | -0.0656 (-0.066) | match (F identical to M because the GA map is constant) |
| Cost-guided | -0.1507 (-0.151) | -0.1844 (-0.184) | -0.0032 (-0.003) | -0.0720 (-0.072) | -0.1385 (-0.139) | -0.0042 (-0.004) | match |
| Matched control | -0.0015 (-0.001) | +0.0016 (+0.002) | +0.0150 (+0.015) | +0.0016 (+0.002) | +0.0133 (+0.013) | +0.0133 (+0.013) | match (A shows -0.001, true value -0.0015: rounding edge) |
| Smooth | +0.1232 | +0.1174 | +0.0683 | +0.1433 | +0.0884 | +0.1150 | match |
| HILL ref | -0.2366 | -0.2759 | -0.0452 | -0.1831 | -0.2750 | -0.2036 | match |

(Bracketed values are what the table shows.)

CNN columns:
- CNN^a cost-guided = e39 seeds_summary e60_n4186 mean Q1 = +0.0143 (recomputed seeds +0.0184, +0.0130, +0.0115). Match.
- CNN^a GA = e26 ORIG seed 0 minus RANDSEQ seed 0 = 0.9104 - 0.9134 = -0.0030. Match.
- CNN^a HILL = 0.6026 - 0.9134 = -0.3108. Match.
- CNN^b = e39y e60 Q1 = -0.1868 (random-key AUC 0.8206, cost-guided 0.6339). Match.

Source mixing: confirmed. The caption discloses it. The GA and HILL CNN^a cells come from e26 (early stopping, patience 20, seed 0, random-key AUC 0.9134) while the cost-guided cell comes from e39 (no early stopping, three seeds, seed-0 random-key AUC 0.9032). The same nominal configuration gives different random-key AUCs (0.913 vs 0.903 in seed 0). The e26 cost-guided Q1 for seed 0 is +0.008 and the e39 one is +0.018. The column is therefore not like-for-like within itself (low-medium).

Caption note: "random-key AUC 0.82" for CNN^b is correct (0.8206).

## Task 2: V2 passages (item table)

| Statement (location) | Recomputed | Verdict |
|---|---|---|
| F: 34,671 features; random-key AUC 0.848 / 0.949 (results, detector paragraph) | 0.8483 / 0.9490; per seed 0.852/0.846/0.847 and 0.951/0.950/0.946 | match |
| F Q1 -0.139 (0.01), -0.113 (0.02), every seed below -0.10 | -0.1385, -0.1127; per seed -0.141,-0.137,-0.137 / -0.115,-0.116,-0.106 | match |
| F P1 +0.012, +0.006 | +0.0117, +0.0062 | match |
| MDE 0.003 for F at 0.01 | 0.0028 (-0.0028 seed-0 lower bound) | match |
| M Q1 -0.004 / +0.002; every seed between -0.010 and +0.004; lowest bound -0.027 | -0.0042 / +0.0016; per seed -0.010,+0.003,-0.006 / -0.002,+0.003,+0.004; lower bound -0.027 | match |
| Matched control within 0.013 for both | +0.0133 (0.01), +0.0104 (0.02) | match at rounding, but 0.0133 exceeds 0.013 |
| HILL vs random under M -0.204 / -0.218 (CLAIMS) | -0.2036 / -0.2177 | match |
| CNN: 0.913, 0.907 random key; 0.910 GA; 0.922, 0.919 cost-guided; Q1 +0.008 (-0.010 to +0.027), +0.011 (-0.006 to +0.031); P1 -0.003 (-0.012 to +0.006) | e26 summary: 0.9134/0.9075/0.9104/0.9217/0.9188; Q1 +0.0083, +0.0113; P1 -0.0031 [-0.0115, +0.0056] | match |
| 30-epoch first-round net Q1 +0.013, +0.006, +0.011 | not re-derivable in this round (e21/e22 not in scope) | not checked |
| Grid: -0.193 (4 ep, 600), -0.052 (10 ep, 1000), -0.012 (10 ep, 2500), -0.018 to +0.018 from 30 ep | -0.1930, -0.0517, -0.0119; 30+ ep range -0.0175 to +0.0184 | match |
| 11 of 16 cells with random-key AUC > 0.85, 10 satisfy Q1 >= -0.02, one does not (4 ep, 4186, -0.026, interval -0.046 to -0.009) | 11 / 10; the violating cell -0.0259 [-0.046, -0.011] | match |
| Three seeds: 4 ep -0.017 (-0.026, -0.017, -0.006); 60 ep +0.014 (+0.018, +0.013, +0.012) | -0.0165; -0.0259,-0.0174,-0.0062; +0.0143; +0.0184,+0.0130,+0.0115 | match |
| "each interval touching or including zero" at 60 ep | stored: [-0.0003,+0.0364], [-0.0063,+0.0338], seed 2 includes zero | match |
| "-0.197 in an earlier verification run" | not in stored V2 files; grid gives -0.193 | provenance only, not checkable here |
| Yedroudj-Net-style: 0.82 random, cost-guided 0.634, Q1 -0.187 [-0.206, -0.168]; -0.116 at 4 ep | 0.8206, 0.6339, -0.1868 [-0.2055, -0.1670]; -0.1159 | match |
| HILL residual 0.603, -0.311 | 0.6026, -0.3108 | match |
| SRNet-style fixed recipe: val 0.900, test 0.904; partner val 0.505, 0.502, 0.501 | 0.9004/0.904; 0.5051, 0.5023, 0.5013 | match |
| "In the first round the cost-guided set trained, the random-key set failed three times" | e26 srnet files: COSTKEY 0.9289/0.9357; RANDSEQ 0.5018, 0.5015, 0.5124 | match |
| Equal change count, 1.4 percent, F: HILL -0.147, SUNI -0.099 vs random hybrid | -0.1465, -0.0988 | match |
| "that is 0.003 and 0.040 from the cost-guided key (HILL -0.008...)" | HILL vs COSTKEY -0.0080; SUNI +0.0398 | MISMATCH: "0.003" should be 0.008 (inconsistent with its own parenthesis) |
| HILL -0.008 interval includes zero in all seeds | [-0.023,+0.002], [-0.016,+0.011], [-0.023,+0.001] | match |
| M at 1.4 percent: gap 0.043 / 0.012 | -0.0432 / -0.0116 | match |
| 0.37 percent, F: HILL -0.056, SUNI -0.030; above cost-guided hybrid +0.016, +0.042 | -0.0560, -0.0299; +0.0158, +0.0420 | match |
| 0.37 percent, M: +0.015, +0.051 vs random; +0.027, +0.063 vs cost-guided | +0.0153, +0.0511; +0.0272, +0.0629 | match |
| OASIS 0.002 bpp: random 0.729 (A), 0.752 (D); Q1 -0.017, -0.029, every seed negative; Q4 +0.042, +0.034 | 0.7290/0.7522; -0.0173, -0.0288 (per seed -0.016,-0.016,-0.0195 / -0.034,-0.019,-0.033); +0.0416, +0.0341 | match |
| "matched control within 0.007" | seed means -0.0066, -0.0055; per seed up to -0.011 (A seed 1), +0.0024..-0.0112 (D) | match on means only (low) |
| CT 0.002: 0.957 / 0.986; Q1 -0.103 (A), -0.056 (D) | 0.9567/0.9862; -0.1026, -0.0555 | match |
| CT HILL "AUC 0.81 and 0.91 against 1.00" | CLAIMS E32: HILL A 0.807/0.909 at 0.01/0.02 bpp, D 0.896/0.947 | number from a different payload and detector (see defect 10) |
| CT 0.01/0.02: Q1 -0.028 to -0.010; random 0.993-1.000 | tab_replication/CLAIMS E32 consistent (OASIS D 0.993 is the 0.993 minimum) | match |
| GAMINX vs random 0.01: -0.066 (-0.070, -0.061, -0.066), interval -0.078 to -0.054 | -0.0656; -0.0697,-0.0613,-0.0658; worst bounds -0.0779/-0.0542 | match |
| GAMINX 0.02: -0.030 (-0.036 to -0.024) | -0.0298; -0.0364/-0.0242 | match |
| 16 x fitness evaluations of GAMIN | pop 100 x 50 gen = 5000 vs 200 x 400 = 80000 (stegmorph.py, lab24.py) | match |
| GAMIN -0.027 / -0.029 (0.01), -0.018 / -0.019 (0.02); GAMINS -0.053 / -0.055, -0.042 / -0.036 | e30: -0.0267/-0.0286, -0.0177/-0.0186; -0.0528/-0.0555, -0.0424/-0.0362 | match |
| Cost-guided 0.073 / 0.083 lower than GAMINX | -0.1385+0.0656 = 0.0729; -0.1127+0.0298 = 0.0829 | match |
| "half to a quarter" of the cost-guided gain | 0.47 and 0.27 | match |
| MDE A 0.005 (0.0047), 0.003 (0.0026), D 0.004, F 0.003; zero at D/F 0.02; seed means +0.006 to +0.012 | mde json and per-seed CIs in e24/e37 JSON agree; means +0.0063..+0.0124 | match (but see defect 1 on what this bound means) |
| K AUC 0.981, 0.983, 0.945, 0.976 (0.01); 0.991, 0.994, 0.978, 0.991 (0.02) | 0.9805, 0.9832, 0.9448, 0.9762; 0.9914, 0.9936, 0.9778, 0.9913 | match |
| "against 0.852, 0.857, 0.844 and 0.783 for maxSRM without key" | seed 0: 0.8524, 0.8574, 0.8425, 0.7827. 0.844 is the 3-seed mean of COSTKEY (0.8425, 0.849, 0.8407) | MISMATCH (mixes seed 0 and the seed mean; seed-0 value is 0.843 as in CLAIMS) |
| K: ORIG +0.003 [-0.002, +0.008]; GAMINX -0.004; COSTKEY -0.036, -0.014 intervals below zero; M on same seed -0.010, -0.002 | +0.0027 [-0.0017,+0.0079]; -0.0043; -0.0357 [-0.044,-0.027], -0.0136 [-0.022,-0.007]; -0.0099, -0.0020 | match |
| Abstract/overview "0.11 to 0.19" and "0.14 to 0.18" | Q1 A,D,F at 0.01/0.02: 0.113 to 0.193; at 0.01: 0.139 to 0.184 | match |
| Abstract: AUC drop by GAMINX "0.03 to 0.07" | 0.030 to 0.066 | match |
| Abstract: maxSRM "-0.004", CNN "+0.014 at 60 epochs", "-0.19" Yedroudj | as above | match |
| Abstract/Discussion: HILL 0.275 vs 0.147 (F), 0.204 vs 0.043 (M) | -0.2750 / -0.1465; -0.2036 / -0.0432 | match |
| Method: 100 learners, 2000 features, 16 and 36 characters at 0.01 / 0.02 | code: DSUB 2000, NL 100; message(): (int(bpp*16384)-32)//8 = 16 and 36 | match |
| Payload 0.032 and 0.0027 bpp, "about 1.4 / 0.37 percent" | hybrid 0.01 bpp 1.40 percent (e24); HILL 0.03/0.04 bpp 1.28/1.79 percent so 0.032 is about 1.38 percent; the 0.0027 bpp hybrid share is not stored anywhere | 1.4 percent verified; 0.37 percent for the hybrid at 0.0027 not verifiable (defect 8) |
| CT/OASIS payload 0.002 bpp, "smallest payload the format allows" | message(): L = max(1, (32-32)//8) = 1 character, so 0.002 and 0.0027 bpp both embed one character (40 bits) | internally consistent only because of max(1,...); the two labels are the same effective payload (defect 9) |
| Runtime table | residual 60 ep: e39 33.5-44.7, e26 33.4-49.9 min (table says 37-50); Yedroudj 38.9-39.7 (39); SRNet e26 61-91, e36 72-74 | "37-50" slightly off (low) |
| tab_budget rows | all val/test AUCs match JSON; "Best ep." is JSON best_epoch + 1 (1-indexed) | match |

## Task 3: tab_hyp rows

Rule texts are quoted from state/CLAIMS.md (V2 pre-registration, lines 446-457 and later).

- **H5** (first-round rule, Q1(C) >= -0.02). Label "Partly met". Justified: seeds' estimates satisfy except one 4-epoch seed (-0.026) and the Yedroudj network, which is far below. The row text numbers are correct. The label "Partly" is fair; the Yedroudj result (-0.187) is a true violation of the rule as written for that architecture, so the row is closer to "Not met" for that network. It is disclosed in the row.
- **H7** ("S removes most of the gain, Q1(S) >= -0.05"). Label "Not met". Justified for SRM-lite S on T2 (-0.072, -0.067). The row adds "met on T1" and "met for real maxSRM". Fine.
- **H9** ("GA-key null and position effect replicate on a non-saturated, non-JPEG collection"). Label "Partly met". Two overstatements: (a) the unsaturated cell on OASIS (0.002 bpp) is JPEG-derived, which the rule excludes; only IXI T1 is non-JPEG, and T1 already failed the strict GA-key bound in 2 of 8 cells; (b) the GA key (ORIG) was not run in e40 at 0.002 bpp, so the GA-key null is not tested on the unsaturated OASIS cell at all. The position effect on OASIS is -0.017 (A), which is under the article's own 0.02 relevance margin (method, statistics), and the Q2 (cost-guided minus matched control) for A is -0.011 with a worst-case interval of -0.033 to +0.007, which includes zero. The row should say the OASIS cell is JPEG-derived and that only detector D (-0.029) clears the margin.
- **H14** ("Q1 <= -0.10 at 0.01 and 0.02 bpp; |P1| <= 0.02"). Label "Met". Justified on estimates (all six per-seed Q1 below -0.10, max P1 0.017). One interval bound (seed 2, 0.02 bpp, upper -0.092) is above -0.10; this is disclosed in the row and in CLAIMS. Acceptable.
- **H15** (Q1 >= -0.05). "Met" justified (-0.004, +0.002, worst -0.027 lower bound).
- **H16** (Q1 >= -0.02 for random-key AUC > 0.85). "Partly met" justified: 10/11 cells; seed means -0.017 and +0.014 comply. Note the pre-registration (V2-H3) also asked for a second architecture; the Yedroudj network never exceeded 0.85, so that part of the hypothesis was not testable. The row does not say so. The CLAIMS entry also does not call the rule untested for the second architecture, only "does not test V2-H3's rule".
- **H17** (validation AUC >= 0.55 on the random-key set). "Met" justified (0.9004).
- **H18** (both reference embedders >= 0.10 below random hybrid, F). "Partly met" justified: HILL -0.147 passes; S-UNIWARD -0.0988 (seeds -0.098, -0.097, -0.101) misses by 0.001. Strictly, the rule is a conjunction and one conjunct fails, so "Not met as written" would also be defensible. The row text is accurate.
- **H19** (OASIS and CT in 0.6-0.8, and a further non-JPEG collection). "Partly met": OASIS yes, CT no (0.957/0.986), the extra collection not added. One of three components is fully met; "Partly met" is fair but generous.
- **H20** (GA does not exceed the cost-guided gain; key-known detector). Label "Met". The GA part is clearly met (0.066 vs 0.139; 0.030 vs 0.113). The key-known expectation (3) was pre-registered as an expectation and is NOT met (CLAIMS says so). Putting the whole row under "Met" is an overstatement relative to the table caption ("Met means the rule held in every cell it covered"). Recommend "Met for the GA; key-known expectation (3) not met".
- **H1, H2-H4, H6, H8, H10-H13** (not asked): not re-verified here beyond the main-table numbers.

## Task 4: integrity

(a) Subjects arrays. Compared pairwise, slice by slice, in code paths used for every cross-run contrast: e24 vs e37 vs e41 for all seeds and both payloads (all equal, length 1131); e38 hi, lo, su against e37 (asserted equal, 1131 each, all seeds); e41/k vs e37; e39 and e39y RANDSEQ vs COSTKEY (equal for every cell); e26 vs split; e40 oasis vs oasis_test (equal, 689). All equal to data/splits/ixi_test.npz['subject']. Note that code/summarize_e38.py, summarize_e41.py, summarize_e39*.py and make_main_table.py do not assert this; they take the subject array of one file only. They give correct results because the arrays are equal, but there is no guard.

(b) Splits. ixi (403/87/87), ixit1 (406/87/88), ixi256 (403/87/87), oasis (242/52/53): zero subject overlap between train, val, test. No duplicate images (md5) across splits for ixi, ixit1, oasis, ct. CT: the 'subject' field is a unique per-image string (5000/600/1500 unique values, e.g. "test31"), so scan-level disjointness cannot be verified from the stored files; it rests on the OrganAMNIST official split. The article correctly says CT bootstrap resamples images. The data section's "split by CT scan: 115, 16 and 70 scans" cannot be reproduced from data/splits.

(c) Model selection and settings.
- code/exp37_fullsrm.py: no model selection at all. The FLD ensemble has fixed dsub=2000, nl=100 (env defaults), ridge lam=1e-3 (not stated in the article, low), standardisation from training data only, score = mean standardised projection, and no test data used in fitting. Bootstrap is over test subjects. Matches the article (100 learners, 2000 features). Not a full Kodovsky ensemble: no OOB-based threshold or subspace-dimension search (the article says "our implementation").
- code/exp39_budget.py and code/nets26.py train(): checkpoint = best validation AUC (400-slice validation subsample from the val split), no early stopping in the sweep (patience 10^6), test scored once after loading. No test-set selection.
- code/exp36_srnet_fix.py: best-validation checkpoint, test scored after. No test-set selection.
- Maps for detector M/S are computed "from the image under test" (cover for cover, stego for stego), so for cost-guided and smooth keys the cover and stego maps can differ slightly (HILL cost of a modified image); this is the disclosed method but is a mild asymmetry that is not present for K (shared map). Not leakage, but worth a sentence.

(d) Claims log order. The V2 pre-registration ("V2 round: plan and pre-registration", line 446) and "V2 step 0 closed" precede every V2 outcome. Run parameters were logged before runs for V2.1, V2.3 (calibration), V2.4 (payload chosen from a 600-slice pilot, disclosed), V2.5 (GAMINX), key-known detector (expectations declared before the run), the Yedroudj run. Order within the file is consistent. Limits: entries carry dates only (no clock times for V2), the log has no hash chain or external timestamp, so the order cannot be verified independently of file position. The V2-H5 pre-registration was fixed after the first-round results were known (acknowledged in the Limitations). The e38_calib file stores detector AUCs (it ran detector A: HILL 0.58, RANDSEQ 0.90 at 0.03 bpp); the log says only the changed-pixel share was read. This cannot be verified, and the article's "no detector output" is not literally true of the stored file.

## Defects (severity)

1. HIGH. The "no reduction larger than 0.005 AUC" statement (abstract, highlights, discussion RQ1, conclusion) is stated more broadly than the data. (a) The bound is the worst per-seed bootstrap interval lower bound of non-refit intervals (not a pooled bound over seeds), computed on IXI T2 at 0.01 and 0.02 bpp for A, D, F/M only. (b) The article's own refit-aware bootstrap gives lowest bounds of -0.006 (A, 0.01) and -0.014 for D (P1 +0.003, -0.014 to +0.020, 60 replicates), so under refitting the bound is not 0.005. (c) Highlight 2 says the GA key was not more secure "at any payload, detector or collection tested (no gain above 0.005 AUC)". The 0.005 figure does not exist for payloads 0.05-0.09, SPAM, T1, OASIS, CT, CNNs. The T1 SPAM interval bound is -0.030. Restrict to "IXI T2, 0.01 and 0.02 bpp, SRM-lite and full SRM, without refit" or recompute under refit.
2. MEDIUM. Overview (results.tex): "the difference is positive ... in every column where it was measured" is false for CNN^a (-0.003).
3. MEDIUM. Equal-count paragraph: "0.003 and 0.040 from the cost-guided key (HILL -0.008...)" should read 0.008 and 0.040.
4. MEDIUM. OASIS 0.002 bpp "the position effect appears": detector A's Q1 (-0.017) is below the paper's own 0.02 margin and Q2 for A (-0.011) has an interval including zero; "about a fifth of T2" (results, H9 row) is inaccurate: -0.017/-0.151 = 0.11, -0.029/-0.184 = 0.16. The GA key was not run in e40, so the "unsaturated null" for OASIS does not exist.
5. MEDIUM. H9 and H20 labels (see Task 3). H20 "Met" bundles a pre-registered expectation that was not met.
6. MEDIUM. CNN^a column mixes e26 (early stopping, seed 0) and e39 (fixed 60 epochs, 3 seeds). Disclosed in the caption, but the seed-0 random-key AUCs differ (0.913 vs 0.903), so the column is not within-run consistent. The e26 cost-guided counterpart (+0.008) is not what is in the table (+0.014).
7. MEDIUM. Leftover first-round text: Fig. method caption ("five detectors") and the TikZ diagram (detectors A, B, D, C, S only; "C CNN ... early stopping on val AUC"; payload 0.01 to 0.09; data box lists only IXI T1 and OASIS, no CT or 256x256; no F, M, K, SRNet-style, Yedroudj); related.tex comparison table row "five detectors"; the heatmap caption/figure shows only A, D, B, S and the first-round CNN (30 epochs, 5239 slices) with no F/M columns and its CNN Q1 cell (+0.01, 30 epochs) differs from the +0.014 in tab_main; fig_roc and fig_hill captions say "four detectors" (fine only if they show A, D, B, S). The abstract's "nine detector types" is not defined anywhere; counting A, D, B, S, F, M, K, residual, SRNet-style, Yedroudj gives ten (nine without SRNet-style, which gives no contrast).
8. LOW-MEDIUM. 0.37 percent changed pixels for the hybrid at 0.0027 bpp is not stored; e38_calib contains only 0.03, 0.04 and 0.05 bpp for HILL and S-UNIWARD. The hybrid share is an extrapolation (linear in the log). The 1 character message makes it plausible (40 raw bits vs 160 at 0.01 bpp) but it is a claim without a stored measurement.
9. LOW. 0.002 bpp (OASIS/CT) and 0.0027 bpp (equal-count hybrid) and 0.0025 bpp (256x256) are nominal labels; for 128x128 the first two embed the same single character (40 bits, 0.0024 bpp effective), so "0.002" and "0.0027" are one and the same payload with different labels. Explain once.
10. LOW. CT HILL numbers (0.81, 0.91 vs 1.00) are for 0.01/0.02 bpp (detector A), but sit in a paragraph about 0.002 bpp, and the same CT HILL result for D (0.896/0.947) is omitted.
11. LOW. K paragraph mixes seed-0 AUCs (0.852, 0.857, 0.783) with a 3-seed mean (0.844) in one list; should be 0.843 for seed 0.
12. LOW. Matched control "within 0.013": value is 0.0133 (F/M, 0.01 bpp); "within 0.007" for OASIS holds only for seed means (per seed to 0.011).
13. LOW. Runtime table: residual "37-50 min" vs stored 33.4-49.9; full SRM "1.5-6.5 min" vs about 1.6-8 min in the e37 log timings. tab_budget omits the V2 SRNet runs (e36) discussed in the text.
14. LOW. fig_protocol.png step 5: title text overlaps the body text (rendering defect). The protocol is described as "eight-step" and the figure shows eight steps; fine.
15. LOW. Not verifiable: CT scan-level split, the log's order beyond file position, calibration "no AUC used", provenance of "-0.197" and the first-round 30-epoch values.
16. LOW. Methods say the contrast bootstrap uses 1000 resamples; the V2 summary scripts (e38, e39 seeds, e41) use 500 and different seeds. Quoted intervals are consistent with this (e.g. -0.046 to -0.009) but the Methods statement is not true for those summaries.

## What I could not check

CT scan-disjointness, first-round numbers outside the V2 passages (e21/e22 30-epoch CNN, dose-response, refit bootstrap, T1, 256x256), figure image contents other than the heatmap and protocol, and any absolute timing beyond what is stored in JSON/log files.
