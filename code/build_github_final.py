"""Builds github_final/: the folder to push to GitHub. Starts from a copy of StegMorph-repo (keeps .git and history), then refreshes code, claims log, results (no .pt, files under 30 MB), split manifests, article sources and figures, the final PDF, LICENSE (MIT), README and checksums. Nothing is committed or pushed. Run from the project root."""
import os, shutil, glob, hashlib, datetime
SRC, OUT = "StegMorph-repo", "github_final"
shutil.rmtree(OUT, ignore_errors=True); shutil.copytree(SRC, OUT, symlinks=True)
def cp(src, dst=None):
    d = os.path.join(OUT, dst or src); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(src, d)
shutil.rmtree(os.path.join(OUT, "code"), ignore_errors=True)
for f in glob.glob("code/**/*", recursive=True):
    if os.path.isfile(f) and "__pycache__" not in f and not f.endswith(".pyc"): cp(f)
for f in ("stegmorph.py", "state/CLAIMS.md", "state/STATE.json", "literature_matrix.csv"):
    if os.path.exists(f): cp(f)
for f in glob.glob("results/**/*", recursive=True):
    if not os.path.isfile(f) or f.endswith(".pt") or "_VOID" in f or "/ckpt/" in f or "/data" in f or "/cache/" in f or f.endswith((".h5", ".npy", ".nii", ".gz")) or os.path.getsize(f) >= 30e6: continue
    if "BRIEFING_for_first_author" in f: continue
    cp(f)
for f in glob.glob("data/splits/*manifest*.json"): cp(f)
for pat in ("*.tex", "*.bib", "*.bst", "*.cls", "*.sty"):
    for f in glob.glob("Overleaf/article/" + pat): cp(f)
for f in glob.glob("Overleaf/article/sections/*.tex") + glob.glob("Overleaf/article/tables/*.tex") + glob.glob("Overleaf/article/figures/*.png") + glob.glob("Overleaf/article/figures/fig*.pdf") + glob.glob("Overleaf/article/figures/*.tikz") + glob.glob("Overleaf/article/figures/*standalone.tex") + glob.glob("Overleaf/article/figures/*standalone.pdf"): cp(f)
for f in glob.glob(os.path.join(OUT, "Overleaf/article/figures/*.png")):  # older PNG versions from the previous push; the paper now uses the PDF figures
    os.remove(f)
cp("Overleaf/article/article.pdf"); cp("Overleaf/article/article.pdf", "StegMorph_article.pdf")
for junk in ("journal_decision.md",):
    if os.path.exists(os.path.join(OUT, junk)): os.remove(os.path.join(OUT, junk))
open(os.path.join(OUT, "LICENSE"), "w").write("""MIT License

Copyright (c) 2026 Fernaz Narin Nur, Sarbajit Paul Bappy, SKM Shadekul Islam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
open(os.path.join(OUT, "README.md"), "w").write(f"""# Optimised Pixel Selection and the Detectability of Hybrid LSB/PVD Steganography: A Controlled Evaluation on Brain MRI

Authors: Fernaz Narin Nur, Sarbajit Paul Bappy (equal contribution, first authors), SKM Shadekul Islam. Corresponding author: Sarbajit Paul Bappy (bappy15-6155@s.diu.edu.bd). Department of Computer Science and Engineering, Daffodil International University, Dhaka, Bangladesh.

Code, append-only claims log, result files and article sources for the study. Folder refreshed {datetime.date.today().isoformat()} (version 3). The compiled paper is `StegMorph_article.pdf`.

## What the study asks and finds
Does a genetic-algorithm (GA) pixel key make hybrid LSB/PVD steganography harder to detect than a random key of the same embedder? On subject-disjoint brain MRI with operator-matched controls, the GA key was never harder to detect (bound 0.005 AUC on IXI T2). Choosing low-cost textured pixels does lower detectability for rich-model features, but maxSRM removes that gain on IXI T2 and not on MSD or BraTS, and a competent SRNet-style network detects the cost-guided key better than the random key (mean +0.033 AUC over three seeds). Residual CNNs on MSD and BraTS did not reach the pre-registered competence level and are not interpreted.

## Contents
- `code/`: embedders, detectors, experiment drivers, split builders, figure, table and macro scripts. `make_macros.py` writes `Overleaf/article/numbers.tex`, so every number in the paper comes from the stored result files.
- `state/CLAIMS.md`: append-only log. Each hypothesis and decision rule was written before the runs it covers; failed rules are reported as failed.
- `results/`: result JSON, score arrays and logs for every experiment (model checkpoints are not in this repository, see below).
- `data/splits/`: subject-split manifests with checksums. Image data are not included.
- `octave_reference/`: the reference HILL and S-UNIWARD simulators as distributed in the Aletheia toolkit, with their own licence files (research and non-profit use).
- `Overleaf/article/`: LaTeX sources, tables, figures and the compiled PDF.

## Data (not redistributed)
IXI T2 and T1 (CC BY-SA 3.0, brain-development.org), OASIS cross-sectional, OrganAMNIST from MedMNIST+ (CC BY 4.0, Zenodo 10519652), Medical Segmentation Decathlon Task01 brain tumour, BraTS 2020 training data (only the 107 patients not present in MSD are used). Download them separately and build the splits with `code/build_*_splits.py`.

## Reproduce
Python 3.14, numpy 2.5, scipy 1.18, scikit-learn 1.9, torch 2.15 (MPS), nibabel 5.5, Octave 11 with the image package. From the repository root: build the splits, run `SCH=... DETS=... PAY=... OUT=results/eXX python code/exp24.py SEED` (exact settings in `results/*/run.sh`), then `python code/make_macros.py`, `python code/make_tables.py` and the figure scripts, and compile `Overleaf/article/article.tex` (pdflatex, bibtex, pdflatex twice). Seeds 0, 1, 2: a seed fixes the messages, keys, the 80% training-subject subsample and the network initialisation.

Trained network checkpoints are large (about 3 GB for the SRNet-style curriculum runs) and are not in this repository; the training scripts (`code/exp42_curriculum.py`) regenerate them, and the authors can share them on request.

## Licence
MIT for the authors' code and text (see `LICENSE`). Third-party simulators in `octave_reference/` and the image collections keep their own licences.

## Paths
Local absolute paths in logs were replaced by `<PROJECT_ROOT>`. Run scripts from the repository root.
""")
for junk in ("Overleaf/article/article_v1_backup.tex", "Overleaf/article/main.tex", "Overleaf/article/example.bib"):
    if os.path.exists(os.path.join(OUT, junk)): os.remove(os.path.join(OUT, junk))
for root, ds, fs in os.walk(OUT):  # replace local absolute paths, as in earlier releases
    ds[:] = [d for d in ds if d != ".git"]
    for f in fs:
        if f.endswith((".log", ".sh", ".json", ".md", ".py", ".txt", ".tex", ".csv", ".out", ".ipynb")):
            p_ = os.path.join(root, f)
            try: t = open(p_, encoding="utf-8").read()
            except Exception: continue
            t2 = t.replace("<PROJECT_ROOT>", "<PROJECT_ROOT>").replace("<TMP>/octbrats", "<TMP>/octbrats").replace("<HOME>", "<HOME>")
            if t2 != t: open(p_, "w", encoding="utf-8").write(t2)
rows = []
for root, ds, fs in os.walk(OUT):
    ds[:] = [d for d in ds if d != ".git"]
    for f in sorted(fs):
        if f == "SHA256SUMS.txt": continue
        p = os.path.join(root, f); rows.append(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + os.path.relpath(p, OUT))
open(os.path.join(OUT, "SHA256SUMS.txt"), "w").write("\n".join(sorted(rows, key=lambda r: r.split("  ", 1)[1])) + "\n")
print(len(rows), "files")
