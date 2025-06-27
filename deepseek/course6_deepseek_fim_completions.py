from openai import OpenAI
import os
import dotenv
# In FIM (Fill In the Middle) completion, users can provide a prefix and a suffix (optional),
# and the model will complete the content in between.
# FIM is commonly used for content completion、code completion.
dotenv.load_dotenv()
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")

deepseek_client=OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/beta"
)

response = deepseek_client.completions.create(
    model="deepseek-chat",
    prompt="def fib(a):",
    suffix="    return fib(a-1) + fib(a-2)",
    max_tokens=128
)
print(response.choices[0].text)