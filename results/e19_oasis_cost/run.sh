source ../../.venv_py314/bin/activate
for s in 0 1 2; do DS=oasis NTR_FEAT=3146 NTR_CNN=3146 NTE=689 EPOCHS=30 PAY=0.01,0.02 DETS=A,B,C,D python ../../code/exp19_dataset_cost.py $s > e19_seed$s.log 2>&1; done
echo ALLDONE > e19_done.txt
