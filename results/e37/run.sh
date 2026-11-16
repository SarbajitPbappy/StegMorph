# V2.1: full SRM (F) and maxSRM (M) with an FLD ensemble. Run from the project root. Needs tools/dde/bin/{SRM,maxSRM}.mex (see tools/dde).
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 NW=5 OUT=results/e37
for S in 0 1 2; do SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,ANTIKEY,HILLR PAY=0.01,0.02 DETS=F,M python code/exp37_fullsrm.py $S > results/e37/seed$S.log 2>&1; done
echo done > results/e37/e37_done.txt
