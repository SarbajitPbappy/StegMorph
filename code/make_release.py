"""Builds release/StegMorph_evaluation_release.zip for deposit (Zenodo/OSF/GitHub): code, claims log, result JSON/scores/logs, trained CNN checkpoints, figures, article sources, split manifests, checksums. Data are NOT included (public collections: IXI, OASIS, MedMNIST+)."""
import os, shutil, hashlib, zipfile, glob, datetime
R = "release/pkg"; shutil.rmtree("release", ignore_errors=True); os.makedirs(R)
def cp(src, dst=None):
    dst = os.path.join(R, dst or src); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
for f in glob.glob("code/**/*", recursive=True):
    if os.path.isfile(f) and "__pycache__" not in f and not f.endswith(".pyc"): cp(f)
for f in ["stegmorph.py", "state/CLAIMS.md", "state/STATE.json", "literature_matrix.csv"]:
    if os.path.exists(f): cp(f)
for f in glob.glob("github/aletheia_src/aletheia-master/aletheia-cache/octave/*"): cp(f, "octave_reference/" + os.path.basename(f))
for f in glob.glob("results/**/*", recursive=True):
    if os.path.isfile(f) and "/data" not in f and not f.endswith(".pt") and "_VOID" not in f and os.path.getsize(f) < 30e6: cp(f)
for f in glob.glob("results/e26/*.pt"): cp(f)
for f in glob.glob("data/splits/*manifest*.json"): cp(f)
for f in glob.glob("Overleaf/article/figures/*.png") + glob.glob("Overleaf/article/sections/*.tex") + glob.glob("Overleaf/article/tables/*.tex") + ["Overleaf/article/article.tex", "Overleaf/article/refs.bib", "Overleaf/article/article.pdf"]:
    if os.path.exists(f): cp(f)
open(os.path.join(R, "README.md"), "w").write(f"""# Evaluation of GA-keyed hybrid LSB/PVD steganography on brain MRI: code, claims log and results
Built {datetime.date.today().isoformat()}. Authors: Fernaz Narin Nur, Sarbajit Paul Bappy (equal contribution).

## Contents
- `code/`: embedders and detectors (`lab24.py`, `exp24.py` driver, `nets26.py`, `exp26_cnn.py`, ...), split builders, figure/table scripts (`make_paper_figs.py`, `make_paper_figs2.py`, `make_tables.py`), `octave/` wrappers of the reference HILL and S-UNIWARD simulators.
- `octave_reference/`: the reference simulators as distributed in the Aletheia toolkit (HILL: Shenzhen University 2014; S-UNIWARD: DDE Lab, Binghamton 2013) with their licence files. Keep the notices; research/non-profit use only.
- `state/CLAIMS.md`: append-only log with every pre-registration and outcome (written before the experiments they cover). It should be deposited with its original time stamps; the file system time stamps are in the zip.
- `results/`: result JSON, score arrays, logs and CNN checkpoints (`results/e26/*.pt`) for experiments E1-E35; `results/litsearch/` documents the literature search.
- `data/splits/*manifest*.json`: subject-split manifests with checksums. The image data are not included: IXI (T2 and T1, CC BY-SA 3.0, brain-development.org), OASIS cross-sectional, OrganAMNIST from MedMNIST+ (CC BY 4.0, Zenodo 10519652).
- `Overleaf/article/`: article sources and compiled PDF.

## Reproduce
Python 3.14, numpy 2.5, scipy 1.18, scikit-learn 1.9, torch 2.15 (MPS), nibabel 5.5, Octave 11 with the image package. From the project root: build the splits (`code/build_ixi_splits.py`, `code/build_ixi_t1_splits.py`, `code/build_ct_splits.py`, `code/build_ixi256_splits.py`), then `SCH=... DETS=... PAY=... OUT=results/eXX python code/exp24.py SEED` (see `results/*/run.sh` for the exact settings of every experiment), `python code/make_paper_figs2.py` and `python code/make_tables.py`.
Seeds: 0, 1, 2 (0, 1 for 256x256); a seed fixes the messages, the keys, the 80% training-subject subsample and the network initialisation.
""")
sums = []
for root, _, fs in os.walk(R):
    for f in fs: p = os.path.join(root, f); sums.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, R)}")
open(os.path.join(R, "SHA256SUMS.txt"), "w").write("\n".join(sorted(sums)) + "\n")
with zipfile.ZipFile("release/StegMorph_evaluation_release.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, fs in os.walk(R):
        for f in fs: p = os.path.join(root, f); z.write(p, os.path.relpath(p, R))
print("zip", round(os.path.getsize("release/StegMorph_evaluation_release.zip") / 1e6, 1), "MB;", len(sums), "files")
