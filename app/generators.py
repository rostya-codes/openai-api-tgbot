import asyncio
from openai import AsyncOpenAI

from config import AI_API_TOKEN

client = AsyncOpenAI(api_key=AI_API_TOKEN)


async def gpt_text(req, model):
    completion = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': req}],
        model=model
    )
    print(completion.choices[0].message.content)


asyncio.run(gpt_text('Hello World на C++', 'gpt-4o'))
