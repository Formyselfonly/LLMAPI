import dotenv
import os
import google.generativeai as genai
dotenv.load_dotenv()
GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model=genai.GenerativeModel("gemini-1.5-flash")
response=model.generate_content("How to baking bread?")
print(response.text)
