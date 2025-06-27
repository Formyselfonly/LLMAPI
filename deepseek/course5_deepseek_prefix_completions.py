from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DeepSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
# The chat prefix completion follows the Chat Completion API,
# where users provide an assistant's prefix message for the model
# to complete the rest of the message.
deepseek_client=OpenAI(
    base_url="https://api.deepseek.com/beta",
    api_key=DeepSEEK_API_KEY
)
prompt="What's your name?"
messages=[
    {"role":"user","content":f"Please me translate into Chinese:{prompt}"},
    {"role":"assistant","content":"```\n","prefix":True}
]

response=deepseek_client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    stream=False,
    stop=["```"]
)
print(response.choices[0].message.content)

