# V2.3: reference embedders at equal modification count. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 NW=5 ENGINE=mps DETS=F,M
for S in 0 1 2; do
 SCH=HILLR,SUNIR PAY=0.032 OUT=results/e38/hi python code/exp37_fullsrm.py $S > results/e38/hi_seed$S.log 2>&1
 SCH=RANDSEQ,COSTKEY PAY=0.0027 OUT=results/e38/lo python code/exp37_fullsrm.py $S > results/e38/lo_seed$S.log 2>&1
 SCH=SUNIR PAY=0.01 OUT=results/e38/su python code/exp37_fullsrm.py $S > results/e38/su_seed$S.log 2>&1
done
echo done > results/e38/e38_done.txt
