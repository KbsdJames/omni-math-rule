set -ex

DATASET_TYPE=$1
INPUT_PATH=$2
EXP_NAME=$3
SPLIT="test"

# English open datasets
python3 -u math_eval.py \
    --data_name ${DATASET_TYPE} \
    --exp_name ${EXP_NAME} \
    --split ${SPLIT} \
    --input_path ${INPUT_PATH} \
