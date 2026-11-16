# Novelty check, round 4 (12 Nov 2026): full-text read of the MOLSBM papers (written by this session)
Source files read in full by text extraction (pypdf), all in Paper/ (user-supplied):
- Sabeti & Faiazi, "MOLSBM: A Multi-Objective LSB Matching Steganography Method", IST 2024 (6 pages). Text extraction lost the security-results page; experimental setup read, results tables NOT recovered.
- Sabeti, "Enhancement of LSB Matching Steganography using Multiobjective Optimization Embedding to Improve Security and Imperceptibility", ISeCure 18(1), Jan 2026, doi 10.22042/isecure.2025.477842.1172 (journal version, 17 pages, read via extraction; tables 7 and 8 recovered).
- Sabeti & Faiazi, "Secure Image Steganography with High Visual Image Quality Based on LSBM and Genetic Algorithm", JSCIT 9(4), 2021 (14 pages) and MKGM (Persian, 12 pages): earlier GA-LSBM versions, abstracts only skimmed.

## What MOLSBM does and how it is evaluated
- Per block, NSGA-II picks (1) an 8-bit seed for a pseudo-random generator that selects embedding pixels whose LSB already matches the data bit (fewest changes) and (2) the +/-1 direction to minimise histogram change. Cover: NRCS natural-scene images (about 2,000; 1,000 test), random binary payload, MATLAB.
- Security evaluated in two ways: (a) Table 7, detection accuracy of classical LSBM attacks (ker1, ker2, CNGL, ALE) against LSBM, LCG, MKGM, 2GA and MOLSBM at 0.3, 0.5, 0.8 bpp; (b) Table 8, universal steganalysis (SPAM 686, SRM, maxSRM, maxSRMd2), AUC and test error at 0.05 to 0.3 bpp, reported for MOLSBM (the extracted text shows only MOLSBM rows, so a side-by-side with LSBM/random in Table 8 is not confirmed).
- No CNN steganalysis detector, no medical image, no subject-level split, no operator-matched random-key control (the seed search is the optimisation; the baselines are other methods, not a random-key version of itself).

## Consequences for our claim wording
- PRE-EMPTED: any claim that nobody has tested optimised pixel selection against SRM/SPAM-type steganalysis. MOLSBM does, and reports lower detectability than LSBM.
- NOT pre-empted: our design (GA contrast key in a hybrid LSB/PVD embedder, operator-matched random-key controls with equal PVD/LSB counts and equal payload, subject-disjoint MRI splits, CNN detector, detector-dependence with a smooth/textured dose-response). MOLSBM reduces the NUMBER of changed pixels (data bit already equals the LSB), which lowers detectability of LSBM through fewer modifications. That mechanism is different from a position effect at equal changes, so the two results do not contradict each other.
- A reviewer will ask: does a GA key reduce detection only because of fewer changes? In our runs RANDMIX/COSTMIX control the number of PVD/LSB pairs but we have not reported changed-pixel counts per scheme in the paper: add this as a table (mean changed pixels and MSE per scheme, from stats_test in the JSONs).
- Safe wording: "we test whether pixel-ORDER selection (no change in the number of modifications) improves security, with operator-matched random keys". Avoid: "first", "no prior work tests GA pixel selection against steganalysis".
- Related-work text to add: Sabeti & Faiazi 2024; Sabeti 2026 (ISeCure); Sabeti & Faiazi 2021 (JSCIT). Verify their baselines before describing results in detail.

Status: novelty remains OPEN-PROVISIONAL (narrow). Still outstanding: a verifier pass on the final wording, the 2021 and 2026 papers' Table 8 comparison, and an index-based search for other GA-LSB papers.

## Scope decision (12 Nov 2026)
Only English-language papers count for the novelty check (user decision). Dropped from the check: Sabeti and Faiazi 2GA body (JSCIT 9(4), 2021) and MKGM (Persian). Their English abstracts may still be cited. Remaining Tier 1 reads: Damghani 2021, Karakis SPCAC 2020, Vazquez 2022 full text, Aljughaiman 2026, MI-STEG metadata.
