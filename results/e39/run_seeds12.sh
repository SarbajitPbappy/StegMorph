# V2.2: seeds 1 and 2 for the two cells that decide V2-H3 (4 epochs and 60 epochs, 4186 pairs). Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 OUT=results/e39
for S in 1 2; do python code/exp39_budget.py $S net "4:4186,60:4186" > results/e39/grid_seed$S.log 2>&1; done
echo done > results/e39/seeds12_done.txt
