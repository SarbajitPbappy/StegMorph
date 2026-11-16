# V2.5: stronger GA (GAMINX) with detectors F and M. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 NW=4 ENGINE=mps DETS=F,M
for S in 0 1 2; do SCH=GAMINX PAY=0.01,0.02 OUT=results/e41 python code/exp37_fullsrm.py $S > results/e41/seed$S.log 2>&1; done
echo done > results/e41/e41_done.txt
