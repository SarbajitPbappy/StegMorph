# E24/E25: real HILL and S-UNIWARD, selection-channel-aware detector S. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=8
export SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,ANTIKEY,ANTIMIX,HILLSIM,HILLR,SUNIR DETS=A,B,D,S PAY=0.01,0.02 OUT=results/e24
for s in 0 1 2; do python code/exp24.py $s > results/e24/e24_seed$s.log 2>&1; done
echo done > results/e24/e24_done.txt
