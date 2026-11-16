#!/bin/bash
# V3-H22 attempt 2 (declared in state/CLAIMS.md): SRNet-style, seed 0, final-stage epoch cap 120, both keys re-run, tag a2.
cd "<PROJECT_ROOT>"; source .venv_py314/bin/activate
export OUT=results/e42 NPROC=6 TAG=a2 LAST_EPOCHS=120
[ -f results/e42/srnet_RANDSEQ_s0_a2.json ] || python code/exp42_curriculum.py 0 srnet RANDSEQ >> results/e42/chain_srnet_a2.out 2>&1
[ -f results/e42/srnet_COSTKEY_s0_a2.json ] || WARMSTART="results/e42/ckpt/srnet_RANDSEQ_s0_a2_stage{stage}_best.pt" python code/exp42_curriculum.py 0 srnet COSTKEY >> results/e42/chain_srnet_a2.out 2>&1
echo ALLDONE >> results/e42/chain_srnet_a2.out
