from openai import AsyncOpenAI
from src.services.text_generation.base import BaseTextGenerationService
from src.core.config import settings

class OpenAITextGenerationService(BaseTextGenerationService):
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate_text(self, completion_config: dict) -> str:
        response = await self.openai_client.chat.completions.create(**completion_config)
        return response.choices[0].message.content
    
    async def generate_text_stream(self, completion_config: dict):
        response = await self.openai_client.chat.completions.create(**completion_config,stream=True)
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content