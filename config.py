# coding: utf-8
# Author：Chanpoe
# Date ：2024/09/13 16:30
# IDE：PyCharm

from pydantic import BaseModel


class Config(BaseModel):
    # API key
    openai_api_key: str = ''
    gemini_api_key: str = ''
    github_access_token: str = ''

    # Model Name
    openai_model_name: str = 'gpt-4o-mini'
    gemini_model_name: str = 'gemini-pro'
    github_model_name: str = 'gpt-4o'

    # 优先级
    chat_command_priority: int = 10

    # 是否开启对话功能
    enable_chat: bool = False
