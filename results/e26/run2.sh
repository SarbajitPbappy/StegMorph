# E26 second queue (see CLAIMS.md amendment 2). Waits for the running residual-net job (seed 0 ORIG, HILLR) to finish.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 OUT=results/e26 MAXEP=60 PATIENCE=20
while pgrep -f "exp26_cnn.py 0 net ORIG,HILLR" > /dev/null; do sleep 20; done
INIT=1 python code/exp26_cnn.py 0 srnet RANDSEQ > results/e26/q6.log 2>&1
python code/exp26_cnn.py 1 net RANDSEQ,COSTKEY > results/e26/q4.log 2>&1
if python - <<'PY'
import json; import sys; sys.exit(0 if json.load(open("results/e26/srnet_RANDSEQ_b0.01_s0_i1.json"))["best_val_auc"] < 0.55 else 1)
PY
then INIT=2 python code/exp26_cnn.py 0 srnet RANDSEQ > results/e26/q7.log 2>&1; fi
echo done > results/e26/e26_done.txt
