from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

################ For pretrained models ################
model_name = "gpt2-xl"  # gpt2-medium, gpt2-large, gpt2-xl
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
########################################################

################ For pretrained models ################
#model_path = '/data3/greatxue/llm_uncer/cqa_tryout/gpt2-train/results/checkpoint-3500' # Change to the path
#model = GPT2LMHeadModel.from_pretrained(model_path)
#tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
########################################################

def ques_gpt2(ques, gpu=False, max_length=100):
    if gpu:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input = tokenizer(ques, return_tensors="pt").to(device)
    else:
        input = tokenizer.encode(question, return_tensors="pt")

    output = model.generate(
        input,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    ans = tokenizer.decode(output[0], skip_special_tokens=True)
    return ans

if __name__ == "__name__":
    question = "I got married with Helen, hence she is my"
    answer = ques_gpt2(question)
    print("Ans from GPT-2:\n", answer)

