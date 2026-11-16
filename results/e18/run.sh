source ../../.venv_py314/bin/activate
for s in 0 1 2; do PAY=0.01,0.02 DETS=A,D python ../../code/exp18_antikey.py $s > e18_seed$s.log 2>&1; done
echo ALLDONE > e18_done.txt
