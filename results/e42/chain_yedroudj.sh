#!/bin/bash
cd "<PROJECT_ROOT>"; source .venv_py314/bin/activate
for s in 0 1 2; do for sch in RANDSEQ COSTKEY; do
  [ -f results/e42/yedroudj_${sch}_s${s}.json ] && continue
  OUT=results/e42 NPROC=8 python code/exp42_curriculum.py $s yedroudj $sch >> results/e42/chain_yedroudj.out 2>&1
done; done
echo ALLDONE >> results/e42/chain_yedroudj.out
