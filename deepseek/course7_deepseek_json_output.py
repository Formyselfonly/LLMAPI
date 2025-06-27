from openai import OpenAI
import os
import dotenv
import json
# DeepSeek provides JSON Output to ensure the model outputs valid JSON strings.
dotenv.load_dotenv()
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")

deepseek_client=OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)


system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]

response=deepseek_client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={
        "type":"json_object"
    }
)
answer=response.choices[0].message.content
print(answer)
print(type(answer))