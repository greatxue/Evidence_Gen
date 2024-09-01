import json
import re

input = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/result_.json'
output = '/data3/greatxue/llm_uncer/cqa_tryout/qwen-qa/json_result/resultOK.json'

with open(input, 'r', encoding='utf-8') as file:
    data = json.load(file)

if data:
    first_item = data[0]
    qwen_answer_text = first_item.get("qwen_answer", "")
    match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
    final_answer = match.group(1) if match else ""

    reference_answer = first_item.get("reference_answer", "").strip()
    
    print("First item:")
    print(f"Final Answer: '{final_answer}'")
    print(f"Reference Answer: '{reference_answer}'")

for item in data:
    qwen_answer_text = item.get("qwen_answer", "")
    match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
    final_answer = match.group(1) if match else ""

    if final_answer.strip().lower() == item.get("reference_answer", "").strip().lower():
        item["mark"] = 1
    else:
        item["mark"] = 0

with open(output, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)