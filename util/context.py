# coding: utf-8
# Author：Chanpoe
# Date ：2024/09/24 10:04
# IDE：PyCharm

class OpenAIContext:
    def __init__(self, character: str = "default"):
        # 角色身份
        self.character = character
        # 历史消息
        self.historical_messages = None
        # 设置默认历史消息
        self.set_default_history()

    def set_default_history(self):
        # 默认角色身份
        if self.character == "default":
            self.historical_messages = [
                {
                    "role": "system",
                    "content": "末尾附带不包含🤖的emoji表情，并且使用尽可能短但是意思表述完整的中文回答，如果生成的内容包含markdown格式，请在回复的开头第一行加上'markdown=true'",
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

    def clear_history(self):
        self.set_default_history()
