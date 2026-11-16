# Verification round 3 (2026-11-12): manuscript v0 after round-2 fixes

Read-only audit; nothing else changed. HILL validation run twice in own scratch dirs.

## 1. Round-2 defects vs current Paper/MANUSCRIPT_DRAFT_v0.md
| # | Defect | Status | Evidence |
|---|---|---|---|
| 1 | "never more secure" (abstract) | NOT FIXED | Abstract still: "the GA key is never more secure than a random key". 5.1 itself is fine. |
| 2 | "statistically equivalent" floor-bound | PARTLY | Abstract now says "indistinguishable ... (within +/-0.02 AUC under our primary analysis; this equivalence is not robust to a more conservative standard error)". Still says "indistinguishable"; floor/saturated AUC (E11 C/A 0.05) not named in abstract; 5.1 lists equivalences with no caveat (caveat only in 7b). |
| 3 | "dose-response" | NOT FIXED | Contributions (iii) "with a dose-response check" and heading "5.3 Dose-response (E18)" remain; only 7b notes three points + ceiling. Abstract avoids the word. |
| 4 | "far less detectable than every StegMorph variant" | NOT FIXED | Abstract unchanged; no caveat that HILL is an entropy simulator at unmatched distortion (table 5.5 shows MSE 0.0037 vs 0.0226 but abstract does not). Last abstract sentence ("does not make LSB/PVD hybrids competitive") still strong. |
| 5 | three vs four detectors; CNN scope | PARTLY | Fixed: "four detectors" listed. CNN 0.60 vs 0.91 and +0.006..+0.013 still lack "at 0.01 bpp" in the abstract (stated in 5.4/section 7). |
| 6 | ranges | FIXED | "0.14 to 0.22", "0.05 to 0.13". JSON: Q1 cost-key A/D 0.142..0.218; ANTIKEY A/D 0.054..0.132. |
| 7 | 578 subjects | FIXED | "577 subjects", "403/87/87"; manifest 403+87+87 = 577. |
| 8 | Sabeti sentence | PARTLY | Fixed: lower detection only under ker1/ker2/CNGL/ALE; "no LSBM baseline row ... not confirmed". Not fixed: "Earlier versions: ... JSCIT 9(4), 2021" still stated as fact (Persian body unread); "read in full by text extraction" overstated (round-3/4 notes: IST 2024 results page lost, Table 8 no baseline). |
| 9 | Luo/Denemark/Vazquez | FIXED (as honest labels) | "abstract level only" retained. Not re-read by me. |
| 10 | novelty | FIXED | No "first"/"novel" claim; section 8 forbids it. |
| 11 | Limitations | PARTLY | 7b added: SE floor, 3-point dose-response, no non-HILL control, no CNN learning curve, no 0.02 CNN. Section 7 has selection channel, test-subject-only bootstrap, shared test subjects. Missing: E18 reuses E14 seeds (bit-identical A numbers = reproducibility, not replication); seeds do not resample training data; 0.02 margin arbitrary. |
| 12 | header "not yet re-verified" | PARTLY | Header still says "Not yet independently re-verified after E16 to E18" (stale but conservative). |
| HILL | "3 to 7 percent" / 3x redundancy wording | FIXED in manuscript | Now "ratio ... between about 0.9 and 1.0 ... varies between runs and evidence not yet stored". "3 to 7 percent" no longer in Paper (grep). BUT section 3 still asserts cost-map agreement "max relative error 1.7e-4, Spearman >= 0.99999 on 20 slices" with no stored artefact (unverifiable). |

## 2. Number re-check (abstract + section 5) against JSON
All match: 403/87/87 (manifest); 5/30 differences and 7/30 equivalences (holm_v2.json: p_holm<.05 = 5, p_tost_holm<.05 = 7); 5.1 values +0.033 (E11 B 0.05), +0.036 (E14 B 0.02), +0.016 (E14 A 0.01), OASIS -0.035 (SE 0.033, not significant); Q1 A -0.145/-0.183 (means of -0.144/-0.142/-0.149 and -0.185/-0.182/-0.181); E17 D 0.01: -0.205/-0.218/-0.211 (printed -0.212, JSON -0.2115, rounding), 0.02: -0.217/-0.201/-0.216; ANTIKEY-RANDSEQ 0.01 bpp A/D 0.119..0.132, 0.02 0.054..0.068; CNN Q1 +0.013/+0.006/+0.011 (E16); CNN AUC RANDSEQ 0.906-0.914 vs HILL 0.596-0.608; B HILL 0.535 vs COSTKEY 0.566 (seed 0; 3-seed means 0.537/0.566); ranges 0.14-0.22 and 0.05-0.13 correct; 577 correct. Table 5.5 verified in round 2 (not recomputed).
Wording nits: "COSTMIX about 0" is true for A (-0.004..+0.007) but D shows +0.014/+0.015 (CI above 0) at 0.01 bpp and the CNN +0.018 (seed 0); ANTIMIX A seed 0 +0.017 CI above 0. Small relative to -0.2, but not "0".

## 3. Overclaim scan
"never more secure" (abstract, NOT FIXED); "equivalent"/"indistinguishable" (abstract, caveated but still headline; 5.1 uncaveated); "dose-response" (contributions iii, 5.3 heading); "CNN null": 5.4 states it depends on training budget and only 0.01 bpp (good), abstract says "sees no gain" without scope; "novel"/"first": absent (OK).

## 4. hill_validate.py rerun (HILL.m copied to scratch; Octave unseeded; numpy side seeded)
Run 1: 0.01 bpp Octave 0.00353 vs numpy 0.00330 (ratio 0.935, corr -0.081); 0.02 bpp 0.00760 vs 0.00757 (ratio 0.996, corr 0.596).
Run 2: 0.01 bpp 0.00364 vs 0.00330 (ratio 0.906, corr 0.507); 0.02 bpp 0.00757 vs 0.00757 (ratio 1.000, corr -0.117).
(Round 2: 0.896/1.014.) Ratios stable within roughly 0.90-1.01, consistent with manuscript "between about 0.9 and 1.0" (1.014 slightly above). Per-slice correlation is NOT stable (-0.12..0.70) over 12 slices, so no per-slice agreement can be claimed. Script has no output artefact and one redundant Octave call per slice. Mean-level agreement only.

## 5. Still required before the abstract can be called verified
1. Replace "never more secure" with "not more secure in any cell tested".
2. Rewrite "indistinguishable/equivalent" to name the 0.005 SE floor and near-saturated detectors, or recompute with t/refit-aware SE.
3. Rename "dose-response" (contributions + 5.3) to "monotone position effect" until a non-HILL texture control exists.
4. Qualify "far less detectable than every variant" (unmatched distortion, simulator, no STC) and soften the final sentence.
5. Add "at 0.01 bpp" to the abstract CNN statements.
6. Fix Sabeti: "earlier versions" as inference, no "read in full" claim.
7. Store HILL cost-map and distortion checks as JSON/log files, or drop the 1.7e-4 / 0.99999 numbers.
8. Add missing limitations (E18 reuses E14 seeds; train data not resampled; 0.02 margin arbitrary); update header status.
9. Open items from CLAIMS: non-HILL texture control, training-subject bootstrap, CNN learning curve and 0.02 bpp run, independent literature search.
