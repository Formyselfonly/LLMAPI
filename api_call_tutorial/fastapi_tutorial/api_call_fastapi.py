from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app=FastAPI()

class MessageResponse(BaseModel):
    message:str

@app.get("/api",response_model=MessageResponse)
async def api_example():
    return MessageResponse(message="Hello from FastAPI")

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)