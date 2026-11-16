# GPU-engine equivalence check: seed 0, RANDSEQ and COSTKEY, 0.01 bpp, detector F, ENGINE=mps; compare with results/e37/seed0 (ENGINE=np).
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 NW=3 ENGINE=mps
SCH=RANDSEQ,COSTKEY PAY=0.01 DETS=F NBOOT=200 OUT=results/e37_gpucheck python code/exp37_fullsrm.py 0 > results/e37_gpucheck/check.log 2>&1
