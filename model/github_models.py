# coding: utf-8
# Author：Chanpoe
# Date ：2024/09/24 09:53
# IDE：PyCharm
import os
import asyncio
import nonebot

from nonebot import logger
from openai import AsyncOpenAI

from ..util.context import OpenAIContext

# 创建一个 OpenAI 客户端
try:
    client = AsyncOpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=nonebot.get_driver().config.github_access_token,  # 使用环境变量获取API密钥
    )
except:
    logger.error('请先在`.env`中配置 GITHUB_ACCESS_TOKEN 环境变量！')


# 默认使用 GitHub Model 提供的 gpt-4o-mini模型
async def get_chat_completion(context: OpenAIContext, model: str = "gpt-4o-mini"):
    response = await client.chat.completions.create(  # 在这里添加 'await'
        messages=context.historical_messages,
        model=model,
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    return response


async def main():
    response_data = await get_chat_completion()
    print(response_data.choices[0].message.content)  # 获取并打印内容


if __name__ == '__main__':
    asyncio.run(main())
