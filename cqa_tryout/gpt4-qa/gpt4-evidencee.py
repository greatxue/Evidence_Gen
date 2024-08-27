from utils.openai import client
from datasets import load_dataset
from extract import extract_evidence
import time

dataset = load_dataset("tau/commonsense_qa")
split = 'validation' 

total = 0
correct = 0
MAX = 200

file_path = '/Users/kevinshuey/Documents/Github/llm_uncer/cqa_tryout/gpt_evidence.txt' 
evidence_sections = extract_evidence(file_path)
print("Evidence extracted.")
print(evidence_sections[0])
time.sleep(4)


for item in dataset[split]:
    if False: # for further purpose
        total +=1
        continue
    else:
        try:
            question = item['question']
            choices = item['choices']['text'] 
            answer_key = item['answerKey']

            prompt = f"Question: {question}\nOptions:\n"
            for idx, choice in enumerate(choices):
                prompt += f"{chr(65 + idx)}. {choice}\n"
            prompt += f"Here is some evidence which could be helpful to solve the problem:\n"
            prompt += evidence_sections[total]
            prompt += f'\n'
            prompt += "Based on the evidence and your own knowledge, answer directly the capitalized letter standing for the choice. No reason required."

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a student answering multiple choice exercises."},
                    {"role": "user", "content": prompt}
                ],
            )

            gpt_answer = response.choices[0].message.content.strip()

            if gpt_answer[:1].upper() == answer_key:
                correct += 1
            total += 1

            print(f"{total}-th Processing... {gpt_answer[:1]} vs {answer_key}.")

            
        except Exception as e:
            print(f"Error on question {total + 1}: {e}")
            continue  

    if total >= MAX:
        break

acc = correct / total
print(f"Total questions: {total}")
print(f"Correct answers: {correct}")
print(f"Accuracy: {acc:.2%}")