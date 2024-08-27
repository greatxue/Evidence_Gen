from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

#model_name = "gpt2-xl"  # gpt2-medium, gpt2-large, gpt2-xl
#model = GPT2LMHeadModel.from_pretrained(model_name)
#tokenizer = GPT2Tokenizer.from_pretrained(model_name)

model_path = '/data3/greatxue/llm_uncer/cqa_tryout/gpt2-train/results/checkpoint-3500'
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def ask_gpt2(question, max_length=100):
    inputs = tokenizer.encode(question, return_tensors="pt").to(device)

    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer


input_text = "Question: What is the capital of France?\nOptions:\nA. Berlin\nB. Paris\nC. Madrid\nD. Rome\nAnswer:"
inputs = tokenizer(input_text, return_tensors="pt").to(device)
outputs = model.generate(**inputs, max_length=50, num_beams=5, early_stopping=True)
print("Generated answer:", tokenizer.decode(outputs[0], skip_special_tokens=True))