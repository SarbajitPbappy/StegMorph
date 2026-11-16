# Holm correction across E11-E14 (60 tests)

Holm correction + equivalence (TOST) across E11-E14. Inputs: stored JSON only.
Per cell/contrast: mean diff over 3 seeds; SE from each seed's subject-bootstrap 95% CI ((hi-lo)/3.92); pooled SE = mean of seed SEs
(conservative: the three seeds reuse the same test subjects, so no 1/sqrt(3) shrinkage). Two-sided normal p for H0: diff=0.
TOST p for equivalence margin +/-0.02: max(p(diff>-0.02), p(diff<+0.02)). Holm over the whole family, separately for difference and equivalence tests.

| exp | cell | contrast | diff | SE | p | p Holm | differs (Holm<0.05) | TOST p Holm | equivalent (<0.05) |
|---|---|---|---|---|---|---|---|---|---|
| E11 | IXI|A|0.02 | P1_ORIG-RANDSEQ | +0.002 | 0.004 | 0.534 | 1 | no | 1.88e-05 | YES |
| E11 | IXI|A|0.02 | P3_ORIG-RANDMIX | +0.001 | 0.003 | 0.837 | 1 | no | 4.01e-07 | YES |
| E11 | IXI|A|0.05 | P1_ORIG-RANDSEQ | +0.000 | 0.001 | 0.799 | 1 | no | 4.38e-200 | YES |
| E11 | IXI|A|0.05 | P3_ORIG-RANDMIX | -0.000 | 0.001 | 0.816 | 1 | no | 6.5e-174 | YES |
| E11 | IXI|B|0.02 | P1_ORIG-RANDSEQ | +0.037 | 0.008 | 5.86e-06 | 0.00031 | YES | 1 | no |
| E11 | IXI|B|0.02 | P3_ORIG-RANDMIX | +0.020 | 0.008 | 0.0155 | 0.572 | no | 1 | no |
| E11 | IXI|B|0.05 | P1_ORIG-RANDSEQ | +0.033 | 0.006 | 3.07e-07 | 1.72e-05 | YES | 1 | no |
| E11 | IXI|B|0.05 | P3_ORIG-RANDMIX | +0.017 | 0.006 | 0.00466 | 0.21 | no | 1 | no |
| E11 | IXI|C|0.02 | P1_ORIG-RANDSEQ | +0.000 | 0.001 | 0.946 | 1 | no | 2.4e-39 | YES |
| E11 | IXI|C|0.02 | P3_ORIG-RANDMIX | +0.000 | 0.002 | 1 | 1 | no | 1.38e-37 | YES |
| E11 | IXI|C|0.05 | P1_ORIG-RANDSEQ | -0.000 | 0.000 | 0.806 | 1 | no | 0 | YES |
| E11 | IXI|C|0.05 | P3_ORIG-RANDMIX | +0.000 | 0.000 | 1 | 1 | no | 0 | YES |
| E12 | IXI|A|0.005 | P1_ORIG-RANDSEQ | +0.016 | 0.004 | 0.000204 | 0.0104 | YES | 1 | no |
| E12 | IXI|A|0.005 | P3_ORIG-RANDMIX | +0.002 | 0.004 | 0.583 | 1 | no | 0.00226 | YES |
| E12 | IXI|A|0.01 | P1_ORIG-RANDSEQ | +0.010 | 0.005 | 0.0492 | 1 | no | 0.955 | no |
| E12 | IXI|A|0.01 | P3_ORIG-RANDMIX | -0.004 | 0.004 | 0.398 | 1 | no | 0.00389 | YES |
| E12 | IXI|B|0.005 | P1_ORIG-RANDSEQ | +0.026 | 0.008 | 0.000582 | 0.0279 | YES | 1 | no |
| E12 | IXI|B|0.005 | P3_ORIG-RANDMIX | +0.013 | 0.008 | 0.108 | 1 | no | 1 | no |
| E12 | IXI|B|0.01 | P1_ORIG-RANDSEQ | +0.025 | 0.009 | 0.00674 | 0.296 | no | 1 | no |
| E12 | IXI|B|0.01 | P3_ORIG-RANDMIX | +0.015 | 0.009 | 0.0777 | 1 | no | 1 | no |
| E12 | IXI|C|0.005 | P1_ORIG-RANDSEQ | +0.013 | 0.006 | 0.0184 | 0.664 | no | 1 | no |
| E12 | IXI|C|0.005 | P3_ORIG-RANDMIX | -0.004 | 0.006 | 0.505 | 1 | no | 0.101 | no |
| E12 | IXI|C|0.01 | P1_ORIG-RANDSEQ | +0.007 | 0.004 | 0.0548 | 1 | no | 0.0172 | YES |
| E12 | IXI|C|0.01 | P3_ORIG-RANDMIX | -0.001 | 0.004 | 0.843 | 1 | no | 1.64e-05 | YES |
| E13noHH | noHH|A|0.01 | P1_ORIG-RANDSEQ | -0.005 | 0.008 | 0.496 | 1 | no | 1 | no |
| E13noHH | noHH|A|0.01 | P3_ORIG-RANDMIX | -0.018 | 0.008 | 0.0287 | 1 | no | 1 | no |
| E13noHH | noHH|B|0.01 | P1_ORIG-RANDSEQ | +0.059 | 0.016 | 0.000262 | 0.0128 | YES | 1 | no |
| E13noHH | noHH|B|0.01 | P3_ORIG-RANDMIX | +0.018 | 0.021 | 0.393 | 1 | no | 1 | no |
| E13noHH | noHH|C|0.01 | P1_ORIG-RANDSEQ | +0.014 | 0.005 | 0.00382 | 0.176 | no | 1 | no |
| E13noHH | noHH|C|0.01 | P3_ORIG-RANDMIX | +0.003 | 0.005 | 0.564 | 1 | no | 0.0235 | YES |
| E13noIOP | noIOP|A|0.01 | P1_ORIG-RANDSEQ | -0.002 | 0.013 | 0.909 | 1 | no | 1 | no |
| E13noIOP | noIOP|A|0.01 | P3_ORIG-RANDMIX | -0.004 | 0.013 | 0.737 | 1 | no | 1 | no |
| E13noIOP | noIOP|B|0.01 | P1_ORIG-RANDSEQ | +0.051 | 0.029 | 0.0788 | 1 | no | 1 | no |
| E13noIOP | noIOP|B|0.01 | P3_ORIG-RANDMIX | +0.028 | 0.022 | 0.207 | 1 | no | 1 | no |
| E13noIOP | noIOP|C|0.01 | P1_ORIG-RANDSEQ | +0.032 | 0.012 | 0.00875 | 0.352 | no | 1 | no |
| E13noIOP | noIOP|C|0.01 | P3_ORIG-RANDMIX | +0.024 | 0.012 | 0.046 | 1 | no | 1 | no |
| E13oasis | oasis|A|0.01 | P1_ORIG-RANDSEQ | -0.035 | 0.007 | 7.69e-07 | 4.23e-05 | YES | 1 | no |
| E13oasis | oasis|A|0.01 | P3_ORIG-RANDMIX | -0.009 | 0.007 | 0.242 | 1 | no | 1 | no |
| E13oasis | oasis|B|0.01 | P1_ORIG-RANDSEQ | -0.007 | 0.010 | 0.474 | 1 | no | 1 | no |
| E13oasis | oasis|B|0.01 | P3_ORIG-RANDMIX | -0.002 | 0.010 | 0.814 | 1 | no | 1 | no |
| E13oasis | oasis|C|0.01 | P1_ORIG-RANDSEQ | +0.010 | 0.003 | 0.00254 | 0.119 | no | 0.0466 | YES |
| E13oasis | oasis|C|0.01 | P3_ORIG-RANDMIX | -0.014 | 0.005 | 0.0102 | 0.399 | no | 1 | no |
| E14 | IXI|A|0.01 | P1_ORIG-RANDSEQ | +0.016 | 0.004 | 0.000253 | 0.0127 | YES | 1 | no |
| E14 | IXI|A|0.01 | Q1_COSTKEY-RANDSEQ | -0.145 | 0.009 | 0 | 0 | YES | 1 | no |
| E14 | IXI|A|0.01 | Q2_COSTKEY-COSTMIX | -0.148 | 0.008 | 0 | 0 | YES | 1 | no |
| E14 | IXI|A|0.02 | P1_ORIG-RANDSEQ | +0.003 | 0.004 | 0.382 | 1 | no | 0.000146 | YES |
| E14 | IXI|A|0.02 | Q1_COSTKEY-RANDSEQ | -0.183 | 0.007 | 0 | 0 | YES | 1 | no |
| E14 | IXI|A|0.02 | Q2_COSTKEY-COSTMIX | -0.185 | 0.007 | 0 | 0 | YES | 1 | no |
| E14 | IXI|B|0.01 | P1_ORIG-RANDSEQ | +0.022 | 0.009 | 0.0086 | 0.352 | no | 1 | no |
| E14 | IXI|B|0.01 | Q1_COSTKEY-RANDSEQ | -0.025 | 0.009 | 0.00758 | 0.321 | no | 1 | no |
| E14 | IXI|B|0.01 | Q2_COSTKEY-COSTMIX | -0.024 | 0.009 | 0.00747 | 0.321 | no | 1 | no |
| E14 | IXI|B|0.02 | P1_ORIG-RANDSEQ | +0.036 | 0.008 | 7.61e-06 | 0.000396 | YES | 1 | no |
| E14 | IXI|B|0.02 | Q1_COSTKEY-RANDSEQ | -0.028 | 0.011 | 0.0125 | 0.474 | no | 1 | no |
| E14 | IXI|B|0.02 | Q2_COSTKEY-COSTMIX | -0.048 | 0.010 | 4.04e-06 | 0.000218 | YES | 1 | no |
| E14 | IXI|C|0.01 | P1_ORIG-RANDSEQ | +0.004 | 0.004 | 0.275 | 1 | no | 0.000674 | YES |
| E14 | IXI|C|0.01 | Q1_COSTKEY-RANDSEQ | +0.014 | 0.010 | 0.163 | 1 | no | 1 | no |
| E14 | IXI|C|0.01 | Q2_COSTKEY-COSTMIX | +0.003 | 0.009 | 0.734 | 1 | no | 1 | no |
| E14 | IXI|C|0.02 | P1_ORIG-RANDSEQ | -0.002 | 0.002 | 0.268 | 1 | no | 2.03e-42 | YES |
| E14 | IXI|C|0.02 | Q1_COSTKEY-RANDSEQ | +0.005 | 0.005 | 0.354 | 1 | no | 0.0415 | YES |
| E14 | IXI|C|0.02 | Q2_COSTKEY-COSTMIX | +0.003 | 0.005 | 0.523 | 1 | no | 0.00803 | YES |

Differences surviving Holm: 13/60. Equivalences (within +/-0.02) surviving Holm: 19/60.
Limitation: SE is derived from the bootstrap CI over test subjects only; detector refit variance is covered only by the seed spread. Treat p-values as approximate.