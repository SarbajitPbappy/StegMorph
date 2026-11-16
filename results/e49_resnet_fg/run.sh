# V3-H27: converged residual CNN on the MSD collection (foreground keys). Start only when the GPU is free (after SRNet-style attempt 2). Run from the project root.
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
export OUT=results/e49_resnet_fg DS=msdt2 BPP=0.005 SCHEMES=RANDFG,COSTFG NPROC=${NPROC:-6}
for S in 0 1 2; do python code/exp49_resnet_fg.py $S net 60:ALL >> results/e49_resnet_fg/run.out 2>&1; done
echo done > results/e49_resnet_fg/done.txt
