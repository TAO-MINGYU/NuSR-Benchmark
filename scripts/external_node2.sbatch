#!/usr/bin/env bash
#SBATCH --job-name=nusr-external-v020
#SBATCH --partition=CLUSTER
#SBATCH --nodelist=node2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=256
#SBATCH --mem=0
#SBATCH --no-requeue
set -euo pipefail

# No wall-time cap: CLUSTER's confirmed default and maximum are UNLIMITED.
# Arguments are absolute, frozen paths prepared before this one submission.
baseline_python="$1"
baseline_source="$2"
baseline_config="$3"
export PYTHONPATH="$baseline_source"
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 OMP_THREAD_LIMIT=1
export MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export JULIA_NUM_THREADS=1 JULIA_NUM_GC_THREADS=1 PYTHON_JULIACALL_THREADS=1
export CUDA_VISIBLE_DEVICES=""
exec srun --exact --nodes=1 --ntasks=1 --cpus-per-task=256 --cpu-bind=threads \
    "$baseline_python" -u -m nuclearbench.external_stage --config "$baseline_config"
