import json

input_file = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/resultOK.json'
output_file = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/ex_resultOK.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

extracted_data = []
for item in data:
    extracted_item = {
        'total': item.get('total', None),
        'mark': item.get('mark', None)
    }
    extracted_data.append(extracted_item)

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(extracted_data, file, indent=4, ensure_ascii=False)

print(f"Extracted fields saved to {output_file}")