import json
import re
from collections import defaultdict

class jsonManager:
    def __init__(self, input_file=None, output_file=None, input_file2=None):
        self.input = input_file
        self.input2 = input_file2
        self.output = output_file
        
    def replace_item_json(self):
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            if 'qwen_answer' in item:
                item['model_answer'] = item.pop('qwen_answer')  
            if 'qwen_answer_wo' in item:
                item['model_answer_wo'] = item.pop('qwen_answer_wo')  

        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"Replaced 'prompt' with 'prompt_wo' and saved to {self.output}")

    def extract_json(self):
        '''Extracts part of json items and save them into a new one.
        '''
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        extracted_data = []
        for item in data:
            extracted_item = {
                'total': item.get('total', None),
                'mark': item.get('mark', None)
            }
            extracted_data.append(extracted_item)

        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(extracted_data, file, indent=4, ensure_ascii=False)

        print(f"Extracted fields saved to {self.output}")        

    def eval_json_result(self):
        '''Evaluates the effect of evidence by analyzing the result combination of (0, 1).
        '''
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        count_dict = defaultdict(int)

        for item in data:
            mark = item.get('mark', None)
            mark_wo = item.get('mark_wo', None)
            
            if mark is None:
                mark = 'missing'
            if mark_wo is None:
                mark_wo = 'missing'
            
            count_dict[(mark, mark_wo)] += 1

        print("Combination counts:")
        for combination, count in count_dict.items():
            print(f"mark={combination[0]}, mark_wo={combination[1]}: {count}")

    def list_json(self):
        """Examines in detail by listing all entries that changed.
        """

        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        total_values = {
            'mark=1, mark_wo=0': [],
            'mark=0, mark_wo=1': []
        }

        for item in data:
            mark = item.get('mark', None)
            mark_wo = item.get('mark_wo', None)
            total = item.get('total', None)
            
            if mark == 1 and mark_wo == 0:
                total_values['mark=1, mark_wo=0'].append(total)
            elif mark == 0 and mark_wo == 1:
                total_values['mark=0, mark_wo=1'].append(total)
                
        print("Total values for each combination:")
        for combination, values in total_values.items():
            print(f"{combination}:")
            for value in values:
                print(f"  {value}")

    def merge_json(self):
        '''Merges 2 json files into one.
        '''
        with open(self.input, 'r') as f1, open(self.input2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        merged_data = {}

        for item in data1:
            key = item['total']
            merged_data[key] = item 

        for item in data2:
            key = item['total']
            if key in merged_data:
                merged_data[key].update(item) 
            else:
                merged_data[key] = item  

        merged_list = list(merged_data.values())

        with open(self.output, 'w') as f:
            json.dump(merged_list, f, indent=4)

        print(f"Merged fields saved to {self.output}")        

    def remove_json(self):
        '''Removes some item of json.
        '''
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            if 'mark' in item:
                del item['mark']

        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"Updated data with 'mark' field removed saved to {self.output}") 

    def generate_json_result(self):
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if data:
            first_item = data[0]
            qwen_answer_text = first_item.get("qwen_answer", "")
            match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
            final_answer = match.group(1) if match else ""

            reference_answer = first_item.get("reference_answer", "").strip()
            
            print("First item:")
            print(f"Final Answer: '{final_answer}'")
            print(f"Reference Answer: '{reference_answer}'")

        for item in data:
            qwen_answer_text = item.get("qwen_answer", "")
            match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
            final_answer = match.group(1) if match else ""

            if final_answer.strip().lower() == item.get("reference_answer", "").strip().lower():
                item["mark"] = 1
            else:
                item["mark"] = 0

        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)  

#####################################################################################################
in1 = '/data3/greatxue/llm_uncer/cqa_tryout/json_result/results-bookqa-gpt/gpt4-bookqa.json'
in2 = '/data3/greatxue/llm_uncer/cqa_tryout/json_result/results-bookqa-gpt/results-bookqa-gpt.json'
ou = '/data3/greatxue/llm_uncer/dd.json'
manager = jsonManager(in1, ou, in2)
manager.replace_item_json()