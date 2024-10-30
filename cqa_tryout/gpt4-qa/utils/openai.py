import openai
import yaml


def load_client(key_path= '/home/wenhao/Project/greatxue/llm_uncer/cqa_tryout/gpt4-qa/utils/openai_key.yaml'):
    openai._reset_client()
    key = yaml.safe_load(open(key_path))
    for k, v in key.items():
        setattr(openai, k, v)
    return openai._load_client()


client = load_client()
