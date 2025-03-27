from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id:int
    name:str="Shijie Zheng",
    signup_ts:datetime|None=None,
    friends:list[int]=[]

external_data={
    "id":"123",
    "signup_ts":"2017-06-01 12:22",
    "friends":[1,"2",b"3"]
}

user=User(**external_data)
print(user)


# You declare the "shape" of the data as classes with attributes.
#
# And each attribute has a type.
#
# Then you create an instance of that class with some values and it will validate the values,
# convert them to the appropriate type (if that's the case) and give you an object with all the data.