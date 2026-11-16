#!/bin/bash
# E9: subject-disjoint real-cover test on IABI (IXI T2). Downloads ~70 MB from Hugging Face, then runs seeds 0-2.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
[ -d .venv_mac ] || python3 -m venv .venv_mac
source .venv_mac/bin/activate
pip install -q torch numpy scipy scikit-learn pillow huggingface_hub
mkdir -p data/raw/IABI results/e9
python3 - <<'PY'
from huggingface_hub import hf_hub_download
import shutil
import os
for f in ("train.npz","val.npz","test.npz"):
    if os.path.exists("data/raw/IABI/"+f): continue
    p = hf_hub_download("aluk4/iabi-mri-brain", f, repo_type="dataset"); shutil.copyfile(p, "data/raw/IABI/"+f); print("got", f)
PY
cd results/e9
export IABI_DIR="$ROOT/data/raw/IABI" PYTHONPATH="$ROOT/code" EPOCHS=15 PAY=0.01,0.02
for SEED in 0 1 2; do
  echo "=== E9 seed $SEED ($(date)) ==="
  python3 "$ROOT/code/exp9_iabi.py" $SEED 2>&1 | tee e9_seed$SEED.log
done
echo ALL DONE
