# E7 (PRELIMINARY, seed 0 only): small CNN detector on the E6 design — EXPLORATORY, NOT VERIFIED

Detector C: fixed 5x5 high-pass (SRM s5 kernel) -> 5 conv blocks (BN, ReLU, avgpool), global pool, 2-way FC; Adam 1e-3 cosine, 15 epochs, flips; trained per fold on grouped 5-fold CV (same folds/groups as E6), OOF scores rank-normalised per fold; CPU. Schemes: RAND, GA, RAND_GAMIX (random selection with the GA's branch-bit quotas). Payloads 0.01 and 0.02 bpp (raw). One CNN training seed, one stego replicate. 90% CIs from group bootstrap WITHOUT retraining (optimistic).

| set | bpp | AUC RAND | AUC GA | AUC RAND_GAMIX | P1 GA-RAND (ci90) | P3 GA-RANDGAMIX (ci90) | GA MSE / RAND MSE |
|---|---|---|---|---|---|---|---|
| T_raw (real tumour) | 0.01 | .746 | .687 | .690 | -0.059 (-0.070,-0.049) | -0.004 (-0.008,+0.002) | .023/.054 |
| T_raw | 0.02 | .851 | .790 | .808 | -0.061 (-0.073,-0.050) | -0.019 (-0.029,-0.010) | .048/.104 |
| A_noise (synthetic noise) | 0.01 | .852 | .586 | .698 | -0.266 (-0.279,-0.252) | -0.112 (-0.125,-0.097) | .029/.128 |
| A_noise | 0.02 | .963 | .734 | .882 | -0.229 (-0.240,-0.218) | -0.148 (-0.160,-0.135) | .074/.236 |

Reading (exploratory):
1. With a CNN, the MSE-driven GA is LESS detectable than random in all 4 cells (opposite sign to the SRM-lite+LR / SPAM+HGB result of E6, where GA was more detectable on A_noise and ~equal on T_raw).
2. On real tumour covers most of the GA advantage is reproduced by random selection with the GA's branch mix (P3 ~ 0 to -0.02); on A_noise a large part is NOT (P3 -0.11..-0.15), i.e. position choice matters for the CNN there.
3. Likely explanation (untested): GA lowers MSE 2-4x, i.e. avoids large-magnitude changes; SRM-lite truncates residuals at T=2 and so may be blind to magnitude, whereas the CNN is not. Hence the earlier "GA harm" is probably a weak-detector artefact; detector choice flips the sign.
4. Caveats: single CNN seed and replicate; CNN small and short-trained; no true subject IDs; A_noise synthetic; CIs optimistic. Needs replication (seed 1 running), verification, and ideally a detector-ablation (CNN on truncated residuals).
No SUCCESS_* state.
