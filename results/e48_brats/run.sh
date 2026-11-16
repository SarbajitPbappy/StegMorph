# V3.6 (V3-H26): BraTS 2020 cohort (data/splits/bratst2_*.npz, built by code/build_brats_splits.py). NOT STARTED.
# Payload comes from results/e48_brats/payload_bratst2_RANDFG.json (chosen on VALIDATION only, detector A, seed 0): export PAYB=<chosen> before running, e.g. PAYB=0.005 bash results/e48_brats/run.sh
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
: "${PAYB:?set PAYB from the validation-only payload selection}"
export TMPOCT=<TMP>/octbrats NPROC=${NPROC:-6} NW=${NW:-3} ENGINE=np DS=bratst2 PAY=$PAYB SCH=RANDFG,ORIG,RANDSEQ,COSTFG,ANTIFG,COSTKEY,COSTMIX,ANTIKEY
for S in 0 1 2; do
  [ -f results/e48_brats/e24_seed$S.json ] || DETS=A,D OUT=results/e48_brats python code/exp24.py $S > results/e48_brats/AD_seed$S.log 2>&1
  [ -f results/e48_brats/e37_seed$S.json ] || DETS=F,M OUT=results/e48_brats python code/exp46_msd_fg.py $S > results/e48_brats/FM_seed$S.log 2>&1
done
echo done > results/e48_brats/done.txt
