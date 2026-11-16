# Holm v2 (30 primary tests)

Honest Holm v2 (responds to verifier defects 1 and 5). Inputs: stored JSON only.
SE per cell = sqrt(bootstrap_SE^2 + seed_SD^2): subject-bootstrap SE (test-subject variance) plus between-seed SD (detector refit / key / message
variance across the 3 runs). Still NOT covering training-subject resampling (seeds reuse the full train split): stated limitation.
Family: PRIMARY contrasts only, non-duplicated cells: P1 (GA key vs random key) for E11 (0.02, 0.05), E12 (0.005 only; its 0.01 duplicates E14), E13 (3 scenarios), E14 (0.01, 0.02);
plus Q1 (cost-guided vs random) for E14. Floor SE 0.005 (no p below what AUC resolution supports). Two-sided normal p; TOST for +/-0.02.

| exp | cell | contrast | diff | SE | p Holm | differs | TOST p Holm | equivalent |
|---|---|---|---|---|---|---|---|---|
| E11 | IXI|A|0.02 | P1_ORIG-RANDSEQ | +0.002 | 0.005 | 1 | no | 0.00494 | YES |
| E11 | IXI|A|0.05 | P1_ORIG-RANDSEQ | +0.000 | 0.005 | 1 | no | 0.00102 | YES |
| E11 | IXI|B|0.02 | P1_ORIG-RANDSEQ | +0.037 | 0.018 | 0.893 | no | 1 | no |
| E11 | IXI|B|0.05 | P1_ORIG-RANDSEQ | +0.033 | 0.009 | 0.00746 | YES | 1 | no |
| E11 | IXI|C|0.02 | P1_ORIG-RANDSEQ | +0.000 | 0.005 | 1 | no | 0.000999 | YES |
| E11 | IXI|C|0.05 | P1_ORIG-RANDSEQ | -0.000 | 0.005 | 1 | no | 0.000977 | YES |
| E12 | IXI|A|0.005 | P1_ORIG-RANDSEQ | +0.016 | 0.007 | 0.427 | no | 1 | no |
| E12 | IXI|B|0.005 | P1_ORIG-RANDSEQ | +0.026 | 0.010 | 0.204 | no | 1 | no |
| E12 | IXI|C|0.005 | P1_ORIG-RANDSEQ | +0.013 | 0.011 | 1 | no | 1 | no |
| E13 | noHH|A|0.01 | P1_ORIG-RANDSEQ | -0.005 | 0.012 | 1 | no | 1 | no |
| E13 | noHH|B|0.01 | P1_ORIG-RANDSEQ | +0.059 | 0.025 | 0.364 | no | 1 | no |
| E13 | noHH|C|0.01 | P1_ORIG-RANDSEQ | +0.014 | 0.007 | 1 | no | 1 | no |
| E13 | noIOP|A|0.01 | P1_ORIG-RANDSEQ | -0.002 | 0.014 | 1 | no | 1 | no |
| E13 | noIOP|B|0.01 | P1_ORIG-RANDSEQ | +0.051 | 0.030 | 1 | no | 1 | no |
| E13 | noIOP|C|0.01 | P1_ORIG-RANDSEQ | +0.032 | 0.053 | 1 | no | 1 | no |
| E13 | oasis|A|0.01 | P1_ORIG-RANDSEQ | -0.035 | 0.033 | 1 | no | 1 | no |
| E13 | oasis|B|0.01 | P1_ORIG-RANDSEQ | -0.007 | 0.011 | 1 | no | 1 | no |
| E13 | oasis|C|0.01 | P1_ORIG-RANDSEQ | +0.010 | 0.040 | 1 | no | 1 | no |
| E14 | IXI|A|0.01 | P1_ORIG-RANDSEQ | +0.016 | 0.005 | 0.0276 | YES | 1 | no |
| E14 | IXI|A|0.01 | Q1_COSTKEY-RANDSEQ | -0.145 | 0.009 | 0 | YES | 1 | no |
| E14 | IXI|A|0.02 | P1_ORIG-RANDSEQ | +0.003 | 0.005 | 1 | no | 0.00998 | YES |
| E14 | IXI|A|0.02 | Q1_COSTKEY-RANDSEQ | -0.183 | 0.007 | 0 | YES | 1 | no |
| E14 | IXI|B|0.01 | P1_ORIG-RANDSEQ | +0.022 | 0.014 | 1 | no | 1 | no |
| E14 | IXI|B|0.01 | Q1_COSTKEY-RANDSEQ | -0.025 | 0.010 | 0.263 | no | 1 | no |
| E14 | IXI|B|0.02 | P1_ORIG-RANDSEQ | +0.036 | 0.009 | 0.00103 | YES | 1 | no |
| E14 | IXI|B|0.02 | Q1_COSTKEY-RANDSEQ | -0.028 | 0.015 | 1 | no | 1 | no |
| E14 | IXI|C|0.01 | P1_ORIG-RANDSEQ | +0.004 | 0.005 | 1 | no | 0.0181 | YES |
| E14 | IXI|C|0.01 | Q1_COSTKEY-RANDSEQ | +0.014 | 0.011 | 1 | no | 1 | no |
| E14 | IXI|C|0.02 | P1_ORIG-RANDSEQ | -0.002 | 0.005 | 1 | no | 0.00349 | YES |
| E14 | IXI|C|0.02 | Q1_COSTKEY-RANDSEQ | +0.005 | 0.006 | 1 | no | 0.0691 | no |

Differences surviving Holm: 5/30; equivalences within +/-0.02: 7/30.