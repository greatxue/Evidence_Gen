import os
# Set environment variable for Dashscope API key
os.environ['DASHSCOPE_API_KEY'] = 'sk-da1b1321d9d344a6ae18e27fac23c6ae'
import argparse
import time
from http import HTTPStatus
from datasets import load_dataset
import dashscope
import pandas as pd

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

def load_csv_data(file_path):
    try:
        data = pd.read_csv(file_path)
        if "problem" not in data.columns:
            raise ValueError("CSV file must contain 'problem' column.")
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
    
def main(args):
    # Load dataset
    file_path = "/home/wenhao/Project/greatxue/llm_uncer/data/simple_eval.csv"
    data = load_csv_data(file_path)
    
    total = 0
    max_questions = args.max_questions
    
    with open(args.output_path, "w") as f:
        for idx, row in data.iterrows():
            if total >= max_questions:
                print(f"Reached the maximum of {max_questions} problems. Exiting.")
                break           
            try:
                problem = row['problem']

                # 构建解答 Prompt
                answer_prompt = f"Please provide a detailed answer for the following problem:\n{problem}"
                answer = query_model(args.model_name, answer_prompt)

                if answer is None:
                    print(f"Failed to get a response for problem {total + 1}. Skipping.")
                    continue

                # 构建证据 Prompt
                evidence_prompt = (
                    "Now, provide an explanation or reasoning for the answer above. "
                    "The explanation should be helpful and clear, without directly repeating the answer."
                )
                evidence = query_model(args.model_name, evidence_prompt)

                # 写入文件
                f.write(f"Problem {total + 1}:\n")
                f.write(f"{problem}\n")
                f.write(f"Answer:\n{answer.strip()}\n")
                f.write(f"Explanation:\n{evidence.strip() if evidence else 'N/A'}\n")
                f.write("\n" + "="*50 + "\n\n")

                print(f"Processed problem {total + 1}.")
                total += 1

            except Exception as e:
                print(f"Error on problem {total + 1}: {e}")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, required="allenai/openbookqa")
    parser.add_argument("--model_name", type=str, default="qwen1.5-7b-chat")
    parser.add_argument("--output_path", type=str, default="evidence.txt")
    parser.add_argument("--max_questions", type=int, default=200)

    args = parser.parse_args()
    main(args)