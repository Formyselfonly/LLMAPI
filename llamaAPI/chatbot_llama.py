import requests

def llama_chatbot(model,messages):
    url="http://localhost:11434/api/chat"
    payload={
        "model":model,
        "messages":messages,
        "format":"json",
        "stream":False
    }
    response=requests.post(url,json=payload)
    # print(response)
    if response.status_code==404:
        print(f"Error:model'{model}' not found,so we will use llama3.2 3B")
        payload = {
            "model": "llama3.2",
            "messages": messages,
            "format": "json",
            "stream": False
        }
        response=requests.post(url,json=payload)
    if response.status_code == 200:
        try:
            data = response.json()
            # Extract assistant response
            assistant_message = data.get("message", {}).get("content", "No response received")
            # assistant_message = data.get("message").get("content")
            # print("Assistant Response:", assistant_message)
            # Append the assistant's response to messages for continuity
            # messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message  # Return the assistant's response
        except requests.exceptions.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def muti_chat(model):

    messages=[
        {"role": "assistant", "content": "Hello,How can I assist you?"},
        # {"role":"user","content":"You are a helpful assistant llama"}
    ]

    while True:
        user_input=input("user:")
        # print(type(user_input))
        messages.append({"role":"user","content":user_input})
        # print(messages)
        assistant_response=llama_chatbot(model,messages)
        messages.append({"role":"assistant","content":assistant_response})
        # print(messages)
        if assistant_response:
            print("Assistant:",assistant_response)
        if user_input.lower()=="exit":
            print("End of Conversation")
            break
model="llama3.1"
muti_chat(model)