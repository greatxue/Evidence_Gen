import argparse
import time
import json
from http import HTTPStatus
from datasets import load_dataset
####################################################################################################
import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-da1b1321d9d344a6ae18e27fac23c6ae'
import dashscope
#from utils.openai import client  # gpt-api currently unavailable 
####################################################################################################
from utils.extract import extract_evidence
####################################################################################################

def load_data(dataset_name, split):
    if dataset_name == "openbookqa":
        dataset = load_dataset("allenai/openbookqa")
        return dataset[split]
    elif dataset_name == "commonsenseqa":
        dataset = load_dataset("tau/commonsense_qa")
        return dataset[split]
    else:
        raise ValueError(f"Dataset {dataset_name} is not available.")
####################################################################################################

def _query_qwen(prompt, temp):
    messages = [
        {'role': 'user', 'content': prompt}]
    response = dashscope.Generation.call(
        'qwen1.5-7b-chat',
        messages=messages,
        result_format='message',
        temperature=temp
    )
    if response.status_code == HTTPStatus.OK:
        ans = response['output']['choices'][0]['message']['content']
        return ans
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
'''
def _query_gpt(prompt, temp):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    ans = response.choices[0].message.content.strip()
    return ans
'''
def query_model(model_name, prompt, temp=0):
    if model_name=="qwen1.5-7b-chat":
        return _query_qwen(prompt, temp)
    #elif model_name=="gpt-4o":
    #    return _query_gpt(prompt, temp)
    else:
        raise ValueError(f"The model {model_name} is not available.")
####################################################################################################

def combine_prompt(question, choices, prompt_type, num, evidence_sections):
    if prompt_type == "direct":
        prompt = f"Question: {question}\nOptions:\n"
        for idx, choice in enumerate(choices):
            prompt += f"{chr(65 + idx)}. {choice}\n"
        prompt += "Answer directly with the capitalized letter standing for the choice, with the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."
            
    elif prompt_type == "CoT":
        prompt = f"Question: {question}\nOptions:\n"
        for idx, choice in enumerate(choices):
            prompt += f"{chr(65 + idx)}. {choice}\n"
        prompt += "Based on your own knowlege, think about the question step by step.\n"
        prompt += "In the final sentence, answer the question in the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."
        
    elif prompt_type == "evidence":
        prompt = "Evidence: \n"
        prompt += evidence_sections[num]
        prompt += '\n'
        prompt += f"Question: {question}\nOptions:\n"
        for idx, choice in enumerate(choices):
            prompt += f"{chr(65 + idx)}. {choice}\n"
        prompt += "Based on your own knowledge, answer directly with the capitalized letter standing for the choice, in the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."
    
    elif prompt_type == "evidenceCoT":
        prompt = "Evidence: \n"
        prompt += evidence_sections[num]
        prompt += '\n'
        prompt += f"Question: {question}\nOptions:\n"
        for idx, choice in enumerate(choices):
            prompt += f"{chr(65 + idx)}. {choice}\n"
        prompt += "Based on your own knowledge, think about the question step by step.\n"
        prompt += "In the final sentence, answer the question in the format 'The final answer is: X.', where X is the UNIQUE capitalized letter standing for the choice."

    else:
        raise ValueError(f"Invalid prompt type {prompt_type} specified.")
    
    return prompt
####################################################################################################


def create_result(prompt_type, num, prompt, model_ans, answer_key):
    if prompt_type == "direct":
        result = {
            "num": num,
            "prompt_direct": prompt,
            "ans_direct": model_ans,
            "reference_answer": answer_key
        }

    elif prompt_type == "CoT":
        result = {
            "num": num,
            "prompt_CoT": prompt,
            "ans_CoT": model_ans,
            "reference_answer": answer_key
        }

    elif prompt_type == "evidence":
        result = {
            "num": num,
            "prompt_evidence": prompt,
            "ans_evidence": model_ans,
            "reference_answer": answer_key
        }

    elif prompt_type == "evidenceCoT":
        result = {
            "num": num,
            "prompt_evidenceCoT": prompt,
            "ans_evidenceCoT": model_ans,
            "reference_answer": answer_key
        }

    return result

def main(args):
    data = []
    num = 0
    
    evidence_sections = extract_evidence(args.evidence_path)
    print("Evidence has been extracted. Testing:\n")
    print("====================Test Sample====================")
    print(evidence_sections[0])
    print("===================================================")
    time.sleep(2)
    
    dataset = load_data(args.dataset_name, args.split)
    
    for item in dataset:
        try:
            if args.dataset_name == "commonsenseqa":
                question = item['question']
            elif args.dataset_name == "openbookqa":
                question = item['question_stem']
            
            choices = item['choices']['text']
            answer_key = item['answerKey']

            prompt = combine_prompt(question, choices, args.prompt_type, num, evidence_sections)
            print("====================Prompt=========================")
            print(prompt)

            model_ans = query_model(args.model_name, prompt, temp=0)
            print("====================Result=========================")
            print(model_ans)

            result = create_result(args.prompt_type, num, prompt, model_ans, answer_key)
            data.append(result)
            print(f"============={num} Processed=========================")
            print("==================================================")

            num += 1
        
        except Exception as e:
            print(f"Error on question {num + 1}: {e}")
            continue  

        time.sleep(1)
    
        if num >= args.max_questions:
            break
    with open(args.output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", type=str, default="validation")
    parser.add_argument("--max_questions", type=int, default=200)
    parser.add_argument("--dataset_name", type=str, default="openbookqa")
    parser.add_argument("--model_name", type=str, default="qwen1.5-7b-chat")
    parser.add_argument("--prompt_type", type=str, default="direct")
    parser.add_argument("--evidence_path", type=str, default="evidence.txt")
    parser.add_argument("--output_path", type=str, default="output.txt")
    
    args = parser.parse_args()
    main(args)













