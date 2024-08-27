from datasets import load_dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
import os 
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID" 
os.environ['CUDA_VISIBLE_DEVICES'] = "1,4" 
dataset = load_dataset("tau/commonsense_qa")

def aggregate(examples):
    inputs = []
    targets = []

    for question, choices, answer in zip(examples['question'], examples['choices'], examples['answerKey']):
        input_str = f"Question: {question}\nOptions:\n"
        for i, choice in enumerate(choices['text']):
            input_str += f"{chr(65+i)}. {choice}\n"
        target_str = f"{answer}\n"
        
        inputs.append(input_str)
        targets.append(f"Answer:\n{target_str}")

    return {"input_text": inputs, "target_text": targets}

def tokenize(examples):
    inputs = examples["input_text"]
    targets = examples["target_text"]

    model_inputs = tokenizer(inputs, padding="max_length", truncation=True, max_length=128)
    labels = tokenizer(targets, padding="max_length", truncation=True, max_length=128)["input_ids"]

    model_inputs["labels"] = labels
    return model_inputs

processed = dataset.map(aggregate, batched=True)

print("================Input Text Example================")
print(processed['train'][0]['input_text'])
print("\n================Target Text Example================")
print(processed['train'][0]['target_text'])

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
)

tokenized = processed.map(tokenize, batched=True)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
)

trainer.train()