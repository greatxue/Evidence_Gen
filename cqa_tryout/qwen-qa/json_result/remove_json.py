import json

input_file = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/prev/result_woOK.json'
output_file = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/result_no_mark.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

for item in data:
    if 'mark' in item:
        del item['mark']

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"Updated data with 'mark' field removed saved to {output_file}")