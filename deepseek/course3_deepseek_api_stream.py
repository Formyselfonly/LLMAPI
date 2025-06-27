from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")

deepseek_client=OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def deepseek_api_call_stream(messages):
    completions=deepseek_client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True
    )
    reasoner_content=""
    content=""
    for chunk in completions:
        delta=chunk.choices[0].delta
        # Safely check and append reasoning_content
        if hasattr(delta, "reasoning_content") and delta.reasoning_content:
            reasoner_content += delta.reasoning_content

        # Safely check and append content
        if hasattr(delta, "content") and delta.content:
            content += delta.content

    return reasoner_content,content



# Round 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
reasoning1, content1 = deepseek_api_call_stream(messages)
print("Reasoning 1:\n", reasoning1)
print("Answer 1:\n", content1)

# Round 2
messages.append({"role": "assistant", "content": content1})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
reasoning2, content2 = deepseek_api_call_stream(messages)
print("Reasoning 2:\n", reasoning2)
print("Answer 2:\n", content2)
