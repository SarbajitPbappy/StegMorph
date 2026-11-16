# E27 (IXI T1), E32 (CT), E34 (256x256). Waits for the downloads. Run from the project root.
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=8
# 256x256 splits need only IXI T2 (already on disk)
python code/build_ixi256_splits.py > results/e34_build.log 2>&1
while [ ! -f results/e24/e24_done.txt ]; do sleep 60; done
while [ "$(stat -f %z data/raw/IXI_T1/IXI-T1.tar)" -lt 4840816640 ]; do sleep 60; done
mkdir -p data/raw/IXI_T1/vol && tar -xf data/raw/IXI_T1/IXI-T1.tar -C data/raw/IXI_T1/vol && python code/build_ixi_t1_splits.py > results/e27_build.log 2>&1
mkdir -p results/e27 results/e32 results/e34
export DETS=A,B,D,S DS=ixit1 OUT=results/e27 PAY=0.01,0.02 SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,ANTIKEY,ANTIMIX,HILLR,SUNIR
for s in 0 1 2; do python code/exp24.py $s > results/e27/e27_seed$s.log 2>&1; done; echo done > results/e27/done.txt
if [ -f data/raw/medmnist/organamnist_128.npz ] && [ "$(stat -f %z data/raw/medmnist/organamnist_128.npz)" -ge 707925571 ]; then
  python code/build_ct_splits.py > results/e32_build.log 2>&1
  export DETS=A,D DS=ct OUT=results/e32 SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,HILLR
  for s in 0 1 2; do python code/exp24.py $s > results/e32/e32_seed$s.log 2>&1; done; echo done > results/e32/done.txt
fi
export DETS=A,D DS=ixi256 OUT=results/e34 SCH=RANDSEQ,ORIG,COSTKEY,COSTMIX,HILLR
for s in 0 1; do python code/exp24.py $s > results/e34/e34_seed$s.log 2>&1; done; echo done > results/e34/done.txt
