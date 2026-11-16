"""Main contrast table of version 2 (Overleaf/article/tables/tab_main.tex), from stored results only. IXI T2, 128x128, 0.01 bpp, seed means of 3 seeds.
Rows: contrast against the random key (RANDSEQ) of the same embedder; columns: detectors A (SRM-lite + logistic), D (SRM-lite + trees), B (SPAM + trees), S (maxSRM-lite), F (full SRM + ensemble), M (real maxSRM + ensemble), residual CNN (60 epochs, 4186 pairs), Yedroudj-Net-style CNN (60 epochs, 1 seed)."""
import json, numpy as np, os
def e24(src, det, bpp, c):
    v = [json.load(open(f"results/{src}/e{'24' if src != 'e37' else '37'}_seed{s}.json"))["results"] for s in (0, 1, 2)]; key = f"{'ixi' }|{det}|{bpp}"
    return float(np.mean([r[key]["contrasts"][c]["diff"] for r in v]))
def sc(path, a, b, det, ix=None):
    from sklearn.metrics import roc_auc_score
    A, B = np.load(path[0], allow_pickle=True), np.load(path[1], allow_pickle=True); al = np.arange(len(A[f"{det}|{a}|pc"]))
    f = lambda Z, k: roc_auc_score(np.r_[np.zeros(len(al)), np.ones(len(al))], np.r_[Z[f"{det}|{k}|pc"], Z[f"{det}|{k}|ps"]])
    return f(A, a) - f(B, b)
bpp = 0.01; rows = {}
for name, c in (("GA key, contrast objective", "ORIG-RANDSEQ"), ("Cost-guided key", "COSTKEY-RANDSEQ"), ("Matched control of the cost-guided key", "COSTMIX-RANDSEQ"), ("Smooth-pixel key", "ANTIKEY-RANDSEQ"), ("Reference HILL (0.37\\% changed pixels)", "HILLR-RANDSEQ")):
    r = []
    for src, det in (("e24", "A"), ("e24", "D"), ("e24", "B"), ("e24", "S"), ("e37", "F"), ("e37", "M")): r.append(e24(src, det, bpp, c))
    rows[name] = r
# larger GA from stored scores
gx = {}
for det in ("F", "M"):
    v = []
    for s in (0, 1, 2):
        pe = f"results/e41/scores_s{s}_b{bpp}.npz"
        if os.path.exists(pe): v.append(sc((pe, f"results/e37/scores_s{s}_b{bpp}.npz"), "GAMINX", "RANDSEQ", det) if False else None)
gxrow = [None] * 4
def gaminx(det):
    from sklearn.metrics import roc_auc_score
    out = []
    for s in (0, 1, 2):
        pe, pr = f"results/e41/scores_s{s}_b{bpp}.npz", f"results/e37/scores_s{s}_b{bpp}.npz"
        if not os.path.exists(pe): continue
        A, B = np.load(pe, allow_pickle=True), np.load(pr, allow_pickle=True); n = len(A[f"{det}|GAMINX|pc"]); y = np.r_[np.zeros(n), np.ones(n)]
        out.append(roc_auc_score(y, np.r_[A[f"{det}|GAMINX|pc"], A[f"{det}|GAMINX|ps"]]) - roc_auc_score(y, np.r_[B[f"{det}|RANDSEQ|pc"], B[f"{det}|RANDSEQ|ps"]]))
    return float(np.mean(out)) if out else None, len(out)
gF, nF = gaminx("F"); gM, nM = gaminx("M")
rows["GA key, minimal-cost objective (large search)"] = [None, None, None, None, gF, gM]
cnn_q1 = json.load(open("results/e39/e39_seeds_summary.json"))["e60_n4186"]["mean_q1"]; yq1 = json.load(open("results/e42/summary_srnet_a2.json"))["mean_q1"]  # SRNet-style, attempt 2, three valid seeds; the Yedroudj-style result is excluded (failed the competence rule)
e26 = {k: json.load(open(f"results/e26/net_{k}_b0.01_s0.json"))["test_auc"] for k in ("RANDSEQ", "ORIG", "HILLR")}
cnn = {"GA key, contrast objective": e26["ORIG"] - e26["RANDSEQ"], "Cost-guided key": cnn_q1, "Reference HILL (0.37\\% changed pixels)": e26["HILLR"] - e26["RANDSEQ"]}
yed = {"Cost-guided key": yq1}
fmt = lambda v: "--" if v is None else f"{v:+.3f}".replace("-", "$-$")
tex = "\\setlength{\\tabcolsep}{2.5pt}\\begin{tabular}{@{}p{3.4cm}cccccccc@{}}\n\\toprule\nKey (against random key) & A & D & B & S & F & M & CNN$^{a}$ & CNN$^{b}$ \\\\\n\\midrule\n"
order = ["GA key, contrast objective", "GA key, minimal-cost objective (large search)", "Cost-guided key", "Matched control of the cost-guided key", "Smooth-pixel key", "Reference HILL (0.37\\% changed pixels)"]
for k in order: tex += f"{k} & " + " & ".join(fmt(v) for v in rows[k]) + f" & {fmt(cnn.get(k))} & {fmt(yed.get(k))} \\\\\n"
tex += "\\bottomrule\n\\end{tabular}\n"; open("Overleaf/article/tables/tab_main.tex", "w").write(tex); print(tex); print("GAMINX seeds used:", nF, nM)
