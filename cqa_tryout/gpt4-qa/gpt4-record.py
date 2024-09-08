import openai
from utils.openai import client
from datasets import load_dataset
from evidence.extract import extract_evidence
import time
import json

data = []

dataset = load_dataset("allenai/openbookqa")
split = 'validation' 

total = 0
correct = 0
MAX = 200

file_path = '/data3/greatxue/llm_uncer/cqa_tryout/gpt4-qa/evidence/evi_bookqa.txt'
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
            {"role": "user", "content": prompt}
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

            #prompt = f"Evidence: \n"
            #prompt += evidence_sections[total]
            #prompt += f'\n'
        
            prompt = f"Question: {question}\nOptions:\n"
            for idx, choice in enumerate(choices):
                prompt += f"{chr(65 + idx)}. {choice}\n"

            #prompt += f"Based on the evidence and your own knowlege, think about the question.\n"
            prompt += f"Based on your own knowlege, think about the question.\n"
            prompt += f"Then answer the question in the final line, with the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."
            print(prompt)

            #response = ques_gpt(prompt)
            #gpt_ans = response.choices[0].message.content.strip()
            #print(gpt_ans)

            result = {
                "total": total, 
                "prompt": prompt,
                #"qwen_answer_wo": gpt_ans,
                #"reference_answer": answer_key,
                #"mark": "",
                #"mark_wo": ""
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

with open('results++.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)