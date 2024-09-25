# coding: utf-8
# Author：Chanpoe
# Date ：2024/09/24 10:04
# IDE：PyCharm

from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from typing import List, Any


# 上下文基类
class Context:
    def __init__(self, character: str = "default"):
        # 角色身份
        self.character = character
        # 历史消息
        self.historical_messages: List[Any] = []
        # 设置默认历史消息
        self.set_default_history()

    # 重置对话消息，将对话历史记录设置为角色身份对应的system prompt
    def set_default_history(self):
        pass

    # 添加一条用户发送的消息
    def add_user_message(self, content: str):
        pass

    # 添加一条AI回复的消息
    def add_assistant_message(self, content: str):
        pass

    # 清除对话历史记录
    def clear_history(self):
        self.set_default_history()


class OpenAIContext(Context):
    def __init__(self, character: str = "default"):
        super().__init__(character=character)
        # 设置默认历史消息
        self.set_default_history()

    def set_default_history(self):
        # 默认角色身份
        if self.character == "default":
            self.historical_messages = [
                {
                    "role": "system",
                    "content": "末尾附带不包含🤖的emoji表情，并且使用尽可能短但是意思表述完整的中文回答，回答的风格幽默一些。如果生成的内容包含markdown格式，请在回复的开头第一行加上'markdown=true'",
                }
            ]
        # todo: 添加其他角色身份
        else:
            self.historical_messages = []

    def add_user_message(self, content: str):
        self.historical_messages.append({
            "role": "user",
            "content": content,
        })

    def add_assistant_message(self, content: str):
        self.historical_messages.append({
            "role": "assistant",
            "content": content,
        })


# Llama对话上下文与OpenAI对话上下文相同，故继承OpenAIContext
class LlamaContext(OpenAIContext):
    def __init__(self, character: str = "default"):
        super().__init__(character=character)
        self.set_default_history()


if __name__ == '__main__':
    context = LlamaContext()
    print(context.historical_messages)
    print(context.character)
