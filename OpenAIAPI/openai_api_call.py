from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
user_input="""
"""

client = OpenAI(
    api_key=OPENAI_API_KEY
)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",
         "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)
# completion.choices[0].message

message=completion.choices[0].message
answer=message.content
print(answer)