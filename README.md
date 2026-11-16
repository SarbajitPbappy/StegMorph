# Optimised Pixel Selection and the Detectability of Hybrid LSB/PVD Steganography: A Controlled Evaluation on Brain MRI

Authors: Fernaz Narin Nur, Sarbajit Paul Bappy (equal contribution, first authors), SKM Shadekul Islam. Corresponding author: Sarbajit Paul Bappy (bappy15-6155@s.diu.edu.bd). Department of Computer Science and Engineering, Daffodil International University, Dhaka, Bangladesh.

Code, append-only claims log, result files and article sources for the study. Folder refreshed 2026-11-16 (version 3).

## What the study asks and finds
Does a genetic-algorithm (GA) pixel key make hybrid LSB/PVD steganography harder to detect than a random key of the same embedder? On subject-disjoint brain MRI with operator-matched controls, the GA key was never harder to detect (bound 0.005 AUC on IXI T2). Choosing low-cost textured pixels does lower detectability for rich-model features, but maxSRM removes that gain on IXI T2 and not on MSD or BraTS, and a competent SRNet-style network detects the cost-guided key better than the random key (mean +0.033 AUC over three seeds). Residual CNNs on MSD and BraTS did not reach the pre-registered competence level and are not interpreted.

## Contents
- `code/`: embedders, detectors, experiment drivers, split builders, figure, table and macro scripts. `make_macros.py` writes `numbers.tex`, so every number in the paper comes from the stored result files.
- `state/CLAIMS.md`: append-only log. Each hypothesis and decision rule was written before the runs it covers; failed rules are reported as failed.
- `results/`: result JSON, score arrays and logs for every experiment (model checkpoints are not in this repository, see below).
- `data/splits/`: subject-split manifests with checksums. Image data are not included.
- `octave_reference/`: the reference HILL and S-UNIWARD simulators as distributed in the Aletheia toolkit, with their own licence files (research and non-profit use).

## Data (not redistributed)
IXI T2 and T1 (CC BY-SA 3.0, brain-development.org), OASIS cross-sectional, OrganAMNIST from MedMNIST+ (CC BY 4.0, Zenodo 10519652), Medical Segmentation Decathlon Task01 brain tumour, BraTS 2020 training data (only the 107 patients not present in MSD are used). Download them separately and build the splits with `code/build_*_splits.py`.

## Reproduce
Python 3.14, numpy 2.5, scipy 1.18, scikit-learn 1.9, torch 2.15 (MPS), nibabel 5.5, Octave 11 with the image package. From the repository root: build the splits, run `SCH=... DETS=... PAY=... OUT=results/eXX python code/exp24.py SEED` (exact settings in `results/*/run.sh`), then `python code/make_macros.py`, `python code/make_tables.py` and the figure scripts. Seeds 0, 1, 2: a seed fixes the messages, keys, the 80% training-subject subsample and the network initialisation.

Trained network checkpoints are large (about 3 GB for the SRNet-style curriculum runs) and are not in this repository; the training scripts (`code/exp42_curriculum.py`) regenerate them, and the authors can share them on request.

## Licence
MIT for the authors' code and text (see `LICENSE`). Third-party simulators in `octave_reference/` and the image collections keep their own licences.

## Paths
Local absolute paths in logs were replaced by `<PROJECT_ROOT>`. Run scripts from the repository root.
# StegMorph
