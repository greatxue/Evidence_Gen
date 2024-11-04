import json
from collections import Counter, defaultdict
import argparse
import itertools

def analyze_marks(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    individual_marks_count = Counter()
    pairwise_combination_count = Counter()

    for item in data:
        individual_marks_count['mark_direct'] += item.get("mark_direct", 0)
        individual_marks_count['mark_CoT'] += item.get("mark_CoT", 0)
        individual_marks_count['mark_evidence'] += item.get("mark_evidence", 0)
        individual_marks_count['mark_evidenceCoT'] += item.get("mark_evidenceCoT", 0)

        mark_keys = ["mark_direct", "mark_CoT", "mark_evidence", "mark_evidenceCoT"]
        for (mark1, mark2) in itertools.combinations(mark_keys, 2):
            key_prefix = f"{mark1}_{mark2}"
            key = f"{key_prefix}_{item.get(mark1, 0)}{item.get(mark2, 0)}"
            pairwise_combination_count[key] += 1

    # Group by key_prefix (e.g., 'mark_direct_mark_CoT') for sorted output
    grouped_combinations = defaultdict(list)
    for key in sorted(pairwise_combination_count):
        key_prefix = "_".join(key.split("_")[:2])  # Extract 'mark1_mark2' prefix
        grouped_combinations[key_prefix].append((key, pairwise_combination_count[key]))

    # Write results to output file
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write("Individual mark counts:\n")
        for mark_type, count in individual_marks_count.items():
            out_file.write(f"{mark_type}: {count}\n")

        out_file.write("\nPairwise combination counts:\n")
        for key_prefix, combinations in grouped_combinations.items():
            out_file.write(f"\n{key_prefix}:\n")
            for key, count in combinations:
                out_file.write(f"  {key}: {count}\n")

    print(f"Analysis results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()
    analyze_marks(args.input_path, args.output_path)









'''
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
'''