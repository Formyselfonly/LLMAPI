import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from datetime import datetime
from client_main import DeepSeekClient
from context_main import Conversation


class TestDeepSeekClient(unittest.TestCase):

    @patch('requests.Session.post')
    def test_successful_request(self, mock_post):
        """测试成功的API请求"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "test response"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = DeepSeekClient()
        request = ChatRequest(messages=[{"role": "user", "content": "hello"}])
        response = client.chat_completion(request)

        self.assertEqual(response["choices"][0]["message"]["content"], "test response")

    @patch('requests.Session.post')
    def test_rate_limit_error(self, mock_post):
        """测试速率限制错误处理"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "error": {"message": "Rate limit exceeded"}
        }
        mock_post.return_value = mock_response

        client = DeepSeekClient()
        request = ChatRequest(messages=[{"role": "user", "content": "hello"}])

        with self.assertRaises(APIError) as context:
            client.chat_completion(request)

        self.assertIn("Rate limit exceeded", str(context.exception))


@pytest.mark.asyncio
async def test_async_stream():
    """测试异步流式响应处理"""
    mock_session = AsyncMock()
    mock_response = AsyncMock()

    # 模拟流式响应数据
    chunks = [
        b'data: {"choices": [{"delta": {"content": "Hello"}}]}\n\n',
        b'data: {"choices": [{"delta": {"content": " World"}}]}\n\n',
        b'data: [DONE]\n\n'
    ]
    mock_response.content.iter_chunks.return_value = chunks
    mock_response.__aenter__.return_value = mock_response
    mock_session.post.return_value = mock_response

    client = DeepSeekClient()
    client.async_session = mock_session

    request = ChatRequest(messages=[{"role": "user", "content": "hi"}], stream=True)

    responses = []
    async for resp in client.async_chat_completion(request):
        responses.append(resp)

    assert len(responses) == 2
    assert responses[0]["choices"][0]["delta"]["content"] == "Hello"
    assert responses[1]["choices"][0]["delta"]["content"] == " World"


class TestConversation(unittest.TestCase):

    def setUp(self):
        self.conv = Conversation(max_tokens=100)

    def test_message_trimming(self):
        """测试消息自动截断逻辑"""
        # 添加多条消息直到超过Token限制
        for i in range(10):
            msg = Message(role="user", content="This is a long message " * 5)
            self.conv.add_message(msg)

        # 验证消息数量在合理范围内
        self.assertLess(len(self.conv.messages), 10)
        self.assertLessEqual(self.conv.token_count, self.conv.max_tokens)

    def test_context_selection(self):
        """测试上下文选择逻辑"""
        # 添加不同长度的消息
        messages = [
            ("short", 10),
            ("medium " * 5, 30),
            ("long " * 20, 100),
            ("medium " * 5, 30),
            ("short", 10)
        ]

        for content, _ in messages:
            self.conv.add_message(Message(role="user", content=content))

        # 请求限制Token数的上下文
        context = self.conv.get_context(max_tokens=50)
        self.assertEqual(len(context), 2)  # 应该返回最新的两条短消息