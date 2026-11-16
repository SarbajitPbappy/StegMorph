# V2.2 second architecture (Yedroudj-Net-style). Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 OUT=results/e39y
python code/exp39_budget.py 0 yedroudj "4:4186,60:4186" > results/e39y_seed0.log 2>&1
echo done > results/e39y_done.txt
