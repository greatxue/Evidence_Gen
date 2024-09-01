import json

input_file = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/RESULT_reallyOK.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

total_values = {
    'mark=1, mark_wo=0': [],
    'mark=0, mark_wo=1': []
}

for item in data:
    mark = item.get('mark', None)
    mark_wo = item.get('mark_wo', None)
    total = item.get('total', None)
    
    if mark == 1 and mark_wo == 0:
        total_values['mark=1, mark_wo=0'].append(total)
    elif mark == 0 and mark_wo == 1:
        total_values['mark=0, mark_wo=1'].append(total)
        
print("Total values for each combination:")
for combination, values in total_values.items():
    print(f"{combination}:")
    for value in values:
        print(f"  {value}")