# Novelty check, round 5 (12 Nov 2026): full-text read of 9 distinct papers (12 PDF files) (all pages, pypdf text extraction)

Method: every page extracted with pypdf (python -I). No page was unreadable in the English-language files; figures and some table cells (Mansour Tables I to V headers, Aljughaiman figure content) are not recovered by text extraction and are marked where it matters. "p." = PDF page number (journal page given where the journal number differs). Quotes are verbatim (<= 25 words). Where a point is absent I write "not found in text".

File identity (duplicate files detected by identical page and character counts):
- PMC12873396.pdf == "Optimization-driven steganographic system based on fused maps and blowfish encryption.pdf"
- frobt-09-1031299.pdf == "Confidentiality in medical images through a genetic-based steganography algorithm in artificial intelligence.pdf"
- TSP_CMC_35881.pdf == "MI-STEG ... Ensemble Deep Learning.pdf"
So 12 files contain 9 distinct papers (Eze; Mansour; Aljughaiman ACO; Aljughaiman PSO; MI-STEG; Apau review; Vazquez; Damghani; Ozcan SVM).

Language note: "Steganalysis on Medical Images with Support Vector Machine" has an English title and abstract but a Turkish body. Quotes from the body are Turkish. Flagged per the English-only rule; it is recorded because it is the only brain-MRI steganalysis paper with an SVM, but it does not change any verdict.

## 1. Summary table

| # | Paper (short) | Embedding | Location/key selection | Cover data | Security evaluation | Random-key baseline under trained detector? | Operator-/modification-matched control? | Seeds / CIs |
|---|---|---|---|---|---|---|---|---|
| 1 | Eze et al., EMBC 2020 | Evaluation framework; tests C4S spread-spectrum, Zain et al., LSB replacement | none (algorithms abstracted) | Pneumonia chest X-ray (Kaggle) | PSNR, BER, SVM diagnostic accuracy; no steganalysis | not found in text | not found in text | not found in text |
| 2 | Mansour and Abdelrahim (venue not printed) | DRT (Ripplet) transform-domain LSB + RSA | Adaptive GA for OPAP and block flipping (fitness = PSNR; block-flip fitness uses RS likelihood terms) | 8 images (colour and gray MRI "CBD/GBD" + Pepper, Lena, Retina, Baboon) | PSNR, capacity, RS analysis (Tables IV, V) | not found in text | not found in text | not found in text |
| 3 | Aljughaiman and Alrawashdeh, Sci Rep 2026 (ACO) | Content-adaptive LSB, AES-GCM/RSA | Saliency x gradient map + block-wise ACO; ablation modes ACO / random / perm / saliency_topk | BOSSbase 1.01 (cover), USC-SIPI (secret); not medical | PSNR/SSIM/MSE for all modes; Xu-Net and Ye-Net (ROC/AUC, confusion matrices) for ACO only plus a "without ACO" run | Random mode compared on PSNR only; under CNN the "without ACO" run is also at chance (uninformative) | Equal payload only; no matched modification count | single deterministic split; no seeds, no CIs |
| 4 | Aljughaiman and Alrawashdeh, Sci Rep 2026 (PSO) | Priority-guided LSB substitution, Blowfish | Fused entropy/Laplacian map; PSO optimises alpha, gamma (fitness = MSE) | BOSSbase, USC-SIPI; not medical | Xu-Net, Ye-Net AUC; RS | not found in text | not found in text | not found in text; single split |
| 5 | Karakis, MI-STEG, CMC 2023 | Steganalysis paper: S-UNIWARD, HUGO, MIPOD (+ sequential LSB for pre-training) | none (not a GA paper) | Brain MRI (epilepsy and healthy), 5961 train/val images, 3064 test images from a different dataset | Pre-trained CNN ensemble (11 nets), accuracy, detection error | no | no | five-fold CV; no CIs reported in text |
| 6 | Apau et al., PLOS ONE 2024 (SLR) | Review of 125 papers | n/a | n/a | RS and chi-square focus; "security" rating is qualitative | n/a | n/a | n/a |
| 7 | Vazquez et al., Front. Robot. AI 2022 | Non-modifying: GA finds host pixels whose LSB already equals the bit; cover unchanged | GA random walk seeded by key | 30 medical secret images hidden in 3 natural covers | none (argues steganalysis not applicable) | not found in text | not found in text | not found in text |
| 8 | Damghani et al., IET Image Process. 2021 | JPEG DCT, distortion-minimising, ICA-optimised embedding path/interaction | Imperialist competitive algorithm | 3 MRI sample images shown; 1000-image JPEG set for security, source not stated | JSRM + ensemble classifier E_OOB vs J-UNIWARD and UED | no (compares with J-UNIWARD, UED) | no | not found in text |
| 9 | Özcan, Karakış, Güler, SIU 2020 (Turkish body) | 6 sequential/region LSB variants | fixed scan orders and background/brain region | 6778 DICOM brain MR images, augmented | 216 DCT features, SVM; accuracy 0.9928 | no (no random-key variant) | no | not found in text |

## 2. Per-paper notes with quotes

### 2.1 Eze et al. (EMBC 2020), file Eze.pdf (4 pp.)
- Title: "A New Evaluation Method for Medical Image Information Hiding Techniques" (p.1). Authors: Peter Eze, Udaya Parampalli, Robin Evans, Dongxi Liu. 2020 IEEE EMBC (conference name from PDF metadata; printed footer "978-1-7281-1990-8/20/$31.00 (c)2020 IEEE 6119"). DOI not printed in text.
- Method: evaluation framework, not an embedder. "all specific implementations of algorithms are abstracted away" (p.1). Case study: C4S, Zain et al., LSB replacement (p.2).
- Data: "Pneumonia Chest-Xray dataset ... over 3,000 (large) sized X-ray images" (p.3). Not MRI. Subject split: not found in text.
- Security: "Privacy score ... combine capacity and Bit Error rate (BER)" (p.2); PSNR distortion; SVM accuracy is used as a diagnostic-preservation score ("classification and prediction accuracy is used as one of the criteria", p.3). No steganalysis detector. Random baseline, matched control, seeds/CIs: not found in text.
- Verdict: does not pre-empt (not).

### 2.2 Mansour and Abdelrahim, file Mansour.pdf (20 pp.)
- Title: "An Evolutionary Computing Enriched RS Attack Resilient Medical Image Steganography Model for Telemedicine Applications" (p.1). Authors: Romany F. Mansour, Elsaid MD. Abdelrahim. Venue, volume, DOI: not printed in extracted text (PDF metadata only gives a 2018 Word creation date).
- Method: Discrete Ripplet Transform LSB embedding + RSA. GA role: "adaptive genetic algorithm (AGA) for optimal pixel adjustment process (OPAP)" (p.1). "a chromosome is encoded as an array of 64 genes possessing the permutations 1 to 64" (p.12), with "PSNR is considered as the fitness value" (p.12). A second AGA stage does "block flipping and adjustment" to reduce RS-detectable group counts (p.11 to p.12).
- Data: "both the color magnetic resonance image (MRI) images as well as gray MRI images" (p.12); "we have applied Stegnalysis on all eight biomedical images" (p.17). Patient/subject split: not found in text.
- Security: RS analysis only, tables IV (cover) and V (stego) with unlabeled columns in the extraction (column headers lost; marked unreadable). Quote on outcome: AGA block mapping "makes it difficult or even infeasible for attackers to identify" the hidden data (p.18). No SRM/SPAM/CNN, no AUC or accuracy, no random-key baseline, no matched control, no seeds/CIs: not found in text. The hypothesis stated is "block adjustment can perform better than the standard pixel adjustment based OPAP" (p.17), i.e. the comparison is against standard OPAP, not a random order.
- Verdict: not pre-empted (GA for security against RS only, no trained detector, no random control).

### 2.3 Aljughaiman and Alrawashdeh, Sci Rep 2026, file PMC12852717.pdf (22 pp.)  [CLOSEST PAPER]
- Title: "Content-adaptive LSB steganography with saliency fusion, ACO dispersion, and hybrid encryption with ablation study" (p.1). Authors: Ahmed Aljughaiman, Rana Alrawashdeh. Scientific Reports (2026) 16:3829, https://doi.org/10.1038/s41598-025-33920-9 (printed in footer).
- Method: LSB replacement into positions chosen by a saliency x gradient content map plus block-wise ACO; indices regenerated from RSA-derived seeds ("seed_key = SHA256(pub || 0x00)", p.7). Selection channel = ACO.
- Ablation modes: "the index selection mode (ACO, random, perm, saliency_topk)" (p.15). Research question: "Does ACO-based index selection outperform random, perm, and saliency_topk at matched payload sizes?" (p.2). Result on imperceptibility: "All index-selection modes (ACO, random, perm, and saliency_topk) differ by less than 0.5 dB" (abstract, p.1). So a random-index baseline exists, but it is compared on PSNR/SSIM/MSE, not under a steganalyser.
- Data: cover BOSSbase 1.01 (grayscale natural), secret USC-SIPI (p.6). Not medical, no MRI, no subject split.
- Security: "assesses security ... through the evaluation of two prominent CNN models, Xu-Net and Ye-Net" (p.16). Training: "160 training pairs and 20 validation and test pairs that result from a deterministic split" (p.16). Outcome: "The overall accuracy reaches 50% in all scenarios" for Xu-Net with ACO (p.16); Ye-Net "selects the trivial all-cover decision" (p.18). A "without ACO" run is also at chance: "AUC values remain at 0.53, 0.52, and 0.52" (p.17) and "The non-ACO stego ... random-level behavior" (p.19). Because the control is as undetected as the treatment, the experiment has no power to distinguish key quality; the claim "exhibits random-level detectability" (p.1) is only a statement that the detectors did not learn. No SRM/SPAM, no boosted trees. The paper's own text concedes the detectors are undertrained: "the detector probably needs retraining and calibration with ACO stego data" (p.18).
- Which index mode the "without ACO" security run uses (random, perm or saliency_topk): not found in text.
- Matched modification count: not found in text (payload matched via bpp only). Seeds, CIs, repeated runs: not found in text (single deterministic split, 20 test pairs).
- Verdict: PARTLY relevant (it is the only paper in this set that has a random-index ablation next to a metaheuristic and runs a CNN steganalyser), but it does NOT pre-empt our claim: random vs ACO compared only on PSNR; security run uninformative (control also at chance, n=20 test pairs); not medical; no operator-matched controls; no feature-based detector comparison; no seeds/CIs.

### 2.4 Aljughaiman and Alrawashdeh, Sci Rep 2026, file PMC12873396.pdf = "Optimization-driven ..." (29 pp.)
- Title: "Optimization-driven steganographic system based on fused maps and blowfish encryption" (p.1). Authors: Ahmed Aljughaiman, Rana Alrawashdeh. Scientific Reports (2026) 16:4922, https://doi.org/10.1038/s41598-026-35556-9.
- Method: Blowfish-encrypted bitstream; "priority-guided Least Significant Bits (LSB) substitution" (p.1); fused entropy + Laplacian-noise map.
- Selection: "we optimize the process of embedding location selection and ordering using Particle Swarm Optimization (PSO) to maximize both security and image quality" (p.1). In the method the fitness is only distortion: "Fitness(alpha, gamma) = MSE(I,S)" (p.8, eq. 4); swarm N=18, 25 iterations (p.8).
- Data: BOSSbase (cover), USC-SIPI (secret) (p.1). Not medical.
- Security: Xu-Net/Ye-Net and RS. Abstract: "AUC for Ye-Net / Xu-Net reaches 0.49-0.57 ... RS statistics remain at 0.59-0.66" (p.1). Training "160 training pairs and 20 validation and test pairs" (p.14). Authors concede the weakness: "The selection channel operates deterministically, which makes it vulnerable to RS analysis, while our PSO objective focuses on minimizing MSE instead of RS evidence" (p.23). So the PSO objective is not detectability.
- Random-key/random-location baseline under any detector: not found in text. Matched control: not found in text. Seeds/CIs: not found in text.
- Verdict: not pre-empted. Note the useful admission that a distortion-only fitness does not suppress RS evidence.

### 2.5 Karakis, MI-STEG (CMC 2023), file TSP_CMC_35881.pdf (18 pp.)
- Title: "MI-STEG: A Medical Image Steganalysis Framework Based on Ensemble Deep Learning" (p.1). Author: Rukiye Karakis. Computers, Materials & Continua, 2023, vol. 74, no. 3, pp. 4649-4666 (page footers "4650 CMC, 2023, vol.74, no.3" ... "4666"), DOI 10.32604/cmc.2023.035881 (p.1). Received 8 Sep 2022, accepted 26 Oct 2022.
- Not a GA paper. Embedding methods are S-UNIWARD, HUGO, MIPOD; "random data in the range of 1.0-0.1 bpp payloads were hidden into the cover images" (p.4). Sequential LSB at 1.0 bpp for base pre-training (p.5).
- Data: brain MRI of epilepsy patients and healthy volunteers: "The dataset combining 5961 images was divided into training and validation sets ... 90% and 10%" (p.6), i.e. an image-level split of slices (subject-level split inside the training set: not found in text). Test set is a different dataset: "a different dataset containing 3064 T1-weighted brain MR images was used as a testing set" (p.6), which is subject- and site-disjoint by construction (cover-source mismatch).
- Detector: eleven pre-trained DenseNet/ResNet/Inception CNNs, ensemble; "Five-fold cross-validation was used to repeat training" (p.9). Metrics: accuracy, detection error, precision, recall, F1. Claims "medical image steganalysis ... for the first time in literature" (p.4); also notes prior medical-steganalysis work is "rather rare" (p.12).
- Random-key baseline, operator-matched controls, GA key, CIs: not found in text.
- Verdict: not pre-empted. Relevant as prior art for CNN steganalysis of brain-MRI stego with content-adaptive embedders (so we must not claim first CNN steganalysis on brain MRI) and as a data-split precedent (cross-dataset test).

### 2.6 Apau et al. (PLOS ONE 2024), systematic review (47 pp.)
- Title: "Image steganography techniques for resisting statistical steganalysis attacks: A systematic literature review". Authors: Richard Apau, Michael Asante, Frimpong Twum, James Ben Hayfron-Acquah, Kwame Ofosuhene Peasah. PLOS ONE 19(9): e0308807, 16 Sep 2024, https://doi.org/10.1371/journal.pone.0308807 (p.1).
- Scope: 125 articles; "robustness against well-known universal statistical steganalysis attacks including Regular-Singular (RS) and Chi-Square (X2)" (abstract, p.1). Metrics observed: "PSNR, MSE, SSIM, NC, and BPP" are the commonly used ones (p.34). SRM/SPAM/CNN steganalysers: the review text does not discuss SRM or SPAM as evaluation tools (the only SPAM hit is a reference title, p.43); "SRM" as a detector: not found in text.
- How "security" is rated: "The overall security is evaluated by taking into consideration all the parameters previously discussed, most importantly PSNR values, Encryption, Real-time implementation, Compression, and embedding process" (p.23). So the review's security column is a qualitative Delphi rating, not detector output.
- GA / metaheuristic entries (Tables 9 and 10, p.26 to p.28 and p.29, p.32). The review identifies studies only by RS number; titles are in S1 Appendix (DOCX, not in this PDF). Entries found:

| RS id | Year | Technique (as listed) | Metric reported in review | Review security rating |
|---|---|---|---|---|
| RS8 | 2014 | GA | BPP 1.96, PSNR 45.39; "Steganalysis attacks not simulated" | not in Table 10 text recovered |
| RS9 | 2015 | GA, logistic maps, LSB | PSNR 51.33, MSE 0.0032, SSIM 0.9997 | Average |
| RS1 | 2016 | GA | PSNR "mentioned but values not stated"; "Not robust against steganalysis attacks" | Low |
| RS3 | 2016 | GA, LSB, AES | PSNR not stated | Average |
| RS7 | 2016 | GA and DCT | Capacity 68.75%, PSNR 52.78, NC 0.9999 | Average |
| RS6 | 2018 | GA and LSB | PSNR 63, RS = 6.25% | Average |
| RS2 | 2020 | GA and RNS | PSNR 13.0036, MSE 0.3683 | Low |
| RS5 | 2021 | GA | BPP 1, PSNR 80.42, SSIM 0.9988 | Good |
| RS4 | 2022 | GA and IWT | BPP 0.75, PSNR 51.77 | Average |
| RS10 | 2023 | LSB, ECC and GA | BPP 3.39, PSNR 50.53, RS = 0.2450 | High |
| RS12 | 2023 | Hamilton path, GA | BPP 3, PSNR 41.80 | Average |
| RS18 | 2023 | GA, LSB | BPP 3.5, PSNR 46.07, SSIM 0.9979 | Average |

- Other metaheuristics (PSO, ACO, ICA): none listed by name in the extracted tables; the techniques column is dominated by GA, GAN, CNN, AED, RDH.
- Any GA entry that reports a random baseline under SRM/SPAM/CNN: none. The only steganalysis-type numbers attached to GA entries are RS percentages (RS6, RS10); no AUC or detection error is tabulated. Individual studies' own experiments (which are in S1 Appendix and the cited papers) are not visible, so this conclusion is limited to what the review tables report: not found in text for any GA entry.
- One MRI-covered entry exists (RS56, 2016, "AED, LSB and Symmetric Encryption", "MRI Image", Table 10, p.29), not GA.
- Verdict: does not pre-empt; supports a "gap" statement: GA studies in the review are judged by PSNR/RS and a qualitative rating. Caveat: because the study list is in a DOCX appendix not available here, do not cite it as proof that no GA paper uses SRM/SPAM; cite it as showing the reviewed tables report no such evaluation.

### 2.7 Vazquez et al., Frontiers in Robotics and AI, file frobt-09-1031299.pdf (10 pp.)
- Title: "Confidentiality in medical images through a genetic-based steganography algorithm in artificial intelligence". Authors: Eduardo Vazquez, Stephanie Torres, Giovanny Sanchez, Juan-Gerardo Avalos, Marco Abarca, Thania Frias, Emmanuel Juarez, Carlos Trejo, Derlis Hernandez. Front. Robot. AI 9:1031299, published 6 Oct 2022, doi: 10.3389/frobt.2022.1031299.
- Method: the cover is not modified; the GA finds host pixels whose existing bit equals the secret bit: "any random walk propose by the GA can be used to store the secret image without producing any distortion" (p.9). The "key" is seed S + guide sequence G (abstract, p.1).
- Data: "30 medical images were used" as secrets, hidden in landscape/flower/Mona Lisa covers (p.7 to p.8). Not MRI covers.
- Security: no steganalysis run: "the existing steganalysis techniques cannot be applied to this image" (p.9); security is argued as key complexity. Random baseline under a detector, matched control, seeds/CIs: not found in text. (The paper does mention PSNR = infinity, p.8.)
- Verdict: not pre-empted. Different mechanism (no modification). Round 4 notes list it as "Vazquez 2022"; it is the file named "Confidentiality in medical images ...".

### 2.8 Damghani, Mofrad, Damghani, IET Image Processing 2021, file IET ... Damghani ... .pdf (10 pp.)
- Title: "Medical JPEG image steganography method according to the distortion reduction criterion based on an imperialist competitive algorithm". Authors: Hamidreza Damghani, Farshid Babapour Mofrad, Leila Damghani. IET Image Process. 2021;15:705-714, DOI 10.1049/ipr2.12055 (p.1). Received 16 Jan 2020, accepted 8 Oct 2020.
- Method: JPEG DCT-domain, J-UNIWARD-style costs, ICA used to account for interactions between embedding changes (abstract: "adaptive approach that comes from the interactions between the changes made during the embedding algorithm", p.1).
- Data: "we chose three brains magnetic resonance imaging images" for illustration (p.7). The 1000-image set for security: "All the 1000 images are JPEG with three quality factors 75, 85, 95" (p.9); whether this set is medical: not found in text. Subject split: not found in text.
- Security: JSRM with ensemble classifier E_OOB, five payloads 0.1-0.5 bpnzAC, compared against J-UNIWARD and UED: "best performance is in 0.5 embedding payload by about 7.2%" (p.10, improvement over J-UNIWARD). Random-key baseline: not found in text. Matched control: not found in text. Seeds/CIs: not found in text. The text says message bits are "randomly create[d]" (p.7), which concerns payload only.
- Verdict: not pre-empted (JPEG domain, compared with cost-based methods, not with a random key; but it does show a feature-based detector improvement from optimisation, consistent in direction with our feature-based result).

### 2.9 Özcan, Maroof, Karakış, Güler, SIU 2020, file Steganalysis on Medical Images with Support Vector Machine.pdf (4 pp., Turkish body)
- Title (bilingual): "Medikal Görüntüler Üzerinde Destek Vektör Makinesi ile Steganaliz / Steganalysis on Medical Images with Support Vector Machine". Authors: Fatmanur Betül Maroof Özcan, Rukiye Karakış, İnan Güler. 2020 28th Signal Processing and Communications Applications Conference (SIU), 5-7 Oct 2020; DOI from PDF metadata (not printed in the page text): 10.1109/SIU49456.2020.9302235; printed ISBN line "978-1-7281-7206-4/20/$31.00 (c)2020 IEEE".
- English abstract: "the secret message ... is embedded into the LSBs of the MR image pixels by using six different methods" and "99.28% accuracy" (p.1). Six methods are fixed scan orders and intensity regions (LSB1 to LSB4 start corners; LSB5 background below mean, LSB6 brain above mean; p.2, Turkish).
- Data: 6778 DICOM brain MR images (p.2, "6778 adet DICOM uzantılı beyin MR görüntüsü"); data augmentation (flips, sharpening, gamma, rotation, translation) applied and the augmented pool split 61086 train / 29364 test (Table I, p.2), i.e. image-level split; subject-level split: not found in text.
- Detector: 216 DCT-derived features, SVM with RBF/linear/polynomial kernels; best accuracy 0.9928, AUC 0.9928 (Table II, p.4). No SRM/SPAM, no boosted trees, no CNN.
- Random-key baseline, matched control, seeds/CIs: not found in text. Per-method results are not broken out in the table (not found in text).
- Verdict: not pre-empted. It does show that sequential/region LSB in brain MRI is trivially detectable, and that a within-pool split inflates accuracy; cite only as motivation for subject-disjoint splits (no leakage claim can be made about it beyond "augmentation then split", which the text states).

## 3. Verdict per paper vs our claim

Claim tested: GA-chosen pixel order/key versus a RANDOM key with operator-matched controls (same PVD/LSB pairs, same modification count), under trained detectors (SRM/SPAM, boosted trees, CNN), on brain MRI with subject-disjoint splits, multiple seeds, CIs; plus the finding that cost/texture position selection lowers detectability for feature-based detectors but not for a full-budget CNN.

| Paper | Pre-empts? | Why |
|---|---|---|
| Eze 2020 | Not | Framework; no detector for stego presence; X-ray. |
| Mansour and Abdelrahim | Not | GA for OPAP/RS block flipping; RS only; no random control. |
| Aljughaiman ACO 2026 | Partly (random-index ablation + CNN steganalysis, closest) | Random vs ACO on PSNR only; CNN runs at chance for both; n=20 test pairs; BOSSbase; no matched control; no CIs. |
| Aljughaiman PSO 2026 | Not | PSO fitness = MSE; Xu/Ye-Net at chance; RS admitted vulnerable; no random control. |
| Karakis MI-STEG 2023 | Not (but prior art for brain-MRI CNN steganalysis) | No GA, no random key; adaptive embedders only. |
| Apau 2024 SLR | Not | Qualitative security rating; GA entries carry PSNR/RS only. |
| Vazquez 2022 | Not | Non-modifying GA scheme, no steganalysis run. |
| Damghani 2021 | Not | JPEG ICA path vs J-UNIWARD under JSRM; no random key. |
| Özcan 2020 | Not | SVM on fixed-order/region LSB; no key. |

Net verdict for the NARROW claim (random-key, operator-/modification-matched controls under trained detectors on brain MRI, subject-disjoint, seeds and CIs, with the feature-versus-CNN dependence): NOT pre-empted by any of these papers; combined with round 4 (Luo 2010; MOLSBM 2024 and ISeCure 2026), the narrow claim remains open. Closest paper in this batch: Aljughaiman and Alrawashdeh, Sci Rep 16:3829 (2026) (random-index mode ablation and Xu-Net/Ye-Net), but its random baseline is evaluated on PSNR only and its security runs are uninformative. Closest overall remains MOLSBM/Sabeti 2026 from round 4 (optimised selection evaluated with SPAM/SRM).

Wording cautions arising from this round:
- Avoid "first medical steganalysis" or "first CNN steganalysis of brain MRI": Karakis 2023 claims the first and Özcan et al. 2020 did SVM on brain MRI.
- Avoid "no GA/metaheuristic paper compares against random locations": Aljughaiman ACO 2026 has a random-index mode (PSNR only). Safe phrasing: "to our knowledge, none of the surveyed metaheuristic selection papers compares optimised and random keys under trained steganalysers with operator-matched controls".
- Position the CNN null (no gain from position selection) against the Aljughaiman papers, whose CNN detectors are at chance for both treatment and control with 160 training pairs: a detector that has not learned the task cannot show a key effect, which supports requiring a full-budget CNN (control must be detectable first).
- The Aljughaiman PSO paper's own admission (p.23) that MSE-based PSO fails to suppress RS evidence supports the point that GA fitness (distortion) differs from detectability.

## 4. Bibliographic metadata read from the PDFs

Only fields actually printed (or in PDF metadata, as noted) are given. "not printed" means not found in the extracted text.

1. Eze, P.; Parampalli, U.; Evans, R.; Liu, D. "A New Evaluation Method for Medical Image Information Hiding Techniques." 2020 42nd Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC), Montreal, 20-24 July 2020 (conference from PDF metadata). Printed pages 6119-6122 (footer; first page 6119, last 6122). Printed ISBN line 978-1-7281-1990-8/20. DOI: not printed.
2. Mansour, R. F.; Abdelrahim, E. M. "An Evolutionary Computing Enriched RS Attack Resilient Medical Image Steganography Model for Telemedicine Applications." Venue, year, volume, pages, DOI: not printed (20-page manuscript; PDF created April 2018 per metadata). Affiliations: Assiut University (New Valley), Tanta University, Egypt.
3. Aljughaiman, A.; Alrawashdeh, R. "Content-adaptive LSB steganography with saliency fusion, ACO dispersion, and hybrid encryption with ablation study." Scientific Reports 16:3829 (2026). DOI 10.1038/s41598-025-33920-9. 22 PDF pages.
4. Aljughaiman, A.; Alrawashdeh, R. "Optimization-driven steganographic system based on fused maps and blowfish encryption." Scientific Reports 16:4922 (2026). DOI 10.1038/s41598-026-35556-9. 29 PDF pages.
5. Karakis, R. "MI-STEG: A Medical Image Steganalysis Framework Based on Ensemble Deep Learning." Computers, Materials & Continua 74(3), 2023, pp. 4649-4666. DOI 10.32604/cmc.2023.035881. Received 8 Sep 2022; accepted 26 Oct 2022.
6. Apau, R.; Asante, M.; Twum, F.; Hayfron-Acquah, J. B.; Peasah, K. O. "Image steganography techniques for resisting statistical steganalysis attacks: A systematic literature review." PLOS ONE 19(9): e0308807, 16 Sep 2024. DOI 10.1371/journal.pone.0308807.
7. Vazquez, E.; Torres, S.; Sanchez, G.; Avalos, J.-G.; Abarca, M.; Frias, T.; Juarez, E.; Trejo, C.; Hernandez, D. "Confidentiality in medical images through a genetic-based steganography algorithm in artificial intelligence." Frontiers in Robotics and AI 9:1031299, 6 Oct 2022. DOI 10.3389/frobt.2022.1031299.
8. Damghani, H.; Babapour Mofrad, F.; Damghani, L. "Medical JPEG image steganography method according to the distortion reduction criterion based on an imperialist competitive algorithm." IET Image Processing 15(3):705-714, 2021. DOI 10.1049/ipr2.12055.
9. Özcan, F. B. M.; Karakış, R.; Güler, İ. (printed as Fatmanur Betül MAROOF ÖZCAN, Rukiye KARAKIŞ, İnan GÜLER). "Steganalysis on Medical Images with Support Vector Machine" (Turkish title "Medikal Görüntüler Üzerinde Destek Vektör Makinesi ile Steganaliz"). 2020 28th Signal Processing and Communications Applications Conference (SIU), 5-7 Oct 2020. DOI 10.1109/SIU49456.2020.9302235 (PDF metadata, not printed in page text); page range: not printed (4-page paper). Body in Turkish.

Items not resolved from the PDFs (author must verify before citing): Mansour and Abdelrahim venue/year/DOI; Eze DOI; SIU 2020 page range.
