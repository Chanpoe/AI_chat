# coding: utf-8
# Author：Chanpoe
# Date ：2024/09/24 09:53
# IDE：PyCharm
import os
import asyncio
import nonebot
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

from nonebot import logger
from openai import AsyncOpenAI

from ..util.context import OpenAIContext, LlamaContext

try:
    # Github Model 使用的 OpenAI 客户端
    github_openai_model_client = AsyncOpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=nonebot.get_driver().config.github_access_token,  # 使用环境变量获取API密钥
    )
    #
    github_meta_model_client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(nonebot.get_driver().config.github_access_token),
    )
except:
    logger.error('请先在`.env`中配置 GITHUB_ACCESS_TOKEN 环境变量！')


# 默认使用 GitHub Model 提供的 gpt-4o-mini模型
async def get_github_gpt_chat_completion(context: OpenAIContext, model: str = "gpt-4o-mini"):
    response = await github_openai_model_client.chat.completions.create(  # 在这里添加 'await'
        messages=context.historical_messages,
        model=model,
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    return response


async def get_github_llama_chat_completion(context: LlamaContext, model: str = "Meta-Llama-3.1-70B-Instruct"):
    response = github_meta_model_client.complete(
        messages=context.historical_messages,
        model=model,
        temperature=0.8,
        max_tokens=4096,
        top_p=0.1
    )
    return response


async def main():
    response_data = await get_github_gpt_chat_completion()
    print(response_data.choices[0].message.content)  # 获取并打印内容


if __name__ == '__main__':
    asyncio.run(main())
