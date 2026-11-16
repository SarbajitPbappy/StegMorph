# Verification round 4 (independent recompute, 12 Nov 2026)

Scope: Overleaf/article/article.tex and refs.bib against results/e9..e19 JSON, results/holm/holm_v2.json, state/CLAIMS.md, results/NOVELTY_notes_round4.md, data/splits/*.npz, code/exp19_*.py. No article edits were made. Line numbers refer to article.tex unless stated.

## Defects, ranked

### HIGH
None. Every number in the abstract, the tables and the Holm counts that I recomputed matches the stored JSON, apart from the items below. No leakage or label problem was found.

### MED
1. **Line 323 (OASIS, "matched control stays within about 0.01 of the random key" for SPAM).** The JSON does not support this.
   - COSTMIX minus RANDSEQ for SPAM at 0.01 bpp is +0.0211 (seed 0, CI [0.003, 0.040]), +0.0063 and -0.0002.
   - The control therefore leaves the 0.01 band, and in seed 0 it is itself detectable at a 0.02-sized shift.
   - At 0.02 bpp it is -0.008 to +0.005, which is fine.
   - The conclusion "positional" still holds, because Q2 (cost-guided minus control) is -0.10 in seed 0, but the sentence must say "within about 0.02 (0.01 bpp) and 0.01 (0.02 bpp)".
2. **Lines 32, 303, 323, 340 (abstract and discussion), pre-registered H19a/H19d are not stated as not confirmed, and the SPAM result is not labelled exploratory outside Section 5.9.**
   - E19 outcome in CLAIMS: H19a and H19d NOT CONFIRMED, saturation on OASIS A/C/D, SPAM effect exploratory (no hypothesis was stated), H19b and H19c confirmed.
   - Line 323 says the IXI effect is "neither confirmed nor refuted" for these detectors. The pre-registered outcome is "not confirmed". Q1(D) = -0.007 to -0.009 at 0.01 bpp with CI below 0 but far from the -0.02 threshold.
   - The abstract says OASIS "reproduced the GA-key result ... so only the SPAM detector showed the position effect" without saying this was unplanned. The same applies to the RQ5 paragraph (line 340).
   - Suggested wording: "H19a and H19d were not confirmed; the SPAM gain is an exploratory, not pre-registered observation".
   - Calling the study a "replication" (line 303, table caption, RO5) is acceptable only with "partial".
3. **Line 213 and Table `tab:ablation` row 1 (COSTMIX versus random for detector D: "+0.014 and +0.015" / "+0.014 (D)").**
   - Stored values: Q3(D) at 0.01 bpp = +0.014, +0.002, +0.0148 (mean +0.010). At 0.02 bpp = +0.005, +0.008, +0.002 (mean +0.005).
   - "+0.014 and +0.015" are the maxima of the 0.01 bpp seeds, not per-payload figures.
   - Report "+0.002 to +0.015 (0.01 bpp), +0.002 to +0.008 (0.02 bpp)", or the means.
4. **Lines 244, 272, 336 and Table `tab:key` (CNN at 0.02 bpp "not run"; "fewer slices and epochs" CNN did show a gain).**
   - A 0.02 bpp CNN run exists in E14 (3000 slices, 15 epochs), with Q1(C) = +0.005, +0.007, +0.002. It is not full budget, but "not run" and "no 0.02 CNN run is available" are inaccurate. Say "full-budget CNN not run at 0.02 bpp".
   - The E14 CNN with intermediate budget (3000 slices, 15 epochs) showed NO gain at 0.01 bpp either (+0.010 to +0.019).
   - The -0.197 value comes from the verifier's reduced run (600 pairs, 4 epochs, seed 7, 300 test slices; COSTKEY validation AUC only 0.54, i.e. an undertrained CNN). The text "fewer training slices and epochs the CNN did show a gain ... the CNN budget is a decisive factor" reads as a graded budget effect that the data do not show. Reword to "a severely undertrained CNN behaves like SRM-lite".
5. **Line 244 (CNN CIs "include zero or lie above it").** All three E16 intervals include zero: [-0.005, 0.032], [-0.011, 0.024], [-0.004, 0.026]. None lies above zero. Delete "or lie above it".
6. **Line 299 (computational cost, "boosted-tree detector ... about 25 minutes" per seed).** The E17 logs and file timestamps give about 13 minutes per seed (stego build 422 + 133 s, detector fits to 522 s + 238 s; seed completion times 04:18, 04:31, 04:44). Use about 13 minutes. The other timings are correct: build 7.2 min, CNN about 20 min per scheme, 6947 s per seed, i.e. 1.9 h.
7. **Line 110 (Table `tab:related` caption: MOLSBM papers "read in full by text extraction (some pages by OCR)").**
   - NOVELTY_notes_round4.md says the IST 2024 paper lost its security-results page in extraction ("results tables NOT recovered") and mentions no OCR.
   - "Read in full" is too strong for sabeti2024molsbm. Write "read by text extraction; the security-results page of the IST paper was not recovered".
   - The OCR statement is not supported by the notes, so confirm it or remove it.
   - Line 93 (SPAM/SRM AUCs reported for the proposed method) and the "(proposed method only)" cell in the table are consistent with notes Table 8, and the "as available to us" hedge is appropriate.

### LOW
8. **Line 268 (HILL versus SPAM "0.535 against 0.566").** These are HILL versus COSTKEY (the best hybrid variant), and 0.535 is seed 0. Means: HILL 0.537, COSTKEY 0.566, random key 0.592, GA key 0.614. The sentence sits in a paragraph that compares with the random key (0.91 for the CNN), so state "against the cost-guided key (0.566); random key 0.592".
9. **Line 323 (HILL on OASIS "0.66 / 0.89 / 0.50").** Payload not stated. These are the 0.01 bpp values. At 0.02 bpp they are 0.84 (SRM-lite and trees), 0.98 (CNN) and 0.50-0.51 (SPAM). Add "at 0.01 bpp" or give both.
10. **Line 191 (round trip "verified on the GA, random, cost-guided and smooth-pixel keys").**
    - The scripts assert extraction only for the first 2 images of each of the train, validation and test sets (`if i < 2: assert`), at every payload.
    - The independent verifier checks (60/60 for GA, random, COSTKEY; 20/20 for ANTIKEY) were on IXI. OASIS round trip is covered only by the in-script assertion on 2 images per set. Add "(OASIS: first two images per split)".
11. **Line 195 and abstract ("claims written down before each experiment was run").** For the experiments reported this holds. CLAIMS shows that the E6b and E7 pre-registrations were written after earlier results had been seen. They are not in the paper, but the statement should be limited to "for the experiments reported here".
12. **Line 295.** The denemark2014selection citation supports selection-channel-aware detectors only, not "learned detectors"; the sentence stretches it. The CNN is not selection-channel-aware.
13. **Table `tab:oasis` uses `\hline` and `\resizebox`; other tables use booktabs.** Style only. One Overfull hbox of 11.4 pt at lines 254-265 (`tab:mse` region).

## Verified OK (recomputed from JSON)
- **OASIS table `tab:oasis`.** All 12 ranges recomputed independently from 'auc' across the 3 seeds in results/e19_oasis_cost and e19_oasis_anti, and they match.
  - GA minus random, all four detectors: 0.01 bpp -0.0170 (B seed 2) to +0.0007, i.e. -0.017 to +0.001. 0.02 bpp -0.0044 to +0.0046.
  - Cost-guided minus random: A -0.0071 to -0.0045; D -0.0094 to -0.0073; CNN -0.0002 to +0.0003; B -0.108 to -0.079 (0.01) and -0.170 to -0.150 (0.02). All B CIs lie below 0 (caption true).
  - Smooth minus random: +0.0018 to +0.0055 (0.01), about 0 (0.02).
  - The quoted lowest GA difference -0.017 with CI [-0.034, +0.003] is exact. The random-key AUC statement (A 0.996-0.997, D 0.992-0.994, C 0.9999, 1.00 at 0.02) is exact. Subject and slice counts are 242/52/53 and 3146/676/689.
- **IXI Table `tab:key` and ablation.** All ranges match E14, E16, E17 and E18.
  - Cost-guided A: mean -0.1453 and -0.1826.
  - D: -0.205 to -0.218 and -0.2005 to -0.2169.
  - C (E16): +0.0063 to +0.0128.
  - Smooth A and D ranges match.
  - GA key D: +0.0093 to +0.0194 and +0.0026 to +0.0066.
  - All smooth CIs lie above 0.
- **Abstract ranges.** 0.14 to 0.22 and 0.05 to 0.13 hold, with the minimum |Q1(A)| 0.142 and maximum Q1(D) 0.218. The CNN +0.006 to +0.013 holds.
- **MSE table `tab:mse`.** All MSE and PVD/LSB pair entries match the stats_test values (e.g. 0.0204/0.0408; 19.9/200.2; 28.1/184.0; HILL 0.0037/0.0080).
- **Holm.** The 30-test family in holm_v2.json gives 5 differences and 7 equivalences. Recomputed with SE x1.5 it gives 2 and 0, matching the text. All 7 equivalences have SE equal to the 0.005 floor. The listed survivors match (SPAM +0.033 at 0.05 bpp, SPAM +0.036 at 0.02 bpp, SRM-lite +0.016 at 0.01 bpp, two Q1 SRM-lite). E13 OASIS -0.035 has SE 0.033 and does not survive. The "earlier version 60 tests: 29/24 and 5/10" figures come from CLAIMS and were not recomputed (the old table uses a different SE definition).
- **Counts.** 403/87/87 subjects, 577 total, 5239/1131/1131 slices. Payload characters: 16 chars at 0.01 and 36 chars at 0.02 bpp are correct (3 x (32 + 8L) bits = 480 and 960, matching 20 PVD x 4 + 200 LSB x 2 pairs and 40 x 4 + 400 x 2). E16: 5239 slices, 30 epochs, 87 test subjects. CNN AUCs HILL 0.608 and random 0.9065 give "about 0.60 / 0.91". HILL SRM-lite LR difference -0.236 gives "-0.24".
- **MOLSBM/Sabeti description** (lines 93, 247, 295) is consistent with NOVELTY_notes_round4.md. The fewer-modifications mechanism is described, and no "first" or "no prior work" claim is made. The article says explicitly "no claim of priority" (line 84). No unqualified "first" or "equivalent" appears. Equivalence is qualified (SE floor, "not proven"). The paper does not claim H19a or H19d replicated.
- **Data and code integrity (OASIS and IXI).**
  - Subject sets in data/splits/oasis_{train,val,test}.npz are disjoint: 242/52/53 subjects, all pairwise intersections empty, no exact-duplicate images across splits (MD5), none inside a split either. The same holds for IXI (403/87/87).
  - The manifest flags jpeg_origin true for OASIS.
  - exp19_dataset_cost.py differs from exp14 by only the dataset variable, key naming and the added detector D (same features, boosted trees). exp19_dataset_anti.py differs from exp18 only by the dataset variable and key naming.
  - The test set is the same for all schemes (`Cte`, with one stego set per scheme). The message is the same across schemes for an image. Labels are cover = 0 and stego = 1 per image. The scaler is fit on training data only, and the CNN validation set `Cva` is separate and used only for checkpoint selection.
  - `mix_infeasible` is 0 for the test set (the fallback of COSTMIX to a random key occurred in 1 training image at 0.02 bpp only).
  - Cover/stego training pairs come from the training subjects only.
  - The OASIS `cls` field (dementia class) is not used as a label. The class balance (533/143/13 in test) is irrelevant to the cover/stego task.
  - The CNN trains on all 3146 slices for 30 epochs as stated.
- **LaTeX.** The temp copy compiled with pdflatex and bibtex, 9 pages, with 0 undefined references and 0 undefined citations (all 11 cited keys exist). Warnings: 1 Overfull hbox (11.4 pt, `tab:mse`) and 1 bibtex warning, "empty pages in li2014hill".

## Bibliography (refs.bib), incomplete or marked "to verify"
No metadata was invented or changed.
- fridrich2012rich (lines 65-71): note "to verify"; no volume, number, pages or doi.
- pevny2010spam (lines 73-79): note "to verify"; no volume, pages or doi.
- li2014hill (lines 81-87): note "to verify"; no pages or doi; bibtex warns "empty pages".
- vazquez2022 (lines 51-56): @misc; author "Vazquez et al.", title "(title and author list to be completed)", journal only in note.
- aljughaiman2026 (lines 58-63): @misc; authors collective placeholder, title "(title to be completed)", details "to be completed".
- karakis2023misteg (lines 89-94): @misc; author "Karakis and others", title "(full title and author list to be completed)". Journal data (CMC 74(3):4649) only in note.
- sabeti2021secure (lines 41-49): no doi. pages 70--82 cannot be checked against the notes.
- sabeti2024molsbm: pages 737--741 (5 pages) versus the notes' "6 pages". Not necessarily wrong, but check against the publisher.
- luo2010edge: no volume, number or pages. denemark2014selection: complete. sabeti2026isecure: complete.
- The top comment in refs.bib states that entries marked "to verify" come from general knowledge.
- Other manuscript placeholders: second author "Supervisor name to be completed", `\journal{...to be confirmed}`, Funding, Author contributions, Conflict of interest "to be confirmed", Data availability "public release details will be added".
