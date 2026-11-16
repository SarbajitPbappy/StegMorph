# Briefing for Fernaz Ma'am (first author): final state

Written 2026-11-14. Version 1 is tagged `v1-submitted-draft`. Version 2 is finished and verified; the article (20 pages) is `StegMorph_article.pdf`. Claims and outcomes are in the append-only `state/CLAIMS.md`.

## Main findings
1. **GA key vs random key:** no benefit for any detector, payload or collection. On IXI T2 no reduction larger than 0.005 AUC (full SRM, SRM-lite) fits the data (0.014 with refitted detectors). The GA puts its pixels in textured regions no more often than chance (34.3% vs 33.3%).
2. **Position matters:** choosing low-cost pixels directly lowers AUC by 0.11 to 0.19 against SRM-lite and full SRM, with an ordered dose-response, for five cost maps and for LSB replacement and LSB matching. This is a known principle; the contribution is the matched control.
3. **The detector decides:** real maxSRM given the pool removes the gain (-0.004 / +0.002). A residual CNN trained 30+ epochs shows about zero gap; a 4-epoch, 600-pair net shows -0.19. A Yedroudj-style net (AUC 0.82 on random keys) still shows -0.19. The SRNet-style net failed on the cost-guided set three times, so it gives no contrast.
4. **Reference embedders:** HILL and S-UNIWARD are far less detectable at equal payload mainly because they change a quarter as many pixels; at equal change counts the gap shrinks (HILL -0.147 vs random hybrid, level with the cost-guided key).
5. **Other data:** OASIS at 0.002 bpp is unsaturated with effects about a tenth to a sixth of IXI; CT stays saturated.
6. A GA with a HILL-cost fitness and a large search recovers part of the gain (-0.066 / -0.030).

## Limits to state honestly
Key-known detector is one seed; the CNN conclusion rests on one residual architecture; no extra non-JPEG collection (BraTS or fastMRI) because it needs a data request; pre-registration is an author-held log, not an independent registry; two references were added from memory and need checking.

## Needed from the authors
Target journal name; confirm the repository is public; verify `kodovsky2012ensemble` and `yedroudj2018yedroudj`; optionally request BraTS/fastMRI.
