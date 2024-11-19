import anthropic
import dotenv
import os

dotenv.load_dotenv()
ANTHROPIC_API_KEY=os.environ.get("ANTHROPIC_API_KEY")

client=anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY
)
completions=client.messages.create(
    max_tokens=1024,
    model="claude-3-haiku-latest",
    messages=[
        {"role":"user","content":"Hello,Claude"}
    ]
)
message=completions.content
print(message)