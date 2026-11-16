#!/bin/bash
# V3.1 (V3-H22): SRNet-style attempt 1, seed 0 (pre-registered recipe, code/exp42_curriculum.py): random key first, then the cost-guided key warm-started from the random-key checkpoint of the same stage. Starts when the running Yedroudj-style job has ended.
cd "<PROJECT_ROOT>"; source .venv_py314/bin/activate
while pgrep -f "exp42_curriculum.py . yedroudj" >/dev/null; do sleep 60; done
export OUT=results/e42 NPROC=6 TAG=a1
[ -f results/e42/srnet_RANDSEQ_s0_a1.json ] || python code/exp42_curriculum.py 0 srnet RANDSEQ >> results/e42/chain_srnet_a1.out 2>&1
[ -f results/e42/srnet_COSTKEY_s0_a1.json ] || WARMSTART="results/e42/ckpt/srnet_RANDSEQ_s0_a1_stage{stage}_best.pt" python code/exp42_curriculum.py 0 srnet COSTKEY >> results/e42/chain_srnet_a1.out 2>&1
echo ALLDONE >> results/e42/chain_srnet_a1.out
