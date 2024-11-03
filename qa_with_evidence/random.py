import json
import re

def extract_final_answer(text):
    """Extract the final answer (capital letter) from the answer text."""
    match = re.search(r"final answer is:\s*([A-Za-z])", text)
    return match.group(1) if match else ""

def generate_json_result(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        # Extract reference answer
        reference_answer = item.get("reference_answer", "").strip().upper()

        # Define answer types to process
        answer_types = ["direct", "CoT", "evidence", "evidenceCoT"]

        for answer_type in answer_types:
            # Extract answer text for the current type
            answer_text = item.get(f"ans_{answer_type}", "")
            # Extract the final answer from the answer text
            final_answer = extract_final_answer(answer_text).upper()

            # Store the final answer under a specific key
            item[f"choice_{answer_type}"] = final_answer

            # Calculate mark based on comparison with reference answer
            item[f"mark_{answer_type}"] = 1 if final_answer == reference_answer else 0

        # Optionally, log first item for verification
        if data.index(item) == 0:
            print('====================Testing========================')
            print("First item example:")
            for answer_type in answer_types:
                print(f"ans_{answer_type}: '{item[f'ans_{answer_type}']}'")
                print(f"mark_{answer_type}: {item[f'mark_{answer_type}']}")
            print('===================================================')

    # Write modified data to output JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Processed data saved to {output_file}.")

generate_json_result("/home/wenhao/Project/greatxue/llm_uncer/output/merged_json/11022329-openbookqa-merged.json", "/home/wenhao/Project/greatxue/llm_uncer/output/merged_json/11022329-openbookqa-marked.json")