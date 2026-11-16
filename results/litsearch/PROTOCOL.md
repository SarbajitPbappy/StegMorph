# Documented literature search (13 Nov 2026)

Aim: find English-language studies that (a) choose embedding positions in spatial-domain image steganography with a heuristic or metaheuristic (GA, PSO, ACO, ABC, ...), or (b) steganalyse medical images, and check whether any of them compares the optimised key with an operator-matched random key under trained steganalysers.

Index: Crossref REST API (`api.crossref.org/works`, field `query.bibliographic`, 60 rows per query and record type, journal articles and proceedings papers published from 2010-01-01). Scopus and Web of Science were not available from the environment used for this work; PubMed was not queried because the topic is not biomedical-literature indexed. Code: `code/litsearch_crossref.py`; raw output `crossref_raw.json`.

Queries (Q1-Q8):
1. steganography genetic algorithm pixel selection LSB
2. steganography particle swarm optimization embedding location LSB
3. metaheuristic optimization pixel selection image steganography security steganalysis
4. LSB PVD hybrid steganography genetic algorithm
5. steganography medical image optimization steganalysis
6. steganalysis brain MRI deep learning
7. content-adaptive steganography random key comparison optimized embedding location steganalysis SRM
8. evolutionary algorithm embedding path LSB matching steganalysis resistance

Flow: 960 records returned; 739 unique DOIs after de-duplication; 555 with a steganography-related title; 350 after a keyword screen of titles for optimisation, medical or steganalysis terms (`screen1.json`); 52 titles with a metaheuristic term and 20 with a medical term (72 candidates after merging, `screen2.json`).

Inclusion: spatial-domain image steganography with optimised position selection, or medical-image steganography/steganalysis; English; evaluation with steganalysis reported. Exclusion: audio/video/text, transform-domain only without a spatial counterpart, reviews without experiments.

Limits (important): the screen is by title; Crossref carries abstracts for only a few of the candidates and most full texts are paywalled, so only the studies listed in Table 1 of the article (about 22 English papers read in full across earlier rounds) were assessed in depth. A candidate that was screened only by title may contain a random-key comparison; the article therefore states "in the studies we read" and never "no study". The search was run once, by one reader.
