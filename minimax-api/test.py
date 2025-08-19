from openai import OpenAI
from langchain_openai import ChatOpenAI
import dotenv
import os
dotenv.load_dotenv()
MINIMAX_API_KEY=os.getenv("MINIMAX_API_KEY")
llm=ChatOpenAI(
    api_key=MINIMAX_API_KEY,
    model="MiniMax-M1",
    base_url="https://api.minimaxi.com/v1",
)
response=llm.invoke("who are you?")
print(response)