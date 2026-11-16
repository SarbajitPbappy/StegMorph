# E27: IXI T1 (NIfTI) replication. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=6
export DETS=A,B,D,S DS=ixit1 OUT=results/e27 PAY=0.01,0.02 SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,ANTIKEY,ANTIMIX,HILLR,SUNIR
for s in 0 1 2; do python code/exp24.py $s > results/e27/e27_seed$s.log 2>&1; done; echo done > results/e27/done.txt
