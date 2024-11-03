import json
from collections import Counter

def analyze_marks(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Initialize counters
    individual_marks_count = Counter()
    combination_count = Counter()

    for item in data:
        # Count individual mark types
        individual_marks_count['mark_direct'] += item.get("mark_direct", 0)
        individual_marks_count['mark_CoT'] += item.get("mark_CoT", 0)
        individual_marks_count['mark_evidence'] += item.get("mark_evidence", 0)
        individual_marks_count['mark_evidenceCoT'] += item.get("mark_evidenceCoT", 0)

        # Create a combination key (e.g., '1010') for the mark values
        combination_key = (
            f"{item.get('mark_direct', 0)}"
            f"{item.get('mark_CoT', 0)}"
            f"{item.get('mark_evidence', 0)}"
            f"{item.get('mark_evidenceCoT', 0)}"
        )

        # Count this specific combination
        combination_count[combination_key] += 1

    # Open output file to write results
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Write individual mark counts
        out_file.write("Individual mark counts:\n")
        for mark_type, count in individual_marks_count.items():
            out_file.write(f"{mark_type}: {count}\n")

        # Write combination counts
        out_file.write("\nCombination counts (e.g., '0000', '0101'):\n")
        for combination, count in combination_count.items():
            out_file.write(f"{combination}: {count}\n")

    print(f"Analysis results saved to {output_file}")

# Usage
input_file = "/home/wenhao/Project/greatxue/llm_uncer/output/merged_json/11022329-openbookqa-marked.json"  # Replace with the path to your JSON file
output_file = "/home/wenhao/Project/greatxue/llm_uncer/output/merged_json/11022329-openbookqa.txt"    # Replace with the desired output text file name
analyze_marks(input_file, output_file)