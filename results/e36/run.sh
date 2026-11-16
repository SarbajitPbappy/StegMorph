# V2.2 / V2-H4: one fixed SRNet-style attempt on the random-key set. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 OUT=results/e36
python code/exp36_srnet_fix.py 0 RANDSEQ > results/e36/q1.log 2>&1
python code/exp36_srnet_fix.py 0 COSTKEY > results/e36/q2.log 2>&1
