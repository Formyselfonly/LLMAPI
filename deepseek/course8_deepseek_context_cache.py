from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
deepseek_client=OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def deepseek_chat(prompt):
    completions=deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role":"system","content":"You're my helpful assistant"},
            {"role":"user","content":prompt}
        ]
    )
    return completions.choices[0].message.content

def deepseek_reasoner(prompt):
    completions=deepseek_client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "You're my helpful assistant"},
            {"role": "user", "content": prompt}
        ]
    )
    answer=completions.choices[0].message
    return answer.reasoning_content,answer.content

prompt="Help me just translate this into CN and don't provide other:What's your name?"
chat_answer=deepseek_chat(prompt)
reasoner_answer=deepseek_reasoner(prompt)
print(f"""
-----------------------------------
Chat Answer: {chat_answer}
-----------------------------------
Reasoner Answer: {reasoner_answer}
-----------------------------------
""")