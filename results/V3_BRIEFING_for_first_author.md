# Version 3 round: briefing for Fernaz Ma'am (first author)

DRAFT written 2026-11-15 while two jobs are still running (SRNet-style network, attempt 2; then BraTS). Items marked [open] are filled in when those finish. Everything below is in the append-only claims log (state/CLAIMS.md) with the date it was decided; nothing in this file replaces it.

## What version 3 set out to do
Make the network results valid or drop them, add one more non-JPEG collection, repeat the weak checks with three seeds, and make the paper's numbers come from one script. It also added a rule: a network contrast counts only if both keys reach a loss plateau and the random-key validation AUC is at least 0.85.

## What came out (all in the claims log)
- Yedroudj-style network (H21): not competent (random-key validation AUC 0.828 and 0.827, two seeds). The earlier gap of -0.19 is withdrawn from the abstract and highlights. Trained with the curriculum its gap is -0.019 and -0.006, so the earlier large value came from an under-trained network.
- SRNet-style network (H22): attempt 1 was not valid (the cost-guided run had not reached a plateau). Attempt 2 (last-stage cap raised from 60 to 120 epochs, declared before the run): random key valid (validation AUC 0.950, plateau reached); cost-guided partner [open].
- Key-known maxSRM, three seeds (H23): partly met. It beats the key-unknown detector as predicted, but the cost-guided gain is larger with the key known than with the pool known (-0.042 and -0.015 against -0.004 and +0.002), so one of three expectations fails in every seed.
- New collection, MSD brain tumour (H24b): not met as written, in the direction that supports the main claim. The GA key was more detectable than the foreground random key (by 0.14 to 0.21 AUC); the cost-guided key was easier to hide (-0.23 to -0.32). Unlike IXI, maxSRM given the pool does not remove the gain here (-0.233). We do not know why.
- GA key on OASIS (H25): met (difference between -0.016 and +0.006 AUC).
- Residual CNN on MSD (H27): declared, not yet run [open].
- BraTS 2020 (H26a to H26d): rules written before the download; includes a check for cases shared with MSD [open].

## What changed in the paper
Detector table (ten rows) and one detector count taken from it; a third-round results subsection; hypotheses rows H21 to H25 and H24b; limitations and conclusion rewritten (the network result rests on one competent architecture; maxSRM result limited to IXI T2); every number comes from numbers.tex, which a script writes from the stored result files. The script caught a rounding slip (4-epoch seed mean -0.016, not -0.017). I also fixed a stray line before the document class that stopped the file compiling. Abstract and highlights are drafted for both SRNet outcomes and go in when it is known.

## Decisions I made under "no approval needed" (for you to check)
1. Second SRNet attempt with only the epoch cap changed (declared before the run).
2. Skipped Yedroudj seed 2: one failing seed already decides the competence rule.
3. Foreground-restricted baseline for MSD, because the unrestricted random key is saturated.
4. The MSD residual CNN uses the fixed 60-epoch recipe with no plateau test (stated in H27).

## What stays fixed
Claims go into the log before the runs they cover; failed rules are reported as failed; no upload of the release package (it is built as a local folder only); the target journal is the authors' decision (see journal_decision.md).
