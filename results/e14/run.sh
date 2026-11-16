source ../../.venv_py314/bin/activate
PAY=0.01,0.02 python ../../code/exp14_costkey.py 0 > e14_seed0.log 2>&1
PAY=0.01,0.02 python ../../code/exp14_costkey.py 1 > e14_seed1.log 2>&1
PAY=0.01,0.02 python ../../code/exp14_costkey.py 2 > e14_seed2.log 2>&1
