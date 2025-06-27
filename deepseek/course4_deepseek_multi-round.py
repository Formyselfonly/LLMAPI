from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
deepseek_client=OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

messages=[{"role": "user", "content": "What's the highest mountain in the world?"}]
response=deepseek_client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

assistant_content=response.choices[0].message.content
# print(assistant_content)
# messages.append(response)
messages.append({"role":"assistant","content":assistant_content})
print(f"Messages Round 1: {messages}")
# print(1,messages[0])
# print(2,messages[1])

messages.append({"role":"user","content":"What I just said? Summary for me!"})
response=deepseek_client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)
assistant_content=response.choices[0].message.content
messages.append({"role":"assistant","content":assistant_content})
print(f"Messages Round 2:{messages}")


