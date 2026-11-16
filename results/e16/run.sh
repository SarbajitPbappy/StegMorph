source ../../.venv_py314/bin/activate
for s in 0 1 2; do PAY=0.01 DETS=C NTR_CNN=5239 EPOCHS=30 python ../../code/exp14_costkey.py $s > e16_seed$s.log 2>&1; done
echo ALLDONE > e16_done.txt
