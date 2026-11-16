# Novelty check, round 2 (11 Nov 2026) - IN PROGRESS, not a verdict
Search tools: Scite and alphaXiv failed to connect this session; only standard web search worked (5 queries in this round, on top of 15+ in earlier rounds).
Snippets only; no full text read in this round. Treat every item as "to verify in the original".

| Topic | Closest hit | What it implies for us |
|---|---|---|
| Edge/texture-guided LSB pixel selection | Luo, Huang, Huang, "Edge Adaptive Image Steganography Based on LSB Matching Revisited", IEEE TIFS 2010 (doi 10.1109/tifs.2010.2041812) | Texture-guided selection in LSB with better security vs several steganalyzers is PUBLISHED. Our COSTKEY result is not new as a method. |
| Cost-function guided embedding (HILL, S-UNIWARD, WOW) | Content-adaptive literature (Fridrich/Denemark group) | Matches our HILL benchmark: real adaptive embedders are far less detectable. Not new. |
| GA pixel selection vs RS/chi-square | Several GA+LSB papers (e.g. arXiv 1204.2616) | Claim security by RS/chi-square only; none found comparing GA key against a random key under SRM/SPAM/CNN. Gap NOT yet confirmed absent. |
| Random key vs optimized path ablation | None found | Open, but absence in web snippets is weak evidence. |
| Optimisation pixel selection, null result vs random | None found | Open, same caveat. |
| PVD+LSB on MRI with subject-level split | None found | Open, same caveat. |

Provisional reading: the cost-guided key is prior art (not a contribution). The possibly-novel part is the controlled NEGATIVE finding (GA key is not more secure than a random key under operator-matched controls, three detectors, subject-disjoint splits). Needs: full-text read of Vazquez and Denemark WIFS14, more queries via a working scholarly index, and recorded in literature_matrix.csv.

## Update (later same day)
- Denemark, Sedighi, Cogranne, Holub, Fridrich, "Selection-channel-aware rich model for steganalysis of digital images", IEEE WIFS 2014, pp. 48-53, doi 10.1109/WIFS.2014.7084302 (confirmed via HAL record hal-02362227; abstract-level only, full PDF NOT read). Relevance: detectors that use the selection channel (maxSRMd2) work better, and overly adaptive schemes look more vulnerable. It does not compare an optimised key against a random key, so it is not a direct overlap with our negative result. It does warn that our detectors (no selection-channel knowledge) are weaker than the state of the art: a limitation to state in the paper.
- Vazquez (frobt 2023): my guessed URL returned 404; not read. Need the correct URL or DOI from literature_matrix.csv before reading.

## Correction
Vazquez et al. was already read earlier (doi 10.3389/frobt.2022.1031299, year 2022, not 2023; my 404 URL was a wrong guess). Earlier gate notes: zero-alteration GA scheme (cover unchanged), fitness = located bits, no steganalysis, no random-selection control, no MRI security test. So it does not overlap with our negative result. Read was targeted extraction, not a linear read.
