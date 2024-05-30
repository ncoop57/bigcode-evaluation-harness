#!/bin/bash
#SBATCH --account="stablecode"
#SBATCH --job-name=bigcode_eval
#SBATCH --partition=p5
#SBATCH --container-image=ghcr.io\#bigcode-project/evaluation-harness-multiple
#SBATCH --container-mounts=/opt/slurm:/opt/slurm,/admin/slurm:/admin/slurm,/weka/ckpts/stablecode_modelablations/:/app/ckpts
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:1
#SBATCH --exclusive
#SBATCH --qos=normal
#SBATCH --output=multipl_logs/%x_%j.out
#SBATCH --error=multipl_logs/%x_%j.err

# LANGUAGES=("py" "js" "java" "php" "cpp" "rs")
LANGUAGE=$1
MODELNAME=$2

python3 main.py \
    --model $3 \
    --tasks multiple-$LANGUAGE \
    --load_generations_path /app/ckpts/$MODELNAME/$LANGUAGE\_gens_temp_0.2_multiple-$LANGUAGE.json \
    --metric_output_path /app/ckpts/$MODELNAME/{$LANGUAGE}_metrics_temp_0.2.json \
    --allow_code_execution  \
    --temperature 0.2 \
    --n_samples 50