from utils.openai import client
from datasets import load_dataset
import time

# Load the OpenBookQA dataset
dataset = load_dataset("allenai/openbookqa")
split = 'validation' 

total = 0
correct = 0
MAX = 200
evifile = "gpt_evidence.txt"

with open(evifile, "w") as f:
    for item in dataset[split]:
        if total + 1 not in [31, 40, 53, 54, 61, 63, 70, 80, 91, 98, 118, 122, 143, 169, 198]: # for further purpose
            total += 1
            continue
        else:
            try:
                question = item['question_stem']
                choices = item['choices']['text']
                answer_key = item['answerKey']

                prompt = f"Question: {question}\nOptions:\n"
                for idx, choice in enumerate(choices):
                    prompt += f"{chr(65 + idx)}. {choice}\n"
                prompt += "Answer directly with the capitalized letter standing for the choice."

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

                evidence_prompt = f"Generate evidence to help a confusing student to answer this question\n"
                evidence_prompt += "Do not mention the correct answer directly in your evidence directly, or you are actually telling them the answer."
                evidence_prompt += f"Question: {question}\nOptions:\n"
                for idx, choice in enumerate(choices):
                    evidence_prompt += f"{chr(65 + idx)}. {choice}\n"
                evidence_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a student helper."},
                        {"role": "user", "content": evidence_prompt}
                    ],
                )

                evidence = evidence_response.choices[0].message.content.strip()
                time.sleep(1)

                f.write(f"Question {total}:\n")
                f.write(f"{question}\n")
                f.write(f"Options: {choices}\n")
                f.write(f"GPT-4 Answer: {gpt_answer[:1]}\n")
                f.write(f"Correct Answer: {answer_key}\n")
                f.write(f"Evidence: {evidence}\n\n")
                print(f"...Evidence written.")

                
            except Exception as e:
                print(f"Error on question {total + 1}: {e}")
                continue  

        if total >= MAX:
            break

acc = correct / total
print(f"Total questions: {total}")
print(f"Correct answers: {correct}")
print(f"Accuracy: {acc:.2%}")