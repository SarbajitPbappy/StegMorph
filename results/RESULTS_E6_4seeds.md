# E6 addendum: seeds 2 and 3 added (4 stego/crop replicates total) — EXPLORATORY

Same code (exp6.py, unmodified); seeds change crop positions, Alzheimer permutation and stego randomisation, so replicates share source images and are NOT fully independent. Mean of 4 seeds, SD across seeds, mean per-seed 90% bootstrap CI (optimistic: no refit, no multiplicity correction, near-duplicate cluster proxy for groups).

Per-cell numbers: see e6_4seed_summary table below (copied from the run output).

Headline (AUC differences, contrast = first minus second):
- A_noise (synthetic-noise Alzheimer covers): P1 GA-RAND = +0.027/+0.071 (A/B @0.005), +0.055/+0.096 (@0.01), +0.025/+0.045 (@0.02): all 6 CIs exclude 0. P3 GA-vs-random-with-GA's-branch-mix = -0.003..+0.005, all 6 CIs include 0 and across-seed SD <= 0.009. So most of the GA's extra detectability on these covers is reproduced by random selection that copies the GA's branch-bit mix. P2 (GA within RAND's branch mix) = +0.006..+0.029, 4 of 6 CIs exclude 0 (smallest-margin): a modest position effect remains, largest for detector B at 0.005 (+0.029, about 40% of P1).
- T_raw (real tumor covers): all contrasts within about +/-0.03, CIs include 0 in 17 of 18 (P1 B@0.02 +0.017, CI90 (+0.001,+0.032)); across-seed SD up to 0.02, i.e. replicate noise is as large as the effects. No evidence GA helps or hurts there.
- Interpretation caveat: branch-bit quotas only approximately equalise the operator mix (pairs and low-branch share differ slightly); the dark-background / 2-LSB mechanism is untested. Detectors are SRM-lite+LR and SPAM+HGB only (no CNN; torch install blocked/slow).
- No SUCCESS_* state: novelty gate for this angle is PARTIAL, and the evidence is exploratory.

## Table
cell | contrast: per-seed diffs (s0..s3), mean, SD across seeds, mean AUCs RAND/GA
T_raw|A|0.005 | P1 m=-0.004 sd=0.006 ci90~(-0.016,+0.010) [-0.011 +0.000 +0.002 -0.006] ; P2 m=+0.001 sd=0.006 ci90~(-0.011,+0.012) [+0.003 +0.001 -0.008 +0.006] ; P3 m=+0.007 sd=0.014 ci90~(-0.005,+0.019) [+0.001 +0.015 +0.022 -0.009]
T_raw|B|0.005 | P1 m=+0.010 sd=0.020 ci90~(-0.008,+0.031) [-0.015 +0.004 +0.030 +0.021] ; P2 m=-0.012 sd=0.013 ci90~(-0.032,+0.010) [-0.027 +0.003 -0.017 -0.005] ; P3 m=+0.004 sd=0.007 ci90~(-0.017,+0.025) [-0.003 +0.003 +0.002 +0.014]
T_raw|A|0.01 | P1 m=+0.006 sd=0.012 ci90~(-0.004,+0.017) [-0.008 +0.012 +0.019 +0.002] ; P2 m=+0.009 sd=0.008 ci90~(-0.000,+0.018) [-0.001 +0.016 +0.015 +0.004] ; P3 m=+0.007 sd=0.008 ci90~(-0.003,+0.016) [-0.001 +0.002 +0.015 +0.010]
T_raw|B|0.01 | P1 m=+0.012 sd=0.008 ci90~(-0.006,+0.031) [+0.010 +0.008 +0.006 +0.025] ; P2 m=+0.005 sd=0.004 ci90~(-0.014,+0.024) [+0.003 +0.006 +0.010 +0.001] ; P3 m=-0.007 sd=0.018 ci90~(-0.024,+0.011) [-0.025 -0.019 +0.002 +0.014]
T_raw|A|0.02 | P1 m=+0.002 sd=0.003 ci90~(-0.004,+0.007) [-0.002 +0.004 +0.003 +0.001] ; P2 m=+0.001 sd=0.002 ci90~(-0.004,+0.006) [-0.002 +0.001 +0.002 +0.002] ; P3 m=+0.001 sd=0.005 ci90~(-0.003,+0.006) [+0.006 +0.003 -0.006 +0.002]
T_raw|B|0.02 | P1 m=+0.017 sd=0.014 ci90~(+0.001,+0.032) [-0.002 +0.025 +0.030 +0.014] ; P2 m=+0.012 sd=0.009 ci90~(-0.003,+0.027) [+0.013 +0.020 +0.015 +0.000] ; P3 m=-0.002 sd=0.011 ci90~(-0.018,+0.013) [-0.014 -0.003 -0.002 +0.013]
A_noise|A|0.005 | P1 m=+0.027 sd=0.008 ci90~(+0.014,+0.038) [+0.027 +0.015 +0.031 +0.033] ; P2 m=+0.012 sd=0.005 ci90~(+0.001,+0.023) [+0.010 +0.008 +0.020 +0.009] ; P3 m=+0.005 sd=0.007 ci90~(-0.006,+0.016) [+0.011 +0.011 +0.000 -0.002]
A_noise|B|0.005 | P1 m=+0.071 sd=0.008 ci90~(+0.056,+0.088) [+0.082 +0.069 +0.072 +0.062] ; P2 m=+0.029 sd=0.011 ci90~(+0.012,+0.047) [+0.024 +0.046 +0.026 +0.022] ; P3 m=-0.002 sd=0.009 ci90~(-0.018,+0.013) [+0.009 +0.000 -0.014 -0.005]
A_noise|A|0.01 | P1 m=+0.055 sd=0.013 ci90~(+0.042,+0.069) [+0.061 +0.037 +0.054 +0.068] ; P2 m=+0.012 sd=0.013 ci90~(-0.000,+0.024) [+0.005 -0.003 +0.021 +0.025] ; P3 m=-0.003 sd=0.006 ci90~(-0.014,+0.009) [+0.003 +0.002 -0.007 -0.009]
A_noise|B|0.01 | P1 m=+0.096 sd=0.007 ci90~(+0.082,+0.108) [+0.087 +0.094 +0.101 +0.101] ; P2 m=+0.020 sd=0.007 ci90~(+0.007,+0.033) [+0.016 +0.012 +0.023 +0.029] ; P3 m=+0.001 sd=0.007 ci90~(-0.011,+0.013) [-0.006 +0.010 -0.001 -0.000]
A_noise|A|0.02 | P1 m=+0.025 sd=0.003 ci90~(+0.019,+0.032) [+0.023 +0.026 +0.029 +0.023] ; P2 m=+0.008 sd=0.005 ci90~(+0.002,+0.015) [+0.004 +0.007 +0.016 +0.005] ; P3 m=+0.001 sd=0.001 ci90~(-0.004,+0.006) [+0.000 +0.000 +0.001 +0.002]
A_noise|B|0.02 | P1 m=+0.045 sd=0.004 ci90~(+0.036,+0.053) [+0.049 +0.042 +0.040 +0.047] ; P2 m=+0.006 sd=0.005 ci90~(-0.002,+0.015) [+0.012 +0.005 +0.001 +0.008] ; P3 m=-0.002 sd=0.006 ci90~(-0.007,+0.004) [+0.006 -0.004 -0.002 -0.007]
