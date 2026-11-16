"""Writes Overleaf/article/numbers.tex: every number used in the abstract, highlights, discussion and conclusion as a LaTeX macro, computed from stored result files only.
One command regenerates all of them:  python code/make_macros.py   (run from the project root). Each macro name is documented by its source in the dictionary below (SRC)."""
import json, os, numpy as np
R = lambda p: json.load(open(p))
M, SRC = {}, {}
def mean_of(d):
    """mean of the per-seed values when stored (more precise than the 4-decimal mean field)"""
    if "seeds" in d: return float(np.mean([x["diff"] if "diff" in x else x["q1"] for x in d["seeds"]]))
    if "per_seed" in d: return float(np.mean(d["per_seed"]))
    return float(d["mean"])
def put(name, value, src, nd=3, signed=False, pct=False, plain=False):
    """store a macro. value is a float (formatted with nd decimals; negative numbers use a math minus) or a string/int (stored as is)."""
    if isinstance(value, (int, np.integer)) or isinstance(value, str): s = str(value)
    else:
        v = float(value) * (100 if pct else 1); s = f"{abs(v):.{nd}f}"
        if v < 0 and round(abs(v), nd) != 0: s = f"$-{s}$"
        elif signed and v > 0 and round(abs(v), nd) != 0: s = f"$+{s}$"
    M[name] = s; SRC[name] = src
def absr(name, value, src, nd=3): put(name, abs(float(value)), src, nd)
# ---- data -----------------------------------------------------------------------------------------------------------
man = R("data/splits/ixi_split_manifest.json"); put("nSubjIxi", sum(man[k]["n_subjects"] for k in ("train", "val", "test")), "data/splits/ixi_split_manifest.json")
mm = R("data/splits/msdt2_split_manifest.json"); put("nSubjMsd", sum(mm[k]["n_subjects"] for k in ("train", "val", "test")), "data/splits/msdt2_split_manifest.json")
put("nTrainSubjMsd", mm["train"]["n_subjects"], "msdt2 manifest"); put("nValSubjMsd", mm["val"]["n_subjects"], "msdt2 manifest"); put("nTestSubjMsd", mm["test"]["n_subjects"], "msdt2 manifest")
put("nSlicesMsd", sum(mm[k]["n_images"] for k in ("train", "val", "test")), "msdt2 manifest")
# ---- GA null: bound on a possible gain (V2.5) and mechanism ---------------------------------------------------------
mde = R("results/e41/mde_orig_vs_random.json"); cells = [k for k in mde if k.split("|")[1] in ("A", "D", "F")]
put("mdeBound", max(mde[k]["max_gain_bound"] for k in cells), "results/e41/mde_orig_vs_random.json (max over A, D, F at 0.01, 0.02 bpp)", 3)
lo = [R(f"results/e43/e31_D_seed{s}.json")["results"][f"IXI|D|{b}"]["contrasts"]["P1_ORIG-RANDSEQ"]["ci95"][0] for s in (0, 1, 2) for b in ("0.01", "0.02")]
for s in (1, 2):
    a = R(f"results/e31/e31_A_seed{s}.json")["results"]; lo += [a[k]["contrasts"]["P1_ORIG-RANDSEQ"]["ci95"][0] for k in a if "|A|" in k]
if os.path.exists("results/e23/e23_A_seed0.json"): a = R("results/e23/e23_A_seed0.json")["results"]; lo += [a[k]["contrasts"]["P1_ORIG-RANDSEQ"]["ci95"][0] for k in a if "|A|" in k] if isinstance(a, dict) else []
put("mdeRefit", max(0.0, -min(lo)), "results/e43 (D, 3 seeds) and results/e31 (A, seeds 1 and 2): largest reduction not excluded by a lower bound of P1", 3)
ga = R("results/ga_stats.json"); put("gaTexShare", ga["tex_share"]["mean"], "results/ga_stats.json", 1, pct=True); put("chanceTexShare", 33.3, "one third by construction (top third of pixels by texture)")
put("gaObjGain", (ga["contrast_gain"]["mean"] - 1), "results/ga_stats.json (contrast_gain minus 1)", 0, pct=True)
# ---- main contrasts (IXI T2, seed means) --------------------------------------------------------------------------------
def e24m(src, det, bpp, c, prefix="e24"):
    v = [R(f"results/{src}/{prefix}_seed{s}.json")["results"][f"ixi|{det}|{bpp}"]["contrasts"][c]["diff"] for s in (0, 1, 2)]; return float(np.mean(v)), v
q = {}
for det, src, pre in (("A", "e24", "e24"), ("D", "e24", "e24"), ("F", "e37", "e37"), ("M", "e37", "e37"), ("B", "e24", "e24"), ("S", "e24", "e24")):
    for b in ("0.01", "0.02"): q[(det, b)] = e24m(src, det, b, "COSTKEY-RANDSEQ", pre)[0]
rich = [q[(d, b)] for d in ("A", "D", "F") for b in ("0.01", "0.02")]
put("qRichLo", min(abs(x) for x in rich), "min |Q1| over detectors A, D, F at 0.01 and 0.02 bpp (results/e24, results/e37)", 2); put("qRichHi", max(abs(x) for x in rich), "max |Q1| over A, D, F at 0.01 and 0.02 bpp", 2)
put("qFone", q[("F", "0.01")], "results/e37 F Q1 0.01 bpp", 3); put("qFtwo", q[("F", "0.02")], "results/e37 F Q1 0.02 bpp", 3)
put("qMone", q[("M", "0.01")], "results/e37 M Q1 0.01 bpp", 3, signed=True); put("qMtwo", q[("M", "0.02")], "results/e37 M Q1 0.02 bpp", 3, signed=True)
for det in ("A", "D", "F", "M"):
    p = [e24m("e24" if det in "AD" else "e37", det, b, "ORIG-RANDSEQ", "e24" if det in "AD" else "e37")[0] for b in ("0.01", "0.02")]
    put(f"pOne{det}", p[0], f"P1 detector {det} 0.01 bpp", 3, signed=True); put(f"pTwo{det}", p[1], f"P1 detector {det} 0.02 bpp", 3, signed=True)
# ---- CNN budget ---------------------------------------------------------------------------------------------------------
b = R("results/e39/e39_summary.json"); put("cnnShortGap", b["e4_n600"]["q1"], "results/e39/e39_summary.json e4_n600", 3); absr("cnnShortGapAbs", b["e4_n600"]["q1"], "abs of the same", 2)
from sklearn.metrics import roc_auc_score
def q1_scores(ep):
    out = []
    for sd in (0, 1, 2):
        a = [np.load(f"results/e39/net_{k}_s{sd}_e{ep}_n4186_scores.npz", allow_pickle=True) for k in ("RANDSEQ", "COSTKEY")]
        f = lambda Z: roc_auc_score(np.r_[np.zeros(len(Z["pc"])), np.ones(len(Z["ps"]))], np.r_[Z["pc"], Z["ps"]]); out.append(f(a[1]) - f(a[0]))
    return float(np.mean(out))
bs = R("results/e39/e39_seeds_summary.json"); put("cnnFourEp", q1_scores(4), "results/e39 stored score files, mean over seeds of unrounded AUC differences", 3, signed=True); put("cnnSixtyEp", q1_scores(60), "results/e39 stored score files, mean over seeds", 3, signed=True)
put("cnnSixtyAuc", bs["e60_n4186"]["mean_random_auc"], "same, random-key AUC at 60 epochs", 3)
# ---- Yedroudj-style (V2.2 single seed; V3.1 curriculum) -----------------------------------------------------------------------
yv2 = [k for k in b if "yed" in k.lower()]
if os.path.exists("results/e42/summary_yedroudj.json"):
    y = R("results/e42/summary_yedroudj.json"); put("yedSeeds", y["n_seeds"], "results/e42/summary_yedroudj.json"); put("yedQmean", y["mean_q1"], "same", 3, signed=True)
    put("yedQlo", min(r["q1"] for r in y["seeds"]), "same", 3, signed=True); put("yedQhi", max(r["q1"] for r in y["seeds"]), "same", 3, signed=True)
    put("yedValLo", min(r["val_auc_random"] for r in y["seeds"]), "random-key validation AUC, minimum over seeds", 3); put("yedValHi", max(r["val_auc_random"] for r in y["seeds"]), "random-key validation AUC, maximum", 3)
    put("yedCompetent", "yes" if y["valid_contrast"] else "no", "competence rule (V3 pre-registration)")
if os.path.exists("results/e42/summary_srnet_a2.json"):
    _f = "results/e42/summary_srnet_a2.json"; sr = R(_f)
    put("srnetSeeds", sr["n_seeds"], _f); put("srnetQ", sr["mean_q1"], _f, 3, signed=True)
    S_ = sr["seeds"]
    put("srnetCIlo", min(x["ci"][0] for x in S_), _f, 3); put("srnetCIhi", max(x["ci"][1] for x in S_), _f, 3)  # widest per-seed 95% bounds
    put("srnetQlo", sr["range_q1"][0], _f, 3, signed=True); put("srnetQhi", sr["range_q1"][1], _f, 3, signed=True)
    put("srnetValLo", min(x["val_auc_random"] for x in S_), _f, 3); put("srnetValHi", max(x["val_auc_random"] for x in S_), _f, 3)
    put("srnetAucRand", sr["mean_random_auc"], _f, 3); put("srnetAucCost", sum(x["auc_costkey"] for x in S_) / len(S_), _f, 3)
# ---- reference embedders (V2.3) ----------------------------------------------------------------------------------------
e38 = R("results/e38/e38_summary.json")
put("hillEqRand", mean_of(e38["F|1.4pct|HILLR@0.032 minus RANDSEQ@0.01"]), "results/e38 F, 1.4 pct changed pixels", 3); put("hillEqCost", mean_of(e38["F|1.4pct|HILLR@0.032 minus COSTKEY@0.01"]), "results/e38", 3, signed=True)
put("suniEqRand", mean_of(e38["F|1.4pct|SUNIR@0.032 minus RANDSEQ@0.01"]), "results/e38", 3); put("suniEqCost", mean_of(e38["F|1.4pct|SUNIR@0.032 minus COSTKEY@0.01"]), "results/e38", 3, signed=True)
# ---- larger GA (V2.5) --------------------------------------------------------------------------------------------------
e41 = R("results/e41/e41_summary.json"); put("gaminxOne", mean_of(e41["F|0.01|GAMINX-RANDSEQ"]), "results/e41 F 0.01 bpp", 3); put("gaminxTwo", mean_of(e41["F|0.02|GAMINX-RANDSEQ"]), "results/e41 F 0.02 bpp", 3)
absr("gaminxOneAbs", mean_of(e41["F|0.01|GAMINX-RANDSEQ"]), "abs", 3); absr("gaminxTwoAbs", mean_of(e41["F|0.02|GAMINX-RANDSEQ"]), "abs", 3)
# ---- key-known detector (V3-H23), three seeds -------------------------------------------------------------------------------
if os.path.exists("results/e41/k/summary_3seeds.json"):
    k3 = R("results/e41/k/summary_3seeds.json")["summary"]
    for b_, nm in (("0.01", "One"), ("0.02", "Two")): put(f"kQ{nm}", k3[b_]["q1_K"]["mean"], "results/e41/k/summary_3seeds.json", 3); put(f"kPool{nm}", k3[b_]["q1_M"]["mean"], "same (Q1 under M)", 3, signed=True); put(f"kGap{nm}", k3[b_]["e1_rand"]["mean"], "K minus M AUC, random key", 3)
# ---- OASIS 0.002 bpp and GA key on OASIS (V3-H25) ---------------------------------------------------------------------------
e40 = R("results/e40/e40_summary.json")
for det in ("A", "D"): put(f"oasisQ{det}", mean_of(e40[f"oasis|{det}"]["contrasts"]["COSTKEY-RANDSEQ"]), "results/e40 OASIS 0.002 bpp", 3)
og = R("results/e47_oasis_ga/summary.json"); put("oasisGaLo", min(min(og[d]["P1_per_seed"]) for d in ("A", "D")), "results/e47_oasis_ga/summary.json minimum P1 over seeds and detectors", 3, signed=True)
put("oasisGaHi", max(max(og[d]["P1_per_seed"]) for d in ("A", "D")), "same, maximum", 3, signed=True)
# ---- refit bootstrap for D (V3-H23) ------------------------------------------------------------------------------------------
rd = R("results/e43/summary.json"); vals = [v for k, v in rd.items() if k != "rule_met"]
put("refitQlo", min(v["Q1"][0] for v in vals), "results/e43/summary.json", 3); put("refitQhi", max(v["Q1"][0] for v in vals), "same", 3)
# ---- new collection, foreground baseline (V3-H24b) ---------------------------------------------------------------------------
ms = R("results/e46_msd/summary.json"); put("msdBpp", "0.005", "payload chosen on validation (results/e44)")
for det in ("A", "D", "F", "M"):
    c = ms["detectors"][det]["contrasts"]; put(f"msdQ{det}", c["Q1fg"]["mean"], "results/e46_msd/summary.json", 3); put(f"msdP{det}", c["P1fg"]["mean"], "same", 3, signed=True)
put("msdQlo", min(abs(ms["detectors"][d]["contrasts"]["Q1fg"]["mean"]) for d in "ADFM"), "min |Q1fg| over A, D, F, M", 2); put("msdQhi", max(abs(ms["detectors"][d]["contrasts"]["Q1fg"]["mean"]) for d in "ADFM"), "max |Q1fg|", 2)
put("msdPlo", min(ms["detectors"][d]["contrasts"]["P1fg"]["mean"] for d in "ADFM"), "min P1fg", 2); put("msdPhi", max(ms["detectors"][d]["contrasts"]["P1fg"]["mean"] for d in "ADFM"), "max P1fg", 2)
# ---- detector count (one place: the rows of tables/tab_detectors.tex) ------------------------------------------------------------
rows_ = [l for l in open("Overleaf/article/tables/tab_detectors.tex") if " & " in l and not l.startswith("Label")]
words_ = {7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven"}; put("nDetectors", len(rows_), "rows of Overleaf/article/tables/tab_detectors.tex"); put("nDetectorsWord", words_.get(len(rows_), str(len(rows_))), "same, in words")
put("nFeatureDetectors", sum(1 for l in rows_ if not l.split("&")[0].strip().endswith("CNN")), "rows that are not CNNs"); put("nCnnDetectors", sum(1 for l in rows_ if l.split("&")[0].strip().endswith("CNN")), "CNN rows")
# ---- BraTS cohort and residual CNN on MSD / BraTS (guarded: only if the result files exist) ---------------------------------------
import os as _os
_m = "data/splits/bratst2_split_manifest.json"
if _os.path.exists(_m):
    _d = json.load(open(_m)); put("nBratsExcluded", len(_d["overlap_excluded"]), _m); put("nBratsKept", _d["n_cases_after_exclusion"], _m); put("nBratsTotal", _d["n_cases_total"], _m)
    for _k, _n in (("train", "Train"), ("val", "Val"), ("test", "Test")): put(f"nBrats{_n}Pat", _d[_k]["n_patients"], _m); put(f"nBrats{_n}Img", _d[_k]["n_images"], _m)
_s = "results/e48_brats/summary.json"
if _os.path.exists(_s):
    _d = json.load(open(_s)); put("bratsPayload", _d["payload_bpp"], _s, nd=4)
    for _det in ("A", "D", "F", "M"):
        _c = _d["detectors"][_det]["contrasts"]; put(f"bratsQ{_det}", _c["Q1fg"]["mean"], _s, signed=False); put(f"bratsP{_det}", _c["P1fg"]["mean"], _s, signed=True)
for _tag, _pre, _f in (("msd", "msdCnn", "results/e49_resnet_fg/summary_msd.json"), ("brats", "bratsCnn", "results/e49_resnet_fg_brats/summary_brats.json")):
    if _os.path.exists(_f):
        _d = json.load(open(_f)); put(f"{_pre}Q", _d["mean_q1fg"], _f); put(f"{_pre}QLo", _d["range_q1fg"][0], _f); put(f"{_pre}QHi", _d["range_q1fg"][1], _f)
        put(f"{_pre}AucRand", float(np.mean([r["auc_random"] for r in _d["seeds"]])), _f); put(f"{_pre}AucCost", float(np.mean([r["auc_cost"] for r in _d["seeds"]])), _f)
        put(f"{_pre}ValLo", min(r["val_auc_random"] for r in _d["seeds"]), _f); put(f"{_pre}Valid", "yes" if _d["valid_contrast"] else "no", _f); put(f"{_pre}RuleMet", "yes" if _d["rule_met"] else "no", _f)
# ---- write -------------------------------------------------------------------------------------------------------------------
with open("Overleaf/article/numbers.tex", "w") as f:
    f.write("% generated by code/make_macros.py from stored result files; do not edit by hand\n")
    for k in sorted(M): f.write(f"\\newcommand{{\\{k}}}{{{M[k]}}} % {SRC[k]}\n")
json.dump(dict(macros=M, sources=SRC), open("results/macros.json", "w"), indent=1); print(len(M), "macros written")
