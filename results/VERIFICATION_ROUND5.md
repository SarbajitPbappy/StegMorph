# Verification round 5 (independent recompute, 13 Nov 2026)

Method: every new number recomputed from results/e20, e21, e22_n1000, e22_n2500, e16, e19_oasis_cost, e19_oasis_anti, e23 with `.venv_py314/bin/python -I`; PDFs re-extracted with pypdf; code diffed; article compiled in a temp copy (pdflatex, bibtex, pdflatex x2).

## Defects (severity ranked)

HIGH
- None found in the numbers. All new numerical claims match the stored files (see "Verified OK").

MED
1. article.tex:93 misattributes a finding. "a particle-swarm selection study reports near-chance detection for both the optimised and the random arm on a small test set (aljughaiman2026)". The PSO paper (PMC12873396, key aljughaiman2026) has a "without PSO" baseline (default LSB replacement, Tables 2, 8, 10, 12), not a random-key arm; NOVELTY_notes_round5 records "random baseline: not found in text". The random-index ablation belongs to the ACO paper (aljughaiman2026aco). Replace "random arm" with "without-PSO arm", or delete the sentence: lines 93 and 95 also cite vazquez2022 and aljughaiman2026 twice (redundant).
2. article.tex:219 (unfixed round-4 defect #3): "+0.010 at 0.01 and +0.005 at 0.02 ... with single-seed maxima of +0.014 and +0.015". Stored Q3(D): 0.01 bpp = +0.014, +0.002, +0.0148; 0.02 bpp = +0.005, +0.008, +0.002. +0.014/+0.015 are both 0.01 bpp maxima; the 0.02 maximum is +0.008. Reads as per-payload maxima, which is wrong.
3. refs.bib sabeti2024molsbm: pages {737--741}. The IST proceedings page range printed in ISeCure ref [51] is 738-743 (round-C notes: page footers garbled). Unresolved conflict; check with IEEE Xplore.
4. Ozcan et al. (article.tex:103, ozcan2020svm): body is Turkish; characterisation ("fixed embedding order, results pooled") rests on a Turkish-text read (it is correct: six scan-order/region LSB variants, accuracy pooled), but the limitations (line 352) and the Table~related note say sources in other languages "were not assessed", and the paper is absent from the table. Either add it to the table with a "Turkish body, read by the author" note or state the exception.

LOW
5. H22 (CNN learning curve; pre-registered prediction: Q1(C) more negative as training shrinks) is NOT supported (stored Q1 = +0.016, +0.015, +0.010, direction opposite). The article reports the numbers honestly (article.tex:250, 342) but never names H22 or says the pre-registered prediction failed. H19a and H19d are disclosed (abstract, line 329, 346). Add one sentence for H22.
6. article.tex:209 "Every experiment used three seeds" conflicts with E23 (one seed, line 352 discloses it).
7. CLAIMS.md E20 outcome: A at 0.01 bpp "-0.097 to -0.112" is wrong (stored -0.097, -0.101, -0.107). The article's pooled "-0.097 to -0.117" is correct. CLAIMS.md E19 outcome says SPAM matched control "within about +/-0.01"; stored max is +0.021 (seed 0, 0.01 bpp), which the article states correctly. CLAIMS entries are stale, not the article.
8. article.tex:301: denemark2014selection (selection-channel-aware rich models) is cited for "the known strength of ... learned detectors"; the paper concerns hand-crafted SCA features, not CNNs. Cite boroumand2019srnet or drop.
9. "full-budget CNN" (30 epochs) versus SRNet's 457+114 epochs (SRNet p5): limits (line 352) and further work mention "longer schedules", so disclosed; consider "all-slice" instead of "full-budget".
10. E19 OASIS 0.02 bpp: COSTMIX fell back to RANDSEQ for 1-2 training images in seeds 0, 1 (mix_infeasible [1,0], [2,0]); negligible but undisclosed. E23 discards the infeasible counter (code/exp23_refit_bootstrap.py, `str_, _, _`).
11. Abstract "AUC difference up to +0.036" for SPAM is a seed mean (earlier experiments); per-seed maximum is +0.039 (E14 B 0.02 bpp). Say "mean".
12. Limitations do not list the JPEG-derived OASIS covers (stated only at line 141 and 329) nor the 53-subject test size.
13. refs.bib incomplete: luo2010edge (no volume, number, pages; article read at abstract level), li2014hill (pages; bibtex "empty pages" warning), ozcan2020svm (pages, DOI from PDF metadata, conference not printed; empty pages warning), alrawashdeh2026texture (volume, pages: in press), sabeti2021secure (no DOI, none found), holub2014suniward (article number), sabeti2024molsbm (pages, item 3). The file header still says "to verify".
14. Compile: 10 pages; no undefined references or citations; 2 bibtex warnings (empty pages: li2014hill, ozcan2020svm). One Overfull hbox 11.4 pt at article.tex:255-271 (Table mse, column too wide). Many underfull boxes in Table related (lines 114-129), cosmetic.
15. Placeholders remaining: article.tex:14 journal; :23 supervisor name; :24-29 empty postcode/address; :359 data availability ("public release details will be added"); :362 author contributions; :365 funding; :368 conflict of interest "(to be confirmed)"; :371 AI statement ("must be reviewed against the target journal's policy").

## Verified OK
- E20 (results/e20): Q1(A) -0.097 to -0.117; Q1(D) -0.118 to -0.162, all 3 seeds, both payloads, all CIs below -0.02; Q3 max +0.0191 (D, 0.01, seed 0), so "within 0.02" holds. "About two thirds" holds (A ~0.70/0.63, D ~0.75 of the HILL effect).
- E21: Q1(C) +0.0083, +0.0053, +0.0030, CIs include 0; random-key AUC 0.9793 to 0.9824.
- E22/E16: mean Q1(C) +0.0157 (n=1000), +0.0149 (2500), +0.0099 (5239); random AUC 0.851, 0.887, 0.910.
- E23: Q1 -0.1416 [-0.1583,-0.1239], -0.1945 [-0.2092,-0.1787]; P1 +0.0130 [-0.0005,+0.0277], +0.0063 [-0.0047,+0.0179]; Q3 +0.0052, +0.0037 (within 0.02); NB=200.
- OASIS table: all ranges (GA, cost-guided A/D/C/SPAM, smooth A/D) and caption ("every interval below zero for SPAM") match; HILL AUCs (0.66, 0.66, 0.89, 0.50); lowest P1 -0.017 [-0.034,+0.003]; matched-control max +0.021. SPAM result labelled exploratory (abstract, line 329, 346).
- H19a, H19d disclosed as not confirmed; H19b (confirmed, uninformative) and H19c consistent with data.
- Quotes spot-checked in the PDFs (9): STC p13 ("smooth regions ... highly detectable ... hard-to-model", Paper STC lines 1138-1141); Rich Models ("hard-to-model regions"); SRNet ("importance of using larger training datasets", 457 epochs); Texture paper (Xu-Net, SR-Net, Ye-Net, fixed seeds 2025/42, chance accuracy); Ambika (five medical images, no steganalysis); Damghani (J-UNIWARD, UED; IET 15:705-714); Karakis (S-UNIWARD, HUGO, MIPOD, epilepsy datasets, 3064 test images from a different dataset); Apau (125 articles); ISeCure/MOLSBM Table 8 only proposed method, mismatch objective = modification count; PSO/ACO 160 training pairs, 20 test pairs, deterministic selection-channel admission (PSO p23).
- Bibliography DOI/volume/pages match the printed metadata in the novelty notes except items 3 and 13.
- Code: exp20 differs from exp17 only in the docstring and `cost_key` (highest 3x3 local std third, same stable sort, permutation, even length); HILL benchmark, COSTMIX pair counts, labels (cover=0, stego=1), subject-disjoint splits, 87 test subjects unchanged; mix_infeasible [0,0] in all E20 runs. exp23 keeps stego generation identical (tags 11/13, same RNG), uses the same resampled train/test index sets for every scheme, resamples subjects with all their rows (cover plus all stego versions) together, refits scaler and logistic regression per replicate, labels cover=0/stego=1.
- Wording: no unqualified "first", "novel", "no prior work", "state of the art", or "equivalent"; priority disclaimer at line 84; "known principle" framing in contributions; English-only scope, no selection-channel-aware detector, single modality, E23 single seed/detector A, and E22 one architecture all appear in Limitations (line 352).
