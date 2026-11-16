# V3.3 (V3-H24b): new collection (MSD brain tumour, T2) at 0.005 bpp. Run from the project root; starts after the CNN-independent CPU jobs it can share with (kept light: NPROC=4, NW=3).
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
export TMPOCT=/private/tmp/claude-501/-Volumes-Sarbajit-Personal-Fernaz-Ma-am/304cb914-923f-43e6-ba9c-dc51ddcec8c3/scratchpad/oct NPROC=4 NW=3 ENGINE=np DS=msdt2 PAY=0.005 SCH=RANDFG,ORIG,RANDSEQ,COSTFG,ANTIFG
for S in 0 1 2; do
  [ -f results/e46_msd/e24_seed$S.json ] || DETS=A,D OUT=results/e46_msd python code/exp24.py $S > results/e46_msd/AD_seed$S.log 2>&1
  [ -f results/e46_msd/e37_seed$S.json ] || DETS=F,M OUT=results/e46_msd python code/exp46_msd_fg.py $S > results/e46_msd/FM_seed$S.log 2>&1
done
echo done > results/e46_msd/done.txt
