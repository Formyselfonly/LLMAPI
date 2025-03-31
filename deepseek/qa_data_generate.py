from random import choice

from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def qa_generate(input):
    response = client.chat.completions.create(
        # deepseek-chat
        # deepseek-reasoner
        model="deepseek-chat",
        max_tokens=8192,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": "You are my helpful assistant"
            },
            {
                "role": "user",
                "content": f"""
                #Guide
                Help me generate QA data and it should be json format.
                #Here is the Example
                ##User Input
                What day it is today? Saturday!
                ##Your Output
                {{
                "Q":"What day it is today?",
                "A":"Saturday"
                }}
                #Start
                {input}
                """
            },
        ],
        stream=False
    )
    # return response
    return response.choices[0].message.content

def qa_multiple(qa,example=""):
    response=client.chat.completions.create(
        model="deepseek-chat",
        max_tokens=8192,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": "You are my helpful assistant"
            },
            {
                "role": "user",
                "content": f"""
                    #Guide
                    Help me generate Multiple QA data based on my QA data for my AI training use,and it should be json format.
                    I will give you a pair of QA data,and you generate multiple QA data which is simliar to this so that I can training use there data.
                    #Here is the Example
                    {example}
                    #Constrain
                    The data of QA that you generate with the origin QA should be simliar,
                    My aim is to use to train,so don't generate QA data that is not related to my origin QA data
                    #Start
                    Here is my QA data:{qa}
                    """
            },
        ],
        stream=False
    )
    return response.choices[0].message.content

emample="""
      ##User Input
        {{
        "Q":"What is the answer of 1+1",
        "A":"2"
        }}
        ##Your Output
        {{
        "Q":"What is the answer of 1+1",
        "A":"2"
        "Q":"1+1",
        "A":"2"
        "Q":"1+1",
        "A":"The answer of 1+1=2"
        }}
"""


qa=qa_generate("Who are u?I'm DeepSeek!")
qa_data=qa_multiple(qa)
print(f"Here is the qa:{qa}\n Here is the qa_data:{qa_data}")

