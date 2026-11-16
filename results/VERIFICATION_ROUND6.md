# Verification round 6 (independent; no project file edited)

Scope: Overleaf/article (article.tex, sections/*.tex, tables/*.tex as of 13 Nov 16:45; discussion.tex was edited during the check), state/CLAIMS.md, results/e23..e35, e16/e21/e22, ga_stats.json, hill_validation_200.json, data/splits. All numbers recomputed from stored JSON/npz; nothing rerun. Line numbers refer to Overleaf/article/.

## 1. Numbers checked (seed means over 3 seeds unless stated; "T2" = IXI T2 128x128)

| # | Claim (file:line) | Article | Stored | Verdict |
|---|---|---|---|---|
| 1 | P1, A and D, 0.01 bpp (results:28, abstract) | +0.008, +0.012 | +0.0079, +0.0124 | MATCH |
| 2 | P1, A and D, 0.02 bpp | +0.008, +0.009 | +0.0081, +0.0094 | MATCH |
| 3 | P1 SPAM (B) 0.01 / 0.02 (results:28) | +0.029, +0.049 | +0.0289, +0.0495 (0.02 bpp lowest bound +0.025) | MATCH |
| 4 | Q1 A (0.01/0.02), D (0.01/0.02) (results:48) | -0.151,-0.181,-0.184,-0.193 | -0.1507,-0.1813,-0.1844,-0.1934 | MATCH |
| 5 | Q3 matched control within 0.005 on T2 (tab_hyp:7) | 0.005 | A/D/S 0.0015..0.0052 (seed means); per seed up to 0.010; SPAM +0.015/+0.018 | MATCH for seed means (A,D,S only) |
| 6 | Q4 A, D (0.01/0.02) (results:48, tab_replication) | +0.123,+0.068,+0.117,+0.059 | +0.1232,+0.0683,+0.1174,+0.059 | MATCH |
| 7 | Q4 SPAM / Q1 SPAM (results:48,63) | +0.068,+0.074 / -0.003,-0.019 | +0.0684,+0.0745 / -0.0032,-0.0194 | MATCH |
| 8 | Q1(S) T2 (results:65) | -0.072, -0.067; Q4(S) +0.143 | -0.0720, -0.0668; +0.1433 | MATCH |
| 9 | Q1(S) T1 | -0.017, -0.035 | -0.0174, -0.0353 | MATCH |
| 10 | HILL ref minus random A,D (results:124) | -0.237,-0.336,-0.276,-0.367 | -0.2365,-0.3359,-0.2759,-0.3672 | MATCH |
| 11 | S-UNIWARD range | -0.221 to -0.320 | A -0.221/-0.306, D -0.259/-0.320 | MATCH |
| 12 | Cost key above reference 0.07 to 0.17 | 0.07-0.17 | HILL 0.086-0.174, S-UNI 0.070-0.127 | MATCH |
| 13 | Payload Q1 A (results:88) | -0.151,-0.181,-0.098,-0.033 | -0.1507,-0.1813,-0.0976,-0.0327 | MATCH |
| 14 | Payload Q1 D | -0.184,-0.193,-0.073,-0.022 | -0.1844,-0.1934,-0.0733,-0.0216 | MATCH |
| 15 | P1 over payloads -0.000..+0.012; random AUC 0.77 to 1.00; smooth +0.005 at 0.05 | as stated | -0.0003..+0.0124; 0.769..0.9994; +0.0046 | MATCH |
| 16 | Dose f=0.7..0.1, A 0.01 (results:50) | -0.100,-0.135,-0.151,-0.156,-0.160 | -0.1002,-0.1354,-0.1507,-0.1563,-0.1601 | MATCH |
| 17 | Dose D range; smooth pools | -0.112 to -0.204; +0.054 to +0.147 | -0.1118..-0.204; +0.0542..+0.1474 | MATCH |
| 18 | Monotone in 7 of 8, eighth by 0.0001 | as stated | smooth A 0.02: Q4(0.2)-Q4(0.1)=+0.0101 | MATCH |
| 19 | Other maps Q1 (A, 0.01) -0.109..-0.142 | as stated | std -0.110, grad -0.115, ent -0.142, S-UNI -0.109 | MATCH |
| 20 | Other maps Q4 (A, 0.01) +0.095..+0.116 (results:50) | +0.116 max | std +0.117, grad +0.095, ent +0.114, S-UNI +0.121 | MISMATCH (max is +0.121) |
| 21 | GA objective table (tab_ga) all 7 rows x 4 cols; LSBK/LSBM vs same-embedder random | e.g. -0.027,-0.053,-0.147,+0.098 | recomputed identical (e.g. -0.0267,-0.0528,-0.1467,+0.0980) | MATCH |
| 22 | Mechanism 11.9% (sd 2.8%), 34.3% (results:30, abstract) | 11.9, 2.8, 34.3 | 11.85 (rounds to 11.9), 2.76, 34.29 (ga_stats.json) | MATCH |
| 23 | Refit A Q1 0.01 (results:164) | -0.142,-0.144,-0.143 | -0.1416,-0.1436,-0.1429 (e23, e31) | MATCH |
| 24 | Refit A Q1 0.02 | -0.195,-0.195,-0.194 | -0.1945,-0.1951,-0.1938 | MATCH |
| 25 | Refit A P1 +0.013,+0.010,+0.009; lowest bound -0.006 | as stated | +0.0130,+0.0104,+0.0091; -0.0058 | MATCH |
| 26 | Refit D Q1 -0.201 [-0.221,-0.181], -0.199; P1 +0.003 [-0.014,+0.020], +0.008; Q3 -0.007 [-0.022,+0.010], +0.007 | as stated | -0.2010 [-0.2210,-0.1812], -0.1985; +0.0033 [-0.0143,+0.0202], +0.0085; -0.0070 [-0.0218,+0.0097], +0.0072 | MATCH |
| 27 | CNN test AUC random 0.913/0.907, GA 0.910, cost 0.922/0.919 | as stated | 0.9134/0.9075, 0.9104, 0.9217/0.9188 | MATCH |
| 28 | CNN Q1 +0.008 [-0.010,+0.027]; seed 1 +0.011 [-0.006,+0.031]; P1 -0.003 [-0.012,+0.006] | as stated | +0.0083 [-0.0101,+0.0273]; +0.0113 [-0.0060,+0.0311]; -0.0031 [-0.0115,+0.0056] | MATCH |
| 29 | CNN HILL 0.603, -0.311 | as stated | 0.6026, -0.3108 | MATCH |
| 30 | tab_budget (epochs, minutes, val/test AUC, 0.60 M) | as stated | all 9 rows consistent with e26/*.json (best epoch printed 1-indexed) | MATCH |
| 31 | 30-epoch CNN Q1 +0.013,+0.006,+0.011; 2500 / 1000 slices +0.015, +0.016 | as stated | +0.0128,+0.0063,+0.0107; +0.0149; +0.0157 | MATCH |
| 32 | "600 pairs, 4 epochs, Q1=-0.197" | -0.197 | not in any results/ dir; only in VERIFICATION_ROUND4.md:29 and VERIFICATION_E10_E14.md:46 (a verifier's reduced run, val AUC 0.54) | MATCH, weak provenance |
| 33 | T1: random AUC 0.60/0.69; P1 +0.002..+0.018; Q1 -0.073,-0.126 / -0.093,-0.140; Q4 +0.082..+0.122 | as stated | 0.6045/0.6914; +0.0021..+0.0181; -0.0727,-0.1265/-0.0930,-0.1404; +0.0822..+0.1217 | MATCH |
| 34 | T1 lowest bound -0.030 (SPAM), -0.022 (A) | as stated | -0.0305 (B,0.01, seed 2), -0.0225 (A,0.02, seed 1) | MATCH (but see D2) |
| 35 | CT: AUC 0.996-1.000; |P1|<=0.001; Q1 -0.028..-0.010; HILL 0.81, 0.91 | as stated | 0.9958..1.0; <=0.0009; -0.0280..-0.0098; 0.807, 0.909 | MATCH |
| 36 | OASIS replication rows (tab_replication) | e.g. 0.997, -0.000, -0.006, +0.003 | 0.997, -0.0001, -0.0061, +0.0026 (A 0.01) etc. | MATCH |
| 37 | 256x256: random AUC 0.998-1.000; cost-guided 0.60 and 0.69 (A) | as stated | 0.9979/1.0; 0.598/0.692 (A) | MATCH |
| 38 | COSTFG minus RANDFG A 0.081,0.146; D 0.065,0.151; smooth fg +0.100..+0.116; matched control within +0.011 | as stated | -0.0810,-0.1464; -0.0648,-0.1508; +0.0996..+0.1159; max +0.0113 | MATCH |
| 39 | RANDFG "0.36 to 0.41 less detectable" than unrestricted (results:149) | 0.36-0.41 (both payloads) | 0.0025 bpp: -0.365 (A), -0.410 (D); 0.005 bpp: -0.243 (A), -0.271 (D) | MISMATCH (0.24-0.41) |
| 40 | "32% of pixels exactly zero; 128 crops 99% foreground" (results:149) | 32%, 99% | 256 test set 34.0%, train 33.5% zeros; 128 crop 98.3% foreground (5x5 mean>10), 99.9% non-zero; no stored result file | MISMATCH (small) |
| 41 | "gain overstated 2.5-fold" (discussion:17) | 2.5 | Q1 vs RANDSEQ / Q1 vs RANDFG: A 4.9, 2.1; D 6.8, 2.2 | MISMATCH (unsupported) |
| 42 | Change reversal 57%/61%/11%/9%, cost key 0.60, 35%, A margin 0.07 | as stated | 57.3/60.8/10.5/9.3%; 0.600; 35.4%; 0.0735 (e33_mechanism.json) | MATCH |
| 43 | HILL numpy vs Octave ratio 1.005/1.003, max prob diff 1.7e-5 | as stated | 1.0052/1.0027; 1.69e-5 | MATCH |
| 44 | Split sizes (tab_data), subject-disjointness | as stated | verified in data/splits/*.npz: train/val/test subject sets disjoint for ixi, ixit1, oasis, ixi256; counts match | MATCH |

## 2. Hypothesis table vs the pre-registered rules in state/CLAIMS.md

The caption (method.tex:73) says "Met" means the rule held "in every cell it covered". Several rows break this definition.

* H11 (tab_hyp:15) "Met (GA with cost fitness -0.02 to -0.055)". CLAIMS "E30 OUTCOME" (H30a) logged PARTLY MET: GAMIN (the faithful-budget distortion GA) gives -0.018/-0.019 at 0.02 bpp, above the -0.02 rule, without all-seed intervals below -0.02. More favourable than the rule allows. Relabel "Partly met (only the stronger-search GAMINS meets the rule)".
* H12 (tab_hyp:16) "Met ... one bound of Q3 for D is -0.022". H23c/H31 require the Q3 interval inside [-0.02,+0.02]; D (-0.022) violates it. Strictly "met with one exception". Also seed 0 of detector A (e23) used all 403 training subjects, while seeds 1,2 and D used the 80% draw (n_train_subjects in JSON), unlike the text in results:164.
* H13 (tab_hyp:17) "met at 256x256 with a foreground baseline". Logged: H34b FAILED its saturation condition (random AUC 0.998-1.0, not <0.99); H35a met in 3 of 4 cells (D 0.0025 bpp one interval reaches -0.0105) and is post hoc (E35 pre-registered after E34/E34b numbers); H32 on CT met for Q1 < -0.02 only in 1 of 4 cells (log: "partial"). The row should say "partly met".
* H9 (tab_hyp:13) "Met on IXI T1": log says H27b "NOT MET STRICTLY" and per-seed bounds fail in 4 of 24 seed-cells (see D2).
* H1 (tab_hyp:5): "two of 16 cells" is not a count that exists in the data: 2 of 8 detector-payload cells, 4 of 24 seed-cells (B 0.01 bpp, all 3 seeds: -0.0247,-0.0256,-0.0305; A 0.02 bpp seed 1: -0.0225).
* H3 (tab_hyp:7): rule |Q3|<=0.02 shown "Met (within 0.005 on T2)" only for A/D/S seed means; SPAM Q3 is +0.015/+0.018 with intervals to +0.044, OASIS SPAM up to +0.021 (VERIFICATION_ROUND5), D on 256 foreground seed 0 +0.029.
* H5 (tab_hyp:9): the pre-registered rule H26a covers both networks and both seeds; the SRNet-style half failed to train. "Met for the residual network" is accurate but should state "SRNet-style: not evaluable". The failed-run rule that the article calls "pre-registered" (results:67) was logged after the failure was seen (E26 AMENDMENT 2, "after the first runs"), though before the repeat runs.
* H8 (tab_hyp:12): rule text (">0.10 below the hybrid keys") is not the logged rule (H24a: >0.10 below RANDSEQ; H24c: cost key > 0.05 above reference). The log says CONFIRMED; the table says "Partly met" (more conservative, acceptable) but rewrites the rule after the fact.
* H6 (tab_hyp:10): rule "non-decreasing within 0.01" fails in 1 of 8 series by 0.0001; "Met ... monotone in seven of eight" is disclosed; acceptable.
* H2, H4, H7, H10 agree with the log (H7 reported honestly as not met on T2).

## 3. Anti-leakage
Verified: subject-disjoint splits (build_ixi_splits.py asserts disjointness; recomputed overlap from the npz files = 0 for ixi, ixit1, oasis, ixi256; CT is scan-disjoint by MedMNIST's official split, no IDs). lab24.seed_train_idx subsamples 80% of training subjects (seed+777) so a subject's cover and all stego versions stay together. exp24.py fits StandardScaler/LogReg/boosted trees on training rows only (lines 42-43) and scores test; the CNN (nets26.train, cnn_mps.fit_predict) restores the best-validation-AUC checkpoint and test is only predicted afterwards; early stopping uses validation AUC; all six 60-epoch residual runs used the full 60 epochs (stopping never fired). Refit bootstrap keeps cover and stego rows of a subject together (exp31_refit.py). No test-set model selection found. Residual points: (a) feature-detector hyperparameters (C=0.05; boosted-tree depth 4, 150 iterations) are hard-coded and their origin is not documented in the log; (b) the E26 amendment (patience 15 -> 20, 100 -> 60 epochs) followed a result that was seen (first attempt, test AUC 0.8816, discarded), disclosed but a researcher degree of freedom; it applies equally to both arms.

## 4. Append-only log
No evidence of in-place edits: every pre-registration (E2..E35) precedes its outcome entry, later corrections are appended ("E23 clarification", "Corrections to this log" in VERIFICATION ROUND 5, "E26 AMENDMENT 2"), E35 and E34b are explicitly labelled post hoc relative to E34, and the E29 payload change 0.10 -> 0.09 bpp is stated in the outcome. Text order cannot prove immutability (single-author file, no hashes or external time stamps; CLAIMS.md was modified at 16:41 today). The article's claim "written before each experiment" (abstract, method.tex:68) should note that E34b, E35 and the E26 failed-run rule were added after related results were seen.

## 5. Overclaiming search
"first": only author-contribution lines (article.tex:23,60) and "first/second" in intro:7 - fine. "state of the art", "novel", "prove", "always", "never", "far less": none in the current text (the "far less" wording was removed; results:147 "far less detectable" for HILL on CT is a measured contrast, OK). "never": results:28 "never measurably more secure", results:88 "never helped at any payload" - supported (P1 range -0.0003..+0.012), but "never helped" is not an equivalence claim and T1 SPAM bounds reach -0.030. Judged items:
* intro:21, abstract, conclusion, discussion:7: "absent for a fully trained CNN"/"leaves a trained CNN unmoved". Evidence: one 0.6 M-parameter residual net, 2 seeds at 0.01 bpp (GA-key CNN only seed 0, no CNN at 0.02 bpp except the older 30-epoch run); the SRNet-style net could not be trained on the random-key set; the article itself shows a short-budget CNN does show the gain. Overstated; say "for one residual CNN".
* discussion:3 "its key behaves like a random key", results:30 "for practical purposes a random key": the GA key has 35% more PVD pairs (27.0 vs 20.0, tab_change) and 10% higher MSE, is 15% shorter after repair (ga_stats len_ratio 0.849, not reported) and is slightly more detectable (P1 +0.008..+0.012, SPAM +0.03..+0.05). Position-wise true, overall overstated.
* discussion:17 "2.5-fold" unsupported (see row 41). discussion:7 "(0.60 ... 0.07)" is one seed, 400 slices, descriptive (stated).
* limits:28 says "a strict reading of two pre-registered rules fails"; at least H11, H12, H13, H27b (4 of 24 seed cells), H34b, H26a(SRNet), H32 also fail strictly. Understated.
* Novelty wording (related:21, discussion:13) is bounded and consistent with results/NOVELTY_final_analysis.md; no priority claimed.

## 6. Citations
All 29 cite keys used in sections/*.tex, tables, article.tex exist in refs.bib; no unused keys. Descriptions in related.tex agree with results/NOVELTY_* notes for Sabeti (2021/2024/2026), Aljughaiman PSO (160 pairs, two CNNs, chance with and without PSO), Alrawashdeh (three CNNs, full model only), Vazquez, Ambika (5 images, no steganalysis), Ozcan, Karakis, Apau (125 studies), Luo, Alnajjar. Discrepancies: related.tex:7 says the ACO paper's CNN detectors are "at chance for all modes", but notes (NOVELTY_final_B B10) say CNNs were run for ACO and "without ACO" only (random-index mode judged on PSNR only; the Table 1 row is right). Damghani is tabulated "medical (JPEG)" although notes record only three MRI images for illustration and the 1000-image security set's source is unstated (round 5, line 106).

## 7. Spot checks
* CNN "null": seed 0 +0.008 [-0.010,+0.027], seed 1 +0.011 [-0.006,+0.031]; lower bounds exceed the -0.02 rule, so "no gain larger than about 0.01-0.02 AUC" is supported for this network and budget. The interval is a test-subject bootstrap with a fixed trained net (no training variance); two seeds only; point estimates are positive, i.e. nothing like the -0.15 to -0.19 of feature detectors. "Null" is fair; "absent for a CNN" in general is not.
* Refit bootstrap: values and intervals recompute; claim "does not widen the intervals enough to change a conclusion" holds for A; for D one seed, 60 replicates, Q3 bound -0.022 violates the pre-registered band (disclosed in tab_hyp only). Seed 0 of A used the full training set.
* 256x256 foreground: Q1 numbers recompute; matched control OK; effect larger at the higher payload; D at 0.0025 bpp one interval above -0.02 (disclosed). The foreground thresholds (5x5 mean > 10) were fixed before E35 but the arm itself is post hoc, which the article does not say. The "32%/99%" background figures are not in any stored result (recomputed 34%/98%).

## Defects ranked

HIGH
1. method.tex:73 and tables/tab_hyp.tex:5,13,15,16,17: caption defines "Met" as holding in every cell, but H1, H9, H11, H12, H13 (and H3, H6) are marked Met although cells fail; H11 contradicts the log label PARTLY MET and H13 hides the failed H34b saturation condition and H32 (3 of 4 CT cells). Fix: use "Met / Partly met / Not met", relabel H11 and H13 "Partly met", H9 and H12 "Met with exceptions", and redefine the caption.
2. tab_hyp.tex:5 and results.tex:145 ("two of 16 cells"): count not reproducible. Fix: "2 of 8 detector-payload cells (SPAM at 0.01 bpp, A at 0.02 bpp); 4 of 24 seed-level intervals". Also results.tex:28 "no point estimate below -0.003" holds only for seed means (A 0.02 seed 1: -0.0092).

MEDIUM
3. article.tex abstract/highlights, intro.tex:21, discussion.tex:7, conclusion: CNN claims generalised from one residual architecture (2 seeds, 0.01 bpp); say "a residual CNN trained from scratch" throughout.
4. discussion.tex:17 "2.5-fold" unsupported (2.1 to 6.8 by detector and payload). Give the range.
5. results.tex:149 "RANDFG 0.36 to 0.41 less detectable": true only at 0.0025 bpp; at 0.005 bpp 0.24 (A) and 0.27 (D). Fix the range or split it.
6. discussion.tex:28 (limitations) understates failed rules (see H11, H12, H13, H27b, H26a, H32, H34b); list them or point to Table 1.
7. method.tex:68 / abstract "claims written down before each experiment": state that E34b, E35 (foreground arms) and the SRNet failed-run rule (results.tex:67 calls it pre-registered) were added after related results were seen.
8. discussion.tex:3 / results.tex:30 "key behaves like a random key / for practical purposes": qualify; the GA key uses 35% more PVD pairs and is 15% shorter after repair.

LOW
9. results.tex:50 Q4 range "+0.095 to +0.116" should end at +0.121 (S-UNIWARD map).
10. results.tex:149 "32% ... 99%": stored images give 34% zeros (256 test set) and 98.3% foreground (128 crops); add the figure to a result file.
11. results.tex:67 "-0.197" for the 600-pair net rests on a verifier note, not on a stored results file; either store it or cite as "a reduced run".
12. results.tex:164: seed 0 of the refit bootstrap (e23) used all 403 training subjects, seeds 1 and 2 an 80% draw; state it. Q3 "within 0.005" is 0.0052 for seed 0.
13. related.tex:7 "CNN detectors at chance for all modes" -> "for the ACO and no-ACO modes"; table row Damghani "medical (JPEG)".
14. tab_hyp.tex:12 (H8) rule text differs from the logged rule H24a/H24c.
15. Detector hyperparameters (exp24.py:42-43) undocumented; add one sentence stating they were fixed a priori or tuned on validation.

## Verdict
Supported (recomputed, or MATCH on 40 of 44 checks): all headline P1/Q1/Q3/Q4 values for A, D, S, SPAM at 0.01/0.02 bpp; payload sweep; dose-response; GA-objective and other-embedder table; mechanism 11.9% and 34.3%; refit-bootstrap numbers; CNN numbers including seed 1 and the budget table; T1, CT, OASIS and 256x256 numbers; reference HILL / S-UNIWARD contrasts; change-reversal numbers; split disjointness and checkpoint-on-validation protocol; citations exist and are described accurately (two small wording issues). The core finding (GA key gives no gain; position gives a large, detector-dependent gain) is well supported.
Overstated or inconsistent: the hypothesis table's "Met" labels (H11, H13, H9, H12), "two of 16 cells", CNN generality, "2.5-fold", the RANDFG range, "behaves like a random key" without qualification, and the limitations paragraph's account of failed pre-registered rules.
