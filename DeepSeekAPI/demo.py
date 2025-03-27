# base_url:https://api.deepseek.com
# api_key:get from console,remember to don't git push to github using .gitginore
# model for deepseek:
# V3: deepseek-chat and R1: deepseek-reasoner



from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()
DEEPSEEK_API_KEY=os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL="https://api.deepseek.com"
client=OpenAI(api_key=DEEPSEEK_API_KEY,base_url=DEEPSEEK_BASE_URL)

response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"system","content":"You're my helpful assistant!"},
        {"role":"user","content":"Hello,Who are you?"}
    ]
)


