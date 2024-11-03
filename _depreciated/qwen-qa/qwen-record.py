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
#dataset = load_dataset("allenai/openbookqa")
split = 'validation' 

total = 0
correct = 0
MAX = 200

file_path = '/home/wenhao/Project/greatxue/llm_uncer/evidence/1031-evi-commonqa-qwen.txt'
evidence_sections = extract_evidence(file_path)
print(f"Evidence extracted.\n====================Test Sample====================")
print(evidence_sections[0])
print('===================================================')
time.sleep(4)

def ques_qwen(ques_str):
    messages = [
        {'role': 'user', 'content': ques_str}]
    response = dashscope.Generation.call(
        'qwen1.5-7b-chat',
        messages=messages,
        result_format='message',  # set the result is message format.
        temperature=0
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
            
            prompt = f"Evidence: \n"
            prompt += evidence_sections[total]
            prompt += f'\n'
        
            prompt += f"Question: {question}\nOptions:\n"
            for idx, choice in enumerate(choices):
                prompt += f"{chr(65 + idx)}. {choice}\n"

            #prompt += f"Based on the evidence and your own knowlege, think about the question.\n"
            prompt += f"Based on your own knowledge, think about the question step by step.\n"
            prompt += f"Then answer the question in the final line, with the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."
            print(prompt)

            response = ques_qwen(prompt)
            qwen_ans = response['output']['choices'][0]['message']['content']
            print(qwen_ans)

            result = {
                "total": total, 
                "prompt": prompt,
                "qwen_answer": qwen_ans,
                "reference_answer": answer_key,
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
        
        time.sleep(1)

    if total >= MAX:
        break

with open('/home/wenhao/Project/greatxue/llm_uncer/logs/1101-commonqa-qwen.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
