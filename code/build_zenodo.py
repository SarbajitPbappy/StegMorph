"""V3.5: build the Zenodo release package as a LOCAL folder (release/zenodo_v3). Nothing is uploaded.
Contents: code/, state/CLAIMS.md, result summaries and per-run JSON (no raw image data, no large checkpoints except best CNN checkpoints), split manifests, article PDF, README, SHA256SUMS.
Usage (project root): python code/build_zenodo.py"""
import os, shutil, hashlib, glob, json, time
ROOT = "."; OUT = "release/zenodo_v3"
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
def cp(src, dst=None):
    dst = os.path.join(OUT, dst or src); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
for f in glob.glob("code/**/*", recursive=True):
    if os.path.isfile(f) and "__pycache__" not in f and not f.endswith(".pyc"): cp(f)
cp("state/CLAIMS.md")
for f in glob.glob("results/**/*", recursive=True):
    if os.path.isfile(f) and f.endswith((".json", ".md", ".sh", ".txt", ".log", ".csv")) and "/ckpt/" not in f: cp(f)
for f in glob.glob("results/e42/ckpt/*_best.pt"):  # best-validation checkpoints only (stage best files are kept as they were used for warm starts)
    cp(f)
for f in glob.glob("data/splits/*manifest*.json"): cp(f)
for f in ("StegMorph_article_FINAL.pdf", "journal_decision.md"):
    if os.path.exists(f): cp(f)
open(os.path.join(OUT, "README.md"), "w").write(f"""# StegMorph: does optimised pixel selection make hybrid LSB/PVD steganography harder to detect?
Local release package, built {time.strftime('%Y-%m-%d %H:%M')}. NOT uploaded anywhere; the DOI and upload are the authors' decision.
- code/: embedders, detectors, experiment drivers, summary and macro scripts (run `python code/make_macros.py` to regenerate every number in the paper from results/).
- state/CLAIMS.md: the append-only claims log with every pre-registration and outcome, including the failures.
- results/: per-run result files (JSON), summaries, logs, run scripts. results/e42 holds the CNN curriculum runs (attempts a1 and a2) and their best checkpoints.
- data/splits: subject/patient split manifests only. The image collections are public (IXI, OASIS, Medical Segmentation Decathlon Task01, BraTS 2020) and must be fetched from their own sources; no images are redistributed here.
- Seeds: 0, 1, 2 for every multi-seed result; seed 0 only where the log says so.
Licences: check each source collection's terms before reuse. Code: add a licence file chosen by the authors before upload.
""")
sums = []
for dp, _, fs in os.walk(OUT):
    for f in fs:
        p = os.path.join(dp, f)
        if f != "SHA256SUMS.txt": sums.append(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + os.path.relpath(p, OUT))
open(os.path.join(OUT, "SHA256SUMS.txt"), "w").write("\n".join(sorted(sums, key=lambda s: s.split("  ")[1])) + "\n")
print(len(sums), "files;", round(sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs) / 1e6), "MB")
