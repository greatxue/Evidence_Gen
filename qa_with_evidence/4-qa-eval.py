import json
from collections import Counter
import argparse
from itertools import combinations

def analyze_marks(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    individual_marks_count = Counter()
    pairwise_combination_count = Counter()

    for item in data:
        # Count individual marks
        individual_marks_count['mark_direct'] += item.get("mark_direct", 0)
        individual_marks_count['mark_CoT'] += item.get("mark_CoT", 0)
        individual_marks_count['mark_evidence'] += item.get("mark_evidence", 0)
        individual_marks_count['mark_evidenceCoT'] += item.get("mark_evidenceCoT", 0)

        # Generate and count two-way combinations of marks
        mark_keys = ["mark_direct", "mark_CoT", "mark_evidence", "mark_evidenceCoT"]
        for (mark1, mark2) in combinations(mark_keys, 2):
            key = f"{mark1}_{mark2}_{item.get(mark1, 0)}{item.get(mark2, 0)}"
            pairwise_combination_count[key] += 1

    # Write results to output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("Individual mark counts:\n")
        for mark_type, count in individual_marks_count.items():
            out_file.write(f"{mark_type}: {count}\n")

        out_file.write("\nPairwise combination counts:\n")
        for combination, count in pairwise_combination_count.items():
            out_file.write(f"{combination}: {count}\n")

    print(f"Analysis results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()
    analyze_marks(args.input_path, args.output_path)