from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2-xl"  # gpt2-medium, gpt2-large, gpt2-xl
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def ask_gpt2(question, max_length=100):
    inputs = tokenizer.encode(question, return_tensors="pt")

    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

question = f"I fucked Xinyi everyday legally, hence she is my"
answer = ask_gpt2(question)
print(f"Ans from GPT-2:\n", answer)