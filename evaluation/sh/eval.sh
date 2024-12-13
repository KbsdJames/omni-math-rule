set -ex

DATASET_TYPE=$1
INPUT_PATH=$2

SPLIT="test"

# English open datasets
DATA_NAME="math"
TOKENIZERS_PARALLELISM=false \
python3 -u math_eval.py \
    --data_name ${DATASET_TYPE} \
    --split ${SPLIT} \
    --input_path ${INPUT_PATH} \