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
    file_path = '/Users/kevinshuey/Documents/Github/llm_uncer/cqa_tryout/gpt_evidence.txt' 
    evidence_sec = extract_evidence(file_path)

    print(evidence_sec[199])
    #for i, evidence in enumerate(evidence_sec):
    #    print(f"Evidence {i+1}:\n{evidence}\n")