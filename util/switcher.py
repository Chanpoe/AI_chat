# coding: utf-8
# Author：Chanpoe
# Date ：2024/09/24 14:53
# IDE：PyCharm

from pydantic import BaseModel


class GitHubModel(BaseModel):
    provider: str = "github"
    models: list = ["gpt-4o-mini", "gpt-4o"]


class OpenAIModel(BaseModel):
    provider: str = "openai"
    models: list = ["gpt-4o-mini", "chatgpt-4o-latest"]


class GoogleModel(BaseModel):
    provider: str = "google"
    models: list = ["gemini-1.5-pro-exp-0827"]


# 当前使用的模型类定义
class CurrentModel(BaseModel):
    provider: str = ""  # 模型接口提供商
    model: str = ""  # 当前模型

    # 切换模型接口提供商
    def switch_provider(self, provider_name: str):
        valid_providers = ['github', 'openai', 'google']
        if provider_name in valid_providers:
            self.provider = provider_name
            # 切换时重置模型
            self.get_default_model(provider_name)
        else:
            raise ValueError(f"{provider_name} is not a valid provider.")

    def get_default_model(self, provider: str):
        if provider == 'github':
            self.model = GitHubModel().models[0]
        elif provider == 'openai':
            self.model = OpenAIModel().models[0]
        elif provider == 'google':
            self.model = GoogleModel().models[0]
        else:
            raise ValueError(f"{provider} is not a valid provider.")

    def switch_model(self, model_name: str):
        # todo 校验模型是否在提供商对应的模型列表中
        self.model = model_name


if __name__ == '__main__':
    current_model = CurrentModel()
    current_model.switch_provider('github')
    print(current_model.provider)
    print(current_model.model)
    current_model.switch_provider('openai')
    print(current_model.provider)
    print(current_model.model)
