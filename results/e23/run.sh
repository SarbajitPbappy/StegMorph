source ../../.venv_py314/bin/activate
PAY=0.01,0.02 DETS=A NB=200 python ../../code/exp23_refit_bootstrap.py 0 > e23_seed0.log 2>&1
echo ALLDONE > e23_done.txt
