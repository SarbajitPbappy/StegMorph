# V3.2 (V3-H23): refit-aware bootstrap for detector D, seeds 0 to 2, 100 replicates per seed and payload (the earlier run, results/e31, had 60 replicates for seed 0 only). Starts after the key-known runs.
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
until [ -f results/e41/k_s12_done.txt ]; do sleep 60; done
export OUT=results/e43 DET=D NREP=100 NJOBS=1
for S in 0 1 2; do
  [ -f results/e43/e31_D_seed$S.json ] && grep -q '"IXI|D|0.02"' results/e43/e31_D_seed$S.json && continue
  python code/exp31_refit.py $S > results/e43/D_seed$S.log 2>&1
done
echo done > results/e43/done.txt
