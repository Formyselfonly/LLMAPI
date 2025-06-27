from typing import Deque, Optional, List
from collections import deque
import tiktoken
import time
from pydantic import BaseModel, Field
from client_main import ChatRequest

from pydantic import BaseModel, Field
import time
from typing import Dict

class Message(BaseModel):
    """单条消息数据模型"""
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str
    timestamp: float = Field(default_factory=time.time)

    def to_api_format(self) -> Dict[str, str]:
        """转换为API需要的格式"""
        return {"role": self.role, "content": self.content}



class Conversation:
    """增强版对话上下文管理

    功能：
    - 消息历史管理
    - 精确Token计数
    - 自动截断策略
    - 上下文窗口优化
    """

    def __init__(
            self,
            max_tokens: int = 4096,
            max_messages: Optional[int] = 100,
            model: str = "deepseek-chat"
    ):
        """
        Args:
            max_tokens: 最大上下文Token数
            max_messages: 最大消息数量（可选）
            model: 用于Token计算的模型名称
        """
        self.max_tokens = max_tokens
        self.max_messages = max_messages
        self.messages: Deque[Message] = deque(maxlen=max_messages)
        self.token_count = 0

        try:
            self.encoder = tiktoken.encoding_for_model(model)
        except:
            self.encoder = None

    def add_message(self, message: Message) -> None:
        """添加消息到历史记录

        1. 计算新消息的Token数
        2. 如果超出限制，移除最旧的消息直到满足要求
        3. 添加新消息并更新Token计数
        """
        new_tokens = self._count_tokens(message.content)

        # 移除旧消息直到满足Token限制
        while self.messages and (self.token_count + new_tokens) > self.max_tokens:
            removed = self.messages.popleft()
            self.token_count -= self._count_tokens(removed.content)

        self.messages.append(message)
        self.token_count += new_tokens

    def _count_tokens(self, text: str) -> int:
        """精确计算文本的Token数"""
        if self.encoder:
            return len(self.encoder.encode(text))
        # 回退到近似算法
        return len(text) // 4

    def get_context(
            self,
            max_tokens: Optional[int] = None,
            min_messages: int = 1
    ) -> List[Dict[str, str]]:
        """获取优化后的对话上下文

        Args:
            max_tokens: 返回的最大Token数（可选）
            min_messages: 至少保留的消息数量

        Returns:
            适合API请求的消息列表
        """
        if not max_tokens or max_tokens >= self.token_count:
            return [msg.to_api_format() for msg in self.messages]

        # 从最新消息开始反向选择，直到满足Token限制
        selected = []
        remaining_tokens = max_tokens

        for msg in reversed(self.messages):
            msg_tokens = self._count_tokens(msg.content)
            if remaining_tokens - msg_tokens < 0 and len(selected) >= min_messages:
                break
            selected.append(msg)
            remaining_tokens -= msg_tokens

        return [msg.to_api_format() for msg in reversed(selected)]

    def clear(self) -> None:
        """清空对话历史"""
        self.messages.clear()
        self.token_count = 0

    def stats(self) -> Dict[str, int]:
        """获取当前对话统计"""
        return {
            "message_count": len(self.messages),
            "token_count": self.token_count,
            "remaining_tokens": self.max_tokens - self.token_count
        }