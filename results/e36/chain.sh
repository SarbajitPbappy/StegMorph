# waits for the first cost-guided partner run to finish, then re-initialises it (INIT=1, then INIT=2 if that also fails to take off)
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 OUT=results/e36
until [ -f results/e36/srnetfix_COSTKEY_s0.json ]; do sleep 20; done
INIT=1 python code/exp36_srnet_fix.py 0 COSTKEY > results/e36/q3.log 2>&1
python - <<'PY'
import json,sys
v=json.load(open("results/e36/srnetfix_COSTKEY_s0_i1.json"))["valid_run"]
sys.exit(0 if v else 1)
PY
if [ $? -ne 0 ]; then INIT=2 python code/exp36_srnet_fix.py 0 COSTKEY > results/e36/q4.log 2>&1; fi
echo done > results/e36/e36_done.txt
