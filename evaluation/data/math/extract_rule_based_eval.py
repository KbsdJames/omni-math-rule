import json
import pdb
import matplotlib.pyplot as plt

def is_pure_number(s):
    return s.isdigit()

data = []
with open('uncertain_case.jsonl', 'r') as f:
    for line in f.readlines():
        data.append(json.loads(line))

print("欢迎进入标注系统！")


testable_data = []
for idx, line in enumerate(data):
    if ('{' in line['answer'] and '}' in line['answer'] and '\\text' not in line['answer'] and ',' not in line['answer'] and '=' not in line ['answer']) or is_pure_number(line['answer']):
        testable_data.append(line)

data = []
with open('consistent_case.jsonl', 'r') as f:
    for line in f.readlines():
        data.append(json.loads(line))

testable_data_1 = []
for idx, line in enumerate(data):
    if ('{' in line['answer'] and '}' in line['answer'] and '\\text' not in line['answer']) or is_pure_number(line['answer']) and ',' not in line['answer'] and '=' not in line['answer']:
        testable_data_1.append(line)

testable_data  = testable_data + testable_data_1

pdb.set_trace()
with open('./testable_data.jsonl', 'w') as f:
    for line in testable_data:
        f.write(json.dumps(line) + '\n')

from collections import Counter
# 提取'difficulty'属性
difficulties = [item['difficulty'] for item in testable_data]

# 统计分布
difficulty_distribution = Counter(difficulties)

# 将字典转换为排序后的列表
sorted_difficulties = sorted(difficulty_distribution.items(), key=lambda x: x[0])

pdb.set_trace()
# 拆分成两个列表：难度和计数
labels, counts = zip(*sorted_difficulties)

# 绘制柱状图
plt.bar(labels, counts, color='skyblue')
plt.xlabel('Difficulty Level')
plt.ylabel('Count')
plt.title('Distribution of Difficulty Levels')
plt.xticks(rotation=45)
plt.grid(axis='y')

# 显示图形
plt.tight_layout()
plt.savefig('./rule_case.png')

# 打印结果
for difficulty, count in difficulty_distribution.items():
    print(f"{difficulty}: {count}")