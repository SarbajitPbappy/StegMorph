# Novelty analysis, final (13 Nov 2026) — decided on the papers already collected, no new search

Sources used: 8 classics and 11 medical/metaheuristic papers read in full (NOVELTY_final_A/B/C), Luo 2010, HILL 2014 and Alnajjar 2025 read in full, 244 abstracts from the authors' Scopus and Web of Science exports, 960 Crossref records. This is a targeted novelty check, not a literature review.

## 1. What is NOT ours (do not claim)
| Item | Established by |
|---|---|
| Changes in textured pixels are harder to detect than changes in smooth pixels | Filler 2011 (STC, p13), Holub 2014 (UNIWARD, p1), Fridrich and Kodovsky 2012 (p9, p13) |
| Position-adaptive embedding beats random-position embedding under trained feature detectors | Luo 2010 (edge-adaptive LSBM against LSB/LSBM/LSBMR/PVD at pseudo-random positions) |
| Selection-channel-aware detectors reduce the advantage of adaptivity | Denemark 2014, Sedighi 2016 (MiPOD, p7-8) |
| Deep residual detectors beat feature detectors on adaptive schemes | Boroumand 2019 (SRNet) |
| CNN or SVM steganalysis of brain MRI exists | Karakis 2023, Ozcan 2020, Chen 2024, Zhou 2024 |
| Metaheuristic (GA, PSO, ACO) pixel or position selection in LSB/PVD, judged on PSNR, SSIM, RS | Kanan 2014, Roy 2015, Sabeti 2021/2024/2026, Aljughaiman 2026 (x2), Alrawashdeh 2026, Ambika 2020, Damghani 2021, Vazquez 2022 |
| Stating that high-contrast locations resist steganalysis | Alnajjar 2025 (asserted, no steganalysis experiment) |

## 2. Contribution by contribution
| # | Contribution | Closest prior work | Gap that remains | Status and recommended wording |
|---|---|---|---|---|
| N1 | GA contrast key is not more secure than a random key of the same operator (trained detectors, matched controls, subject-disjoint MRI, seeds, intervals) | Sabeti 2024/2026: optimised seed and pattern beat random-position LSB matching under classical attacks, but the optimiser also lowers the modification count and the baseline is never tested with trained detectors; Aljughaiman ACO: random-index mode compared on PSNR only; Aljughaiman PSO: with and without optimiser both at chance; Alrawashdeh 2026: GA-only equals fixed LSB on PSNR; Vazquez 2022: authors state the GA is "a random walk" (no detector) | None of them holds operator and modification count fixed and tests the key under feature, selection-aware and CNN detectors with proper splits | OPEN, bounded. Strongest contribution. Phrase as "no study found that..."; never "first" |
| N2 | Mechanism: the GA barely moves the changes toward texture (11.9% objective gain, 34.3% of pixels in the textured third against 33.3%) | Vazquez 2022 argues the same in words | Quantitative evidence on real slices | NEW as evidence, low risk |
| N3 | Operator-matched control design (matched PVD/LSB counts and modifications; foreground-restricted random baseline) | Luo 2010 explicitly differs in operator and rate; none of the 11 medical/metaheuristic papers has a matched arm | Applying and codifying it | MODERATE (methodological). Present as a control design, not a discovery |
| N4 | Detector dependence on the same arms: large for feature detectors, halved for a selection-aware detector, absent for a CNN trained from scratch | MiPOD, SRNet, rich-model papers show detector choice changes conclusions for adaptive schemes | Same operator, key-only changes, three detector families side by side, with CNN budget stated | MODERATE. State as a measurement; the CNN null is budget-dependent and shown for one architecture that trains (SRNet-style failed on the random-key set) |
| N5 | Dose-response across five cost maps, three embedders, payload sweep | Principle known (N1 row in section 1) | Ordered dose-response and the saturation limit | LOW. Supporting evidence only |
| N6 | Empty-background baseline confound at 256x256 | Mayo radiograph papers use content-free pixels for watermarking (different task) | Showing that a whole-image random baseline overstates the gain by 0.4 AUC | LOW to MODERATE. Present as a practical pitfall |
| N7 | Eight-step minimum evaluation protocol | Apau 2024 review finds evaluation relies on PSNR, MSE, RS; no protocol proposed | A protocol whose steps each changed a conclusion here | MODERATE. Present as consolidation backed by this study, not a validated standard |
| N8 | Change-reversal analysis (where detectors find the changes) | Occlusion-style analyses are common | None | NOT a novelty claim; descriptive only |
| N9 | Reference HILL and S-UNIWARD on brain MRI | Karakis 2023 attacks S-UNIWARD, HUGO, MiPOD on brain MRI at image level | Used here as reference arms | NOT a novelty claim |

## 3. Adversarial reading (what a reviewer will say) and our answer
1. "The result is obvious: a GA over random chains cannot choose pixels." Answer: the literature claims otherwise (Sabeti, PSO, ACO, texture-GA), and the mechanism shows why; the result is a measured negative result with controls.
2. "Sabeti already showed an optimised key is more secure." Answer: their gain comes with fewer modifications and was measured against classical LSB-matching attacks; our matched control removes that confound. This is the main threat and should stay visible in the related-work section.
3. "Luo 2010 did position versus random." Answer: acknowledged in the article; operators and rates differ there.
4. "A null for one GA objective says little." Answer: a second GA with a distortion fitness and a direct cost-guided key are included, so the null is for contrast fitness specifically.
5. "Abstract-level screening can miss a paper." Answer: the claim is bounded by the sources assessed and says so.

## 4. Verdict
- Overall: moderate, bounded novelty. The value is an empirical and methodological contribution: a controlled negative result, a matched-control design, a multi-detector measurement and a protocol. There is no new algorithm and no new principle, and the article says so.
- Claimable sentence: "Among the sources we assessed, we found no study that compares an optimised pixel-selection key with a random key of the same embedder, with matched modification count and operator mix, under feature-based, selection-channel-aware and CNN detectors, with subject-level splits on medical images."
- Score: 6.5 / 10 for Novelty (unchanged). It would rise only with an algorithmic contribution or a systematic review, neither of which is planned.
- Suited to venues that value rigorous evaluation (medical image security, applied steganography, reproducibility-oriented journals) more than to venues that need a new method.
