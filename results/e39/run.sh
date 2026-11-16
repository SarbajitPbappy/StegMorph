# V2.2 budget sweep. Run from the project root. Order: smallest budgets first so contrasts appear early.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 OUT=results/e39
python code/exp39_budget.py 0 net "4:600,4:1000,4:2500,4:4186,10:600,10:1000,10:2500,10:4186,30:600,30:1000,30:2500,30:4186,60:600,60:1000,60:2500,60:4186" > results/e39/grid_seed0.log 2>&1
echo done > results/e39/grid_done.txt
