# E28 (cost-map sweep / dose-response), E29 (payload sweep), E30 (other GA objective and embedders). Waits for E24. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=8
while [ ! -f results/e24/e24_done.txt ]; do sleep 30; done
export DETS=A,D
export OUT=results/e28 PAY=0.01,0.02 SCH=RANDSEQ,COSTKEY,ANTIKEY,K:hill:t:0.1,K:hill:t:0.2,K:hill:t:0.5,K:hill:t:0.7,K:hill:s:0.1,K:hill:s:0.2,K:hill:s:0.5,K:hill:s:0.7,K:std:t:0.33,K:std:s:0.33,K:grad:t:0.33,K:grad:s:0.33,K:ent:t:0.33,K:ent:s:0.33,K:suni:t:0.33,K:suni:s:0.33
for s in 0 1 2; do python code/exp24.py $s > results/e28/e28_seed$s.log 2>&1; done; echo done > results/e28/done.txt
export OUT=results/e29 PAY=0.01,0.02,0.05,0.09 SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,ANTIKEY,HILLR,SUNIR
for s in 0 1 2; do python code/exp24.py $s > results/e29/e29_seed$s.log 2>&1; done; echo done > results/e29/done.txt
export OUT=results/e30 PAY=0.01,0.02 SCH=RANDSEQ,ORIG,GAMIN,GAMINS,COSTKEY,LSBK:R,LSBK:C,LSBK:A,LSBM:R,LSBM:C,LSBM:A
for s in 0 1 2; do python code/exp24.py $s > results/e30/e30_seed$s.log 2>&1; done; echo done > results/e30/done.txt
# E31 refit-aware bootstrap
export OUT=results/e31 PAY=0.01,0.02 NREP=200 NJOBS=6
for s in 1 2; do DET=A python code/exp31_refit.py $s > results/e31/e31_A_seed$s.log 2>&1; done
DET=D NREP=60 NJOBS=1 python code/exp31_refit.py 0 > results/e31/e31_D_seed0.log 2>&1
echo done > results/e31/done.txt
echo done > results/chain2_finished.txt
