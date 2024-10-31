import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-da1b1321d9d344a6ae18e27fac23c6ae'
from datasets import load_dataset
import dashscope
import time
from http import HTTPStatus

# Load the OpenBookQA dataset
dataset = load_dataset("tau/commonsense_qa")
split = 'validation' 

total = 0
correct = 0
MAX = 200
evifile = "/home/wenhao/Project/greatxue/llm_uncer/evidence/1030-evi-commonqa-qwen.txt"

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

with open(evifile, "w") as f:
    for item in dataset[split]:
        try:
            question = item['question']
            choices = item['choices']['text']
            answer_key = item['answerKey']

            prompt = f"Question: {question}\nOptions:\n"
            for idx, choice in enumerate(choices):
                prompt += f"{chr(65 + idx)}. {choice}\n"
            prompt += "Answer directly with the capitalized letter standing for the choice."

            response = ques_qwen(prompt)
            gpt_answer = response['output']['choices'][0]['message']['content']

            # Check if the answer is correct
            if gpt_answer[:1].upper() == answer_key:
                correct += 1

            # Increment total after processing a question
            total += 1  

            print(f"{total}-th Processing... {gpt_answer[:1]} vs {answer_key}.")

            # Generate evidence
            evidence_prompt = f"Generate evidence to help a confusing student to answer this question\n"
            evidence_prompt += "Do not mention the correct answer directly in your evidence directly, or you are actually telling them the answer."
            evidence_prompt += f"Question: {question}\nOptions:\n"
            for idx, choice in enumerate(choices):
                evidence_prompt += f"{chr(65 + idx)}. {choice}\n"
            evidence_response = ques_qwen(evidence_prompt)

            evidence = evidence_response['output']['choices'][0]['message']['content'].strip()
            time.sleep(1)

            # Write to file
            f.write(f"Question {total}:\n")
            f.write(f"{question}\n")
            f.write(f"Options: {choices}\n")
            f.write(f"qwen Answer: {gpt_answer[:1]}\n")
            f.write(f"Correct Answer: {answer_key}\n")
            f.write(f"Evidence==: {evidence}\n\n")
            print(f"...Evidence written.")

            # Check if we've reached the maximum number of questions
            if total >= MAX:
                print(f"Reached the maximum of {MAX} questions. Exiting.")
                break

        except Exception as e:
            print(f"Error on question {total + 1}: {e}")
            continue  

# Final statistics
acc = correct / total if total > 0 else 0  # Avoid division by zero
print(f"Total questions: {total}")
print(f"Correct answers: {correct}")