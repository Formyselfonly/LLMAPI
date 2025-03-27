import os
import dotenv
dotenv.load_dotenv()
os.environ["NAME"]="SHIJIEZHENG"
name=os.getenv("NAME")
age=os.getenv("AGE")
print(f"{name} is {age} years old")