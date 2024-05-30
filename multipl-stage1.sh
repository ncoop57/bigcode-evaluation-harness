#!/bin/bash
#SBATCH --account="stablecode"
#SBATCH --job-name=multipl-e
#SBATCH --partition=p5
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --exclusive
#SBATCH --qos=idle
#SBATCH --output=multipl_logs/%x_%j.out
#SBATCH --error=multipl_logs/%x_%j.err

LANGUAGE=$1
MODELNAME=$2
MODELPATH=$3

source /etc/profile.d/modules.sh
module load openmpi cuda/12.1

conda activate code-eval

mkdir -p "/weka/ckpts/stablecode_modelablations/$MODELNAME/"
which python
accelerate launch \
  main.py \
  --model $3  \
  --tasks multiple-$LANGUAGE  \
  --max_length_generation 1024 \
  --temperature 0.2   \
  --do_sample True  \
  --n_samples 50  \
  --batch_size 8  \
  --precision bf16 \
  --trust_remote_code \
  --generation_only \
  --save_generations \
  --save_generations_path "/weka/ckpts/stablecode_modelablations/$MODELNAME/${LANGUAGE}_gens_temp_0.2.json"
