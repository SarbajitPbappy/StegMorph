# V3.3 (V3-H25): GA key (ORIG) on OASIS at 0.002 bpp, detectors A and D, seeds 0 to 2, with the random key (RANDSEQ) as the reference. Run from the project root.
cd "$(dirname "$0")/../.."
source .venv_py314/bin/activate
export NPROC=4 DS=oasis PAY=0.002 SCH=RANDSEQ,ORIG DETS=A,D OUT=results/e47_oasis_ga
for S in 0 1 2; do [ -f results/e47_oasis_ga/e24_seed$S.json ] || python code/exp24.py $S > results/e47_oasis_ga/seed$S.log 2>&1; done
echo done > results/e47_oasis_ga/done.txt
