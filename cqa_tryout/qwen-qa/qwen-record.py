import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-da1b1321d9d344a6ae18e27fac23c6ae'
from http import HTTPStatus
import dashscope
from datasets import load_dataset
from extract import extract_evidence
import time
import json

data = []

dataset = load_dataset("tau/commonsense_qa")
split = 'validation' 

total = 0
correct = 0
MAX = 200
DELAY = 1

file_path = '/data3/greatxue/llm_uncer/cqa_tryout/gpt4-qa/gpt_evidence.txt'
evidence_sections = extract_evidence(file_path)
print("Evidence extracted.")
print(evidence_sections[0])
time.sleep(4)

def ques_qwen(ques_str):
    messages = [
        {'role': 'user', 'content': ques_str}]
    response = dashscope.Generation.call(
        'qwen1.5-7b-chat',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        return response
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

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
            #prompt += f"Here is some evidence which could be helpful to solve the problem:\n"
            #prompt += evidence_sections[total]
            #prompt += f'\n'
            prompt += "Based on your own knowledge, answer directly the capitalized letter standing for the choice."
            #prompt += "Based on the evidence and your own knowledge, answer directly the capitalized letter standing for the choice."

            response = ques_qwen(prompt)
            qwen_ans = response['output']['choices'][0]['message']['content']

            result = {
                "total": total,  # total计数从1开始
                "prompt-wo": prompt,
                "qwen_answer_wo": qwen_ans,
                #"reference_answer": answer_key
            }

            data.append(result)
            print(f"{total} processing...")
            
            total += 1
            
        except Exception as e:
            print(f"Error on question {total + 1}: {e}")
            continue  
        
        time.sleep(DELAY)

    if total >= MAX:
        break

with open('results2.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
