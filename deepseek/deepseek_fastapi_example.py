from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
app = FastAPI()

class Query(BaseModel):
    prompt: str

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

@app.post("/generate")
async def generate_text(query: Query):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": query.prompt}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))