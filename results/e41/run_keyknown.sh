# V2.5 key-known detector (K), seed 0. Waits for the GAMINX runs (e41_done.txt). Run from the project root.
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=3 NW=5 ENGINE=mps
until [ -f results/e41/e41_done.txt ]; do sleep 30; done
mkdir -p results/e41/k
SCH=RANDSEQ,ORIG,COSTKEY,GAMINX PAY=0.01,0.02 DETS=K OUT=results/e41/k python code/exp37_fullsrm.py 0 > results/e41/k_seed0.log 2>&1
echo done > results/e41/k_done.txt
