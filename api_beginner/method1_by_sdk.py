#Recommend using SDK when the API supports the SDK for this scode language
import dotenv
import os
import openai

dotenv.load_dotenv()
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
client=openai.OpenAI(
    api_key=OPENAI_API_KEY
)
completions=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"assistant","content":"I'm your AI assistant"},
        {"role":"user","content":"What can you can for me to improving my English?"}
    ]
)
response_message=completions.choices[0].message
print(response_message)