# V2.4: OASIS and CT at 0.002 bpp. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3
for D in oasis ct; do for S in 0 1 2; do DS=$D SCH=RANDSEQ,COSTKEY,COSTMIX,ANTIKEY PAY=0.002 DETS=A,D OUT=results/e40/$D python code/exp24.py $S > results/e40/${D}_seed$S.log 2>&1; done; done
echo done > results/e40/e40_done.txt
