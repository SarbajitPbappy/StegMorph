source ../../.venv_py314/bin/activate
# E21: full-budget CNN at 0.02 bpp (IXI), then E22 learning curve at 0.01 bpp (CNN training size 1000 and 2500)
for s in 0 1 2; do PAY=0.02 DETS=C NTR_CNN=5239 EPOCHS=30 python ../../code/exp14_costkey.py $s > e21_seed$s.log 2>&1; done
echo ALLDONE > e21_done.txt
cd ../e22_n1000; for s in 0 1 2; do PAY=0.01 DETS=C NTR_CNN=1000 EPOCHS=30 python ../../code/exp14_costkey.py $s > e22_seed$s.log 2>&1; done; echo ALLDONE > e22_done.txt
cd ../e22_n2500; for s in 0 1 2; do PAY=0.01 DETS=C NTR_CNN=2500 EPOCHS=30 python ../../code/exp14_costkey.py $s > e22_seed$s.log 2>&1; done; echo ALLDONE > e22_done.txt
