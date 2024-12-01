import requests

model="llama3.1"
prompt="Who are u?"
messages=[
    {"role":"assistant","content":"I am your powerful and friendly assistant"},
    # {"role":"user","content":"What is the answer of 1+5x5?"}
    {"role":"user","content":"Translate into Chinese:What's wrong with u?"}
]

def llama_generate(model,prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model":model,
        "prompt": prompt,
        "stream":False
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        try:
            data=response.json()
            print("Response:", data.get("response"))
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
    else:
        print("Error:", response.status_code, response.json())

def llama_chat(model,messages):
    url="http://localhost:11434/api/chat"
    payload={
        "model":model,
        "messages":messages,
        "stream":False,
        "format":"json"
    }
    response=requests.post(url,json=payload)
    if response.status_code == 200:
        try:
            data=response.json()
            print("Response:", data.get("message"))
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
    else:
        print("Error:", response.status_code, response.json())


llama_generate(model,prompt)
llama_chat(model,messages)
