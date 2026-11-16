source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=5
export DETS=A,D DS=ixi256 OUT=results/e34b PAY=0.0025,0.005 SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,HILLR
for s in 0 1; do python code/exp24.py $s > results/e34b/e34b_seed$s.log 2>&1; done; echo done > results/e34b/done.txt
