import json
import argparse
import json
import re

def _extract_ans(text):
    match = re.search(r"final answer is:\s*([A-Za-z])", text)
    return match.group(1) if match else ""

def merge_json_files(output_file, *input_files):
    merged_data = {}

    for file_path in input_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        for item in data:
            key = item['num']
            if key in merged_data:
                merged_data[key].update(item)
            else:
                merged_data[key] = item 

    merged_list = list(merged_data.values())
    
    with open(output_file, 'w') as f:
        json.dump(merged_list, f, indent=4)
    print(f"Merged data saved to {output_file}")

def retrieve_choice(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        reference_answer = item.get("reference_answer", "").strip().upper()
        answer_types = ["direct", "CoT", "evidence", "evidenceCoT"]

        for answer_type in answer_types:
            answer_text = item.get(f"ans_{answer_type}", "")
            final_answer = _extract_ans(answer_text).upper()

            item[f"choice_{answer_type}"] = final_answer
            item[f"mark_{answer_type}"] = 1 if final_answer == reference_answer else 0

        if data.index(item) == 0:
            print('====================Testing========================')
            print("First item example:")
            for answer_type in answer_types:
                print(f"ans_{answer_type}: '{item[f'ans_{answer_type}']}'")
                print(f"mark_{answer_type}: {item[f'mark_{answer_type}']}")
            print('===================================================')
            
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Processed data saved to {output_file}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", type=str)
    parser.add_argument("--input_path", type=str, nargs='+')
    parser.add_argument("--marked_path", type=str)
    
    args = parser.parse_args()
    merge_json_files(args.output_path, *args.input_path)
    print("====================Merged=========================")
    retrieve_choice(args.output_path, args.marked_path)
    print("====================Marked=========================")