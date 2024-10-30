from utils.openai import client

prompt = "Based on your trained knowlege, is Prof Tianshu Yu student of Prof Baoxin Li?"
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an assistant helping to distinguish academic relationship."},
        {"role": "user", "content": prompt}
    ],
)

gpt_ans = response.choices[0].message.content.strip()
print(gpt_ans)