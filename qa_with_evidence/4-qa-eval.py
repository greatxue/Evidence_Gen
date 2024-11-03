import json
from collections import Counter
import argparse

def analyze_marks(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    individual_marks_count = Counter()
    combination_count = Counter()

    for item in data:
        individual_marks_count['mark_direct'] += item.get("mark_direct", 0)
        individual_marks_count['mark_CoT'] += item.get("mark_CoT", 0)
        individual_marks_count['mark_evidence'] += item.get("mark_evidence", 0)
        individual_marks_count['mark_evidenceCoT'] += item.get("mark_evidenceCoT", 0)

        combination_key = (
            f"{item.get('mark_direct', 0)}"
            f"{item.get('mark_CoT', 0)}"
            f"{item.get('mark_evidence', 0)}"
            f"{item.get('mark_evidenceCoT', 0)}"
        )

        combination_count[combination_key] += 1

    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("Individual mark counts:\n")
        for mark_type, count in individual_marks_count.items():
            out_file.write(f"{mark_type}: {count}\n")

        out_file.write("\nCombination counts (e.g., '0000', '0101'):\n")
        for combination, count in combination_count.items():
            out_file.write(f"{combination}: {count}\n")

    print(f"Analysis results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()
    analyze_marks(args.input_file, args.output_file)