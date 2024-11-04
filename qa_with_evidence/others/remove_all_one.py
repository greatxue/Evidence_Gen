import json

with open('/home/wenhao/Project/greatxue/llm_uncer/output/merged_json/11031953-openbookqa-marked.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

filtered_data = [
    item for item in data
    if not (item["mark_direct"] == 1 and item["mark_CoT"] == 1 and item["mark_evidence"] == 1 and item["mark_evidenceCoT"] == 1)
]

with open('/home/wenhao/Project/greatxue/llm_uncer/output/merged_json/11031953-openbookqa-marked-removed.json', 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)
