# NOVELTY_final_A: steganalysis and embedding classics (Group A)

Method: every page of each PDF was extracted with pypdf (python -I). No page lacked a text layer. All 8 papers are English. Page numbers are PDF page indices (1 = first PDF page), not printed folios. Quotes are verbatim (ligatures normalised), at most 25 words. "not found in text" means a keyword/context search plus reading of the relevant pages turned up nothing.

Our narrow claim under test: GA-chosen pixel key vs RANDOM key vs OPERATOR-MATCHED controls in hybrid LSB/PVD, trained steganalysers (SRM/SPAM-type + linear/boosted trees, full-budget CNN), brain MRI, subject-disjoint splits, 3+ seeds, subject-cluster bootstrap, dose-response (texture-guided vs smooth-pixel keys) with detector dependence (feature detectors benefit, CNN does not).

---

## 1. Rich Models for Steganalysis of Digital Images
1. Fridrich J., Kodovsky J. (printed "Kodovský"). IEEE Transactions on Information Forensics and Security, vol. 7, no. 3, June 2012, pp. 868-882. DOI printed: 10.1109/TIFS.2012.2190402 (p1). 15 PDF pages.
2. Builds a "rich model": a union of many diverse submodels, each a co-occurrence matrix of quantised noise residuals. Submodels are chosen by training data with ensemble (FLD random-subspace) classifiers. Demonstrated on HUGO, the edge-adaptive (EA) algorithm of Luo et al., and optimally coded +-1 embedding, on BOSSbase.
3. GA/metaheuristic/random-vs-optimised key or location order for LSB/PVD: NO. Not found in text (no LSB/PVD key study; "LSB Matching" appears only as the non-adaptive baseline, p8). The only optimiser is a Nelder-Mead fit of a predictor kernel for detection, not of a stego key (p4: "optimizing the coefficients ... using the Nelder-Mead algorithm to minimize the detection error for the embedding algorithm HUGO").
4. Random-position/random-key baseline: none for keys. The non-adaptive +-1 embedding is the "non-selective" baseline (p8: "Nonadaptive 1 embedding (also called LSB Matching)"), and random enters only in the classifier ("random subspace", p6) and random train/test splits (p6).
5. Bearing statements:
   - Adaptive placement harder for rich model, but detection benefits more: p12 "the detection of both adaptive stego methods benefits more from the rich model than 1 embedding".
   - Reason: p13 "they place embedding changes in hard-to-model regions of images where the rich model better discerns the embedding changes."
   - Non-adaptive embedding falls back on smooth areas: p9 "For small payloads, the amount of changes in edges and textures is so small that detection essentially relies on smooth parts".
   - Quantisation link: p2 "quantization makes the residual more sensitive to embedding changes at spatial discontinuities in the image (at edges and textures)."
   - Edge-adaptive result: p12 "the security of the EA algorithm is comparable with that of 1 embedding for payloads larger than 0.3 bpp" (loses adaptivity at high payload).
   - Selection-channel-aware: not found in text. CNN vs features: not found in text (CNN only appears as a convolutional-code term in references). Training-set size dependence: not found as a studied variable; uses fixed 8074/1000 split (p9 note 6) and says ensembles work "with high-dimensional feature spaces and large training sets" (p1). G-SVM noted as better than ensemble for nonlinear boundaries (p13: "better captured by Gaussian SVMs than the ensemble").
6. Reviewer use: it states both that content-adaptive placement is hard-to-model (so a feature detector gains more on it) and that a non-adaptive scheme is detected via smooth parts. See the adversarial section.

## 2. Steganalysis by Subtractive Pixel Adjacency Matrix (SPAM)
1. Pevny T., Bas P., Fridrich J. IEEE TIFS, vol. 5, no. 2, June 2010, pp. 215-224. DOI printed: 10.1109/TIFS.2010.2045842 (p1). 10 PDF pages.
2. Proposes SPAM features: first/second-order Markov transition matrices of adjacent pixel differences, fed to Gaussian-kernel SVMs. Evaluates mainly on LSB matching over four image databases (CAMERA, BOWS2, JPEG85, NRCS). Also shows the features work on 10 JPEG algorithms.
3. GA/metaheuristic or random-vs-optimised key/location for LSB/PVD: NO. Not found in text.
4. Random-position baseline: none. LSB matching is defined as embedding that "randomly increases or decreases pixel values by one" (p1), i.e. the +-1 sign is random, not a position key study. Embedding is at full-image uniform positions; no key/position comparison in text.
5. Bearing statements:
   - Cover-source dependence of detectors: p1 "most current detectors of LSB matching exhibit performances that vary significantly across different cover sources".
   - Noisy vs smooth covers named: p6 "NRCS images are very noisy, while JPEG85 images are smoothed by the lossy compression."
   - Mismatch/joint training: p6 "The training set of steganalyzers consists of 5000 cover and 5000 stego images randomly selected from three databases."
   - Residual filter as edge detector (p3): "the simplest edge detector". Rationale for differences (p9): stego noise "is an independent random component typically not found in digital media".
   - Content-adaptive/texture-guided harder: not found in text (no adaptive scheme tested). Selection-channel-aware: not found in text. CNN: not found in text. Training-size dependence: not found as a studied variable (fixed 5000/5000 sets, 5-fold CV on SVM hyperparameters, p4).
6. Reviewer use: SPAM is cited as the standard linear/kernel feature detector for LSB-type embedding in noisy vs smooth sources. It says nothing about key/position choice.

## 3. Universal Distortion Function for Steganography in an Arbitrary Domain (UNIWARD)
1. Holub V., Fridrich J., Denemark T. EURASIP Journal on Information Security 2014, 2014:1. DOI printed: 10.1186/1687-417X-2014-1 (p13). 13 PDF pages.
2. Defines UNIWARD, a distortion computed as relative change of directional wavelet-filter-bank coefficients, for spatial, JPEG and side-informed JPEG domains. Embedding uses syndrome-trellis codes. Tested against SRM and a content-selective-residual (CSR) feature attack, ensemble classifier, BOSSbase 1.01.
3. GA/metaheuristic/random-vs-optimised key or LSB/PVD: NO. Not found in text. The paper does mention (p1) a prior parametrised-and-optimised distortion: "a heuristically defined distortion function was parametrized and then optimized to obtain the smallest detectability", and warns it can become more detectable "outside of the model" (p1).
4. Random baseline: only non-adaptive LSBM at uniform cost, p9 "The non-adaptive LSBM was simulated at the ternary bound corresponding to uniform costs". This is a uniform-cost baseline, not a random-key baseline.
5. Bearing statements:
   - Texture-guided design: abstract (p1) "forces the embedding changes to such parts of the cover object that are difficult to model in multiple directions, such as textures or noisy regions, while avoiding smooth regions or clean edges".
   - p1 "embedding costs are typically required to be low in complex textures or 'noisy' areas and high in smooth regions".
   - Empirical: p10 "the non-adaptive LSBM performs poorly across all payloads, while EA appears only marginally better than LSBM".
   - Selection-channel attack: p6 "features designed specifically to utilize the artifacts in the embedding probabilities to probe the security of this unusual selection channel"; p8 shows knowledge of a faulty selection channel can be "used to successfully attack S-UNIWARD".
   - CNN vs features: not found in text. Training-size dependence: not found in text.
6. Reviewer use: gives the design rationale that content-adaptive/textured placement is more secure against rich-model detectors. It is a statement about steganographer-side cost design, with a full-image, non-keyed, non-medical setting.

## 4. Minimizing Additive Distortion in Steganography Using Syndrome-Trellis Codes (STC)
1. Filler T., Judas J., Fridrich J. IEEE TIFS, vol. 6, no. 3, Sept. 2011, pp. 920-935. DOI printed: 10.1109/TIFS.2011.2134094 (p1). 16 PDF pages.
2. Gives a practical coding method (syndrome-trellis codes, Viterbi) to embed a payload while minimising additive per-element distortion, for binary and, via layering, ternary/pentary operations. Includes wet-paper channel results. Demonstrates a spatial scheme (clique-based costs) vs second-order SPAM on BOWS2 and JPEG schemes vs SVM.
3. GA/metaheuristic/random-vs-optimised key or LSB/PVD: NO. Not found in text. Random permutation by stego key appears only as an engineering device: p8 "the cover pixels can be permuted using a stego key before embedding", and "the message size can be used as a seed for the pseudo-random number generator".
4. Random baseline: random cover/message used to estimate code efficiency (p8, "random cover object ... random message"); LSB matching at the uniform (non-adaptive) bound is the security baseline (p13-14, "contrasted with LSB matching simulated on the binary and ternary bounds"). No random-position security baseline.
5. Bearing statements:
   - p13 "Changes made in smooth regions often tend to be highly detectable by blind steganalysis which should lead to high distortion values."
   - p13 "pixels which are in busy and hard-to-model regions can be changed more often."
   - Result vs SPAM (p14): most proposed adaptive schemes "undetectable for relative payloads" below a threshold, and larger changes help "when placed adaptively".
   - Selection-channel-aware, CNN, training-size dependence: not found in text (SVM trained on half the database, p12, no size study).
6. Reviewer use: states as a design premise that smooth-region changes are more detectable than busy-region changes, with SPAM evidence. This is the nearest early statement of "texture good, smooth bad".

## 5. Content-Adaptive Steganography by Minimizing Statistical Detectability (MiPOD)
1. Sedighi V., Cogranne R., Fridrich J. IEEE TIFS, vol. 11, no. 2, Feb. 2016, pp. 221-233. DOI printed: 10.1109/TIFS.2015.2486744 (p1). 14 PDF pages.
2. Models cover pixels as independent heteroscedastic Gaussians, derives the most powerful detector for content-adaptive LSB matching, and designs costs (MiPOD) that minimise its power. Compares to HUGO-BD, WOW, S-UNIWARD, HILL using FLD ensemble with SRM and maxSRMd2 on BOSSbase 1.01 (ten 5000/5000 splits). Also introduces a detectability-limited sender.
3. GA/metaheuristic/random-vs-optimised key: NO. Not found in text. It does note (p1) that distortions "optimized to minimize the empirical detectability" may be "overoptimized" and "become highly detectable should the Warden choose a different feature representation".
4. Random baseline: not found in text (no random-position baseline; random only in the Gaussian model and the ensemble).
5. Bearing statements:
   - Selection-channel-aware: p4 defines "omniscient" vs "indifferent" Warden; p7 uses "the selection-channel-aware version called the maxSRMd2 ... uses the knowledge of change rates"; p7 "lower detection errors when steganalyzing with the selection-channel-aware maxSRMd2 ... in comparison to errors obtained with the SRM".
   - Qualification (p8): "the knowledge of the selection channel does not provide a substantial advantage to the Warden for the tested MiPOD" on a weakly adaptive artificial source; footnote 4 on p8: gain "correspondingly smaller" because MiPOD is only weakly adaptive.
   - Feature detector near optimal: p9 "empirical steganalysis detectors are near optimal" (for homogeneous source); for diverse content p9 "the SRM now performs significantly worse than the optimal LRT because it has to deal with content diversity".
   - Smooth regions: p6 "pixels with ... approximately 0 lie in a smooth image region and should have a small probability of change anyway".
   - Complex content: p10 for complex images the empirical detector overestimates secure payload "due to its lower detection power" (p11).
   - CNN vs feature: not found in text. Training-size dependence: not found in text.
6. Reviewer use: supports "detector information (selection channel) matters and the gain scales with how adaptive the embedding is".

## 6. Deep Residual Network for Steganalysis of Digital Images (SRNet)
1. Boroumand M., Chen M., Fridrich J. IEEE TIFS, vol. 14, no. 5, May 2019, pp. 1181-1193. DOI printed: 10.1109/TIFS.2018.2871749 (p1). 13 PDF pages.
2. Proposes SRNet, a deep residual CNN with an unpooled noise-residual front end and no hand-fixed filters, universal for spatial and JPEG steganography. Evaluated on BOSSbase+BOWS2 (4,000 BOSSbase + all BOWS2 for training, 1,000 validation, 5,000 test) and ImageNet subset, against YeNet, J-XuNet and maxSRMd2 with ensemble/linear classifier. Also tests selection-channel injection into the network.
3. GA/metaheuristic/random-vs-optimised key or LSB/PVD: NO. Not found in text. LSB appears only in the intro (p1: "With the exception of steganographic schemes based on Least Significant Bit (LSB) replacement ... the most accurate detectors have been built using the tools of machine learning").
4. Random baseline: not found in text. "Random" appears as random initialisation, augmentation, random splits.
5. Bearing statements:
   - CNN > feature detector: abstract p1 "have firmly established themselves as superior to the previous detection paradigm - classifiers based on rich media models"; p6 "both network detectors clearly outperform the old steganalysis paradigm".
   - Quantified: p6 linear classifier with maxSRMd2 shows "4-30 times larger (!) false alarms" than SRNet at fixed detection power (S-UNIWARD/HILL).
   - Selection-channel and CNN: p2 "the network should become aware of the selection channel via end-to-end training"; p9 "the SRNet may still benefit from being informed about the probabilistic impact of embedding". p6: SRNet is 1.5% worse than SCA-YeNet for WOW 0.1 bpp because it "does not make explicit use of the selection channel". So CNNs also gain from selection-channel information (contrast with our "CNN does not benefit").
   - Training budget/size: p1 YeNet "pointed out the importance of using larger training datasets for deeper networks"; p5 400k iterations (457 epochs) plus 100k more, curriculum training, p6 "two and half days to train the SRNet on a Titan Xp GPU". p6 "convergence problems when training from a randomly initialized network" is p5. Single random split used: p6 "one random 50/50 split ... not computationally feasible to train all networks on multiple different splits"; five splits for only two settings, std 0.0035 and 0.0016 (p6). Image diversity: p7 ImageNet error larger "by 6.6-9%" than the homogeneous source.
   - Training-set-size ablation (dose-response in N): not found in text.
   - Texture vs smooth key position: not found in text.
6. Reviewer use: a reviewer could say "CNNs beat feature detectors (SRNet) and need large training budgets, so a CNN that does not benefit from key texture is unsurprising or a budget artefact". The paper does not say CNNs are insensitive to texture-guided placement; it reports the opposite direction for selection-channel information.

## 7. Designing Steganographic Distortion Using Directional Filters (WOW)
1. Holub V., Fridrich J. IEEE International Workshop on Information Forensics and Security (WIFS), 2012 (p1 footer: "978-1-4673-2287-4/12/$31.00 (c)2012 IEEE  WIFS 2012"), pp. 234-239. DOI: not printed in extracted text. Title as printed: "Designing Steganographic Distortion Using Directional Filters". 6 PDF pages.
2. Defines WOW: per-pixel costs from directional high-pass filters, aggregated with a reciprocal Hoelder norm so that costs are low only where content is non-smooth in every direction. Embeds with STCs. Compares to HUGO, EA, LSBM using SRM (ensemble FLD, OOB error) and wavelet-domain features on BOSSbase 1.0.
3. GA/metaheuristic/random-vs-optimised key or LSB/PVD: NO. Not found in text. (Mentions earlier parametrised-distortion optimisation, p1: "searched for such values of the parameters that gave the smallest detectability".)
4. Random baseline: not found in text; LSBM at ternary bound is the non-adaptive baseline (p2).
5. Bearing statements:
   - p1 "the aggregation rule is designed to force the embedding changes to highly textured or noisy regions and to avoid clean edges".
   - p1 "Consequently, the new embedding scheme appears markedly more resistant to steganalysis using rich models."
   - p3 "whenever possible the embedding algorithm should embed into textured/noisy areas that are not easily modellable in any direction".
   - p4 "At 0.5 bpp, the EOOB of WOW is almost twice as high as that of HUGO." (adaptivity helps security vs SRM).
   - p6 conclusion: forcing changes "away from smooth areas and clean edges greatly improves steganographic security" (paraphrase of text near "edges greatly improves steganographic security").
   - Selection-channel-aware, CNN, training size: not found in text. Detector adapted to embedding domain (wavelet features, p5): "The most successful steganalysis attacks have always been built in the embedding domain."
6. Reviewer use: a direct "texture-guided placement is more secure vs rich-model/SRM" result, from an adaptive design, with the "avoid smooth areas" principle explicit.

## 8. Selection-Channel-Aware Rich Model for Steganalysis of Digital Images (maxSRM)
1. Denemark T., Sedighi V., Holub V., Cogranne R., Fridrich J. IEEE WIFS 2014 (file name WIFS14; venue string and DOI not printed in the extracted text, so not confirmed from the PDF; the text itself says experiments done "as of writing this paper (May 2014)", p2). 6 PDF pages.
2. Proposes maxSRM/maxSRMd2, SRM variants whose co-occurrence bins accumulate the maximum embedding-change probability, so the detector uses an estimate of the selection channel. Tested against WOW, S-UNIWARD and S-UNIGARD on BOSSbase 1.01 with FLD ensemble, ten 5000/5000 splits, vs SRM and tSRM.
3. GA/metaheuristic/random-vs-optimised key or LSB/PVD: NO. Not found in text.
4. Random baseline: not found in text.
5. Bearing statements:
   - Abstract p1: "even an imprecise knowledge of the embedding probabilities can substantially increase the detection accuracy in comparison with feature sets that do not consider the selection channel".
   - p1 "Overly adaptive embedding schemes seem to be more vulnerable than schemes that spread the embedding changes more evenly throughout the cover."
   - p4: WOW PE at 0.05 bpp drops from .4572 (SRM) to .3539 (maxSRMd2); S-UNIWARD .4533 to .4180 (Table II). Gain larger for the more concentrated embedding.
   - p4 "the difference between SRM and maxSRM will diminish with a decreasing degree of adaptivity of the embedding algorithm."
   - p6: WOW's selection channel is "overly adaptive", "which makes this algorithm more vulnerable to maxSRM".
   - CNN vs feature: not found in text. Training-size dependence: not found in text (fixed 5000/5000).
6. Reviewer use: the strongest prior statement that the benefit of feature-detector improvements scales with embedding concentration.

---

## Summary table

| # | Paper | Venue/yr | GA/metaheur. key for LSB/PVD | Random-key/position baseline | Adaptive placement vs rich/feature detector | Selection-channel-aware | CNN vs features | CNN training budget/size | Threat to texture-vs-smooth novelty |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Rich Models | TIFS 2012 | No | No (non-adaptive +-1 baseline only) | Yes (rich model gains more on adaptive; non-adaptive caught in smooth parts, p9, p12-13) | Not found in text | Not found in text | Not found in text | High as principle |
| 2 | SPAM | TIFS 2010 | No | No | Not found in text | Not found in text | Not found in text | Not found in text | Low |
| 3 | UNIWARD | EURASIP JIS 2014 | No | Uniform-cost LSBM only | Yes (design rationale, p1, p3, p10) | Partly (CSR attack, p6, p8) | Not found in text | Not found in text | Medium-high |
| 4 | STC | TIFS 2011 | No | No (stego-key permutation as coding device, p8) | Yes (smooth changes more detectable, p13) | Not found in text | Not found in text | Not found in text | Medium |
| 5 | MiPOD | TIFS 2016 | No | No | Partial (SRM weaker on diverse content, p9) | Yes (p4, p7, p8) | Not found in text | Not found in text | Medium |
| 6 | SRNet | TIFS 2019 | No | No | Not found in text | Yes, for CNN (p6, p9) | Yes, CNN superior (p1, p6) | Partial (p1, p5, p6) | Medium for CNN claim |
| 7 | WOW | WIFS 2012 | No | No | Yes (p1, p3, p4) | Not found in text | Not found in text | Not found in text | High as principle |
| 8 | maxSRM | WIFS 2014 | No | No | Partial (more adaptive, more detectable with SC info, p1, p4, p6) | Yes (core) | Not found in text | Not found in text | Medium-high |

---

## Adversarial summary: what prior art says about our texture-vs-smooth and CNN-vs-feature findings

None of the eight papers tests a metaheuristic/GA pixel key, a random-key null, or operator-matched controls for hybrid LSB/PVD, and none uses medical images, subject-disjoint splits or subject-cluster bootstrap. Thus the specific controlled design is not pre-empted by Group A.

Strongest reviewer argument that "texture beats smooth for feature detectors" is already known:
- Rich Models p12-13 says "the detection of both adaptive stego methods benefits more from the rich model than 1 embedding" and "they place embedding changes in hard-to-model regions of images where the rich model better discerns the embedding changes". (p9 also says non-adaptive embedding at small payload is detected through "smooth parts".) A reviewer will say: feature detectors are known to profit most from adaptive placement.
- STC p13 ("Changes made in smooth regions often tend to be highly detectable by blind steganalysis"), WOW p1/p3, and UNIWARD p1/p3 each state the principle that embedding should avoid smooth regions and go to textured regions, supported by SRM/SPAM results.
- maxSRM p1/p4 and MiPOD p7 say detector gains scale with how concentrated/adaptive the embedding is. A texture-guided key is a more concentrated selection channel, so a reviewer can say the dose-response with feature detectors is predicted by the selection-channel literature.

Possible reading that goes the other way: the direction in prior art is that content-adaptive placement is MORE secure (harder for rich models) than non-adaptive, while "detection benefits more from the rich model" (Rich Models p12) refers to a bigger gain relative to a model-poor baseline, not to higher absolute detectability. Also the prior art optimises per-pixel distortion costs with STC, not an ordering key in a hybrid LSB/PVD scheme, and none uses a random-key null. Our texture-vs-smooth result must be framed as a controlled test of that principle under a key-selection design, not as the discovery of it; if our texture-guided key is MORE detectable by feature detectors than smooth, that contradicts the "adaptive = more secure" claims of WOW/UNIWARD/STC and needs explicit reconciliation (for example: texture-guided here concentrates changes, matching the "overly adaptive" caveat of maxSRM p1/p6).

On CNN vs feature detector:
- SRNet p1 and p6: CNNs are "superior to the previous detection paradigm", and "both network detectors clearly outperform the old steganalysis paradigm". A reviewer will say a full-budget CNN should dominate feature detectors, so a CNN that does not benefit from texture placement may simply be saturated or insensitive.
- SRNet p6, p9 show CNNs do gain from selection-channel information (SCA-YeNet beats SRNet on WOW 0.1 bpp; SRNet "may still benefit from being informed"). This is not the same as insensitivity to placement, but it weakens a blanket "CNN ignores placement" claim.
- Training budget/size: SRNet p1 (YeNet "importance of using larger training datasets for deeper networks"), p5 (457+114 epochs, curriculum training, convergence problems), p6 (2.5 days GPU). A reviewer can say a CNN null on MRI with small data reflects undertraining. Our "full-budget" CNN wording must be backed by our own budget evidence, since Group A offers no ablation of training-set size (not found in text) to cite.
- None of the eight papers compares CNN vs feature detectors specifically across texture-guided vs smooth placement doses (not found in text), so the detector-dependence finding is not directly pre-empted.

Statistical practice gap in the cited CNN paper: SRNet reports a single random 50/50 split for most results and five splits only for two settings (p6); our multi-seed, subject-cluster bootstrap design is not matched there.

Caveats: DOI for #7 and venue/DOI for #8 are not printed in the PDF text; do not cite them from this file without checking refs.bib or the publisher page. Page numbers are PDF indices; printed folios differ (e.g. Rich Models PDF p1 = printed 868).
