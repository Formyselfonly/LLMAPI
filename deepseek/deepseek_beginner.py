from random import choice

from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def deepseek_api_call(input):
    response = client.chat.completions.create(
        # deepseek-chat
        # deepseek-reasoner
        model="deepseek-chat",
        max_tokens=8192,
        # response_format={
        #     "type": "json_object"
        # },
        messages=[
            {
                "role": "system",
                "content": "You are my helpful assistant"
            },
            {
                "role": "user",
                "content": input

            },
        ],
        stream=False
    )
    # return response
    return response.choices[0].message.content

response_test=deepseek_api_call("What is the range of DeepSeek Temperature and other parameter?")
print(response_test)

# print(f"""
# The Full Response is:{response}
#
# The Completions is:{response.choices[0].message.content}
# [
#     refusal:{response.choices[0].message.refusal}
#     role:{response.choices[0].message.role}
#     audio:{response.choices[0].message.audio}
#     function_call:{response.choices[0].message.function_call}
#     tool_calls:{response.choices[0].message.tool_calls}
# ]
# """)
