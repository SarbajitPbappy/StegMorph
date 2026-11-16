# E8 three-seed addendum (seeds 0-2), appended to RESULTS_E7_E8.md
Mean test AUC over 3 seeds (SRM-lite+LR / SCA-lite+LR / SPAM+HGB). Raw JSONs: results/e8/.
Per-seed values are in the JSONs; every paired-bootstrap CI vs RAND for GREEDY_TEX and HILL_SIM is entirely below 0 in all 3 seeds on both datasets and all 3 detectors.
Direction of every effect was the same in all seeds; seed 0 findings are therefore not seed artefacts.
Conclusion unchanged: the content-adaptive cost sharply lowers detectability vs random/MSE-GA selection, but the idealised HILL_SIM embedder remains far stronger (AUC ~0.5-0.58). Not a groundbreaking claim.

A_raw @ 0.02 bpp mean AUC (3 seeds):
  RAND|srm: 1.000
  RAND|sca: 0.992
  RAND|spam: 1.000
  GREEDY_TEX|srm: 0.779
  GREEDY_TEX|sca: 0.824
  GREEDY_TEX|spam: 0.705
  HILL_SIM|srm: 0.543
  HILL_SIM|sca: 0.547
  HILL_SIM|spam: 0.504

T_raw @ 0.01 bpp mean AUC (3 seeds):
  RAND|srm: 0.887
  RAND|sca: 0.834
  RAND|spam: 0.689
  GREEDY_TEX|srm: 0.696
  GREEDY_TEX|sca: 0.750
  GREEDY_TEX|spam: 0.513
  HILL_SIM|srm: 0.570
  HILL_SIM|sca: 0.578
  HILL_SIM|spam: 0.511
