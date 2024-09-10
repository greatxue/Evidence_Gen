from utils.openai import client
from datasets import load_dataset
from evidence.extract import extract_evidence
import time
import json

data = []

dataset = load_dataset("allenai/openbookqa")
split = 'validation'

train_set = dataset['train']
few_shot_examples = []
few_shot_count = 10 

for i in range(few_shot_count):
    question = train_set[i]['question_stem']
    choices = train_set[i]['choices']['text']
    answer_key = train_set[i]['answerKey']

    few_shot_example = f"Question: {question}\nOptions:\n"
    for idx, choice in enumerate(choices):
        few_shot_example += f"{chr(65 + idx)}. {choice}\n"
    few_shot_example += f"The final answer is: {answer_key}.\n\n"

    few_shot_examples.append(few_shot_example)

few_shot_prompt = "".join(few_shot_examples)

total = 0
correct = 0
MAX = 200

file_path =  '/data3/greatxue/llm_uncer/cqa_tryout/gpt4-qa/evidence/evi_commonqa.txt'
evidence_sections = extract_evidence(file_path)
print(f"Evidence extracted.\n====================Test Sample====================")
print(evidence_sections[0])
print('===================================================')
time.sleep(4)

def ques_gpt(ques_str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a student answering multiple choice exercises."},
            {"role": "user", "content": ques_str}
        ],
    )
    if response.choices[0]:
        return response
    else:
        print('No valid GPT-response generated.')

for item in dataset[split]:
    if False: # for further purpose
        total +=1
        continue
    else:
        try:
            question = item['question_stem']
            choices = item['choices']['text']
            answer_key = item['answerKey']

            prompt = f"Here are some examples to show you the answer of similar questions."
            prompt += few_shot_prompt  
            
            prompt += "Here is the problem you need to answer."
            prompt += f"Question: {question}\nOptions:\n"
            for idx, choice in enumerate(choices):
                prompt += f"{chr(65 + idx)}. {choice}\n"
            

            prompt += f"Based on your own knowledge and the given examples, think about the question.\n"
            prompt += f"Answer the question in the final line, with the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."
            print(prompt)

            response = ques_gpt(prompt)
            gpt_ans = response.choices[0].message.content.strip()
            print(gpt_ans)

            result = {
                "total": total,
                "prompt_few": prompt,
                "model_answer_few": gpt_ans,
                "mark_few": ""
            }

            data.append(result)
            print(f"=============================={total} processing==============================")
            print(f"========================================================================")

            total += 1
        except Exception as e:
            print(f"Error on question {total + 1}: {e}")
            continue

    if total >= MAX:
        break

with open('resul.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)