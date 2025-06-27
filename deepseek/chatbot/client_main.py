import json
import os
import time
from typing import List, Dict, Any, Optional, AsyncGenerator
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
import requests
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# 加载环境变量
load_dotenv()


class APIConfig(BaseModel):
    """API配置数据模型"""
    api_key: str = Field(..., min_length=32)
    base_url: str = "https://api.deepseek.com/v1"
    timeout: int = Field(30, gt=0)
    max_retries: int = Field(3, ge=0)

    @validator('api_key')
    def validate_key(cls, v):
        if not v.startswith('sk-'):
            raise ValueError("Invalid API key format")
        return v


class ChatRequest(BaseModel):
    """聊天请求数据模型"""
    messages: List[Dict[str, str]]
    model: str = "deepseek-chat"
    temperature: float = Field(0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(None, gt=0)
    stream: bool = False

    @validator('messages')
    def validate_messages(cls, v):
        if not v:
            raise ValueError("Messages list cannot be empty")
        for msg in v:
            if msg['role'] not in ('system', 'user', 'assistant'):
                raise ValueError("Invalid message role")
        return v


class DeepSeekClient:
    """增强版DeepSeek API客户端

    功能：
    - 同步/异步双模式支持
    - 自动重试机制
    - 请求验证
    - 响应解析
    """

    def __init__(self):
        self.config = self._load_config()
        self.session = requests.Session()
        self.session.headers.update(self._default_headers)
        self.async_session = None

    @property
    def _default_headers(self) -> Dict[str, str]:
        """返回默认请求头"""
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "DeepSeekBot/1.0"
        }

    def _load_config(self) -> APIConfig:
        """从环境变量加载并验证配置"""
        return APIConfig(
            api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            timeout=int(os.getenv("API_TIMEOUT", "30")),
            max_retries=int(os.getenv("MAX_RETRIES", "3"))
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout
        ))
    )
    def chat_completion(self, request: ChatRequest) -> Dict[str, Any]:
        """同步聊天请求

        Args:
            request: 验证过的聊天请求对象

        Returns:
            解析后的API响应字典

        Raises:
            APIError: 对于业务逻辑错误
            requests.exceptions.RequestException: 对于网络错误
        """
        url = f"{self.config.base_url}/chat/completions"

        try:
            response = self.session.post(
                url,
                json=request.dict(exclude_none=True),
                timeout=self.config.timeout,
                stream=request.stream
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)

    async def async_chat_completion(
            self,
            request: ChatRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """异步流式聊天请求

        Args:
            request: 验证过的聊天请求对象

        Yields:
            流式响应的事件数据

        Raises:
            APIError: 对于业务逻辑错误
        """
        if self.async_session is None:
            self.async_session = aiohttp.ClientSession(headers=self._default_headers)

        url = f"{self.config.base_url}/chat/completions"

        try:
            async with self.async_session.post(
                    url,
                    json=request.dict(exclude_none=True),
                    timeout=self.config.timeout
            ) as response:
                if response.status != 200:
                    await self._handle_http_error(response)

                async for line in response.content:
                    if line.startswith(b"data: "):
                        chunk = line[6:].strip()
                        if chunk == b"[DONE]":
                            break
                        yield json.loads(chunk)
        except Exception as e:
            raise APIError(f"Stream error: {str(e)}") from e

    def _handle_http_error(self, error):
        """统一处理HTTP错误"""
        if isinstance(error, requests.exceptions.HTTPError):
            status_code = error.response.status_code
            try:
                error_data = error.response.json()
                msg = error_data.get("error", {}).get("message", "Unknown error")
            except ValueError:
                msg = error.response.text or "Unknown error"
        else:  # aiohttp
            status_code = error.status
            msg = error.message

        error_map = {
            400: f"Bad request: {msg}",
            401: "Invalid API key - please check your configuration",
            403: "Permission denied",
            429: f"Rate limit exceeded: {msg}",
            500: f"Server error: {msg}"
        }

        raise APIError(error_map.get(status_code, f"HTTP {status_code}: {msg}"))


class APIError(Exception):
    """自定义API异常"""

    def __init__(self, message: str, code: Optional[int] = None):
        super().__init__(message)
        self.code = code