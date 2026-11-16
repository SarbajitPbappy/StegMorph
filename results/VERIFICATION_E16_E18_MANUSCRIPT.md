# Independent verification round 2: E16-E18, Holm v2, HILL validation, manuscript v0 (2026-11-12)

Read-only audit. Scratch scripts are in the session scratchpad (holm_ind.py, rt2.py, hv/). Nothing in code/, results/e*/, state/, Paper/ or notebooks/ was changed. Web was not used.

## A. CLAIMS.md sections

| Section | Verdict | Evidence |
|---|---|---|
| E16 OUTCOME | VERIFIED (scope as stated) | results/e16/e14_seed{0,1,2}.json: n_train_cnn 5239, epochs 30, C 0.01. Q1 = +0.0128 [-0.0048,+0.0322], +0.0063 [-0.0110,+0.0235], +0.0107 [-0.0043,+0.0259]; every number matches. RANDSEQ AUC 0.906/0.914/0.911, HILL 0.608/0.601/0.596. Caveat: no learning curve or convergence evidence (best epoch picked by val AUC, 30 epochs). The 0.02 bpp cell was not re-run. COSTMIX is more detectable than RANDSEQ for the CNN (Q3 +0.018, CI above 0, seed 0). |
| E17 OUTCOME | VERIFIED | Q1(D) 0.01 bpp: -0.205/-0.218/-0.2115; 0.02 bpp: -0.2169/-0.2005/-0.2158; every CI high is below -0.18. P1(D): +0.009/+0.015/+0.019 (0.01), +0.003/+0.003/+0.006 (0.02). All match. Q2 is about -0.22 and Q3 about 0, so the effect is positional. |
| E18 OUTCOME | numbers VERIFIED; "dose-response confirmed" and "texture-matched control defect addressed" PARTIALLY | Q4 (JSON name Q1_ANTIKEY-RANDSEQ): A 0.01 .124/.132/.121, D 0.01 .130/.119/.127, A 0.02 .068/.065/.064, D 0.02 .059/.057/.054, all CI low above 0.043. Q5 (seed 2): .116/.130/.072/.058 correct. The ANTIMIX control has the same pair counts as ANTIKEY (14.5/211.1 vs 14.5/211.0 at 0.01 bpp; 29.0/422.1 vs 29.0/422.0 at 0.02 bpp) and Q3 is about 0. Issues: (1) there are three points (low-cost, random, high-cost), so "dose-response" is a monotone ordering, not a graded dose. The 0.02 bpp ANTIKEY AUC is 0.98, so the effect is compressed by the ceiling. (2) The verifier-1 request was a control that separates "HILL cost" from "texture or region". ANTIKEY is the opposite pool by the same HILL cost, so cost and texture stay confounded. Nothing tests a non-HILL mask such as local variance or a tissue mask. I checked that the zero-valued-pixel share is only 0.2% in the ANTIKEY pool, so a background-zero explanation is unlikely. (3) E18 A-detector RANDSEQ/ORIG numbers are bit-identical to E14 (0.769, 0.783), because the seeds are deterministic. This is reproducibility, not independent replication. |
| HOLM v2 | arithmetic VERIFIED (5/30 differences, 7/30 equivalences); inference PARTIALLY | See section C and D. |
| HILL SIMULATOR VALIDATION | PARTIALLY | No stored output exists for it (only the CLAIMS text). I re-ran code/hill_validate.py after copying HILL.m into the scratch dir (Octave is unseeded). Result: 0.01 bpp Octave 0.00368 vs numpy 0.00330 (ratio 0.896, correlation 0.249); 0.02 bpp 0.00747 vs 0.00757 (ratio 1.014, correlation 0.700). CLAIMS says ratio 0.935/0.972 and correlation 0.24/0.33. So the agreement is about +-10% and varies run to run. "3 to 7 percent" is not a stable statement. Also CLAIMS says the payload is "before 3x redundancy", but len(_text_to_bits) includes the 3x redundancy (stegmorph.py:97-101, REDUNDANCY = 3), and exp14 comments agree with the code. The "HILL.m cost-map agreement (max rel err 1.7e-4, Spearman 0.99999)" has no stored artefact; grep over code/results/state found only the CLAIMS text. Detectability of Octave stego was not measured. |

## B. Manuscript v0 (Paper/MANUSCRIPT_DRAFT_v0.md)

Numbers traced to JSON (all OK unless listed under defects):
- 5.2: Q1 A -0.145 and -0.183 are 3-seed means (-0.1453, -0.1826). The D values match E17.
- 5.3: +0.119..+0.132 (0.01) and +0.054..+0.068 (0.02) match.
- 5.4: +0.013/+0.006/+0.011 match.
- 5.5 table: all 20 cells recomputed from stats_test of results/e14 (A, B and C runs give identical stats). They match to the printed rounding:
  - RANDSEQ: 19.9/200.2, MSE 0.0204 (0.01 bpp); 40.1/400.0, MSE 0.0408 (0.02 bpp).
  - ORIG: 26.9/186.3, MSE 0.0225; 53.0/374.1, MSE 0.0444.
  - COSTKEY: 28.1/184.0, MSE 0.0226; 56.2/367.6, MSE 0.0450.
  - COSTMIX: 28.1/183.9, MSE 0.0227; 56.2/367.5, MSE 0.0452.
  - HILL: MSE 0.0037 and 0.0080.
  - The "about 10 percent higher" claim matches (0.0226/0.0204 = 1.108).
- 5.1: P1 numbers match holm_v2 (E11 B 0.05 +0.033; E14 B 0.02 +0.036; E14 A 0.01 +0.016). The list of equivalences matches (A: E11 0.02/0.05, E14 0.02; C: E11 0.02/0.05, E14 0.01/0.02).
- Abstract "CNN AUC about 0.60 against 0.91" matches E16 (HILL 0.596-0.608, RANDSEQ 0.906-0.914).
- 5.6: HILL 0.535 vs COSTKEY 0.566 for B (seed 0) matches.
- Section 3 citations of the 20-slice cost check, and "3 to 7 percent" for distortion: not traceable (see A).

Defects and overclaims in the manuscript:
1. Abstract and 5.1 "never more secure than a random key". This is the wording the first verification asked to soften. Holm v2 makes the OASIS -0.035 non-significant, but "never" is still a universal statement from 30 cells, many inconclusive. Use "not more secure in any cell we tested; not robustly better".
2. Abstract "statistically equivalent to it" is floor-bound. All 7 surviving equivalences have SE exactly equal to the 0.005 floor (my re-run), and three involve AUC about 1.0 (E11 C 0.05, A 0.05, C 0.02; AUC 0.9996 for C at 0.05). With SE x1.5, 0 equivalences and 2 differences survive. The "+0.016 worse against SRM-lite at 0.01 bpp" survives only because of the floor (SE 0.005, Z = 3.3). Say "equivalence rests on a 0.005 SE floor and saturated detectors".
3. "Dose-response" (abstract/contributions/5.3): three levels, a ceiling at 0.02 bpp, and only SRM-lite features. The cost map vs texture confound is untested (see A).
4. Abstract and 5.6 "far less detectable than every StegMorph variant". The margin for SPAM at 0.01 bpp is small. HILL is an entropy-bound simulator without STC, it changes 6x fewer pixels (MSE 0.0037 vs 0.0226), and it is not matched on distortion. The sentence "does not make LSB/PVD hybrids competitive with content-adaptive embedding" is directionally plausible but is a stronger conclusion than a simulator at unmatched distortion supports.
5. The abstract says "three detectors", but four are used (A, B, C, D) and the body also names D. The abstract's CNN result is at 0.01 bpp only; the abstract does not say so.
6. Abstract "raises it by 0.06 to 0.13": the minimum is 0.054, so "0.05 to 0.13". Also "0.15 to 0.22": the minimum is 0.142 (A at 0.01 bpp), so "0.14 to 0.22".
7. Section 4 "IXI 578 subjects": the manifest gives 403+87+87 = 577.
8. Related work on Sabeti. "reports lower detectability than LSBM" under "SPAM, SRM, maxSRM and maxSRMd2" is not supported for the feature detectors. Results/NOVELTY_notes_round3.md says Table 8 (ISeCure 2026) has no baseline row, and round 4 says the extracted text shows only MOLSBM rows. The lower-than-LSBM claim is supported only for the LSBM-specific attacks (ker1, ker2, CNGL, ALE; Table 7). Also, JSCIT 2021 (2GA, 9(4) Winter 2021, confirmed from the PDF's first page) is an earlier GA-LSBM paper by the same authors, and the notes show its body is Persian and unread. "Earlier versions" is an inference. Persian MKGM is unreadable. The MOLSBM IST 2024 results page was lost in extraction.
9. Luo-Huang-Huang: described only as "texture/edge-guided selection is already published". This is fine (snippet-level in round 2; the PDF is not in Paper/; I could not check it). Denemark WIFS 2014: "abstract level only" is honest. The PDF is in Paper/, but the claim that selection-channel detectors are stronger is the abstract-level statement. Vazquez 2022 (doi 10.3389/frobt.2022.1031299): the PDF abstract confirms "GA, private key, no alteration of cover". "No steganalysis and no random control" comes from the notes, targeted extraction only. I did not re-read the full text.
10. Novelty wording: no "first" claim appears in the manuscript. Section 8 explicitly forbids it. Contribution (iii) "detector-dependence finding" and (i) "operator-matched control design" are not worded as novel. OK. Keep the "no paper found" caveat. Note that Sabeti's MOLSBM minimises modifications, a different mechanism, which the manuscript already says.
11. Section 7 is mostly complete but misses: (a) no SRM/SPAM/CNN ensemble with a real selection channel; (b) the equivalence margin of 0.02 is arbitrary and the SE has a floor; (c) no texture or region control other than the HILL-cost thirds; (d) the CNN null has no learning curve; (e) seeds change messages and keys only, not train data or test data; (f) E18 reuses the E14 seeds.
12. Header "Every number comes from stored JSON ... Not yet re-verified" is correct. Section 9 cites the notebook; not checked.

Contradictions with earlier documents: only item 1 (softening requested by verification 1) and the 3-to-7 percent HILL line (CLAIMS wording, not reproducible on rerun).

## C. Code review

- exp17_srm_hgb.py vs exp14_costkey.py: the diff is two lines (L99 `fc["D"] = (FA(Ctr), FA(Cte))` and L108-109 routing D to FA features). D uses the same SRM-lite features as A and `HistGradientBoostingClassifier(max_iter=150, lr 0.1, depth 4, random_state=seed)` (feat_fit, L82-86). So D is SRM-lite features plus boosted trees, as claimed. Note that with 10,478 training rows sklearn's default early_stopping='auto' turns on (n>10000), so a random 10% internal validation split (not subject-grouped) is used inside the training set; this is not test leakage.
- exp18_antikey.py vs exp14_costkey.py: the substantive diff is the cost_key pool (`[-(img.size//3):]` instead of `[: img.size//3]`, L51) plus renamed schemes and the D hook. ANTIKEY takes the highest-cost third (I confirmed on 20 test slices: mean pool cost 9.1e7 against a global mean of 3.0e7 and a lowest-third mean of 0.059). COSTKEY (exp14) takes the lowest third. ANTIMIX uses `used_pairs` on ANTIKEY and `mix_key` with its counts. The JSON confirms the pair counts match (see A). If `mix_key` is infeasible it falls back to the random key (`short` counter), and `mix_infeasible` is stored in the JSON; I did not enumerate it, but Q3 is about 0, consistent with few or no fallbacks.
- Leakage: train covers/stegos come from the train split (tag 11), val from val (12), test from test (13). Cover features are shared across schemes. The scaler is fit on train only. The message seed uses seed*10**7 + payload + image index + tag, so messages and keys differ between seeds and are identical across schemes within an image. The seeds do NOT change the train subset (n = 5239, all of it) or the test set; so "seeds" are not independent replicates of the data.
- Round trip: exp14/17/18 assert extract(embed) only for i < 2. My check (D below) covers 20 slices.
- holm_v2.py: SE = sqrt(mean bootstrap SE^2 + SD_seeds^2) with SE = CI width / 3.92 and floor 0.005: formula correct. TOST p = max(P(Z > (m+0.02)/se), P(Z < (m-0.02)/se)): correct. Holm step-down with a running maximum of (n-rank)*p, capped at 1: correct, applied separately to the difference and the equivalence families. Defects: (a) SE floor drives all 7 equivalences; (b) the normal approximation with 3 seeds (SD with 2 df) should use t(2) or a bootstrap; (c) the bootstrap SE does not shrink with seeds, but SD is not divided by sqrt(3), which is conservative, while neither covers training-subject resampling; (d) the family pools P1 (GA key vs random) and Q1 (cost key vs random) and includes ceiling cells; (e) Q1 p-values such as 1e-133 are not meaningful.

## D. Reproduction

- Round trip: ANTIKEY keys (cost_key from code/exp18_antikey.py) on 20 test slices (every 56th), 0.01 bpp, random messages: 20/20 extract(embed) == message.
- Holm v2 re-derived independently (scratch holm_ind.py, built directly from the JSON, not from holm_v2.py): n = 30, 5 differences (E11 B 0.05; E14 A 0.01 P1; E14 A 0.01 Q1; E14 A 0.02 Q1; E14 B 0.02 P1) and 7 equivalences. Cell diffs and SEs are identical to holm_v2.json (max abs deviation 0.0).
- Sensitivity: SE x1.5 gives 2 differences / 0 equivalences; SE x2 gives 2 / 0. Only the two SRM-lite Q1 contrasts survive that.
- HILL validation re-run: see A.
- Not done: full experiments, CNN retraining, web checks, the Persian papers, the IST 2024 results page.

## E. Verdicts and fixes

| Claim | Verdict |
|---|---|
| E16: CNN null at 0.01 bpp, full data | VERIFIED (no convergence curve; 0.02 not run) |
| E17: SRM-lite gain survives boosted trees | VERIFIED |
| E18: Q4/Q5 numbers | VERIFIED |
| E18: dose-response confirmed, texture control done | PARTIALLY |
| Holm v2 5/30 and 7/30 | VERIFIED as arithmetic; PARTIALLY as inference |
| HILL validation "3 to 7 percent" | PARTIALLY (rerun gives 10% and 1%; no stored artefact) |
| Manuscript numbers (abstract, 5.1-5.6) | VERIFIED except items 6 and 7 |
| Manuscript wording | PARTIALLY (items 1-4, 8) |
| Novelty framing | VERIFIED (no "first" claim) |

Defects ranked:
1. HIGH. Equivalence claims rest on an arbitrary SE floor and saturated AUCs (B2). Abstract wording must change.
2. HIGH. Sabeti related-work sentence implies a feature-detector comparison vs LSBM that the notes say is absent (B8).
3. MEDIUM. Cost-map vs texture/region confound not isolated; "dose-response" overclaims three points at a ceiling.
4. MEDIUM. HILL not matched on distortion and not run through a detector; the cost-map check and distortion check lack stored evidence; "before 3x redundancy" wording is wrong.
5. MEDIUM. Seeds do not resample data (train/test fixed), E18 reproduces E14 exactly; honest uncertainty needs training-subject resampling.
6. LOW. "Never more secure" universal; abstract says three detectors (four used) and omits the 0.01-bpp scope of the CNN result; range roundings (0.05/0.14); 578 vs 577 subjects; round-trip asserted for i < 2 only; CNN has no learning curve.

Before any SUCCESS_* state:
- Rewrite abstract/5.1 equivalence claims or compute equivalence with a defensible SE (cluster bootstrap with detector refit and training-subject resampling; t-based).
- Add a non-HILL texture or region control (local-variance mask; random key inside a tissue mask), and call E18 "monotone position effect", not "dose-response", until then.
- Store the HILL.m cost-map comparison and the distortion validation as JSON with fixed Octave seeds; correct "3 to 7 percent" and the redundancy wording.
- Fix the Sabeti sentence (LSBM-specific attacks only; Table 8 has no baseline) and mark 2GA/MKGM as unread bodies.
- Add learning curve (or a second CNN architecture) and a 0.02 bpp CNN run.
- Fix the abstract detector count, ranges and subject count; add the missing limitations (item 11).
- Keep the novelty gate: independent literature search still outstanding.
