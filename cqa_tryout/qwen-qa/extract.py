def extract_evidence(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    evidence_list = []
    current_evidence = []
    inside_evidence = False

    for line in lines:
        if "Evidence" in line:
            inside_evidence = True
            current_evidence = []
        elif "Question" in line:
            if inside_evidence and current_evidence:
                evidence_list.append("".join(current_evidence).strip())
            inside_evidence = False
        elif inside_evidence:
            current_evidence.append(line)

    if inside_evidence and current_evidence:
        evidence_list.append("".join(current_evidence).strip())

    return evidence_list

if __name__ == "__main__":
    file_path = '/data3/greatxue/llm_uncer/cqa_tryout/gpt4-qa/evidence/evi_bookqa.txt'
    output_file_path = '/data3/greatxue/extracted_evidence.txt'  # 输出文件路径

    evidence_sec = extract_evidence(file_path)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for i, evidence in enumerate(evidence_sec):
            output_file.write(f"Evidence {i+1}:\n{evidence}\n\n")

    print(f"Extracted {len(evidence_sec)} evidence sections to {output_file_path}")