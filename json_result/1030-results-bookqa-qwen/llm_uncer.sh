conda activate llm_uncer
#gpt4 generates the evidence
python3 /home/wenhao/Project/greatxue/llm_uncer/cqa_tryout/qwen-qa/qwen-evidencer-bookqa.py

#qwen answers itself
python3 /home/wenhao/Project/greatxue/llm_uncer/cqa_tryout/qwen-qa/qwen-record.py
#qwen answers with evidence (void the comments)
python3 /home/wenhao/Project/greatxue/llm_uncer/cqa_tryout/qwen-qa/qwen-record.py

######
#OPEN: /home/wenhao/Project/greatxue/llm_uncer/json_result/manage_json.ipynb
