# V3.2 (V3-H23): key-known detector K, seeds 1 and 2, same schemes/payloads/recipe as seed 0 (results/e41/run_keyknown.sh). CPU engine (ENGINE=np) so it does not compete with CNN training for the GPU.
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=2 NW=3 ENGINE=np
for S in 1 2; do
  [ -f results/e41/k/e37_seed$S.json ] && continue
  SCH=RANDSEQ,ORIG,COSTKEY,GAMINX PAY=0.01,0.02 DETS=K OUT=results/e41/k python code/exp37_fullsrm.py $S > results/e41/k_seed$S.log 2>&1
done
echo done > results/e41/k_s12_done.txt
