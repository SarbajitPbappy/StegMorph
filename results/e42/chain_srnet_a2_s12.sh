#!/bin/bash
# V3-H22 attempt 2, seeds 1 and 2 (declared in state/CLAIMS.md): same recipe as seed 0, RANDSEQ then COSTKEY (warm-started from the same seed's random-key checkpoint), LAST_EPOCHS=120, tag a2.
cd "<PROJECT_ROOT>"; source .venv_py314/bin/activate
export OUT=results/e42 NPROC=6 TAG=a2 LAST_EPOCHS=120
for S in 1 2; do
  [ -f results/e42/srnet_RANDSEQ_s${S}_a2.json ] || python code/exp42_curriculum.py $S srnet RANDSEQ >> results/e42/chain_srnet_a2_s12.out 2>&1
  [ -f results/e42/srnet_COSTKEY_s${S}_a2.json ] || WARMSTART="results/e42/ckpt/srnet_RANDSEQ_s${S}_a2_stage{stage}_best.pt" python code/exp42_curriculum.py $S srnet COSTKEY >> results/e42/chain_srnet_a2_s12.out 2>&1
done
echo ALLDONE >> results/e42/chain_srnet_a2_s12.out
