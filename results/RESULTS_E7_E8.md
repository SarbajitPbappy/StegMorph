# E7 (CNN, failed control), E7b (selection-channel-aware detector), E8 (vs idealised adaptive baseline). EXPLORATORY, seed 0 only.
## E7: from-scratch XuNet-lite CNN, A_raw 0.02 bpp, 840 training pairs: AUC 0.501 on RAND (feature detectors: 1.0) => failed positive control, aborted, NO conclusion drawn. CNN steganalysis remains untested (needs GPU / thousands of training images).
## E7b: SCA-lite (maxSRM-style, texture-probability-weighted SRM-lite co-occurrences) + LR. Positive control passed (RAND .985, A_raw 0.02 bpp).
| set (seed 0) | detector | RAND | GA_MSE | GREEDY_TEX |
|---|---|---|---|---|
| A_raw 0.02 | SRM-lite | 1.000 | 1.000 | .758 |
| A_raw 0.02 | SCA-lite | .985 | .974 | .810 |
| T_raw 0.01 | SRM-lite | .853 | .864 | .680 |
| T_raw 0.01 | SCA-lite | .804 | .804 | .729 |
Selection-channel awareness shrinks the texture-cost advantage (T_raw: -0.173 -> -0.075 AUC) but does not remove it (CI of difference vs RAND under SCA-lite on T_raw excludes 0). GA_MSE gives no gain under any detector.
## E8: same schemes plus HILL_SIM (idealised +-1 optimal-coder simulator, no extraction, not a real STC) at the SAME embedded bpp (3x(32+raw bits)/16384).
| set | detector | RAND | GREEDY_TEX | HILL_SIM |
|---|---|---|---|---|
| A_raw 0.02 | SRM-lite | 1.000 | .758 | .547 |
| A_raw 0.02 | SCA-lite | .985 | .810 | .552 |
| A_raw 0.02 | SPAM+HGB | 1.000 | .697 | .529 |
| T_raw 0.01 | SRM-lite | .853 | .680 | .564 |
| T_raw 0.01 | SCA-lite | .804 | .729 | .569 |
| T_raw 0.01 | SPAM+HGB | .672 | .522 | .490 |
## Reading
The idealised adaptive embedder is far harder to detect than the best texture-aware StegMorph-recon variant (e.g. A_raw SCA-lite .552 vs .810). The texture-aware GA/greedy fix recovers part of the gap between random/MSE-driven selection and the adaptive baseline, but the LSB-replacement/PVD embedding itself (2-LSB pairs, triplication, side-information positions) remains the limiting factor. HILL_SIM is an idealised upper bound (no coding overhead, no extractability), so the true gap is smaller, but the ordering is unlikely to flip.
Limits: seed 0 only; N=400/435; feature detectors only; HILL_SIM not extractable.
