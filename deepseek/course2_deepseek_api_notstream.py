from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")

deepseek_client=OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def deepseek_call(messages):
    completions=deepseek_client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=False
    )
    # return completions.choices[0].message.content
    return completions.choices[0].message


messages=[{"role":"user","content":"9.11 and 9.8,which is greater"}]
answer=deepseek_call(messages=messages)
# print(f"answer: \n{answer}\n")
reasoning_content=answer.reasoning_content
print(f"reasoning_content: \n{reasoning_content}\n")
content=answer.content
print(f"content: \n{content}\n")

# print(f"Available model:{deepseek_client.models.list()}")
# print(f"Response:\n{deepseek_call("Hello")}")

messages.append({"role":"assistant","content":content})
messages.append({"role":"user","content":"How many Rs are there in the word 'strawberry' "})
content=deepseek_call(messages=messages)
print(f"messages:\n {messages}\n")
print(f"content:\n{content.content}\n")
