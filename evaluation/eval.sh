# EXP_NAME="QwQ-32B-Preview"
# DATASET_TYPE="gsm8k"
# INPUT_PATH="/mnt/moonfs/gaobofei-m2/inference/results/GSM8K_test_QwQ-32B-Preview.jsonl"
# bash sh/eval.sh $DATASET_TYPE $INPUT_PATH $EXP_NAME

EXP_NAME="QwQ-32B-Preview"
DATASET_TYPE="omni-math"
INPUT_PATH="/mnt/moonfs/gaobofei-m2/inference/results/OmniMATH_test_QwQ-32B-Preview.jsonl"
bash sh/eval.sh $DATASET_TYPE $INPUT_PATH $EXP_NAME
