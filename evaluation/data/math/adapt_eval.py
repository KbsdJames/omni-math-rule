import json
import pdb

data = []
with open('./test_few_shot_v1_-1_seed0_t0.0_s0_e-1 copy.jsonl') as f:
    for line in f.readlines():
        line = json.loads(line)
        line['generation'] = line['code'][0].split('\nProblem')[0]
        data.append(line)

with open('./test.jsonl', 'w') as f:
    for line in data:
        f.write(json.dumps(line) + '\n')
pdb.set_trace()