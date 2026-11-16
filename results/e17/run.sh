source ../../.venv_py314/bin/activate
for s in 0 1 2; do PAY=0.01,0.02 DETS=D python ../../code/exp17_srm_hgb.py $s > e17_seed$s.log 2>&1; done
echo ALLDONE > e17_done.txt
