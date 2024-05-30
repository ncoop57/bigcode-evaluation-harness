#!/bin/bash

# LANGUAGES=("js" "java" "py" "cpp" "rs")
# /weka2/ckpts/code_rephrased/code-py-leetcode/global_step
HF_MODEL_ROOT="/weka2/ckpts/code_rephrased/code-base50-pseudo50/global_step*_hf"
HF_MODELS=($(ls -d $HF_MODEL_ROOT))
LANGUAGES=("py")
# MODEL="deepseek-ai/deepseek-coder-6.7b-instruct"
# # MODELPATH="deepseek-ai/deepseek-coder-1.3b-instruct"
# MODELPATH=""deepseek-ai/deepseek-coder-6.7b-instruct""
for MODEL in "${HF_MODELS[@]}"; do
    # if [[ $MODEL == *"10000_hf"* || $MODEL == *"20000_hf"* ]]; then
    #     continue
    # fi
    # if [[ $MODEL == *"10000_hf"* || $MODEL == *"step5000_hf"* || $MODEL == *"step0_hf"* || $MODEL == *"25001_hf"* ]]; then
    #     continue
    # fi
    # if [[ $MODEL != *"step5000_hf"* ]]; then
    #     continue
    # fi

    MODEL_NAME=$(basename $(dirname $MODEL))_$(basename $MODEL)
    for LANGUAGE in "${LANGUAGES[@]}"; do
        sbatch ./multipl-stage2.sh $LANGUAGE $MODEL_NAME $MODEL
    done
done
# for LANGUAGE in "${LANGUAGES[@]}"; do
#     sbatch ./multipl-stage2.sh $LANGUAGE $MODEL $MODELPATH
# done
