#!/bin/bash
# Run the CNN replicates natively on this Mac (open a VS Code terminal in this folder and run: bash code/run_mac.sh)
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv_mac && source .venv_mac/bin/activate
pip install -q torch numpy scipy scikit-learn pillow
mkdir -p results/mac && cd results/mac
export STEG_DATA="$ROOT/data/raw"
export PYTHONPATH="$ROOT/code"
export EPOCHS=15
for SEED in 2 3; do
  echo "=== seed $SEED ($(date)) ==="
  python3 "$ROOT/code/exp7_mac.py" $SEED 2>&1 | tee e7_mac_seed$SEED.log
done
echo ALL DONE
