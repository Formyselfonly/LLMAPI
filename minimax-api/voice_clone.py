import json
import requests
import dotenv,os
dotenv.load_dotenv()

group_id =os.getenv("MINIMAX_GROUP_ID")
api_key =os.getenv("MINIMAX_API_KEY")

#复刻音频上传
url = f'https://api.minimaxi.com/v1/files/upload?GroupId={group_id}'
headers1 = {
    'authority': 'api.minimaxi.com',
    'Authorization': f'Bearer {api_key}'
}

data = {
    'purpose': 'voice_clone'
}

files = {
    'file': open('output.mp3', 'rb')
}
response = requests.post(url, headers=headers1, data=data, files=files)
file_id = response.json().get("file").get("file_id")
print(file_id)

#示例音频上传
url = f'https://api.minimaxi.com/v1/files/upload?GroupId={group_id}'
headers1 = {
    'authority': 'api.minimaxi.com',
    'Authorization': f'Bearer {api_key}'
}

data = {
    'purpose': 'prompt_audio'
}

files = {
    'file': open('prompt.mp3', 'rb')
}
response = requests.post(url, headers=headers1, data=data, files=files)
prompt_file_id = response.json().get("file").get("file_id")
print(prompt_file_id)


#音频复刻
url = f'https://api.minimaxi.com/v1/voice_clone?GroupId={group_id}'
payload2 = json.dumps({
  "file_id": file_id,
  "voice_id": "test1234"
})
headers2 = {
  'Authorization': f'Bearer {api_key}',
  'content-type': 'application/json'
}
response = requests.request("POST", url, headers=headers2, data=payload2)
print(response.text)