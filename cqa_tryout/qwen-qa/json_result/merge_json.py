import json

file1 = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/prev/ex_resultOK.json'
file2 = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/prev/result_no_mark.json'

with open(file1, 'r') as f1, open(file2, 'r') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

merged_data = {}

for item in data1:
    key = item['total']
    merged_data[key] = item 

for item in data2:
    key = item['total']
    if key in merged_data:
        merged_data[key].update(item) 
    else:
        merged_data[key] = item  

merged_list = list(merged_data.values())

with open('RESULT_reallyOK.json', 'w') as f:
    json.dump(merged_list, f, indent=4)

print("===============Saved===============")