from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app=FastAPI()


@app.get("/deepseek_api")
async def deepseek_api(prompt:str):
    return {"completions":"test"}

# class ModelName(str,Enum):
#     alexnet="alexnet"
#     resnet="resnet"
#     lenet="lenet"
#
# class MessageResponse(BaseModel):
#     message:str


# @app.get("/models/{model_name}")
# async def get_model(model_name:ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name":model_name,"message":"alexnet!"}
#     if model_name.value=="lenet":
#         return {"model_name":model_name,"message":"LeCNN all the images"}
#     if model_name is ModelName.resnet:
#         return {"model_name":model_name,"message":"resnet"}

# @app.get("/api",response_model=MessageResponse)
# async def api_example():
#     return MessageResponse(message="Hello from FastAPI")


# @app.get("/items/{item_id}")
# async def read_item(item_id:int):
#     return {"item_id":item_id}
#
#
# @app.get("/user/{user_id}")
# async def read_user(user_id:str):
#     return {"user_id":user_id}
#
#
# @app.get("/userinfo")
# async def userinfo(username:str,userage:int):
#     return {"username":username,"userage":userage}

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)


