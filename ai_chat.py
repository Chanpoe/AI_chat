# coding: utf-8
# Author：Chanpoe
# Date ：2024/09/23 15:25
# IDE：PyCharm

from nonebot import on_command, get_plugin_config, logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    Message,
    MessageSegment,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from nonebot.internal.rule import Rule
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.params import Arg
from nonebot_plugin_alconna import CustomNode, Image, Reference, UniMessage
from nonebot_plugin_alconna.uniseg.tools import image_fetch, reply_fetch
from nonebot_plugin_alconna.uniseg import UniMsg, Reply

from .config import Config
from .handlers.text_handler import handle_plain_text
from .model.github_models import get_chat_completion
from .util.context import OpenAIContext

# 从全局配置中获取插件配置
plugin_config = get_plugin_config(Config)
test_matcher = on_command('test', rule=to_me(), priority=plugin_config.chat_command_priority)

open_chat_fun = on_command('开启AI对话功能', rule=to_me(), priority=plugin_config.chat_command_priority)
# 获取aichat历史消息
context = OpenAIContext()

chat_matcher = on_command(
    '',
    rule=to_me(),
    priority=plugin_config.chat_command_priority
)

close_chat_fun = on_command('关闭AI对话功能', rule=to_me(), priority=plugin_config.chat_command_priority)
clear_chat_history = on_command('清除对话历史', aliases={'clear', '清除对话'}, rule=to_me(),
                                priority=plugin_config.chat_command_priority)


async def clear_context_history():
    context.clear_history()


@test_matcher.handle()
async def chat_task(bot: Bot, event: Event, state: T_State, msg: UniMsg):
    new_message = MessageSegment.text('Hello, World!')
    # new_message += MessageSegment.image('https://www.baidu.com/img/bd_logo1.png')
    # new_message += MessageSegment.text('test_pic')
    # new_message = MessageSegment.music(type_='163', id_=186016)
    imgs = []

    # for msg_seg in msg:
    #     if isinstance(msg_seg, Image):
    #         # imgs.append(
    #         #     await image_fetch(bot=bot, event=event, state=state, img=msg_seg)
    #         # )
    #         image_url = msg_seg.url
    #         await bot.send(event, MessageSegment.image(image_url))
    #
    await test_matcher.send(new_message)
    # a = 1
    # b = 2


@open_chat_fun.handle()
async def open_chat_fun_task(bot: Bot, event: Event, state: T_State):
    plugin_config.enable_chat = True
    await open_chat_fun.send('AI对话功能已开启')


@close_chat_fun.handle()
async def close_chat_fun_task(bot: Bot, event: Event, state: T_State):
    plugin_config.enable_chat = False
    await close_chat_fun.send('AI对话功能已关闭')
    context.clear_history()


@clear_chat_history.handle()
async def clear_chat_history_task(bot: Bot, event: Event, state: T_State):
    await clear_context_history()
    await clear_chat_history.send('对话历史已清除')


@chat_matcher.handle()
async def chat_with_ai(bot: Bot, event: Event, state: T_State, msg: UniMsg):
    if not plugin_config.enable_chat:
        return
    # 获取用户发送内容
    user_message = msg.extract_plain_text()

    # 将用户发送内容添加到历史消息中
    context.add_user_message(user_message)
    try:
        # 只保留最近20条历史消息
        context.historical_messages = context.historical_messages[0] + context.historical_messages[-20:]
    except:
        pass

    # 调用模型生成聊天回复
    is_chat_success = False
    retry_count = 0
    while not is_chat_success:
        try:
            response = await get_chat_completion(context=context)
            is_chat_success = True
        except Exception as e:
            retry_count += 1
            if retry_count >= 3:
                logger.error(e)
                logger.error(e.args)
                await chat_matcher.send("达到API请求上限，请稍后再试")
                return

    # 发送回复
    assistant_content = response.choices[0].message.content
    await chat_matcher.send(assistant_content)

    # 将助手回复添加到历史消息中，只保留最近20条历史消息
    context.add_assistant_message(assistant_content)
