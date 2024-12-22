export MODEL_PATH='path/to/your/models/QwQ-32B-Preview'
export MODEL_NAME=$(basename $MODEL_PATH)  # 只取最后的文件夹名
export SAVE_PATH="./results/OmniMATH_rule_test_${MODEL_NAME}.jsonl"
export MASTER_ADDR="localhost"
export MASTER_PORT="1231"
export GLOO_SOCKET_IFNAME="lo"
export NCCL_SOCKET_IFNAME="lo"
export WANDB_DISABLED=true
export HF_TOKEN="hf_xxxx"
unset VLLM_USE_MODELSCOPE

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

python inference_vllm.py --model $MODEL_PATH \
    --data_file path/to/your/omni_math_rule.jsonl  \
    --tensor_parallel_size 8 \
    --save_path $SAVE_PATH
