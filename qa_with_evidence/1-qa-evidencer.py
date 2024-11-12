import os
# Set environment variable for Dashscope API key
os.environ['DASHSCOPE_API_KEY'] = 'sk-da1b1321d9d344a6ae18e27fac23c6ae'
import argparse
import time
from http import HTTPStatus
from datasets import load_dataset
import dashscope

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

#TODO
def _load_bookqa(dataset_name):
    pass

def _load_simpleEval(dataset_name):
    pass

def load_data():
    pass

def main(args):
    # Load dataset
    dataset = load_dataset("allenai/openbookqa")
    split = 'validation'
    
    total = 0
    correct = 0
    max_questions = args.max_questions
    
    with open(args.output_path, "w") as f:
        for item in dataset[split]:
            try:
                question = item['question_stem']
                choices = item['choices']['text']
                answer_key = item['answerKey']

                prompt = f"Question: {question}\nOptions:\n"
                for idx, choice in enumerate(choices):
                    prompt += f"{chr(65 + idx)}. {choice}\n"
                prompt += "Answer directly with the capitalized letter standing for the choice."

                response = query_model(args.model_name, prompt)
                gpt_answer = response['output']['choices'][0]['message']['content']

                # Check if the answer is correct
                if gpt_answer[:1].upper() == answer_key:
                    correct += 1

                total += 1  

                print(f"{total}-th Processing... {gpt_answer[:1]} vs {answer_key}.")

                # Generate evidence
                evidence_prompt = "Generate evidence to help a confusing student to answer this question\n"
                evidence_prompt += "Do not mention the correct answer directly in your evidence directly, or you are actually telling them the answer."
                evidence_prompt += f"Question: {question}\nOptions:\n"
                for idx, choice in enumerate(choices):
                    evidence_prompt += f"{chr(65 + idx)}. {choice}\n"
                evidence_response = query_model(args.model_name, evidence_prompt)

                evidence = evidence_response['output']['choices'][0]['message']['content'].strip()
                time.sleep(1)

                # Write to file
                f.write(f"Question {total}:\n")
                f.write(f"{question}\n")
                f.write(f"Options: {choices}\n")
                f.write(f"qwen Answer: {gpt_answer[:1]}\n")
                f.write(f"Correct Answer: {answer_key}\n")
                f.write(f"Evidence==: {evidence}\n\n")
                print("...Evidence written.")

                if total >= max_questions:
                    print(f"Reached the maximum of {max_questions} questions. Exiting.")
                    break

            except Exception as e:
                print(f"Error on question {total + 1}: {e}")
                continue  

    acc = correct / total if total > 0 else 0
    print(f"Total questions: {total}")
    print(f"Correct answers: {correct}")
    print(f"Acc: {acc}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, required="allenai/openbookqa")
    parser.add_argument("--model_name", type=str, default="qwen1.5-7b-chat")
    parser.add_argument("--output_path", type=str, default="evidence.txt")
    parser.add_argument("--max_questions", type=int, default=200)

    args = parser.parse_args()
    main(args)