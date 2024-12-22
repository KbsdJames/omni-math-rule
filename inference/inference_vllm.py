import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from tqdm import tqdm
from datasets import load_from_disk
import argparse
import json
import re
import jsonlines
from fraction import Fraction
from vllm import LLM, SamplingParams
import transformers
import sys
MAX_INT = sys.maxsize
import pdb

def generate_dataset(dataset_path, messages_template):
    query = []
    with open(dataset_path) as f:
        for line in f.readlines():
            query.append(json.loads(line))
    
    messages = []
    for line in query:
        message_line = messages_template.copy()
        message_line[1]['content'] = line['problem']
        messages.append(message_line)
    
    return messages


def batch_data(data_list, batch_size=1):
    n = len(data_list) // batch_size
    batch_data = []
    for i in range(n-1):
        start = i * batch_size
        end = (i+1)*batch_size
        batch_data.append(data_list[start:end])

    last_start = (n-1) * batch_size
    last_end = MAX_INT
    batch_data.append(data_list[last_start:last_end])
    return batch_data


def vllm_test(args, model, data_path, start=0, end=MAX_INT, batch_size=1, tensor_parallel_size=1):
    
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        args.model,
    )
    
    INVALID_ANS = "[invalid]"
    gsm8k_ins = []
    gsm8k_answers = []
    gsm8k_ques_items = []

    with open(data_path,"r+", encoding="utf8") as f:
        for idx, item in enumerate(jsonlines.Reader(f)):
            try:
                messages_template = [
                    {"role": "system", "content": "You are a helpful and harmless assistant. You are Qwen developed by Alibaba. You should think step-by-step and put your final answer within \\boxed{}."},
                    {"role": "user", "content": item['question']}
                ]
            except:
                messages_template = [
                    {"role": "system", "content": "You are a helpful and harmless assistant. You are Qwen developed by Alibaba. You should think step-by-step and put your final answer within \\boxed{}."},
                    {"role": "user", "content": item['problem']}
                ]
            temp_instr = tokenizer.apply_chat_template(messages_template, tokenize=False, add_generation_prompt=True)
            gsm8k_ins.append(temp_instr)
            gsm8k_ques_items.append(item)
            try:
                temp_ans = item['solution']
            except:
                temp_ans = item['answer']
            gsm8k_answers.append(temp_ans)

    gsm8k_ins = gsm8k_ins[start:end]
    gsm8k_ques_items = gsm8k_ques_items[start:end]
    gsm8k_answers = gsm8k_answers[start:end]
    print('lenght ====', len(gsm8k_ins))
    batch_gsm8k_ins = batch_data(gsm8k_ins, batch_size=batch_size)

    stop_tokens = ["Question:", "Question", "USER:", "USER", "ASSISTANT:", "ASSISTANT", "Instruction:", "Instruction", "Response:", "Response"]
    sampling_params = SamplingParams(temperature=0, top_p=1, max_tokens=32768, stop=stop_tokens)

    print('sampleing =====', sampling_params)
    llm = LLM(model=model,tensor_parallel_size=tensor_parallel_size, max_model_len=32768)
    result = []
    res_completions = []
    for idx, (prompt, prompt_answer) in enumerate(zip(batch_gsm8k_ins, gsm8k_answers)):
        if isinstance(prompt, list):
            pass
        else:
            prompt = [prompt]

        completions = llm.generate(prompt, sampling_params)
        for output in completions:
            prompt = output.prompt
            generated_text = output.outputs[0].text
            res_completions.append(generated_text)

    with open(args.save_path, 'w') as f:
        for idx, (source_js, completion, prompt_answer) in enumerate(zip(gsm8k_ques_items, res_completions, gsm8k_answers)):
            source_js['model_generation'] = completion
            f.write(json.dumps(source_js) + '\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str)  # model path
    parser.add_argument("--data_file", type=str, default='')  # data path
    parser.add_argument("--start", type=int, default=0) #start index
    parser.add_argument("--end", type=int, default=MAX_INT)  # end index
    parser.add_argument("--batch_size", type=int, default=5000)  # batch_size
    parser.add_argument("--tensor_parallel_size", type=int, default=8)  # tensor_parallel_size
    parser.add_argument("--save_path",type=str, default='')  # saving path
    return parser.parse_args()
if __name__ == "__main__":
    args = parse_args()
    vllm_test(args=args, model=args.model, data_path=args.data_file, start=args.start, end=args.end, batch_size=args.batch_size, tensor_parallel_size=args.tensor_parallel_size)
