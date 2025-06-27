import asyncio
import os
import time
from typing import Optional, AsyncGenerator
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
import json
from client_main import DeepSeekClient, APIError
from context_main import Conversation,Message
from client_main import ChatRequest
import dotenv
dotenv.load_dotenv()
console = Console()
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")

class ChatBot:
    """完整的聊天机器人实现"""

    def __init__(self):
        self.client = DeepSeekClient()
        self.conversation = Conversation()
        self.history_file = Path("conversation_history.json")

    def _display_welcome(self) -> None:
        """显示欢迎信息"""
        console.print(Panel(
            "[bold green]DeepSeek ChatBot[/] (v1.0)\n"
            "Type your message or use commands:\n"
            "[yellow]/help[/] - Show available commands\n"
            "[yellow]/clear[/] - Reset conversation\n"
            "[yellow]/save[/] - Save conversation to file\n"
            "[yellow]/exit[/] - Quit the program",
            title="Welcome",
            border_style="blue"
        ))

    def _process_command(self, input_text: str) -> bool:
        """处理用户命令

        Returns:
            bool: 如果输入是命令并已处理返回True，否则False
        """
        if not input_text.startswith("/"):
            return False

        command = input_text[1:].lower()

        if command == "help":
            self._display_welcome()
        elif command == "clear":
            self.conversation.clear()
            console.print("[yellow]Conversation history cleared[/]")
        elif command == "save":
            self._save_conversation()
        elif command == "exit":
            return True
        else:
            console.print(f"[red]Unknown command: {command}[/]")

        return True

    def _save_conversation(self) -> None:
        """保存对话历史到文件"""
        try:
            data = {
                "messages": [msg.dict() for msg in self.conversation.messages],
                "stats": self.conversation.stats()
            }
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            console.print(f"[green]Conversation saved to {self.history_file}[/]")
        except Exception as e:
            console.print(f"[red]Failed to save conversation: {str(e)}[/]")

    async def _stream_response(self, response_gen: AsyncGenerator) -> str:
        """处理流式响应并显示打字机效果"""
        full_response = ""
        with Live(console=console, refresh_per_second=10) as live:
            async for chunk in response_gen:
                if not chunk["choices"]:
                    continue

                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")

                if content:
                    full_response += content
                    live.update(Markdown(f"**Assistant:** {full_response}"))

        return full_response

    def _display_thinking(self) -> None:
        """显示思考中状态"""
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                console=console
        ) as progress:
            progress.add_task("Thinking...", total=None)
            time.sleep(0.5)  # 最小显示时间

    async def run(self) -> None:
        """主运行循环"""
        self._display_welcome()

        while True:
            try:
                user_input = console.input("[bold cyan]You:[/] ").strip()

                if not user_input:
                    continue

                # 处理命令
                if self._process_command(user_input):
                    if user_input == "/exit":
                        break
                    continue

                # 添加用户消息到上下文
                user_msg = Message(role="user", content=user_input)
                self.conversation.add_message(user_msg)

                # 准备API请求
                request = ChatRequest(
                    messages=self.conversation.get_context(max_tokens=3500),
                    stream=True
                )

                # 显示思考状态
                self._display_thinking()

                # 获取并显示响应
                response_gen = self.client.async_chat_completion(request)
                assistant_content = await self._stream_response(response_gen)

                # 添加助手响应到上下文
                if assistant_content:
                    assistant_msg = Message(role="assistant", content=assistant_content)
                    self.conversation.add_message(assistant_msg)

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted - use /exit to quit[/]")
            except APIError as e:
                console.print(f"[red]API Error: {str(e)}[/]")
            except Exception as e:
                console.print(f"[red]Unexpected error: {str(e)}[/]")


if __name__ == "__main__":
    bot = ChatBot()
    asyncio.run(bot.run())