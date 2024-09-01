import json
from collections import defaultdict

input_file = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/RESULT_reallyOK.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

count_dict = defaultdict(int)

for item in data:
    mark = item.get('mark', None)
    mark_wo = item.get('mark_wo', None)
    
    if mark is None:
        mark = 'missing'
    if mark_wo is None:
        mark_wo = 'missing'
    
    count_dict[(mark, mark_wo)] += 1

print("Combination counts:")
for combination, count in count_dict.items():
    print(f"mark={combination[0]}, mark_wo={combination[1]}: {count}")