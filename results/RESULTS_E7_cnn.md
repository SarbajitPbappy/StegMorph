# E7 (2 CNN seeds, now replicated): small CNN detector on the E6 design — EXPLORATORY, NOT VERIFIED

Detector C: fixed 5x5 high-pass (SRM s5 kernel) -> 5 conv blocks (BN, ReLU, avgpool), global pool, 2-way FC; Adam 1e-3 cosine, 15 epochs, flips; trained per fold on grouped 5-fold CV (same folds/groups as E6), OOF scores rank-normalised per fold; CPU. Schemes: RAND, GA, RAND_GAMIX (random selection with the GA's branch-bit quotas). Payloads 0.01 and 0.02 bpp (raw). One CNN training seed, one stego replicate. 90% CIs from group bootstrap WITHOUT retraining (optimistic).

| set | bpp | AUC RAND | AUC GA | AUC RAND_GAMIX | P1 GA-RAND (ci90) | P3 GA-RANDGAMIX (ci90) | GA MSE / RAND MSE |
|---|---|---|---|---|---|---|---|
| T_raw (real tumour) | 0.01 | .746 | .687 | .690 | -0.059 (-0.070,-0.049) | -0.004 (-0.008,+0.002) | .023/.054 |
| T_raw | 0.02 | .851 | .790 | .808 | -0.061 (-0.073,-0.050) | -0.019 (-0.029,-0.010) | .048/.104 |
| A_noise (synthetic noise) | 0.01 | .852 | .586 | .698 | -0.266 (-0.279,-0.252) | -0.112 (-0.125,-0.097) | .029/.128 |
| A_noise | 0.02 | .963 | .734 | .882 | -0.229 (-0.240,-0.218) | -0.148 (-0.160,-0.135) | .074/.236 |

Replication (seed 1, same design, different crops/stego/CNN init; NOT independent image pool):
T_raw|C|0.01 AUC mean RAND/GA/RG [0.746, 0.685, 0.689)] P1 [-0.0593, -0.062] P3 [-0.0035, -0.0037]
T_raw|C|0.02 AUC mean RAND/GA/RG [0.847, 0.788, 0.804)] P1 [-0.0609, -0.0568] P3 [-0.0186, -0.0144]
A_noise|C|0.01 AUC mean RAND/GA/RG [0.846, 0.582, 0.687)] P1 [-0.2663, -0.2608] P3 [-0.112, -0.0986]
A_noise|C|0.02 AUC mean RAND/GA/RG [0.958, 0.728, 0.874)] P1 [-0.2293, -0.2308] P3 [-0.1481, -0.1431]


Reading (exploratory):
1. CNN: the MSE-driven GA is less detectable than random in all 4 cells, replicated across 2 seeds (P1 -0.057..-0.062 on tumour MRI, -0.23..-0.27 on noisy Alzheimer; seed-to-seed difference <= 0.006).
2. Mix control P3: ~0 to -0.02 on tumour MRI (GA advantage mostly an operator-mix effect), but -0.10..-0.15 on noisy Alzheimer (position choice matters for the CNN there).
3. This reverses the SRM-lite/SPAM result of E6 (GA more detectable on noisy Alzheimer). The 'detector truncates magnitude' explanation was TESTED in E8 (exp8.py, seed 0, 0.01 bpp: untruncated |difference| histograms of 1st/2nd-order residuals +HGB, plus SRM-lite re-run) and NOT supported: untruncated magnitude features still show GA MORE detectable on noisy Alzheimer (+0.09 HGB, +0.06 SRM-lite) and ~equal on tumour (-0.008..+0.019). So the CNN/feature-detector disagreement is unexplained (CNN may use spatial/joint structure the hand features miss, or be learning noise-specific artefacts of the synthetic-noise covers).
4. Caveats: small CPU-trained CNN (15 epochs), 2 seeds, shared image pool, no subject IDs, noisy-Alzheimer covers synthetic, bootstrap CIs not retrained (optimistic), single-detector-family claim risk. NOT independently verified. No SUCCESS_* state.
