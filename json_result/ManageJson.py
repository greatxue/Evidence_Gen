import json
import re
from collections import defaultdict
import time

class jsonManager:
    def __init__(self, input_file=None, output_file=None, input_file2=None):
        self.input = input_file
        self.input2 = input_file2
        self.output = output_file
        
    def replace_item_json(self):
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            if 'model_answer' in item:
                item['model_answer_wo'] = item.pop('model_answer')  



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

    def eval_json_result_all(self):
        '''Evaluates the effect of evidence by analyzing the result combination of (0, 1, or missing) for mark, mark_wo, and mark_cot.
        '''
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        count_dict = defaultdict(int)

        for item in data:
            # 获取 mark, mark_wo, mark_cot 的值
            mark = item.get('mark', None)
            mark_wo = item.get('mark_wo', None)

            
            # 如果字段为 None，将其标记为 'missing'
            if mark is None:
                mark = 'missing'
            if mark_wo is None:
                mark_wo = 'missing'

            
            # 计数 (mark, mark_wo, mark_cot) 的组合
            count_dict[(mark, mark_wo)] += 1

        # 打印组合计数
        print("Combination counts:")
        for combination, count in count_dict.items():
            print(f"mark={combination[0]}, mark_wo={combination[1]}: {count}")




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

    def list_json_all(self):

        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        total_values = {}

        for item in data:
            # 获取 mark, mark_wo, mark_cot 和 total 值
            mark = item.get('mark', None)
            mark_wo = item.get('mark_wo', None)
            mark_cot = item.get('mark_cot', None)
            total = item.get('total', None)
            
            # 构造组合键
            key = f'mark={mark}, mark_wo={mark_wo}, mark_cot={mark_cot}'
            
            # 将 total 值添加到相应组合的列表中
            if key not in total_values:
                total_values[key] = []
            total_values[key].append(total)

        # 打印所有组合及其对应的 total 值
        print("Total values for each combination:")
        for combination, values in total_values.items():
            print(f"{combination}:")
            for value in values:
                print(f"  {value}")

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
            del item["reference_answer"]


        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"Updated data with 'reference_answer' field removed saved to {self.output}") 

    def generate_json_result(self):
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if data:
            first_item = data[0]
            qwen_answer_text = first_item.get("model_answer_c", "")
            match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
            final_answer = match.group(1) if match else ""

            reference_answer = first_item.get("reference_answer", "").strip()
            
            print("First item:")
            print(f"Final Answer: '{final_answer}'")
            print(f"Reference Answer: '{reference_answer}'")

        for item in data:
            qwen_answer_text = item.get("model_answer_wo", "")
            match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
            final_answer = match.group(1) if match else ""

            item["model_answer"] = final_answer.strip().upper()
            if final_answer.strip().lower() == item.get("reference_answer", "").strip().lower():
                item["mark_wo"] = 1
            else:
                item["mark_wo"] = 0

        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)  
    
    def extract_json_ans(self):
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if data:
            first_item = data[0]
            qwen_answer_text = first_item.get("model_answer_cot", "")
            match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
            final_answer = match.group(1) if match else ""

            reference_answer = first_item.get("reference_answer", "").strip()
            
            print("First item:")
            print(f"Final Answer: '{final_answer}'")
            print(f"Reference Answer: '{reference_answer}'")

        for item in data:
            qwen_answer_text = item.get("model_answer_wo", "")
            match = re.search(r"final answer is:\s*([A-Za-z])", qwen_answer_text)
            final_answer = match.group(1) if match else ""

            item["ans_wo"] = final_answer.strip().upper()

        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)  

    def len_json(self):
        with open(self.input, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            item["len"] = len(item["model_answer"])
            item["len_few"] = len(item["model_answer_few"])

        with open(self.output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)  

    def reorder_keys(self, item):
        '''Reorders the keys in a dictionary based on the specified field order.'''
        key_order = [
            "total", 
            "prompt_wo", "prompt", "prompt_c", "prompt_cot", "prompt_few",
            "model_answer_wo", "model_answer", "model_answer_c", "model_answer_cot", "model_answer_few",
            "mark_wo", "mark", "mark_c", "mark_cot", "mark_few",
            "ans_wo", "ans", "ans_c", "ans_cot", "ans_few", "reference_answer",
            "len_wo", "len", "len_c", "len_cot", "len_few"
        ]
        # Return a new dictionary with keys ordered according to key_order
        return {k: item.get(k) for k in key_order if k in item}

    def merge_json_sort(self):
        '''Merges 2 JSON files into one and reorders the fields.'''
        with open(self.input, 'r') as f1, open(self.input2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        merged_data = {}

        # Merge the data from the first file
        for item in data1:
            key = item['total']
            merged_data[key] = item

        # Merge the data from the second file, updating existing entries or adding new ones
        for item in data2:
            key = item['total']
            if key in merged_data:
                merged_data[key].update(item)
            else:
                merged_data[key] = item

        # Reorder the keys in the merged data according to the desired order
        merged_list = [self.reorder_keys(item) for item in merged_data.values()]

        # Save the reordered merged data to the output file
        with open(self.output, 'w') as f:
            json.dump(merged_list, f, indent=4)

        print(f"Merged and reordered fields saved to {self.output}")

#####################################################################################################

in1 = '/data3/greatxue/llm_uncer/json_result/results-bookqa-gpt4/gpt4-bookqa-allin.json'
in2 =  '/data3/greatxue/llm_uncer/json_result/results-bookqa-gpt4/gpt4-bookqa-allin.json'
ou =  '/data3/greatxue/llm_uncer/json_result/results-bookqa-gpt4/gpt4-bookqa-allin.json'
manager = jsonManager(in1, ou, in2)
#time.sleep(1)
#manager.remove_json()
manager.eval_json_result()

'''
in1 = '/data3/greatxue/result1.json'
in2 = '/data3/greatxue/llm_uncer/json_result/results-qa-gpt4/gpt4-result-commonqa.json'
ou =  '/data3/greatxue/result2.json'
manager = jsonManager(in1, ou, in2)
manager.remove_json()
time.sleep(5)

in1 = '/data3/greatxue/result2.json'
in2 = '/data3/greatxue/llm_uncer/json_result/results-qa-gpt4/gpt4-result-commonqa.json'
ou =  '/data3/greatxue/result3.json'
manager = jsonManager(in1, ou, in2)
manager.merge_json()
time.sleep(5)

in1 = '/data3/greatxue/result3.json'
in2 = '/data3/greatxue/llm_uncer/json_result/results-qa-gpt4/gpt4-result-commonqa.json'
ou =  '/data3/greatxue/result4.json'
manager = jsonManager(in1, ou, in2)
manager.eval_json_result_all()
'''