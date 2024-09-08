import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-da1b1321d9d344a6ae18e27fac23c6ae'
from http import HTTPStatus
import dashscope
from datasets import load_dataset
from extract import extract_evidence
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
            question = item['question_stem']
            choices = item['choices']['text'] 
            answer_key = item['answerKey']
            
            prompt = f"Evidence: \n"
            prompt += evidence_sections[total]
            prompt += f'\n'
        
            prompt += f"Question: {question}\nOptions:\n"
            for idx, choice in enumerate(choices):
                prompt += f"{chr(65 + idx)}. {choice}\n"

            prompt += f"Think about the question with your knowledge first. If you feel hard about the problem, refer to the evidence for help.\n"
            prompt += f"Then answer the question in the final line, with the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."
            print(prompt)

            response = ques_qwen(prompt)
            qwen_ans = response['output']['choices'][0]['message']['content']
            print(qwen_ans)

            result = {
                "total": total, 
                "prompt": prompt,
                "qwen_answer_wo": qwen_ans,
                "reference_answer": answer_key,
                "mark": "",
                "mark_wo": ""
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

with open('results.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
