"""LaTeX tables from stored results. Run from the project root: python code/make_tables.py"""
import json, glob, numpy as np, os
from summarize import agg
T = "Overleaf/article/tables/"; os.makedirs(T, exist_ok=True)
def tab_change():
    A = agg("e24"); names = [("RANDSEQ", "Random key"), ("ORIG", "GA contrast key"), ("COSTKEY", "Cost-guided key"), ("COSTMIX", "Cost-guided control"), ("ANTIKEY", "Smooth-pixel key"), ("HILLR", "HILL (ref.)"), ("SUNIR", "S-UNIWARD (ref.)")]
    s = "\\begin{tabular}{@{}lcccc@{}}\n\\toprule\nScheme & Modified pixels (\\%) & MSE & PVD pairs & LSB pairs \\\\\n & 0.01 / 0.02 bpp & 0.01 / 0.02 bpp & 0.01 / 0.02 & 0.01 / 0.02 \\\\\n\\midrule\n"
    for k, n in names:
        a, b = A[("ixi", "A", 0.01)]["stats"][k], A.get(("ixi", "A", 0.02), A[("ixi", "A", 0.01)])["stats"][k]
        pv = "--" if a["pvd_pairs"] < 0 else f"{a['pvd_pairs']:.1f} / {b['pvd_pairs']:.1f}"; lv = "--" if a["lsb_pairs"] < 0 else f"{a['lsb_pairs']:.0f} / {b['lsb_pairs']:.0f}"
        s += f"{n} & {a['changed_frac']*100:.2f} / {b['changed_frac']*100:.2f} & {a['mse']:.4f} / {b['mse']:.4f} & {pv} & {lv} \\\\\n"
    open(T + "tab_change.tex", "w").write(s + "\\bottomrule\n\\end{tabular}\n")
def tab_data():
    rows = []
    for ds, lab in (("ixi", "IXI T2"), ("ixit1", "IXI T1"), ("oasis", "OASIS"), ("ct", "CT (OrganAMNIST)"), ("ixi256", "IXI T2, $256\\times256$")):
        c = []
        for sp in ("train", "val", "test"):
            f = f"data/splits/{ds}_{sp}.npz"
            if not os.path.exists(f): c = None; break
            d = np.load(f, allow_pickle=True); c.append(f"{len(set(d['subject']))} / {len(d['images'])}" if ds != "ct" else f"{ {'train':115,'val':16,'test':70}[sp]} scans / {len(d['images'])}")
        if c: rows.append(f"{lab} & " + " & ".join(c) + " \\\\\n")
    open(T + "tab_data.tex", "w").write("\\begin{tabular}{lccc}\n\\toprule\nCollection & Train & Validation & Test \\\\\n\\midrule\n" + "".join(rows) + "\\bottomrule\n\\end{tabular}\n")

def tab_replication():
    """Across collections: random-key AUC, P1, Q1, Q4 for detectors A and D (seed means)."""
    def old(folder, ds):
        out = {}
        for f in sorted(glob.glob(f"results/{folder}/e14_seed*.json")):
            for k, v in json.load(open(f))["results"].items(): out.setdefault(k, []).append(v)
        return out
    rows = []
    for lab, fo, ds in (("IXI T2", "e24", "ixi"), ("IXI T1 (NIfTI)", "e27", "ixit1"), ("CT (OrganAMNIST)", "e32", "ct")):
        if not os.path.isdir(f"results/{fo}") or not glob.glob(f"results/{fo}/e24_seed*.json"): continue
        A = agg(fo)
        for bpp in (0.01, 0.02):
            cells = []
            for det in "AD":
                o = A[(ds, det, bpp)]; c = o["con"]; q4 = c.get("ANTIKEY-RANDSEQ", {}).get("mean", float("nan"))
                cells += [f"{o['auc']['RANDSEQ'][0]:.3f}", f"{c['ORIG-RANDSEQ']['mean']:+.3f}", f"{c['COSTKEY-RANDSEQ']['mean']:+.3f}", ("--" if q4 != q4 else f"{q4:+.3f}")]
            rows.append((lab, bpp, cells))
    O = old("e19_oasis_cost", "OASIS"); OA = old("e19_oasis_anti", "OASIS")
    for bpp in (0.01, 0.02):
        cells = []
        for det in "AD":
            r = O[f"OASIS|{det}|{bpp}"]; ra = OA.get(f"OASIS|{det}|{bpp}")
            m = lambda rr, c: float(np.mean([x["contrasts"][c]["diff"] for x in rr]))
            cells += [f"{np.mean([x['auc']['RANDSEQ'] for x in r]):.3f}", f"{m(r, 'P1_ORIG-RANDSEQ'):+.3f}", f"{m(r, 'Q1_COSTKEY-RANDSEQ'):+.3f}", (f"{m(ra, 'Q1_ANTIKEY-RANDSEQ'):+.3f}" if ra else "--")]
        rows.append(("OASIS (JPEG-derived)", bpp, cells))
    s = "\\begin{tabular}{llcccccccc}\n\\toprule\n & & \\multicolumn{4}{c}{A: SRM-lite + logistic} & \\multicolumn{4}{c}{D: SRM-lite + trees} \\\\\nCollection & bpp & random AUC & $P_1$ & $Q_1$ & $Q_4$ & random AUC & $P_1$ & $Q_1$ & $Q_4$ \\\\\n\\midrule\n"
    for lab, bpp, c in rows: s += f"{lab} & {bpp} & " + " & ".join(c) + " \\\\\n"
    open(T + "tab_replication.tex", "w").write(s + "\\bottomrule\n\\end{tabular}\n"); print(s)


def tab_ga():
    A = agg("e30"); rows = [("GA, min-cost, same budget (\\textsc{gamin})", "GAMIN-RANDSEQ"), ("GA, min-cost, stronger search (\\textsc{gamins})", "GAMINS-RANDSEQ"), ("Cost-guided key, PVD/LSB (\\textsc{costkey})", "COSTKEY-RANDSEQ"), ("LSBK, cost-guided key", "LSBK:C-LSBK:R"), ("LSBK, smooth key", "LSBK:A-LSBK:R"), ("LSBM, cost-guided key", "LSBM:C-LSBM:R"), ("LSBM, smooth key", "LSBM:A-LSBM:R")]
    s = "\\begin{tabular}{@{}lcccc@{}}\n\\toprule\nScheme minus random key & A 0.01 & A 0.02 & D 0.01 & D 0.02 \\\\\n\\midrule\n"
    for lab, k in rows: s += lab + " & " + " & ".join(f"{A[('ixi', d, b)]['con'][k]['mean']:+.3f}" for d in "AD" for b in (0.01, 0.02)) + " \\\\\n"
    open(T + "tab_ga.tex", "w").write(s + "\\bottomrule\n\\end{tabular}\n")
if __name__ == "__main__":
    import sys; sys.path.insert(0, "code")
    tab_data(); tab_change(); tab_replication(); tab_ga(); print("tables written")
