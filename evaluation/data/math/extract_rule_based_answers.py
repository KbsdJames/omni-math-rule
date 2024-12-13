import json
import pdb

test_set = []
with open('./test.jsonl') as f:
    for line in f.readlines():
        test_set.append(json.loads(line))

pred_set = []
with open('/mnt/moonfs/gaobofei-m2/inference/Qwen2.5-Math/evaluation/outputs/mnt/moonfs/gaobofei-m2/models/Qwen2.5-Math-1.5B-Instruct/math_eval/math/test_qwen25-math-cot_-1_seed0_t0.0_s0_e-1.jsonl') as f:
    for line in f.readlines():
        pred_set.append(json.loads(line))

consistent_case = []
inconsistent_case_A = []
inconsistent_case_B = []
uncertain_case = []
for pred, test in zip(pred_set, test_set):
    if pred['score'][0] == True and test['correctness'] == True:
        for key in pred:
            if key not in test:
                test[key] = pred[key]
        consistent_case.append(test)
    elif pred['score'][0] == True and test['correctness'] == False:
        for key in pred:
            if key not in test:
                test[key] = pred[key]
        inconsistent_case_A.append(test)
    elif pred['score'][0] == False and test['correctness'] == True:
        for key in pred:
            if key not in test:
                test[key] = pred[key]
        inconsistent_case_B.append(test)
    elif pred['score'][0] == False and test['correctness'] == False:
        for key in pred:
            if key not in test:
                test[key] = pred[key]
        uncertain_case.append(test)

with open('./consistent_case.jsonl', 'w') as f:
    for line in consistent_case:
        f.write(json.dumps(line) + '\n')

with open('./inconsistent_case_A.jsonl', 'w') as f:
    for line in inconsistent_case_A:
        f.write(json.dumps(line) + '\n')

with open('./inconsistent_case_B.jsonl', 'w') as f:
    for line in inconsistent_case_B:
        f.write(json.dumps(line) + '\n')

with open('./uncertain_case.jsonl', 'w') as f:
    for line in uncertain_case:
        f.write(json.dumps(line) + '\n')
pdb.set_trace()