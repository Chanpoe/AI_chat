# coding: utf-8
# Author：Chanpoe
# Date ：2024/5/16 下午11:02
# IDE：PyCharm

import nonebot
from nonebot import on_command
from nonebot import get_plugin_config
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-ai-chat-all-in-one",
    description="AI 对话聚合",
    usage="未定",
    type="application",
    homepage="https://github.com/Chanpoe/ai_chat",
    config=Config
)

config = nonebot.get_driver().config

# 从全局配置中获取插件配置
plugin_config = get_plugin_config(Config)

chat_matcher = on_command('chat', rule=to_me(), aliases={''}, priority=plugin_config.chat_command_priority)


