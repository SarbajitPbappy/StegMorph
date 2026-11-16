"""Builds submission/StegMorph_Overleaf.zip: a self-contained Overleaf project (main file article.tex) in which every figure is a PDF (PNG figures converted, TikZ diagrams also as standalone PDFs). Compiles it once to check, and copies the compiled PDF to submission/. Run from the project root."""
import os, re, shutil, glob, subprocess, zipfile
from PIL import Image
SRC, W, OUT = "Overleaf/article", "submission/overleaf_src", "submission"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(W + "/figures")
for f in ("article.tex", "numbers.tex", "refs.bib", "elsarticle-harv.bst"): shutil.copy2(f"{SRC}/{f}", W)
for d in ("sections", "tables"): shutil.copytree(f"{SRC}/{d}", f"{W}/{d}")
for f in glob.glob(f"{SRC}/figures/*.tikz"): shutil.copy2(f, W + "/figures")
for f in glob.glob(f"{SRC}/figures/*standalone.tex") + glob.glob(f"{SRC}/figures/*standalone.pdf"): shutil.copy2(f, W + "/figures")
used = set(re.findall(r"figures/([A-Za-z0-9_]+)\.(?:png|pdf)", "".join(open(f).read() for f in [f"{SRC}/article.tex"] + glob.glob(f"{SRC}/sections/*.tex"))))
for n in sorted(used):
    if os.path.exists(f"{SRC}/figures/{n}.png"):
        im = Image.open(f"{SRC}/figures/{n}.png"); im = im.convert("RGB") if im.mode != "RGB" else im
        im.save(f"{W}/figures/{n}.pdf", "PDF", resolution=250.0)
    else: shutil.copy2(f"{SRC}/figures/{n}.pdf", f"{W}/figures/{n}.pdf")  # the working folder already holds the PDF
for f in ["article.tex"] + glob.glob(f"{W}/sections/*.tex"):
    f = f if f.startswith(W) else f"{W}/{f}"; t = open(f).read(); open(f, "w").write(re.sub(r"(figures/[A-Za-z0-9_]+)\.png", r"\1.pdf", t))
for cmd in (["pdflatex"], ["bibtex"], ["pdflatex"], ["pdflatex"]):
    r = subprocess.run(cmd + (["-interaction=nonstopmode", "article"] if cmd[0] == "pdflatex" else ["article"]), cwd=W, capture_output=True, text=True)
log = open(f"{W}/article.log").read(); print("undefined:", len(re.findall(r"undefined", log)), "| pages:", re.search(r"\((\d+) pages", log).group(1))
shutil.copy2(f"{W}/article.pdf", f"{OUT}/StegMorph_article_FINAL.pdf")
os.makedirs(f"{OUT}/diagrams_pdf", exist_ok=True)
for f in glob.glob(f"{W}/figures/*.pdf"): shutil.copy2(f, f"{OUT}/diagrams_pdf/")
for ext in ("aux", "log", "out", "blg", "bbl", "spl", "pdf"):
    for f in glob.glob(f"{W}/*.{ext}"):
        if ext == "bbl": continue  # keep the compiled bibliography so Overleaf builds without bibtex problems
        os.remove(f)
with zipfile.ZipFile(f"{OUT}/StegMorph_Overleaf.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, fs in os.walk(W):
        for f in fs:
            p = os.path.join(root, f); z.write(p, os.path.relpath(p, W))
print(len(zipfile.ZipFile(f"{OUT}/StegMorph_Overleaf.zip").namelist()), "files in zip")
