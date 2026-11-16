# E26: stronger CNN training (second attempt, see CLAIMS.md amendment). Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 OUT=results/e26
MAXEP=60 PATIENCE=20 python code/exp26_cnn.py 0 net RANDSEQ,COSTKEY > results/e26/q1.log 2>&1
MAXEP=60 PATIENCE=20 python code/exp26_cnn.py 0 srnet RANDSEQ,COSTKEY > results/e26/q2.log 2>&1
MAXEP=60 PATIENCE=20 python code/exp26_cnn.py 0 net ORIG,HILLR > results/e26/q3.log 2>&1
MAXEP=60 PATIENCE=20 python code/exp26_cnn.py 1 net RANDSEQ,COSTKEY > results/e26/q4.log 2>&1
MAXEP=60 PATIENCE=20 python code/exp26_cnn.py 0 srnet ORIG,HILLR > results/e26/q5.log 2>&1
echo done > results/e26/e26_done.txt
