import os
import openai
import dotenv
import requests

dotenv.load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}
json = {
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Say this is a test!"}],
    "temperature": 0.7
}
response=requests.post(url=url,headers=headers,json=json)
print(response.json())