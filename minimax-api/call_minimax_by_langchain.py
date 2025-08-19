from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os, dotenv

# 加载环境变量
dotenv.load_dotenv()
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")

# 初始化 LLM
llm = ChatOpenAI(
    model="MiniMax-M1",
    api_key=MINIMAX_API_KEY,
    base_url="https://api.minimaxi.com/v1",
)

# 初始化对话历史
chat_history = []

print("欢迎使用 MiniMax 对话助手（输入 'exit' 退出）")
while True:
    user_input = input("你：")
    if user_input.lower() in ["exit", "quit", "退出"]:
        print("再见！")
        break

    # 添加用户消息到对话历史
    chat_history.append(HumanMessage(content=user_input))

    # 获取模型回复
    try:
        response = llm.invoke(chat_history)
        ai_reply = response.content
        print("AI：", ai_reply)
        chat_history.append(AIMessage(content=ai_reply))
    except Exception as e:
        print("出错了：", e)
