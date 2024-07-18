import asyncio
from openai import AsyncOpenAI

from config import AI_API_TOKEN

client = AsyncOpenAI(api_key=AI_API_TOKEN)


async def gpt_text(req, model):
    completion = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': req}],
        model=model
    )
    return {'response': completion.choices[0].message.content,
            'usage': completion.usage.total_tokens}
